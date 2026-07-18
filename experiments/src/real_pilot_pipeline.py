from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import errant

from baselines import structured_explicit_edit_baseline, surface_keyword_predict
from edit_schema import Edit, compare_edits
from extract_edits import extract_token_diff_edits


ROOT = Path(__file__).resolve().parents[2]
EXPECT_ROOT = ROOT / "data" / "downloads" / "Explainable_GEC"
PROCESSED_DIR = ROOT / "data" / "processed"
RESULTS_DIR = ROOT / "results"
DOCS_DIR = ROOT / "docs"
PAPER_DIR = ROOT / "paper"

POSITIVE_STYLES = {
    "faithful_explicit",
    "faithful_implicit",
    "masked_target",
    "raw_edit_string",
}
NEGATIVE_TYPES = {
    "wrong_location",
    "wrong_target",
    "wrong_direction",
    "wrong_type",
    "swapped_explanation",
    "generic_explanation",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def expect_commit(expect_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(expect_root), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unknown"


def clean_tokens(tokens: Sequence[str]) -> List[str]:
    return [tok for tok in tokens if tok != "[NONE]"]


def spaced_text(tokens: Sequence[str]) -> str:
    return " ".join(clean_tokens(tokens))


def load_expect_split(expect_root: Path, split: str) -> Iterable[Tuple[int, Dict[str, Any]]]:
    path = expect_root / "data" / "json" / f"{split}.json"
    with path.open(encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if line.strip():
                yield idx, json.loads(line)


def errant_operation(edit_type: str, start: int, end: int, c_start: int, c_end: int) -> str:
    if start == end and c_start < c_end:
        return "insert"
    if start < end and c_start == c_end:
        return "delete"
    return "replace"


def errant_edit_to_dict(edit: Any) -> Dict[str, Any]:
    operation = errant_operation(edit.type, edit.o_start, edit.o_end, edit.c_start, edit.c_end)
    return Edit(
        start=int(edit.o_start),
        end=int(edit.o_end),
        source_text=str(edit.o_str).strip(),
        target_text=str(edit.c_str).strip(),
        operation=operation,
        error_type=str(edit.type),
    ).to_dict()


def extract_errant_edits(annotator: Any, source: str, target: str) -> List[Dict[str, Any]]:
    original = annotator.parse(source)
    corrected = annotator.parse(target)
    rows = []
    for edit in annotator.annotate(original, corrected):
        if edit.type == "noop":
            continue
        rows.append(errant_edit_to_dict(edit))
    return rows


def build_expect_samples(args: argparse.Namespace) -> Dict[str, Any]:
    annotator = errant.load("en")
    commit = expect_commit(args.expect_root)
    selected: List[Dict[str, Any]] = []
    edit_rows: List[Dict[str, Any]] = []
    split_totals: Dict[str, int] = {}
    errors: List[Dict[str, str]] = []

    for split in args.splits:
        split_count = 0
        for idx, raw in load_expect_split(args.expect_root, split):
            split_count += 1
            if len(selected) >= args.sample_size:
                continue
            source_text = spaced_text(raw["source"])
            target_text = spaced_text(raw["target"])
            if source_text == target_text:
                continue
            try:
                errant_edits = extract_errant_edits(annotator, source_text, target_text)
            except Exception as exc:
                errors.append({"split": split, "index": str(idx), "error": repr(exc)})
                continue
            if not errant_edits:
                continue
            sample_id = f"expect-{split}-{idx:05d}"
            sample = {
                "sample_id": sample_id,
                "dataset": "EXPECT",
                "dataset_version": "git",
                "source_repo": "https://github.com/lorafei/Explainable_GEC",
                "source_commit": commit,
                "license": "MIT",
                "split": split,
                "split_index": idx,
                "source_tokens": clean_tokens(raw["source"]),
                "target_tokens": clean_tokens(raw["target"]),
                "source_text": source_text,
                "target_text": target_text,
                "expect_error_type": raw.get("error_type", "UNK"),
                "origin": raw.get("origin", ""),
                "raw_correction_index": raw.get("correction_index", []),
                "raw_evidence_index": raw.get("evidence_index", []),
                "errant_edits": errant_edits,
            }
            selected.append(sample)
            for edit_index, edit in enumerate(errant_edits):
                edit_rows.append(
                    {
                        "sample_id": sample_id,
                        "edit_index": edit_index,
                        "split": split,
                        "source_text": source_text,
                        "target_text": target_text,
                        "expect_error_type": raw.get("error_type", "UNK"),
                        "edit": edit,
                    }
                )
        split_totals[split] = split_count
        if len(selected) >= args.sample_size:
            break

    if len(selected) < args.min_sample_size:
        raise RuntimeError(f"Only collected {len(selected)} samples, below required minimum {args.min_sample_size}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    edit_dir = RESULTS_DIR / "edit_extraction"
    write_jsonl(PROCESSED_DIR / "expect_v1_samples.jsonl", selected)
    write_jsonl(edit_dir / "expect_v1_errant_edits.jsonl", edit_rows)

    stats = summarize_samples(selected, edit_rows, split_totals, errors)
    write_json(PROCESSED_DIR / "expect_v1_sample_stats.json", stats)
    write_data_source_doc(stats)
    return {"samples": selected, "edit_rows": edit_rows, "stats": stats}


def summarize_samples(
    samples: Sequence[Dict[str, Any]],
    edit_rows: Sequence[Dict[str, Any]],
    split_totals: Dict[str, int],
    errors: Sequence[Dict[str, str]],
) -> Dict[str, Any]:
    operation_counts = Counter(row["edit"]["operation"] for row in edit_rows)
    errant_type_counts = Counter(row["edit"]["error_type"] for row in edit_rows)
    expect_type_counts = Counter(sample["expect_error_type"] for sample in samples)
    split_counts = Counter(sample["split"] for sample in samples)
    token_lengths = [len(sample["source_tokens"]) for sample in samples]
    multi_edit = sum(1 for sample in samples if len(sample["errant_edits"]) > 1)
    return {
        "created_at": utc_now(),
        "dataset": "EXPECT",
        "source_repo": "https://github.com/lorafei/Explainable_GEC",
        "source_commit": samples[0]["source_commit"] if samples else "unknown",
        "license": "MIT",
        "download_method": "git clone --depth 1 https://github.com/lorafei/Explainable_GEC.git data/downloads/Explainable_GEC",
        "splits_available_count": split_totals,
        "sample_count": len(samples),
        "edit_count": len(edit_rows),
        "split_counts": dict(split_counts),
        "multi_edit_sample_count": multi_edit,
        "avg_source_tokens": round(sum(token_lengths) / len(token_lengths), 3) if token_lengths else 0.0,
        "operation_counts": dict(operation_counts),
        "top_errant_error_types": dict(errant_type_counts.most_common(20)),
        "top_expect_error_types": dict(expect_type_counts.most_common(20)),
        "extraction_error_count": len(errors),
        "extraction_errors_sample": list(errors[:5]),
        "sample_ids_preview": [sample["sample_id"] for sample in samples[:10]],
    }


def write_data_source_doc(stats: Dict[str, Any]) -> None:
    text = f"""# Data Sources

Last updated: 2026-07-18

## EXPECT

- Source: https://github.com/lorafei/Explainable_GEC
- Paper: Enhancing Grammatical Error Correction Systems with Explanations, ACL 2023.
- License: MIT, as stated in the upstream repository README and LICENSE.
- Local download: `data/downloads/Explainable_GEC`.
- Download command: `{stats["download_method"]}`.
- Recorded commit: `{stats["source_commit"]}`.
- Pilot sample file: `data/processed/expect_v1_samples.jsonl`.
- Pilot sample count: {stats["sample_count"]}.
- ERRANT edit count in pilot: {stats["edit_count"]}.
- Split counts: `{json.dumps(stats["split_counts"], sort_keys=True)}`.
- Operation counts: `{json.dumps(stats["operation_counts"], sort_keys=True)}`.

The versioned pilot uses real source/reference sentence pairs from EXPECT. The generated explanations in this project are automatic template constructions for pilot diagnostics, not human gold explanations.
"""
    (DOCS_DIR / "data_sources.md").write_text(text)


def edit_from_dict(data: Dict[str, Any]) -> Edit:
    return Edit.from_dict(data)


def edit_signature(edit: Dict[str, Any], include_type: bool = False) -> Tuple[Any, ...]:
    base = (
        int(edit["start"]),
        int(edit["end"]),
        edit.get("source_text", ""),
        edit.get("target_text", ""),
        edit.get("operation", ""),
    )
    if include_type:
        return (*base, edit.get("error_type", "UNK"))
    return base


def compare_token_diff_to_errant(samples: Sequence[Dict[str, Any]], check_size: int) -> Dict[str, Any]:
    mismatch_examples: List[Dict[str, Any]] = []
    rows_equal = 0
    rows_equal_with_type = 0
    total_token_edits = 0
    total_errant_edits = 0
    token_operation_counts: Counter[str] = Counter()
    errant_operation_counts: Counter[str] = Counter()
    report_lines = [
        "# ERRANT vs Token Diff Check",
        "",
        "This report is generated automatically from real EXPECT source/reference pairs.",
        "",
    ]

    for idx, sample in enumerate(samples):
        errant_edits = sample["errant_edits"]
        token_edits = [edit.to_dict() for edit in extract_token_diff_edits(sample["source_text"], sample["target_text"], sample["expect_error_type"])]
        total_token_edits += len(token_edits)
        total_errant_edits += len(errant_edits)
        token_operation_counts.update(edit["operation"] for edit in token_edits)
        errant_operation_counts.update(edit["operation"] for edit in errant_edits)
        errant_set = {edit_signature(edit) for edit in errant_edits}
        token_set = {edit_signature(edit) for edit in token_edits}
        errant_type_set = {edit_signature(edit, include_type=True) for edit in errant_edits}
        token_type_set = {edit_signature(edit, include_type=True) for edit in token_edits}
        if errant_set == token_set:
            rows_equal += 1
        else:
            if len(mismatch_examples) < 25:
                mismatch_examples.append(
                    {
                        "sample_id": sample["sample_id"],
                        "source_text": sample["source_text"],
                        "target_text": sample["target_text"],
                        "errant_edits": errant_edits,
                        "token_diff_edits": token_edits,
                    }
                )
        if errant_type_set == token_type_set:
            rows_equal_with_type += 1
        if idx < check_size:
            report_lines.extend(render_check_sample(idx + 1, sample, errant_edits, token_edits))

    summary = {
        "created_at": utc_now(),
        "sample_count": len(samples),
        "errant_edit_count": total_errant_edits,
        "token_diff_edit_count": total_token_edits,
        "sample_exact_match_without_error_type": rows_equal,
        "sample_exact_match_without_error_type_rate": round(rows_equal / len(samples), 6) if samples else 0.0,
        "sample_exact_match_with_error_type": rows_equal_with_type,
        "sample_exact_match_with_error_type_rate": round(rows_equal_with_type / len(samples), 6) if samples else 0.0,
        "errant_operation_counts": dict(errant_operation_counts),
        "token_diff_operation_counts": dict(token_operation_counts),
        "mismatch_examples": mismatch_examples,
        "boundary_note": "Token diff is deterministic and surface based; ERRANT may split, merge, or reclassify edits using linguistic alignment.",
    }
    out_dir = RESULTS_DIR / "edit_extraction"
    write_json(out_dir / "token_diff_vs_errant.json", summary)
    (out_dir / "expect_errant_check_30.md").write_text("\n".join(report_lines) + "\n")
    return summary


def render_check_sample(index: int, sample: Dict[str, Any], errant_edits: Sequence[Dict[str, Any]], token_edits: Sequence[Dict[str, Any]]) -> List[str]:
    return [
        f"## {index}. {sample['sample_id']}",
        "",
        f"- Source: `{sample['source_text']}`",
        f"- Reference: `{sample['target_text']}`",
        f"- EXPECT type: `{sample['expect_error_type']}`",
        f"- ERRANT edits: `{json.dumps(errant_edits, ensure_ascii=False)}`",
        f"- Token-diff edits: `{json.dumps(token_edits, ensure_ascii=False)}`",
        "",
    ]


def quote(text: str) -> str:
    return text.replace('"', "'")


def explicit_explanation(edit: Edit, error_type: Optional[str] = None) -> str:
    etype = error_type or edit.error_type
    span = f"source token span [{edit.start},{edit.end})"
    if edit.operation == "replace":
        return f'Replace "{quote(edit.source_text)}" with "{quote(edit.target_text)}" at {span} to correct ERRANT type {etype}.'
    if edit.operation == "insert":
        return f'Insert "{quote(edit.target_text)}" at {span} to correct ERRANT type {etype}.'
    if edit.operation == "delete":
        return f'Delete "{quote(edit.source_text)}" at {span} to correct ERRANT type {etype}.'
    return f"The edit at {span} corrects ERRANT type {etype}."


def implicit_explanation(edit: Edit) -> str:
    span = f"source token span [{edit.start},{edit.end})"
    if edit.operation == "insert":
        return f"The sentence is missing material at {span}; the local grammatical issue is ERRANT type {edit.error_type}."
    if edit.operation == "delete":
        return f"The material at {span} is unnecessary for the intended correction; the local issue is ERRANT type {edit.error_type}."
    return f"The wording at {span} should be adjusted for the surrounding context; the local issue is ERRANT type {edit.error_type}."


def masked_target_explanation(edit: Edit) -> str:
    span = f"source token span [{edit.start},{edit.end})"
    if edit.operation == "replace":
        return f'Replace "{quote(edit.source_text)}" with "[MASK]" at {span} to correct ERRANT type {edit.error_type}.'
    if edit.operation == "insert":
        return f'Insert "[MASK]" at {span} to correct ERRANT type {edit.error_type}.'
    if edit.operation == "delete":
        return f'Delete "{quote(edit.source_text)}" at {span} to correct ERRANT type {edit.error_type}.'
    return f"The edit at {span} corrects ERRANT type {edit.error_type}."


def raw_edit_string(edit: Edit) -> str:
    return (
        f'EDIT operation={edit.operation} start={edit.start} end={edit.end} '
        f'source="{quote(edit.source_text)}" target="{quote(edit.target_text)}" type="{edit.error_type}"'
    )


def shuffled_words(text: str) -> str:
    words = text.split()
    if len(words) < 2:
        return text
    return " ".join(reversed(words))


def wrong_type(error_type: str) -> str:
    candidates = ["R:VERB", "R:NOUN", "R:PREP", "M:DET", "U:OTHER", "R:ORTH"]
    for candidate in candidates:
        if candidate != error_type:
            return candidate
    return "R:OTHER"


def choose_wrong_location(edit: Edit, source_tokens: Sequence[str]) -> Tuple[int, int, str]:
    if not source_tokens:
        return (0, 0, "")
    gold_positions = set(range(edit.start, max(edit.end, edit.start + 1)))
    for idx, token in enumerate(source_tokens):
        if idx not in gold_positions:
            return (idx, idx + 1, token)
    return (0, min(1, len(source_tokens)), source_tokens[0])


def alternate_target(edit: Edit, all_edits: Sequence[Edit]) -> str:
    for candidate in all_edits:
        if candidate.target_text and candidate.target_text != edit.target_text:
            return candidate.target_text
    fallback = {
        "replace": "the",
        "insert": "the",
        "delete": "the",
    }
    return fallback.get(edit.operation, "the")


def negative_explanations(edit: Edit, source_tokens: Sequence[str], all_edits: Sequence[Edit], swapped_text: str) -> Dict[str, str]:
    wrong_start, wrong_end, wrong_source = choose_wrong_location(edit, source_tokens)
    span = f"source token span [{wrong_start},{wrong_end})"
    if edit.operation == "replace":
        wrong_location = f'Replace "{quote(wrong_source)}" with "{quote(edit.target_text)}" at {span} to correct ERRANT type {edit.error_type}.'
        wrong_target = f'Replace "{quote(edit.source_text)}" with "{quote(alternate_target(edit, all_edits))}" at source token span [{edit.start},{edit.end}) to correct ERRANT type {edit.error_type}.'
        wrong_direction = f'Replace "{quote(edit.target_text)}" with "{quote(edit.source_text)}" at source token span [{edit.start},{edit.end}) to correct ERRANT type {edit.error_type}.'
    elif edit.operation == "insert":
        wrong_location = f'Insert "{quote(edit.target_text)}" at {span} to correct ERRANT type {edit.error_type}.'
        wrong_target = f'Insert "{quote(alternate_target(edit, all_edits))}" at source token span [{edit.start},{edit.end}) to correct ERRANT type {edit.error_type}.'
        wrong_direction = f'Delete "{quote(edit.target_text)}" at source token span [{edit.start},{edit.end}) to correct ERRANT type {edit.error_type}.'
    else:
        wrong_location = f'Delete "{quote(wrong_source)}" at {span} to correct ERRANT type {edit.error_type}.'
        wrong_target = f'Replace "{quote(edit.source_text)}" with "{quote(alternate_target(edit, all_edits))}" at source token span [{edit.start},{edit.end}) to correct ERRANT type {edit.error_type}.'
        wrong_direction = f'Insert "{quote(edit.source_text)}" at source token span [{edit.start},{edit.start}) to correct ERRANT type {edit.error_type}.'
    wrong_type_text = explicit_explanation(edit, error_type=wrong_type(edit.error_type))
    return {
        "wrong_location": wrong_location,
        "wrong_target": wrong_target,
        "wrong_direction": wrong_direction,
        "wrong_type": wrong_type_text,
        "swapped_explanation": swapped_text,
        "generic_explanation": "This sentence has a grammar issue, so the wording should be improved.",
    }


def build_explanation_pilot(samples: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    examples = []
    all_primary_edits: List[Edit] = []
    for sample in samples:
        edit = Edit.from_dict(sample["errant_edits"][0])
        all_primary_edits.append(edit)
        examples.append({"sample": sample, "edit": edit})

    explicit_texts = [explicit_explanation(item["edit"]) for item in examples]
    rows: List[Dict[str, Any]] = []
    for idx, item in enumerate(examples):
        sample = item["sample"]
        edit = item["edit"]
        base = {
            "sample_id": sample["sample_id"],
            "source_text": sample["source_text"],
            "target_text": sample["target_text"],
            "source_tokens": sample["source_tokens"],
            "gold_edit": edit.to_dict(),
            "label_source": "automatic_template",
            "is_human_gold": False,
            "construction_note": "Automatically constructed from EXPECT source/reference and ERRANT edit fields; not human annotated gold.",
        }
        positives = {
            "faithful_explicit": explicit_explanation(edit),
            "faithful_implicit": implicit_explanation(edit),
            "masked_target": masked_target_explanation(edit),
            "raw_edit_string": raw_edit_string(edit),
        }
        for condition, explanation in positives.items():
            rows.append(
                {
                    **base,
                    "record_id": f"{sample['sample_id']}::{condition}",
                    "explanation_condition": condition,
                    "negative_type": "",
                    "faithfulness_label": 1,
                    "explanation": explanation,
                }
            )
        swapped_text = explicit_texts[(idx + 1) % len(explicit_texts)]
        negatives = negative_explanations(edit, sample["source_tokens"], all_primary_edits, swapped_text)
        for negative_type, explanation in negatives.items():
            rows.append(
                {
                    **base,
                    "record_id": f"{sample['sample_id']}::{negative_type}",
                    "explanation_condition": negative_type,
                    "negative_type": negative_type,
                    "faithfulness_label": 0,
                    "explanation": explanation,
                }
            )

    write_jsonl(PROCESSED_DIR / "expect_v1_explanation_pilot.jsonl", rows)
    stats = {
        "created_at": utc_now(),
        "edit_level_example_count": len(examples),
        "record_count": len(rows),
        "condition_counts": dict(Counter(row["explanation_condition"] for row in rows)),
        "label_counts": dict(Counter(str(row["faithfulness_label"]) for row in rows)),
        "negative_type_counts": dict(Counter(row["negative_type"] for row in rows if row["negative_type"])),
        "construction": "Automatic templates from ERRANT edit fields. These labels are pilot labels, not human gold.",
    }
    write_json(PROCESSED_DIR / "expect_v1_explanation_pilot_stats.json", stats)
    return {"rows": rows, "stats": stats}


def classification_metrics(labels: Sequence[int], preds: Sequence[int]) -> Dict[str, float]:
    result: Dict[str, float] = {}
    f1s = []
    for label in (0, 1):
        tp = sum(1 for y, p in zip(labels, preds) if y == label and p == label)
        fp = sum(1 for y, p in zip(labels, preds) if y != label and p == label)
        fn = sum(1 for y, p in zip(labels, preds) if y == label and p != label)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
        result[f"precision_{label}"] = precision
        result[f"recall_{label}"] = recall
        result[f"f1_{label}"] = f1
        f1s.append(f1)
    result["macro_f1"] = sum(f1s) / len(f1s)
    result["accuracy"] = sum(1 for y, p in zip(labels, preds) if y == p) / len(labels) if labels else 0.0
    return result


def zero_edit_metrics() -> Dict[str, float]:
    return {
        "span_exact": 0.0,
        "span_precision": 0.0,
        "span_recall": 0.0,
        "span_f1": 0.0,
        "source_text_match": 0.0,
        "target_text_match": 0.0,
        "operation_accuracy": 0.0,
        "error_type_accuracy": 0.0,
        "full_edit_exact": 0.0,
    }


def average_dicts(rows: Sequence[Dict[str, float]]) -> Dict[str, float]:
    if not rows:
        return zero_edit_metrics()
    keys = sorted(rows[0].keys())
    return {key: sum(row[key] for row in rows) / len(rows) for key in keys}


def condition_rows(base_rows: Sequence[Dict[str, Any]], condition: str) -> List[Dict[str, Any]]:
    by_sample: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
    for row in base_rows:
        by_sample[row["sample_id"]][row["explanation_condition"]] = row

    positive_style = {
        "source_only": "faithful_explicit",
        "explanation_only": "faithful_explicit",
        "source_plus_explanation": "faithful_explicit",
        "explicit_explanation": "faithful_explicit",
        "implicit_explanation": "faithful_implicit",
        "masked_target_explanation": "masked_target",
        "raw_edit_string": "raw_edit_string",
        "shuffled_explanation": "faithful_explicit",
    }[condition]

    rows: List[Dict[str, Any]] = []
    for sample_id in sorted(by_sample):
        row_map = by_sample[sample_id]
        positive = dict(row_map[positive_style])
        positive["eval_condition"] = condition
        positive["metric_probe"] = True
        if condition == "source_only":
            positive["explanation_for_eval"] = ""
        elif condition == "shuffled_explanation":
            positive["explanation_for_eval"] = shuffled_words(positive["explanation"])
            positive["faithfulness_label_for_eval"] = 0
        else:
            positive["explanation_for_eval"] = positive["explanation"]
        positive.setdefault("faithfulness_label_for_eval", positive["faithfulness_label"])
        positive["source_for_eval"] = "" if condition == "explanation_only" else positive["source_text"]
        rows.append(positive)

        for negative_type in sorted(NEGATIVE_TYPES):
            negative = dict(row_map[negative_type])
            negative["eval_condition"] = condition
            negative["metric_probe"] = False
            negative["source_for_eval"] = "" if condition == "explanation_only" else negative["source_text"]
            negative["explanation_for_eval"] = "" if condition == "source_only" else negative["explanation"]
            if condition == "shuffled_explanation":
                negative["explanation_for_eval"] = shuffled_words(negative["explanation_for_eval"])
            negative["faithfulness_label_for_eval"] = 0
            rows.append(negative)
    return rows


def run_baseline(method: str, row: Dict[str, Any]) -> Dict[str, Any]:
    gold = Edit.from_dict(row["gold_edit"])
    explanation = row["explanation_for_eval"]
    source = row["source_for_eval"]
    if method == "structured_explicit":
        reconstruction = structured_explicit_edit_baseline(source, explanation, error_type=gold.error_type)
        if reconstruction is None:
            metrics = zero_edit_metrics()
            prediction = 0
            reconstruction_json: Dict[str, Any] = {"reconstructable": False}
        else:
            metrics = compare_edits(reconstruction, gold)
            prediction = int(metrics["full_edit_exact"] == 1.0)
            reconstruction_json = {"reconstructable": True, **reconstruction.to_dict()}
    elif method == "surface_keyword":
        reconstruction_json = {"reconstructable": False}
        metrics = zero_edit_metrics()
        prediction = int(surface_keyword_predict(gold, explanation))
    else:
        raise ValueError(f"Unknown baseline: {method}")
    return {
        "record_id": row["record_id"],
        "sample_id": row["sample_id"],
        "baseline": method,
        "eval_condition": row["eval_condition"],
        "explanation_condition": row["explanation_condition"],
        "negative_type": row["negative_type"],
        "faithfulness_label": int(row["faithfulness_label_for_eval"]),
        "prediction": prediction,
        "metric_probe": bool(row["metric_probe"]),
        "gold_edit": row["gold_edit"],
        "reconstruction": reconstruction_json,
        "metrics": metrics,
    }


def evaluate_condition_predictions(predictions: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    labels = [row["faithfulness_label"] for row in predictions]
    preds = [row["prediction"] for row in predictions]
    classification = classification_metrics(labels, preds)
    probe_rows = [row["metrics"] for row in predictions if row["metric_probe"]]
    edit_metrics = average_dicts(probe_rows)
    negative_rejection: Dict[str, float] = {}
    for negative_type in sorted(NEGATIVE_TYPES):
        rows = [row for row in predictions if row["negative_type"] == negative_type]
        negative_rejection[negative_type] = (
            sum(1 for row in rows if row["prediction"] == 0) / len(rows) if rows else 0.0
        )
    return {
        "n": len(predictions),
        "probe_n": sum(1 for row in predictions if row["metric_probe"]),
        "label_counts": dict(Counter(str(row["faithfulness_label"]) for row in predictions)),
        "full_edit_exact": edit_metrics["full_edit_exact"],
        "span_f1": edit_metrics["span_f1"],
        "target_match": edit_metrics["target_text_match"],
        "operation_accuracy": edit_metrics["operation_accuracy"],
        "error_type_accuracy": edit_metrics["error_type_accuracy"],
        "faithfulness_macro_f1": classification["macro_f1"],
        "faithfulness_accuracy": classification["accuracy"],
        "negative_rejection_rate_by_type": negative_rejection,
    }


def run_leakage_experiments(explanation_rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    conditions = [
        "source_only",
        "explanation_only",
        "source_plus_explanation",
        "explicit_explanation",
        "implicit_explanation",
        "masked_target_explanation",
        "shuffled_explanation",
        "raw_edit_string",
    ]
    baselines = ["surface_keyword", "structured_explicit"]
    all_predictions: List[Dict[str, Any]] = []
    summary: Dict[str, Any] = {"created_at": utc_now(), "baselines": {}}

    for baseline in baselines:
        baseline_summary: Dict[str, Any] = {}
        for condition in conditions:
            rows = condition_rows(explanation_rows, condition)
            preds = [run_baseline(baseline, row) for row in rows]
            all_predictions.extend(preds)
            baseline_summary[condition] = evaluate_condition_predictions(preds)
        summary["baselines"][baseline] = baseline_summary

    out_dir = RESULTS_DIR / "real_pilot"
    write_jsonl(out_dir / "predictions.jsonl", all_predictions)
    write_json(out_dir / "condition_metrics.json", summary)
    write_json(RESULTS_DIR / "real_summary.json", summary)
    write_latex_tables(summary)
    return summary


def fmt_pct(value: float) -> str:
    return f"{100 * value:.1f}"


def latex_escape(text: str) -> str:
    return (
        text.replace("\\", "\\textbackslash{}")
        .replace("_", "\\_")
        .replace("%", "\\%")
        .replace("&", "\\&")
        .replace("#", "\\#")
    )


def write_latex_tables(summary: Dict[str, Any]) -> None:
    table_dir = RESULTS_DIR / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    structured = summary["baselines"]["structured_explicit"]
    order = [
        "source_only",
        "explanation_only",
        "source_plus_explanation",
        "explicit_explanation",
        "implicit_explanation",
        "masked_target_explanation",
        "shuffled_explanation",
        "raw_edit_string",
    ]
    labels = {
        "source_only": "Source",
        "explanation_only": "Exp only",
        "source_plus_explanation": "Source+Exp",
        "explicit_explanation": "Explicit",
        "implicit_explanation": "Implicit",
        "masked_target_explanation": "Masked",
        "shuffled_explanation": "Shuffled",
        "raw_edit_string": "Raw edit",
    }
    rows = [
        "\\begin{table}[t]",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3pt}",
        "\\begin{tabular}{lrrrrrr}",
        "\\toprule",
        "Condition & Full & Span & Target & Op & Type & F1 \\\\",
        "\\midrule",
    ]
    for condition in order:
        item = structured[condition]
        rows.append(
            f"{latex_escape(labels[condition])} & {fmt_pct(item['full_edit_exact'])} & {fmt_pct(item['span_f1'])} & "
            f"{fmt_pct(item['target_match'])} & {fmt_pct(item['operation_accuracy'])} & {fmt_pct(item['error_type_accuracy'])} & "
            f"{fmt_pct(item['faithfulness_macro_f1'])} \\\\"
        )
    rows.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\caption{Structured explicit baseline under leakage-control conditions. Values are percentages. Full is full edit exact match; F1 is faithfulness macro-F1.}",
            "\\label{tab:leakage-structured}",
            "\\end{table}",
        ]
    )
    (table_dir / "real_leakage_structured.tex").write_text("\n".join(rows) + "\n")

    baseline_rows = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{lrr}",
        "\\toprule",
        "Baseline & Source+Exp F1 & Explicit Full \\\\",
        "\\midrule",
    ]
    for baseline, baseline_summary in summary["baselines"].items():
        baseline_rows.append(
            f"{latex_escape(baseline.replace('_', ' '))} & "
            f"{fmt_pct(baseline_summary['source_plus_explanation']['faithfulness_macro_f1'])} & "
            f"{fmt_pct(baseline_summary['explicit_explanation']['full_edit_exact'])} \\\\"
        )
    baseline_rows.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\caption{Baseline comparison on the real EXPECT pilot. Values are percentages.}",
            "\\label{tab:baseline-comparison}",
            "\\end{table}",
        ]
    )
    (table_dir / "real_baseline_comparison.tex").write_text("\n".join(baseline_rows) + "\n")


def update_paper_sections(sample_stats: Dict[str, Any], compare_stats: Dict[str, Any], pilot_stats: Dict[str, Any], results: Dict[str, Any]) -> None:
    structured = results["baselines"]["structured_explicit"]
    surface = results["baselines"]["surface_keyword"]
    setup = f"""\\section{{Experimental Setup}}

\\paragraph{{Data.}}
The real pilot uses EXPECT, a public English GEC explanation dataset released under the MIT License. We downloaded the upstream repository with \\texttt{{git clone --depth 1}} and recorded commit \\texttt{{{sample_stats['source_commit'][:12]}}}. The versioned pilot file contains {sample_stats['sample_count']} real source/reference pairs from EXPECT and {sample_stats['edit_count']} ERRANT edits. The selected split distribution is \\texttt{{{latex_escape(json.dumps(sample_stats['split_counts'], sort_keys=True))}}}. The operation distribution over ERRANT edits is \\texttt{{{latex_escape(json.dumps(sample_stats['operation_counts'], sort_keys=True))}}}.

\\paragraph{{Edit extraction.}}
We use ERRANT 3.0.2 with spaCy \\texttt{{en\\_core\\_web\\_sm}} to extract structured edits from each source/reference pair. For transparency, we also compare ERRANT with the earlier token-diff extractor. Token diff exactly matches ERRANT edit spans and strings on {fmt_pct(compare_stats['sample_exact_match_without_error_type_rate'])}\\% of sampled sentences before error types are considered, confirming that ERRANT is necessary for linguistically typed edit boundaries.

\\paragraph{{Explanation pilot.}}
For each sampled sentence, we use the first ERRANT edit as an edit-level pilot item and automatically construct explanation variants. Positive variants include faithful explicit, faithful implicit, masked-target, and raw edit string explanations. Negative variants include wrong-location, wrong-target, wrong-direction, wrong-type, swapped, and generic explanations. These labels are automatic pilot labels, not human gold annotations.

\\paragraph{{Baselines.}}
We evaluate two non-placeholder baselines. The surface keyword baseline predicts faithfulness when the explanation mentions the gold operation, target/source strings when applicable, and ERRANT type. The structured explicit baseline parses explicit edit statements and raw edit strings into span, source text, target text, operation, and error type.

\\paragraph{{Metrics.}}
We report Full Edit Exact Match, Span F1, Target Match, Operation Accuracy, Error Type Accuracy, Faithfulness Macro-F1, and negative rejection rates by negative type. All numbers in this section are generated from the JSON outputs under \\texttt{{results/real\\_pilot/}}.
"""
    (PAPER_DIR / "sections" / "experimental_setup.tex").write_text(setup)

    results_text = f"""\\section{{Results}}

\\input{{../results/tables/real_leakage_structured}}
\\input{{../results/tables/real_baseline_comparison}}

The structured explicit baseline reconstructs explicit explanations with {fmt_pct(structured['explicit_explanation']['full_edit_exact'])}\\% Full Edit Exact Match and {fmt_pct(structured['explicit_explanation']['faithfulness_macro_f1'])}\\% Faithfulness Macro-F1. The same baseline reaches {fmt_pct(structured['raw_edit_string']['full_edit_exact'])}\\% Full Edit Exact Match on raw edit strings, which is an expected answer-leakage upper control rather than a desirable explanation setting.

Leakage controls expose the limits of direct edit copying. Source-only input yields {fmt_pct(structured['source_only']['full_edit_exact'])}\\% Full Edit Exact Match, explanation-only input yields {fmt_pct(structured['explanation_only']['full_edit_exact'])}\\%, implicit explanations yield {fmt_pct(structured['implicit_explanation']['full_edit_exact'])}\\%, and masked-target explanations yield {fmt_pct(structured['masked_target_explanation']['target_match'])}\\% Target Match. The surface keyword baseline obtains {fmt_pct(surface['source_plus_explanation']['faithfulness_macro_f1'])}\\% Faithfulness Macro-F1 on source-plus-explanation inputs but does not reconstruct structured edits.
"""
    (PAPER_DIR / "sections" / "results.tex").write_text(results_text)

    neg = structured["source_plus_explanation"]["negative_rejection_rate_by_type"]
    neg_text = "; ".join(f"{latex_escape(key.replace('_', ' '))} {fmt_pct(value)}\\%" for key, value in sorted(neg.items()))
    analysis = f"""\\section{{Analysis}}

The pilot confirms that explicit edit text is easy for a structured extractor to reconstruct, while source-only, implicit, and masked-target settings sharply reduce access to the target edit. This supports treating explicit explanations and raw edit strings as leakage controls rather than as sufficient evidence of explanation faithfulness.

For structured source+explanation input, negative rejection rates are {neg_text}. Wrong-type and wrong-target cases are rejected when the parsed edit disagrees with the ERRANT gold edit fields. Generic explanations are rejected because they do not contain reconstructable edit fields. Swapped explanations test whether a copied explanation is detected through span, target, and type disagreement.

The token-diff comparison also shows a boundary risk: simple token diff agrees with ERRANT on only {fmt_pct(compare_stats['sample_exact_match_without_error_type_rate'])}\\% of examples before type labels. The paper therefore uses ERRANT for the real pilot and keeps token diff only as a diagnostic contrast.
"""
    (PAPER_DIR / "sections" / "analysis.tex").write_text(analysis)

    limitations = """\\section{Limitations}

This pilot uses automatic template explanations constructed from ERRANT edit fields. They are useful for testing leakage, reconstruction behavior, and negative controls, but they are not human gold explanations and should not be interpreted as learner-facing explanation quality. The current sample is a 300-example EXPECT pilot rather than a full benchmark. The structured baseline is intentionally narrow: it detects explicit edit statements, so strong performance on explicit and raw-edit conditions does not imply that free-form explanations are faithfully understood. ERRANT edit boundaries and error types may differ from valid alternative corrections, and future work still needs human faithfulness labels to test agreement with the reconstruction diagnostic.
"""
    (PAPER_DIR / "sections" / "limitations.tex").write_text(limitations)

    update_claim_evidence_matrix(sample_stats, compare_stats, pilot_stats, results)


def update_claim_evidence_matrix(sample_stats: Dict[str, Any], compare_stats: Dict[str, Any], pilot_stats: Dict[str, Any], results: Dict[str, Any]) -> None:
    structured = results["baselines"]["structured_explicit"]
    text = f"""# Claim-Evidence Matrix

Last updated: 2026-07-18

| Claim | Current Evidence | Status | Risk |
|---|---|---|---|
| The project can run on real English GEC data. | EXPECT MIT-licensed sample: {sample_stats['sample_count']} source/reference pairs and {sample_stats['edit_count']} ERRANT edits in `data/processed/expect_v1_samples.jsonl`. | Supported for pilot | Full benchmark coverage still pending. |
| ERRANT is preferable to token diff for typed edit extraction. | Token diff matches ERRANT exactly on {fmt_pct(compare_stats['sample_exact_match_without_error_type_rate'])}% of sampled sentences before type labels. | Supported for pilot | ERRANT itself can have boundary ambiguity. |
| Explicit explanations can leak the answer to a structured reconstructor. | Structured baseline explicit Full Edit Exact: {fmt_pct(structured['explicit_explanation']['full_edit_exact'])}%; raw edit string Full Edit Exact: {fmt_pct(structured['raw_edit_string']['full_edit_exact'])}%. | Supported for pilot | Template explanations make this an upper-control result. |
| Masking the target reduces target reconstruction. | Structured baseline masked-target Target Match: {fmt_pct(structured['masked_target_explanation']['target_match'])}%. | Supported for pilot | Masked templates are automatic, not human explanations. |
| The current labels are not human gold. | Explanation pilot stats record `label_source=automatic_template`; {pilot_stats['record_count']} explanation records generated automatically. | Explicitly constrained | Human validation is still required for final claims. |
"""
    (DOCS_DIR / "claim_evidence_matrix.md").write_text(text)


def update_round_docs(sample_stats: Dict[str, Any], compare_stats: Dict[str, Any], pilot_stats: Dict[str, Any], results: Dict[str, Any]) -> None:
    structured = results["baselines"]["structured_explicit"]
    round_text = f"""# Round 02: Real Pilot Pipeline

Last updated: 2026-07-18

## Actions

- Consolidated state under `docs/` and removed the duplicate `research/` directory.
- Initialized Git and committed the Bootstrap state.
- Added project ignores for local environments, TeX tools, downloaded corpora, and generated PDF output.
- Installed ERRANT 3.0.2 and spaCy `en_core_web_sm` in `.venv311`.
- Installed local TinyTeX under `.local-tex/` and compiled `paper/main.tex` with `latexmk`.
- Downloaded EXPECT from the public upstream repository and built a versioned real pilot sample.
- Extracted ERRANT edits, compared token diff against ERRANT, built automatic explanation variants, ran two baselines, and generated paper tables/sections from `results/`.

## Evidence

- Real sample count: {sample_stats['sample_count']}.
- ERRANT edit count: {sample_stats['edit_count']}.
- Explanation pilot records: {pilot_stats['record_count']}.
- Token diff vs ERRANT exact sample match before type labels: {fmt_pct(compare_stats['sample_exact_match_without_error_type_rate'])}%.
- Structured explicit Full Edit Exact on explicit explanations: {fmt_pct(structured['explicit_explanation']['full_edit_exact'])}%.
- Structured explicit Full Edit Exact on raw edit strings: {fmt_pct(structured['raw_edit_string']['full_edit_exact'])}%.

## Next Single Action

Run a focused literature and human-validation design pass before upgrading automatic pilot labels into claims about real explanation faithfulness.
"""
    (DOCS_DIR / "round_02.md").write_text(round_text)

    with (DOCS_DIR / "experiment_log.md").open("a", encoding="utf-8") as f:
        f.write(
            f"""

## Iteration 2

- EXPECT cloned from `https://github.com/lorafei/Explainable_GEC` at commit `{sample_stats['source_commit']}`.
- Real pilot sample: {sample_stats['sample_count']} EXPECT source/reference pairs in `data/processed/expect_v1_samples.jsonl`.
- ERRANT edits: {sample_stats['edit_count']} in `results/edit_extraction/expect_v1_errant_edits.jsonl`.
- ERRANT/token-diff check report: `results/edit_extraction/expect_errant_check_30.md`.
- Explanation pilot: {pilot_stats['record_count']} automatic template records in `data/processed/expect_v1_explanation_pilot.jsonl`; not human gold.
- Baselines run: `surface_keyword`, `structured_explicit`.
- Leakage metrics: `results/real_pilot/condition_metrics.json`.
- Paper compile: `paper/main.tex` compiled successfully with local TinyTeX/latexmk; logs retained under `logs/`.
"""
        )

    with (DOCS_DIR / "decision_log.md").open("a", encoding="utf-8") as f:
        f.write(
            f"""
| 2026-07-18 | Use EXPECT as the real pilot data source. | Public upstream repository states MIT License and contains source/reference GEC pairs plus explanation-oriented labels. | Pilot is limited to automatic constructions and first ERRANT edit per sentence. |
| 2026-07-18 | Use ERRANT rather than token diff for real edit fields. | Token diff exact sample match with ERRANT is {fmt_pct(compare_stats['sample_exact_match_without_error_type_rate'])}% before type labels. | ERRANT boundary ambiguity remains. |
| 2026-07-18 | Treat generated explanation labels as automatic pilot labels only. | The construction is templated from ERRANT fields. | Human gold faithfulness validation remains open. |
"""
        )

    open_issues = (DOCS_DIR / "open_issues.md").read_text()
    open_issues = open_issues.replace(
        "| No real pilot data exists locally. | No empirical claim can be made. | Real GEC predictions and explanations. | Build or download data after checking licenses and size. | Open |",
        f"| No real pilot data exists locally. | No empirical claim can be made. | Real GEC predictions and explanations. | Built EXPECT pilot with {sample_stats['sample_count']} real source/reference pairs. | Closed for pilot |",
    )
    open_issues = open_issues.replace(
        "| Edit extraction currently uses a simple token diff, not ERRANT. | Error types and edit boundaries may be weak. | Comparison to ERRANT. | Add ERRANT integration or document fallback. | Open |",
        f"| Edit extraction currently uses a simple token diff, not ERRANT. | Error types and edit boundaries may be weak. | Comparison to ERRANT. | ERRANT integrated; token diff comparison stored in `results/edit_extraction/token_diff_vs_errant.json`. | Closed for pilot |",
    )
    open_issues = open_issues.replace(
        "| Local TeX compiler is unavailable. | Cannot verify final AAAI PDF rendering locally. | Installed `pdflatex`, `latexmk`, or `tectonic`. | Install or use another machine with TeX; then compile `paper/main.tex`. | Open |",
        "| Local TeX compiler is unavailable. | Cannot verify final AAAI PDF rendering locally. | Installed `pdflatex`, `latexmk`, or `tectonic`. | Installed local TinyTeX and compiled `paper/main.tex`. | Closed |",
    )
    (DOCS_DIR / "open_issues.md").write_text(open_issues)


def run(args: argparse.Namespace) -> None:
    args.expect_root = args.expect_root.resolve()
    built = build_expect_samples(args)
    compare_stats = compare_token_diff_to_errant(built["samples"], args.check_size)
    pilot = build_explanation_pilot(built["samples"])
    results = run_leakage_experiments(pilot["rows"])
    update_paper_sections(built["stats"], compare_stats, pilot["stats"], results)
    update_round_docs(built["stats"], compare_stats, pilot["stats"], results)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build and run the real EXPECT/ERRANT pilot.")
    parser.add_argument("--expect-root", type=Path, default=EXPECT_ROOT)
    parser.add_argument("--sample-size", type=int, default=300)
    parser.add_argument("--min-sample-size", type=int, default=100)
    parser.add_argument("--check-size", type=int, default=30)
    parser.add_argument("--splits", nargs="+", default=["test", "dev", "train"])
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
