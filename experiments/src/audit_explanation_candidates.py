from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "data" / "processed" / "model_edit_explanation_candidates.jsonl"
DEFAULT_OUT_DIR = ROOT / "results" / "model_explanations"


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def candidate_flags(row: Dict[str, Any]) -> List[str]:
    candidate = row["open_source_explanation_candidate"].strip()
    low = candidate.lower()
    flags: List[str] = []
    if not candidate:
        flags.append("empty")
    if candidate.lower() == row["prediction"].strip().lower():
        flags.append("prediction_copy")
    if low.startswith("the following is a list"):
        flags.append("generic_list_like")
    if candidate in {
        "The verb should agree with the singular subject.",
        "The verb should agree with the singular subject .",
    }:
        flags.append("few_shot_copy_like")
    if len(candidate.split()) > 35:
        flags.append("too_long")
    return flags or ["no_automatic_flag"]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def render_report(rows: Iterable[Dict[str, Any]], check_size: int) -> tuple[str, Counter[str]]:
    flags = Counter()
    lines = [
        "# Open-Source Explanation Candidate Check",
        "",
        "These are FLAN-T5-base candidates generated from source, model prediction, and the model edit span. They are not human gold and are not template explanations.",
        "",
    ]
    for index, row in enumerate(list(rows)[:check_size], 1):
        local_flags = candidate_flags(row)
        flags.update(local_flags)
        lines.extend(
            [
                f"## {index}. {row['record_id']}",
                "",
                f"- Model: `{row['model_key']}`",
                f"- Behavior: `{row['behavior']}`",
                f"- Predicted edit: `{json.dumps(row['predicted_edit'], ensure_ascii=False)}`",
                f"- Candidate: `{row['open_source_explanation_candidate']}`",
                f"- Flags: `{', '.join(local_flags)}`",
                "",
            ]
        )
    return "\n".join(lines) + "\n", flags


def audit(args: argparse.Namespace) -> None:
    rows = read_jsonl(args.input)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    report, flags = render_report(rows, args.check_size)
    (args.out_dir / "explanation_candidate_check_30.md").write_text(report)
    summary = {
        "candidate_count": len(rows),
        "first_30_flag_counts": dict(flags),
        "model_counts": dict(Counter(row["model_key"] for row in rows)),
        "behavior_counts": dict(Counter(row["behavior"] for row in rows)),
        "note": "Automatic flags are rough diagnostics only. FLAN candidates remain open-source model candidates, not human gold.",
    }
    write_json(args.out_dir / "explanation_candidate_quality_flags.json", summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit open-source model explanation candidates.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--check-size", type=int, default=30)
    return parser.parse_args()


if __name__ == "__main__":
    audit(parse_args())
