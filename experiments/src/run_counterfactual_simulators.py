from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from analyze_counterfactuals import LABELS, multiclass_metrics, original_source_available


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BENCHMARK_DIR = ROOT / "data" / "faithfulness_benchmark"
DEFAULT_COUNTERFACTUALS = ROOT / "results" / "round09" / "counterfactual_labels.jsonl"
DEFAULT_OUT_DIR = ROOT / "results" / "round09"

SELECTED_EXPLANATION_TYPES = {
    "explicit_template",
    "masked_target_template",
    "rule_only",
    "rule_grounded_automatic",
    "gee_style_automatic",
    "wrong_rule",
    "wrong_target",
    "swapped_across_sentence",
    "generic",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def stable_label(key: str) -> str:
    idx = int(hashlib.sha1(key.encode("utf-8")).hexdigest(), 16) % len(LABELS)
    return LABELS[idx]


def load_explanations(path: Path) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in read_jsonl(path):
        if row["explanation_type"] in SELECTED_EXPLANATION_TYPES:
            grouped[row["edit_id"]].append(row)
    return grouped


def contains_edit_terms(example: Dict[str, Any]) -> Dict[str, bool]:
    explanation = example["explanation"].lower()
    edit = example["original_predicted_edit"]
    return {
        "source": bool(edit.get("source_text") and edit["source_text"].lower() in explanation),
        "target": bool(edit.get("target_text") and edit["target_text"].lower() in explanation),
        "operation": bool(edit.get("operation") and edit["operation"].lower() in explanation),
        "type": bool(example["original_error_type"].lower() in explanation),
    }


def variant_family_prior(example: Dict[str, Any]) -> str:
    return "preserve" if example["variant_family"] == "error_irrelevant" else "cancel"


def source_edit_availability(example: Dict[str, Any]) -> str:
    return "preserve" if original_source_available(example["source"], example["original_predicted_edit"]) else "cancel"


def explanation_leakage_simulator(example: Dict[str, Any]) -> str:
    terms = contains_edit_terms(example)
    if not (terms["source"] or terms["target"] or terms["operation"]):
        return "competing_edit"
    if example["variant_family"] == "error_irrelevant":
        return "preserve"
    return source_edit_availability(example)


def explanation_type_heuristic(example: Dict[str, Any]) -> str:
    etype = example["explanation_type"]
    if etype in {"generic", "swapped_across_sentence", "wrong_rule", "wrong_target"}:
        return "competing_edit"
    if example["variant_family"] == "error_irrelevant":
        return "preserve"
    return source_edit_availability(example)


def train_type_prior(train_rows: List[Dict[str, Any]]) -> Dict[Tuple[str, str], str]:
    counts: Dict[Tuple[str, str], Counter[str]] = defaultdict(Counter)
    for row in train_rows:
        counts[(row["explanation_type"], row["variant_family"])][row["actual_behavior_label"]] += 1
    return {key: counter.most_common(1)[0][0] for key, counter in counts.items()}


def build_examples(cf_rows: List[Dict[str, Any]], explanations_by_edit: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    examples = []
    for cf in cf_rows:
        for explanation in explanations_by_edit.get(cf["origin_edit_id"], []):
            examples.append(
                {
                    **cf,
                    "sim_instance_id": f"{cf['counterfactual_id']}::{explanation['explanation_type']}",
                    "explanation_type": explanation["explanation_type"],
                    "explanation": explanation["explanation"],
                    "explanation_label": explanation["label"],
                    "explanation_is_negative": explanation["is_negative"],
                }
            )
    return examples


def evaluate(args: argparse.Namespace) -> None:
    cf_rows = read_jsonl(args.counterfactuals)
    explanations = load_explanations(args.benchmark_dir / "explanation_instances.jsonl")
    examples = build_examples(cf_rows, explanations)
    train_rows = [row for row in examples if row["split"] == "train"]
    type_prior = train_type_prior(train_rows)

    def trained_type_prior(example: Dict[str, Any]) -> str:
        return type_prior.get((example["explanation_type"], example["variant_family"]), variant_family_prior(example))

    methods: Dict[str, Callable[[Dict[str, Any]], str]] = {
        "random": lambda ex: stable_label(ex["sim_instance_id"]),
        "variant_family_prior": variant_family_prior,
        "source_edit_availability": source_edit_availability,
        "explanation_leakage_simulator": explanation_leakage_simulator,
        "explanation_type_heuristic": explanation_type_heuristic,
        "trained_explanation_type_prior": trained_type_prior,
    }

    detailed = []
    method_pairs: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    method_pairs_by_type: Dict[str, Dict[str, List[Tuple[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for example in examples:
        for name, fn in methods.items():
            pred = fn(example)
            gold = example["actual_behavior_label"]
            method_pairs[name].append((pred, gold))
            method_pairs_by_type[name][example["explanation_type"]].append((pred, gold))
            detailed.append(
                {
                    "sim_instance_id": example["sim_instance_id"],
                    "counterfactual_id": example["counterfactual_id"],
                    "origin_edit_id": example["origin_edit_id"],
                    "split": example["split"],
                    "dataset": example["origin_dataset"],
                    "model_key": example["model_key"],
                    "variant_family": example["variant_family"],
                    "actual_behavior_label": gold,
                    "explanation_type": example["explanation_type"],
                    "explanation_label": example["explanation_label"],
                    "method": name,
                    "prediction": pred,
                    "correct": pred == gold,
                    "edit_term_hits": contains_edit_terms(example),
                }
            )

    summary = {
        "created_at": utc_now(),
        "counterfactual_count": len(cf_rows),
        "simulatability_instance_count": len(examples),
        "explanation_type_counts": dict(Counter(row["explanation_type"] for row in examples)),
        "method_metrics": {name: multiclass_metrics(pairs) for name, pairs in method_pairs.items()},
        "method_metrics_by_explanation_type": {
            name: {etype: multiclass_metrics(pairs) for etype, pairs in by_type.items()}
            for name, by_type in method_pairs_by_type.items()
        },
        "important_note": "These are explanation-conditioned automatic simulatability diagnostics. They are not human faithfulness judgments.",
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.out_dir / "counterfactual_simulator_metrics.json", summary)
    write_jsonl(args.out_dir / "counterfactual_simulator_predictions.jsonl", detailed)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate explanation-conditioned counterfactual simulators.")
    parser.add_argument("--counterfactuals", type=Path, default=DEFAULT_COUNTERFACTUALS)
    parser.add_argument("--benchmark-dir", type=Path, default=DEFAULT_BENCHMARK_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


if __name__ == "__main__":
    evaluate(parse_args())
