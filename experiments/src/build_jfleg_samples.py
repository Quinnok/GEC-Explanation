from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JFLEG_ROOT = ROOT / "data" / "downloads" / "jfleg"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "jfleg_v1_samples.jsonl"
DEFAULT_STATS = ROOT / "data" / "processed" / "jfleg_v1_sample_stats.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_lines(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_split(root: Path, split: str) -> List[Dict[str, Any]]:
    split_dir = root / split
    sources = read_lines(split_dir / f"{split}.src")
    refs = [read_lines(split_dir / f"{split}.ref{i}") for i in range(4)]
    rows = []
    for idx, source in enumerate(sources):
        references = [ref[idx] for ref in refs]
        rows.append(
            {
                "sample_id": f"jfleg-{split}-{idx:04d}",
                "dataset": "JFLEG",
                "dataset_version": "git:ee06ff806a208aba815ac45313f4e750a48330a5",
                "dataset_license": "CC-BY-NC-SA-4.0",
                "split": split,
                "source_text": source,
                "target_text": references[0],
                "all_references": references,
                "reference_policy": "ref0 used as primary reference for ERRANT pilot; all four human references retained.",
            }
        )
    return rows


def build(args: argparse.Namespace) -> None:
    if not args.jfleg_root.exists():
        raise SystemExit(
            f"JFLEG root not found: {args.jfleg_root}. Clone https://github.com/keisks/jfleg first."
        )
    rows: List[Dict[str, Any]] = []
    for split in args.splits:
        rows.extend(build_split(args.jfleg_root, split))
    rows = rows[: args.sample_size] if args.sample_size else rows
    write_jsonl(args.output, rows)
    stats = {
        "created_at": utc_now(),
        "source": "https://github.com/keisks/jfleg",
        "commit": "ee06ff806a208aba815ac45313f4e750a48330a5",
        "license": "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International",
        "output": str(args.output),
        "sample_count": len(rows),
        "split_counts": {split: sum(1 for row in rows if row["split"] == split) for split in args.splits},
        "reference_policy": "The benchmark pilot uses ref0 as the primary reference for single-reference ERRANT extraction and retains all four JFLEG references in each row.",
    }
    write_json(args.stats, stats)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build project-format JSONL samples from JFLEG.")
    parser.add_argument("--jfleg-root", type=Path, default=DEFAULT_JFLEG_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stats", type=Path, default=DEFAULT_STATS)
    parser.add_argument("--splits", nargs="+", default=["dev", "test"])
    parser.add_argument("--sample-size", type=int, default=160)
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
