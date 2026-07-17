from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from edit_schema import Edit, compare_edits


def average_metrics(rows: List[Dict[str, float]]) -> Dict[str, float]:
    if not rows:
        return {}
    keys = sorted(rows[0].keys())
    return {key: sum(row[key] for row in rows) / len(rows) for key in keys}


def evaluate_records(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    metric_rows: List[Dict[str, float]] = []
    detailed = []
    for record in records:
        gold = Edit.from_dict(record["edit"])
        reconstruction = record.get("reconstruction")
        if not reconstruction or not reconstruction.get("reconstructable", False):
            metrics = {
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
        else:
            pred = Edit.from_dict(reconstruction)
            metrics = compare_edits(pred, gold)
        metric_rows.append(metrics)
        detailed.append({"sample_id": record.get("sample_id"), "metrics": metrics})
    return {
        "n": len(records),
        "macro_average": average_metrics(metric_rows),
        "details": detailed,
    }


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = evaluate_records(load_jsonl(Path(args.input)))
    write_json(Path(args.output), result)

