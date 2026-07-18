from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

import torch
from huggingface_hub import model_info
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "results" / "model_edits" / "model_edit_dataset.jsonl"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "model_edit_explanation_candidates.jsonl"
DEFAULT_STATS = ROOT / "data" / "processed" / "model_edit_explanation_candidate_stats.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def batches(rows: List[Dict[str, Any]], batch_size: int) -> Iterable[List[Dict[str, Any]]]:
    for start in range(0, len(rows), batch_size):
        yield rows[start : start + batch_size]


def balanced_subset(rows: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    by_model: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_model[row["model_key"]].append(row)
    model_keys = sorted(by_model)
    per_model = max(1, limit // max(1, len(model_keys)))
    selected: List[Dict[str, Any]] = []
    selected_keys: set[int] = set()
    for key in model_keys:
        for row in by_model[key][:per_model]:
            selected.append(row)
            selected_keys.add(row["_row_index"])
    for row in rows:
        if len(selected) >= limit:
            break
        if row["_row_index"] not in selected_keys:
            selected.append(row)
            selected_keys.add(row["_row_index"])
    return selected[:limit]


def prompt_for(row: Dict[str, Any]) -> str:
    edit = row["predicted_edit"]
    return (
        "Task: explain a grammar correction. Return only one short explanation, not the corrected sentence.\n"
        "Before: She go home .\n"
        "After: She goes home .\n"
        "Focus: source token span [1,2).\n"
        "Explanation: The verb should agree with the singular subject.\n"
        f"Before: {row['source']}\n"
        f"After: {row['prediction']}\n"
        f"Focus: source token span [{edit['start']},{edit['end']}).\n"
        "Explanation:"
    )


def clean_explanation(text: str) -> str:
    text = " ".join(text.replace("\n", " ").split())
    text = re.sub(r"^(Explanation:\s*)+", "", text, flags=re.IGNORECASE)
    parts = re.split(r"(?<=[.!?])\s+", text)
    if parts and len(parts[0].split()) >= 3:
        text = parts[0]
    words = text.split()
    deduped: List[str] = []
    for word in words:
        if len(deduped) >= 3 and deduped[-3:] == [word] * 3:
            continue
        deduped.append(word)
    return " ".join(deduped[:45]).strip()


def quote(text: str) -> str:
    return text.replace('"', "'")


def leakage_template(edit: Dict[str, Any]) -> str:
    span = f"source token span [{edit['start']},{edit['end']})"
    if edit["operation"] == "replace":
        return f'Replace "{quote(edit["source_text"])}" with "{quote(edit["target_text"])}" at {span}; ERRANT type {edit["error_type"]}.'
    if edit["operation"] == "insert":
        return f'Insert "{quote(edit["target_text"])}" at {span}; ERRANT type {edit["error_type"]}.'
    if edit["operation"] == "delete":
        return f'Delete "{quote(edit["source_text"])}" at {span}; ERRANT type {edit["error_type"]}.'
    return f"The edit at {span} has ERRANT type {edit['error_type']}."


def generate(args: argparse.Namespace) -> None:
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    all_rows = read_jsonl(args.input)
    for row_index, row in enumerate(all_rows):
        row["_row_index"] = row_index
    rows = balanced_subset(all_rows, args.limit)
    model_id = args.generator_model
    revision = model_info(model_id).sha or "unknown"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id).to("cpu")
    model.eval()
    torch.set_num_threads(1)

    generated_rows: List[Dict[str, Any]] = []
    started = time.time()
    for batch in batches(rows, args.batch_size):
        prompts = [prompt_for(row) for row in batch]
        inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=args.max_input_length)
        with torch.inference_mode():
            output_ids = model.generate(
                **inputs,
                num_beams=args.num_beams,
                max_new_tokens=args.max_new_tokens,
                min_length=3,
                no_repeat_ngram_size=3,
                repetition_penalty=1.2,
            )
        decoded = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        for source_row, prompt, explanation in zip(batch, prompts, decoded):
            candidate = clean_explanation(explanation)
            generated_rows.append(
                {
                    "record_id": f"{source_row['sample_id']}::{source_row['model_key']}::{source_row['_row_index']}::{source_row['predicted_edit']['start']}-{source_row['predicted_edit']['end']}",
                    "sample_id": source_row["sample_id"],
                    "source": source_row["source"],
                    "reference": source_row["reference"],
                    "prediction": source_row["prediction"],
                    "model_key": source_row["model_key"],
                    "model": source_row["model"],
                    "behavior": source_row["behavior"],
                    "predicted_edit": source_row["predicted_edit"],
                    "aligned_reference_edit": source_row["aligned_reference_edit"],
                    "open_source_explanation_candidate": candidate,
                    "open_source_generator": {
                        "model_id": model_id,
                        "model_version": revision,
                        "license": "apache-2.0",
                        "decoding": {
                            "num_beams": args.num_beams,
                            "max_new_tokens": args.max_new_tokens,
                            "no_repeat_ngram_size": 3,
                            "repetition_penalty": 1.2,
                        },
                    },
                    "generator_prompt": prompt,
                    "generator_input_fields": ["source", "model_prediction", "predicted_edit_span"],
                    "uses_reference_in_generator": False,
                    "uses_gold_edit_in_generator": False,
                    "uses_predicted_edit_text_or_type_in_generator": False,
                    "leakage_upper_control_template": leakage_template(source_row["predicted_edit"]),
                    "leakage_control_only": True,
                    "label_source": "open_source_model_candidate_not_gold",
                    "is_human_gold": False,
                }
            )
    duration = time.time() - started
    write_jsonl(args.output, generated_rows)
    stats = {
        "created_at": utc_now(),
        "input": str(args.input),
        "output": str(args.output),
        "candidate_count": len(generated_rows),
        "model_counts": dict(Counter(row["model_key"] for row in generated_rows)),
        "behavior_counts": dict(Counter(row["behavior"] for row in generated_rows)),
        "empty_candidate_count": sum(1 for row in generated_rows if not row["open_source_explanation_candidate"]),
        "prediction_copy_like_count": sum(
            1
            for row in generated_rows
            if row["open_source_explanation_candidate"].strip().lower()
            == row["prediction"].strip().lower()
        ),
        "generator_model": model_id,
        "generator_revision": revision,
        "generator_license": "apache-2.0",
        "duration_seconds": round(duration, 3),
        "seconds_per_candidate": round(duration / len(generated_rows), 6) if generated_rows else 0.0,
        "important_note": "Open-source explanations are model-generated candidates from source/prediction/span prompts. They are not human gold. Explicit templates are retained only as leakage upper controls.",
    }
    write_json(args.stats, stats)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate open-source explanation candidates for model-produced edits.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stats", type=Path, default=DEFAULT_STATS)
    parser.add_argument("--generator-model", default="google/flan-t5-base")
    parser.add_argument("--limit", type=int, default=300)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--num-beams", type=int, default=4)
    parser.add_argument("--max-input-length", type=int, default=512)
    parser.add_argument("--max-new-tokens", type=int, default=48)
    return parser.parse_args()


if __name__ == "__main__":
    generate(parse_args())
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)
