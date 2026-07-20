from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.rulefaith import build_qwen3_manual_audit as audit


DEFAULT_MERGED = ROOT / "annotation" / "rulefaith_qwen3_audit_canonicalized" / "manual_audit_codex_prelabeled_merged_with_key.csv"
DEFAULT_JSON = ROOT / "results" / "rulefaith" / "qwen3_codex_prelabeled_breakdown.json"
DEFAULT_MD = ROOT / "results" / "rulefaith" / "qwen3_codex_prelabeled_breakdown.md"

ISSUE_FIELDS = [
    "human_alignment_error",
    "human_validity_error",
    "human_wrong_rule",
    "human_inapplicable_rule",
    "human_missing_evidence",
    "human_wrong_evidence",
    "human_generic_explanation",
    "human_edit_copy",
    "human_semantic_distortion",
    "human_unsupported_confidence",
]

GROUP_FIELDS = [
    "bucket",
    "audit_priority",
    "candidate_type",
    "dataset",
    "model_key",
    "behavior",
    "operation",
    "error_type",
]


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"CSV has no rows: {path}")
    return rows


def write_json(path: Path, payload: dict[str, Any], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def counts_by(rows: list[dict[str, str]], group_field: str) -> dict[str, dict[str, int]]:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        grouped[row.get(group_field, "") or "UNKNOWN"][row.get("human_decision", "") or "UNKNOWN"] += 1
    return {key: dict(sorted(counter.items())) for key, counter in sorted(grouped.items())}


def summarize(rows: list[dict[str, str]], input_path: Path) -> dict[str, Any]:
    decision_counts = Counter(row.get("human_decision", "") or "UNKNOWN" for row in rows)
    issue_yes_counts = {
        field: sum(1 for row in rows if row.get(field, "").strip().lower() == "yes")
        for field in ISSUE_FIELDS
    }
    return {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "input": str(input_path),
        "label_source": "codex_ai_assisted_prelabelling_not_human_gold",
        "row_count": len(rows),
        "decision_counts": dict(sorted(decision_counts.items())),
        "issue_yes_counts": dict(sorted(issue_yes_counts.items())),
        "decision_by_group": {field: counts_by(rows, field) for field in GROUP_FIELDS},
    }


def markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 Codex Prelabel Breakdown",
        "",
        "These results are Codex-assisted prelabels for internal triage. They are not human labels and must not be used as human-gold evidence.",
        "",
        "## Overall Decisions",
        "",
    ]
    for key, value in summary["decision_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Issue Counts", ""])
    for key, value in summary["issue_yes_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Decision Breakdown", ""])
    for field, groups in summary["decision_by_group"].items():
        lines.append(f"### {field}")
        lines.append("")
        lines.append("| Group | accept | refine | reject | abstain |")
        lines.append("|---|---:|---:|---:|---:|")
        for group, counts in groups.items():
            lines.append(
                f"| {group} | {counts.get('accept', 0)} | {counts.get('refine', 0)} | {counts.get('reject', 0)} | {counts.get('abstain', 0)} |"
            )
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize Codex-assisted Qwen3 audit prelabels.")
    parser.add_argument("--merged", type=Path, default=DEFAULT_MERGED)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--md-output", type=Path, default=DEFAULT_MD)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    merged = resolve(args.merged)
    rows = read_csv(merged)
    summary = summarize(rows, merged)
    write_json(resolve(args.json_output), summary, args.overwrite)
    write_text(resolve(args.md_output), markdown(summary), args.overwrite)
    print(json.dumps({"decision_counts": summary["decision_counts"], "row_count": summary["row_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
