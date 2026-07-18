from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import errant

from analyze_model_edits import extract_edits


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = ROOT / "results" / "round08"


LABELS = ["preserve", "cancel", "change_target", "change_span", "change_operation", "competing_edit"]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def norm(text: str) -> str:
    return " ".join(text.lower().split())


def same_exact(pred: Dict[str, Any], original: Dict[str, Any]) -> bool:
    keys = ["source_text", "target_text", "operation"]
    return all(pred.get(key, "") == original.get(key, "") for key in keys)


def classify_counterfactual_behavior(cf_edits: List[Dict[str, Any]], original: Dict[str, Any]) -> Tuple[str, Dict[str, Any] | None]:
    for edit in cf_edits:
        if same_exact(edit, original):
            return "preserve", edit
    same_source = [edit for edit in cf_edits if norm(edit.get("source_text", "")) == norm(original.get("source_text", ""))]
    if same_source:
        if any(edit.get("operation") != original.get("operation") for edit in same_source):
            return "change_operation", same_source[0]
        if any(norm(edit.get("target_text", "")) != norm(original.get("target_text", "")) for edit in same_source):
            return "change_target", same_source[0]
    same_target = [edit for edit in cf_edits if norm(edit.get("target_text", "")) == norm(original.get("target_text", ""))]
    if same_target:
        return "change_span", same_target[0]
    if cf_edits:
        return "competing_edit", cf_edits[0]
    return "cancel", None


def original_source_available(source: str, original: Dict[str, Any]) -> bool:
    src = norm(original.get("source_text", ""))
    if not src:
        return norm(original.get("target_text", "")) not in norm(source)
    return src in norm(source)


def predict_random(row: Dict[str, Any]) -> str:
    bucket = int(hashlib.sha1(row["counterfactual_id"].encode("utf-8")).hexdigest(), 16) % len(LABELS)
    return LABELS[bucket]


def predict_family_prior(row: Dict[str, Any]) -> str:
    if row["variant_family"] == "error_irrelevant":
        return "preserve"
    return "cancel"


def predict_source_availability(row: Dict[str, Any]) -> str:
    if original_source_available(row["source"], row["original_predicted_edit"]):
        return "preserve"
    return "cancel"


def f1_for_label(pairs: List[Tuple[str, str]], label: str) -> float:
    tp = sum(1 for pred, gold in pairs if pred == label and gold == label)
    fp = sum(1 for pred, gold in pairs if pred == label and gold != label)
    fn = sum(1 for pred, gold in pairs if pred != label and gold == label)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


def multiclass_metrics(pairs: List[Tuple[str, str]]) -> Dict[str, Any]:
    labels = sorted(set(LABELS) | {gold for _, gold in pairs} | {pred for pred, _ in pairs})
    total = len(pairs)
    return {
        "n": total,
        "accuracy": sum(1 for pred, gold in pairs if pred == gold) / total if total else 0.0,
        "macro_f1": sum(f1_for_label(pairs, label) for label in labels) / len(labels) if labels else 0.0,
        "label_f1": {label: f1_for_label(pairs, label) for label in labels},
        "prediction_counts": dict(Counter(pred for pred, _ in pairs)),
        "gold_counts": dict(Counter(gold for _, gold in pairs)),
    }


def render_checks(rows: List[Dict[str, Any]], limit: int) -> str:
    lines = [
        "# Round 08 Counterfactual Check",
        "",
        "Labels below are computed from actual GEC model predictions on counterfactual sources, not from grammar-theory expectations.",
        "",
    ]
    for index, row in enumerate(rows[:limit], start=1):
        lines.extend(
            [
                f"## {index}. {row['model_key']}::{row['variant_family']}::{row['origin_edit_id']}",
                "",
                f"- Original source: `{row['original_source']}`",
                f"- Counterfactual source: `{row['source']}`",
                f"- Counterfactual prediction: `{row['prediction']}`",
                f"- Original edit: `{json.dumps(row['original_predicted_edit'], ensure_ascii=False)}`",
                f"- Counterfactual edits: `{json.dumps(row['counterfactual_predicted_edits'], ensure_ascii=False)}`",
                f"- Actual label: `{row['actual_behavior_label']}`",
                "",
            ]
        )
    return "\n".join(lines)


def analyze(args: argparse.Namespace) -> None:
    annotator = errant.load("en")
    predictions = []
    for path in args.prediction_files:
        predictions.extend(read_jsonl(path))
    rows = []
    for row in predictions:
        cf_edits = extract_edits(annotator, row["source"], row["prediction"])
        label, matched = classify_counterfactual_behavior(cf_edits, row["original_predicted_edit"])
        rows.append(
            {
                "counterfactual_id": row["sample_id"],
                "origin_edit_id": row["origin_edit_id"],
                "origin_sample_id": row["origin_sample_id"],
                "origin_dataset": row["origin_dataset"],
                "split": row["split"],
                "model_key": row["model_key"],
                "model_family": row["model_family"],
                "original_behavior": row["original_behavior"],
                "original_error_type": row["original_error_type"],
                "variant_family": row["variant_family"],
                "variant_strategy": row["variant_strategy"],
                "source": row["source"],
                "prediction": row["prediction"],
                "original_source": row["original_source"],
                "original_prediction": row["original_prediction"],
                "original_predicted_edit": row["original_predicted_edit"],
                "counterfactual_predicted_edits": cf_edits,
                "matched_counterfactual_edit": matched,
                "actual_behavior_label": label,
                "label_source": "actual_original_gec_model_rerun",
            }
        )

    methods = {
        "random": predict_random,
        "variant_family_prior": predict_family_prior,
        "source_edit_availability": predict_source_availability,
    }
    method_pairs: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    method_pairs_by_family: Dict[str, Dict[str, List[Tuple[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        for name, fn in methods.items():
            pred = fn(row)
            gold = row["actual_behavior_label"]
            method_pairs[name].append((pred, gold))
            method_pairs_by_family[name][row["variant_family"]].append((pred, gold))

    summary = {
        "created_at": utc_now(),
        "counterfactual_count": len(rows),
        "model_counts": dict(Counter(row["model_key"] for row in rows)),
        "variant_family_counts": dict(Counter(row["variant_family"] for row in rows)),
        "actual_behavior_counts": dict(Counter(row["actual_behavior_label"] for row in rows)),
        "method_metrics": {name: multiclass_metrics(pairs) for name, pairs in method_pairs.items()},
        "method_metrics_by_variant_family": {
            name: {family: multiclass_metrics(pairs) for family, pairs in family_map.items()}
            for name, family_map in method_pairs_by_family.items()
        },
        "important_note": "Counterfactual labels come from actual reruns of the original public GEC model for each edit.",
    }

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "counterfactual_labels.jsonl", rows)
    write_json(args.out_dir / "counterfactual_method_metrics.json", summary)
    (args.out_dir / "counterfactual_check_30.md").write_text(render_checks(rows, args.check_size) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze actual GEC model behavior on Round 08 counterfactual variants.")
    parser.add_argument("--prediction-files", type=Path, nargs="+", required=True)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--check-size", type=int, default=30)
    return parser.parse_args()


if __name__ == "__main__":
    analyze(parse_args())
