from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.append(str(Path(__file__).resolve().parent))

from baselines import explicit_edit_baseline
from evaluate_reconstruction import evaluate_records, write_json


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def run(input_path: Path, predictions_path: Path, summary_path: Path, raw_results_path: Path) -> None:
    records = load_jsonl(input_path)
    predicted_records = []
    for record in records:
        pred = explicit_edit_baseline(
            source=record["source"],
            explanation=record["explanation"],
            error_type=record["edit"].get("error_type", "UNK"),
        )
        reconstructed = {"reconstructable": False} if pred is None else {"reconstructable": True, **pred.to_dict()}
        predicted_records.append({**record, "reconstruction": reconstructed})
    predictions_path.parent.mkdir(parents=True, exist_ok=True)
    predictions_path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in predicted_records) + "\n")
    summary = evaluate_records(predicted_records)
    summary["note"] = "Toy sanity-check only. Not real GEC evidence."
    write_json(raw_results_path, {"records": predicted_records, "summary": summary})
    write_json(summary_path, summary)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw/toy_pilot.jsonl")
    parser.add_argument("--predictions", default="results/predictions/toy_pilot_predictions.jsonl")
    parser.add_argument("--summary", default="results/summary.json")
    parser.add_argument("--raw-results", default="results/raw_results.json")
    args = parser.parse_args()
    run(Path(args.input), Path(args.predictions), Path(args.summary), Path(args.raw_results))
