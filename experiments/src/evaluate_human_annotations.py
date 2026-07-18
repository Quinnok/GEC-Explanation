from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FORM = ROOT / "annotation" / "round10" / "annotation_form.csv"
DEFAULT_OUTPUT = ROOT / "results" / "round10" / "human_annotation_status.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def label_for(row: Dict[str, str]) -> str:
    if row.get("task_type") == "edit_explanation_faithfulness":
        return row.get("faithfulness_label", "").strip()
    if row.get("task_type") == "counterfactual_edit_simulatability":
        return row.get("simulated_behavior_label", "").strip()
    return ""


def cohen_kappa(pairs: List[Tuple[str, str]]) -> float:
    if not pairs:
        return 0.0
    observed = sum(1 for a, b in pairs if a == b) / len(pairs)
    labels = sorted({label for pair in pairs for label in pair})
    a_counts = Counter(a for a, _ in pairs)
    b_counts = Counter(b for _, b in pairs)
    expected = sum((a_counts[label] / len(pairs)) * (b_counts[label] / len(pairs)) for label in labels)
    if expected == 1.0:
        return 1.0
    return (observed - expected) / (1 - expected)


def evaluate(args: argparse.Namespace) -> None:
    if args.annotator_a and args.annotator_b:
        rows_a = {row["item_id"]: row for row in read_csv(args.annotator_a)}
        rows_b = {row["item_id"]: row for row in read_csv(args.annotator_b)}
        pairs = []
        task_counts = Counter()
        for item_id in sorted(set(rows_a) & set(rows_b)):
            label_a = label_for(rows_a[item_id])
            label_b = label_for(rows_b[item_id])
            if label_a and label_b:
                pairs.append((label_a, label_b))
                task_counts[rows_a[item_id].get("task_type", "unknown")] += 1
        status = "complete" if pairs else "no_completed_overlap"
    else:
        rows = read_csv(args.form)
        filled = [row for row in rows if label_for(row)]
        pairs = []
        task_counts = Counter(row.get("task_type", "unknown") for row in filled)
        status = "blocked_no_human_annotation"

    result = {
        "created_at": utc_now(),
        "status": status,
        "completed_label_count": len(pairs) if pairs else sum(task_counts.values()),
        "paired_overlap_count": len(pairs),
        "task_counts": dict(task_counts),
        "cohen_kappa": cohen_kappa(pairs) if pairs else None,
        "blocked_requirement": None
        if pairs
        else "Double-human annotation files are required before human faithfulness claims can be made.",
    }
    write_json(args.output, result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate completed Round 10 human annotation files.")
    parser.add_argument("--form", type=Path, default=DEFAULT_FORM)
    parser.add_argument("--annotator-a", type=Path)
    parser.add_argument("--annotator-b", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


if __name__ == "__main__":
    evaluate(parse_args())
