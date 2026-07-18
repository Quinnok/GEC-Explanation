from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BENCHMARK = ROOT / "data" / "faithfulness_benchmark" / "edit_records.jsonl"
DEFAULT_OUT_DIR = ROOT / "data" / "counterfactuals"


TOKEN_REPLACEMENTS = {
    "i": "we",
    "my": "our",
    "me": "us",
    "community": "city",
    "restaurant": "cafe",
    "technology": "science",
    "computers": "devices",
    "cars": "vehicles",
    "house": "team",
    "museum": "gallery",
    "family": "friends",
    "people": "students",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def apply_edit_to_source(source: str, edit: Dict[str, Any]) -> str:
    tokens = source.split()
    start = max(0, min(int(edit["start"]), len(tokens)))
    end = max(start, min(int(edit["end"]), len(tokens)))
    target_tokens = edit.get("target_text", "").split()
    return " ".join(tokens[:start] + target_tokens + tokens[end:])


def irrelevant_variant(source: str, edit: Dict[str, Any]) -> tuple[str, str]:
    tokens = source.split()
    start = int(edit["start"])
    end = int(edit["end"])
    for idx, token in enumerate(tokens):
        clean = token.strip("\"'`.,;:!?").lower()
        if start <= idx < end:
            continue
        if clean in TOKEN_REPLACEMENTS:
            replacement = TOKEN_REPLACEMENTS[clean]
            if token[:1].isupper():
                replacement = replacement.capitalize()
            new_tokens = list(tokens)
            new_tokens[idx] = replacement
            return " ".join(new_tokens), f"replace_non_error_token_{idx}_{clean}_to_{replacement.lower()}"
    if tokens and tokens[-1] in {".", "!", "?"}:
        return " ".join(tokens[:-1] + ["today", tokens[-1]]), "append_non_error_time_adverb_before_final_punctuation"
    return source + " today", "append_non_error_time_adverb"


def select_rows(rows: List[Dict[str, Any]], max_per_model: int) -> List[Dict[str, Any]]:
    buckets: Dict[str, Dict[str, List[Dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        buckets[row["model_key"]][row["behavior"]].append(row)
    selected: List[Dict[str, Any]] = []
    seen: set[str] = set()
    for model in sorted(buckets):
        per_behavior = max(1, max_per_model // max(1, len(buckets[model])))
        for behavior in sorted(buckets[model]):
            for row in buckets[model][behavior][:per_behavior]:
                selected.append(row)
                seen.add(row["edit_id"])
        for behavior in sorted(buckets[model]):
            for row in buckets[model][behavior]:
                if len([item for item in selected if item["model_key"] == model]) >= max_per_model:
                    break
                if row["edit_id"] not in seen:
                    selected.append(row)
                    seen.add(row["edit_id"])
    return selected


def build(args: argparse.Namespace) -> None:
    rows = read_jsonl(args.benchmark)
    selected = select_rows(rows, args.max_per_model)
    variants = []
    for row in selected:
        edit = row["predicted_edit"]
        irrelevant_source, irrelevant_strategy = irrelevant_variant(row["source"], edit)
        relevant_source = apply_edit_to_source(row["source"], edit)
        base = {
            "dataset": f"CF_{row.get('dataset', 'UNKNOWN')}",
            "split": row["split"],
            "target_text": row["reference"],
            "origin_edit_id": row["edit_id"],
            "origin_sample_id": row["sample_id"],
            "origin_dataset": row.get("dataset", "UNKNOWN"),
            "original_source": row["source"],
            "original_reference": row["reference"],
            "original_prediction": row["prediction"],
            "original_model_key": row["model_key"],
            "original_model_family": row.get("model_family", "unknown"),
            "original_behavior": row["behavior"],
            "original_error_type": row["error_type"],
            "original_predicted_edit": edit,
        }
        variants.append(
            {
                **base,
                "sample_id": f"cf::{row['edit_id']}::irrelevant",
                "source_text": irrelevant_source,
                "variant_family": "error_irrelevant",
                "variant_strategy": irrelevant_strategy,
                "intended_edit_relation": "preserve_edit_opportunity",
            }
        )
        variants.append(
            {
                **base,
                "sample_id": f"cf::{row['edit_id']}::apply_edit",
                "source_text": relevant_source,
                "variant_family": "rule_relevant",
                "variant_strategy": "apply_original_model_edit_to_source",
                "intended_edit_relation": "remove_or_change_original_edit_opportunity",
            }
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "round08_counterfactual_sources.jsonl", variants)
    by_model: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in variants:
        by_model[row["original_model_key"]].append(row)
    for model, model_rows in by_model.items():
        write_jsonl(args.out_dir / f"round08_counterfactual_sources_{model}.jsonl", model_rows)

    stats = {
        "created_at": utc_now(),
        "origin_edit_count": len(selected),
        "variant_count": len(variants),
        "max_per_model": args.max_per_model,
        "model_counts": dict(Counter(row["model_key"] for row in selected)),
        "variant_family_counts": dict(Counter(row["variant_family"] for row in variants)),
        "behavior_counts": dict(Counter(row["behavior"] for row in selected)),
        "error_type_count": len({row["error_type"] for row in selected}),
        "important_note": "Counterfactual labels are not assigned here; labels must be computed from actual reruns of the original GEC model.",
    }
    write_json(args.out_dir / "round08_counterfactual_source_stats.json", stats)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Round 08 counterfactual source variants from model-produced edits.")
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--max-per-model", type=int, default=8)
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
