from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def merge(args: argparse.Namespace) -> None:
    prediction_rows: List[Dict[str, Any]] = []
    for path in sorted(args.prediction_dir.glob(args.prediction_glob)):
        prediction_rows.extend(read_jsonl(path))
    write_jsonl(args.output, prediction_rows)

    merged_models: Dict[str, Any] = {}
    chunk_metadata = []
    runtime_totals: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for path in sorted(args.prediction_dir.glob(args.metadata_glob)):
        payload = read_json(path)
        chunk_metadata.append({"path": str(path), "metadata": payload})
        for model_key, item in payload.get("models", {}).items():
            merged_models.setdefault(model_key, item)
            runtime = item.get("runtime", {})
            runtime_totals[model_key]["sample_count"] += runtime.get("sample_count", 0)
            runtime_totals[model_key]["changed_count"] += runtime.get("changed_count", 0)
            runtime_totals[model_key]["reference_copy_count"] += runtime.get("reference_copy_count", 0)
            runtime_totals[model_key]["duration_seconds"] += runtime.get("duration_seconds", 0)
    for model_key, totals in runtime_totals.items():
        runtime = merged_models[model_key].setdefault("runtime", {})
        runtime.update({key: round(value, 3) for key, value in totals.items()})
        runtime["seconds_per_sample"] = (
            round(totals["duration_seconds"] / totals["sample_count"], 6) if totals["sample_count"] else 0.0
        )
        runtime["parallel_chunk_note"] = "Summed over independently executed chunks; wall-clock time depends on JOBS."
    write_json(
        args.metadata,
        {
            "created_at": utc_now(),
            "output": str(args.output),
            "row_count": len(prediction_rows),
            "models": merged_models,
            "chunk_count": len(chunk_metadata),
            "chunk_metadata_files": [item["path"] for item in chunk_metadata],
        },
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge JSONL prediction chunks and their metadata.")
    parser.add_argument("--prediction-dir", type=Path, required=True)
    parser.add_argument("--prediction-glob", default="pred_*.jsonl")
    parser.add_argument("--metadata-glob", default="meta_*.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    merge(parse_args())
