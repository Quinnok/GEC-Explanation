from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BENCHMARK = ROOT / "data" / "faithfulness_benchmark"
DEFAULT_ROUND09 = ROOT / "results" / "round09"
DEFAULT_OUT_DIR = ROOT / "annotation" / "round10"
DEFAULT_RESULTS = ROOT / "results" / "round10"


FAITHFULNESS_TYPES = [
    "explicit_template",
    "masked_target_template",
    "rule_only",
    "rule_grounded_automatic",
    "gee_style_automatic",
    "generic",
    "wrong_rule",
    "wrong_target",
    "wrong_direction",
    "swapped_across_sentence",
]

COUNTERFACTUAL_TYPES = [
    "explicit_template",
    "rule_grounded_automatic",
    "generic",
    "wrong_rule",
    "swapped_across_sentence",
]


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


def stable_sort_key(row: Dict[str, Any]) -> str:
    return hashlib.sha1(json.dumps(row, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def balanced_take(rows: List[Dict[str, Any]], key_fields: List[str], limit: int) -> List[Dict[str, Any]]:
    buckets: Dict[tuple[Any, ...], List[Dict[str, Any]]] = defaultdict(list)
    for row in sorted(rows, key=stable_sort_key):
        buckets[tuple(row.get(key, "NA") for key in key_fields)].append(row)
    selected: List[Dict[str, Any]] = []
    seen_ids: set[str] = set()
    per_bucket = max(1, limit // max(1, len(buckets)))
    for key in sorted(buckets):
        for row in buckets[key][:per_bucket]:
            selected.append(row)
            seen_ids.add(row["item_id"])
            if len(selected) >= limit:
                return selected
    for row in sorted(rows, key=stable_sort_key):
        if row["item_id"] not in seen_ids:
            selected.append(row)
            seen_ids.add(row["item_id"])
        if len(selected) >= limit:
            break
    return selected


def edit_string(edit: Dict[str, Any]) -> str:
    if edit["operation"] == "replace":
        return f'replace "{edit.get("source_text", "")}" with "{edit.get("target_text", "")}"'
    if edit["operation"] == "insert":
        return f'insert "{edit.get("target_text", "")}"'
    if edit["operation"] == "delete":
        return f'delete "{edit.get("source_text", "")}"'
    return json.dumps(edit, ensure_ascii=False)


def build_faithfulness_items(edit_rows: List[Dict[str, Any]], explanation_rows: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    edits = {row["edit_id"]: row for row in edit_rows}
    public = []
    metadata = []
    for exp in explanation_rows:
        if exp["explanation_type"] not in FAITHFULNESS_TYPES:
            continue
        edit = edits.get(exp["edit_id"])
        if not edit:
            continue
        item_id = f"r10-faith-{len(public):05d}"
        public_row = {
            "item_id": item_id,
            "task_type": "edit_explanation_faithfulness",
            "dataset": edit.get("dataset"),
            "model_key": edit["model_key"],
            "model_family": edit.get("model_family"),
            "source": edit["source"],
            "model_prediction": edit["prediction"],
            "model_edit": edit_string(edit["predicted_edit"]),
            "error_type": edit["error_type"],
            "model_behavior": edit["behavior"],
            "explanation_type": exp["explanation_type"],
            "explanation": exp["explanation"],
            "question": "Does the explanation faithfully describe why the model made this specific edit?",
            "faithfulness_label": "",
            "rule_correctness_label": "",
            "evidence_label": "",
            "notes": "",
        }
        public.append(public_row)
        metadata.append(
            {
                **public_row,
                "edit_id": exp["edit_id"],
                "instance_id": exp["instance_id"],
                "automatic_label": exp["label"],
                "automatic_is_negative": exp["is_negative"],
                "automatic_negative_type": exp["negative_type"],
                "is_human_gold": False,
            }
        )
    return public, metadata


def build_counterfactual_items(cf_rows: List[Dict[str, Any]], sim_rows: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    sim_by_cf: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in sim_rows:
        if row["method"] == "explanation_leakage_simulator" and row["explanation_type"] in COUNTERFACTUAL_TYPES:
            sim_by_cf[row["counterfactual_id"]].append(row)
    public = []
    metadata = []
    for cf in cf_rows:
        for sim in sim_by_cf.get(cf["counterfactual_id"], []):
            item_id = f"r10-cf-{len(public):05d}"
            public_row = {
                "item_id": item_id,
                "task_type": "counterfactual_edit_simulatability",
                "dataset": cf["origin_dataset"],
                "model_key": cf["model_key"],
                "model_family": cf["model_family"],
                "original_source": cf["original_source"],
                "counterfactual_source": cf["source"],
                "original_model_prediction": cf["original_prediction"],
                "counterfactual_model_prediction": cf["prediction"],
                "model_edit": edit_string(cf["original_predicted_edit"]),
                "variant_family": cf["variant_family"],
                "variant_strategy": cf["variant_strategy"],
                "explanation_type": sim["explanation_type"],
                "question": "Given the explanation and counterfactual source, what should happen to the original edit?",
                "simulated_behavior_label": "",
                "counterfactual_validity_label": "",
                "notes": "",
            }
            public.append(public_row)
            metadata.append(
                {
                    **public_row,
                    "counterfactual_id": cf["counterfactual_id"],
                    "origin_edit_id": cf["origin_edit_id"],
                    "actual_model_behavior_label": cf["actual_behavior_label"],
                    "automatic_simulator_prediction": sim["prediction"],
                    "automatic_simulator_correct": sim["correct"],
                    "is_human_gold": False,
                }
            )
    return public, metadata


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build(args: argparse.Namespace) -> None:
    edit_rows = read_jsonl(args.benchmark_dir / "edit_records.jsonl")
    explanation_rows = read_jsonl(args.benchmark_dir / "explanation_instances.jsonl")
    cf_rows = read_jsonl(args.round09_dir / "counterfactual_labels.jsonl")
    sim_rows = read_jsonl(args.round09_dir / "counterfactual_simulator_predictions.jsonl")

    faith_public, faith_meta = build_faithfulness_items(edit_rows, explanation_rows)
    cf_public, cf_meta = build_counterfactual_items(cf_rows, sim_rows)
    faith_selected = balanced_take(faith_public, ["dataset", "model_key", "model_behavior", "explanation_type"], args.faithfulness_items)
    faith_ids = {row["item_id"] for row in faith_selected}
    faith_meta_selected = [row for row in faith_meta if row["item_id"] in faith_ids]
    cf_selected = balanced_take(cf_public, ["model_key", "variant_family", "explanation_type"], args.counterfactual_items)
    cf_ids = {row["item_id"] for row in cf_selected}
    cf_meta_selected = [row for row in cf_meta if row["item_id"] in cf_ids]
    public_rows = faith_selected + cf_selected
    metadata_rows = faith_meta_selected + cf_meta_selected

    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.results_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "annotation_items.jsonl", public_rows)
    write_jsonl(args.out_dir / "annotation_metadata_with_auto_labels.jsonl", metadata_rows)
    write_csv(args.out_dir / "annotation_form.csv", public_rows)
    adjudication_rows = [
        {
            "item_id": row["item_id"],
            "annotator_a_label": "",
            "annotator_b_label": "",
            "adjudicated_label": "",
            "adjudicator_notes": "",
        }
        for row in public_rows
    ]
    write_csv(args.out_dir / "adjudication_template.csv", adjudication_rows)
    stats = {
        "created_at": utc_now(),
        "public_item_count": len(public_rows),
        "faithfulness_item_count": len(faith_selected),
        "counterfactual_item_count": len(cf_selected),
        "task_counts": dict(Counter(row["task_type"] for row in public_rows)),
        "dataset_counts": dict(Counter(row.get("dataset") for row in public_rows)),
        "model_counts": dict(Counter(row.get("model_key") for row in public_rows)),
        "explanation_type_counts": dict(Counter(row.get("explanation_type") for row in public_rows)),
        "human_gold_count": 0,
        "blocked_requirement": "Double-human annotation cannot be completed by automation; user or external annotators must fill annotation_form.csv.",
    }
    write_json(args.results_dir / "annotation_package_stats.json", stats)

    guidelines = """# Round 10 Annotation Guidelines

## Task A: Edit Explanation Faithfulness

Judge whether the explanation faithfully describes why the model made the shown edit. The question is about the model edit, not whether the edit is grammatically ideal.

Labels:

- `faithful`: the explanation identifies the correct edit target/direction and gives a rule or evidence compatible with the model edit.
- `partially_faithful`: the explanation is related but misses an important span, target, direction, rule, or evidence detail.
- `unfaithful`: the explanation points to the wrong edit, wrong rule, wrong evidence, wrong direction, or is generic.
- `uncertain`: the case is ambiguous, impossible to judge, or depends on an acceptable alternative correction.

## Task B: Counterfactual Edit Simulatability

Given the original edit, explanation, and counterfactual source, predict what should happen to the original edit if the explanation is faithful.

Labels:

- `preserve`: the same edit should still be made.
- `cancel`: the original edit should disappear.
- `change_target`: the edit should remain at the same target but change correction text.
- `change_span`: the correction should move to a different span.
- `change_operation`: the operation should change.
- `competing_edit`: other edits dominate and the original edit behavior cannot be cleanly isolated.
- `uncertain`: the counterfactual is invalid or ambiguous.

## Protocol

Use two independent annotators per item. Do not show annotators `annotation_metadata_with_auto_labels.jsonl`. Resolve disagreements in `adjudication_template.csv`. These files contain no human gold labels until real annotators fill them.
"""
    (args.out_dir / "guidelines.md").write_text(guidelines, encoding="utf-8")
    readme = f"""# Round 10 Annotation Package

Generated: `{stats['created_at']}`

- Public annotation items: `{args.out_dir / 'annotation_items.jsonl'}`
- Spreadsheet form: `{args.out_dir / 'annotation_form.csv'}`
- Hidden automatic metadata: `{args.out_dir / 'annotation_metadata_with_auto_labels.jsonl'}`
- Adjudication template: `{args.out_dir / 'adjudication_template.csv'}`
- Package stats: `{args.results_dir / 'annotation_package_stats.json'}`

No human gold labels have been collected. The automatic labels are included only for later audit after independent annotation.
"""
    (args.out_dir / "README.md").write_text(readme, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Round 10 human annotation package.")
    parser.add_argument("--benchmark-dir", type=Path, default=DEFAULT_BENCHMARK)
    parser.add_argument("--round09-dir", type=Path, default=DEFAULT_ROUND09)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--faithfulness-items", type=int, default=160)
    parser.add_argument("--counterfactual-items", type=int, default=80)
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
