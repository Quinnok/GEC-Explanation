from __future__ import annotations

import argparse
import glob
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge RuleFaith teacher candidate shard JSONL files.")
    parser.add_argument("--glob", required=True, help="Glob pattern for shard JSONL files.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stats", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pattern = args.glob if Path(args.glob).is_absolute() else str(ROOT / args.glob)
    shard_paths = [Path(path) for path in sorted(glob.glob(pattern))]
    rows: List[Dict[str, Any]] = []
    seen: set[str] = set()
    duplicate_ids: List[str] = []
    for shard_path in shard_paths:
        for row in read_jsonl(shard_path):
            candidate_id = row.get("candidate_id")
            if candidate_id in seen:
                duplicate_ids.append(candidate_id)
                continue
            seen.add(candidate_id)
            rows.append(row)
    rows.sort(key=lambda row: (row.get("rulefaith_pool_id", ""), row.get("provider", ""), row.get("candidate_type", "")))
    output = resolve(args.output)
    stats_path = resolve(args.stats)
    write_jsonl(output, rows)
    write_json(
        stats_path,
        {
            "shard_files": [str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path) for path in shard_paths],
            "output": str(output.relative_to(ROOT)) if output.is_relative_to(ROOT) else str(output),
            "candidate_count": len(rows),
            "duplicate_candidate_count": len(duplicate_ids),
            "duplicate_candidate_ids": duplicate_ids[:100],
            "provider_counts": dict(Counter(row.get("provider", "") for row in rows)),
            "candidate_type_counts": dict(Counter(row.get("candidate_type", "") for row in rows)),
            "parse_status_counts": dict(Counter(row.get("parse_status", "") for row in rows)),
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
