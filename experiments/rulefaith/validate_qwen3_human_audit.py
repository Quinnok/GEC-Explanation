from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.rulefaith import build_qwen3_manual_audit as audit


DEFAULT_AUDIT_DIR = ROOT / "annotation" / "rulefaith_qwen3_audit_canonicalized"
DEFAULT_FORM = DEFAULT_AUDIT_DIR / "manual_audit_form.csv"
DEFAULT_KEY = DEFAULT_AUDIT_DIR / "manual_audit_key.csv"
DEFAULT_MERGED = DEFAULT_AUDIT_DIR / "manual_audit_merged_with_key.csv"
DEFAULT_SUMMARY = ROOT / "results" / "rulefaith" / "qwen3_human_audit_validation_summary.json"
DEFAULT_REPORT = ROOT / "results" / "rulefaith" / "qwen3_human_audit_validation_report.md"

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

HUMAN_FIELDS = ISSUE_FIELDS + ["human_notes", "human_decision"]
ISSUE_LABELS = {"yes", "no", "uncertain"}
DECISION_LABELS = {"accept", "refine", "reject", "abstain"}
KEY_FIELDS = ["bucket", "audit_priority", "candidate_type", "behavior", "error_type", "risk_count", "risk_reasons"]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if not rows:
        raise ValueError(f"CSV has no rows: {path}")
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj: Any, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def normalize(value: str) -> str:
    return str(value or "").strip().lower()


def validate_rows(form_rows: list[dict[str, str]], key_rows: list[dict[str, str]], allow_incomplete: bool) -> tuple[dict[str, Any], list[dict[str, str]]]:
    form_ids = [row.get("candidate_id", "") for row in form_rows]
    key_ids = [row.get("candidate_id", "") for row in key_rows]
    if len(form_ids) != len(set(form_ids)):
        raise ValueError("Duplicate candidate_id in completed audit form")
    if set(form_ids) != set(key_ids):
        missing_from_form = sorted(set(key_ids) - set(form_ids))
        extra_in_form = sorted(set(form_ids) - set(key_ids))
        raise ValueError(f"Audit/key candidate_id mismatch: missing={missing_from_form[:5]}, extra={extra_in_form[:5]}")
    missing_columns = [field for field in ["candidate_id", *HUMAN_FIELDS] if field not in form_rows[0]]
    if missing_columns:
        raise ValueError(f"Completed audit form is missing columns: {missing_columns}")

    invalid_cells: list[dict[str, str]] = []
    incomplete_rows: list[str] = []
    uncertain_without_notes: list[str] = []
    decision_counts: Counter[str] = Counter()
    issue_counts: dict[str, Counter[str]] = {field: Counter() for field in ISSUE_FIELDS}

    for row in form_rows:
        cid = row["candidate_id"]
        row_incomplete = False
        for field in ISSUE_FIELDS:
            value = normalize(row.get(field, ""))
            if not value:
                row_incomplete = True
                continue
            if value not in ISSUE_LABELS:
                invalid_cells.append({"candidate_id": cid, "field": field, "value": row.get(field, "")})
                continue
            issue_counts[field][value] += 1
        decision = normalize(row.get("human_decision", ""))
        if not decision:
            row_incomplete = True
        elif decision not in DECISION_LABELS:
            invalid_cells.append({"candidate_id": cid, "field": "human_decision", "value": row.get("human_decision", "")})
        else:
            decision_counts[decision] += 1
        if any(normalize(row.get(field, "")) == "uncertain" for field in ISSUE_FIELDS) and not row.get("human_notes", "").strip():
            uncertain_without_notes.append(cid)
        if row_incomplete:
            incomplete_rows.append(cid)

    if invalid_cells:
        raise ValueError(f"Invalid human labels found: {invalid_cells[:10]}")
    if incomplete_rows and not allow_incomplete:
        raise ValueError(f"Audit form is incomplete: {len(incomplete_rows)} rows have blank required labels")
    if uncertain_without_notes and not allow_incomplete:
        raise ValueError(f"Uncertain labels without notes: {uncertain_without_notes[:10]}")

    key_by_id = {row["candidate_id"]: row for row in key_rows}
    merged: list[dict[str, str]] = []
    for row in form_rows:
        merged_row = dict(row)
        for field in KEY_FIELDS:
            merged_row[field] = key_by_id[row["candidate_id"]].get(field, "")
        merged.append(merged_row)

    completed_count = len(form_rows) - len(set(incomplete_rows))
    summary = {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "row_count": len(form_rows),
        "completed_row_count": completed_count,
        "incomplete_row_count": len(set(incomplete_rows)),
        "is_complete": len(set(incomplete_rows)) == 0,
        "uncertain_without_notes_count": len(uncertain_without_notes),
        "decision_counts": dict(sorted(decision_counts.items())),
        "issue_counts": {field: dict(sorted(counter.items())) for field, counter in issue_counts.items()},
        "incomplete_candidate_ids": sorted(set(incomplete_rows)),
        "uncertain_without_notes_candidate_ids": uncertain_without_notes,
        "allow_incomplete": allow_incomplete,
        "decision": "ready_to_merge_completed_audit" if not incomplete_rows else "waiting_for_human_completion",
    }
    return summary, merged


def markdown(summary: dict[str, Any], merged_path: Path | None) -> str:
    lines = [
        "# Qwen3 Human Audit Validation Report",
        "",
        "## Summary",
        "",
    ]
    for key in [
        "row_count",
        "completed_row_count",
        "incomplete_row_count",
        "is_complete",
        "uncertain_without_notes_count",
        "decision",
    ]:
        lines.append(f"- `{key}`: `{summary[key]}`")
    lines.extend(["", "## Human Decisions", ""])
    for label, count in summary["decision_counts"].items():
        lines.append(f"- `{label}`: {count}")
    lines.extend(["", "## Issue Counts", ""])
    for field, counts in summary["issue_counts"].items():
        lines.append(f"- `{field}`: `{counts}`")
    if merged_path:
        lines.extend(["", "## Merged Output", "", f"- `{merged_path}`"])
    if summary["incomplete_candidate_ids"]:
        lines.extend(["", "## Incomplete Candidate IDs", ""])
        for cid in summary["incomplete_candidate_ids"][:40]:
            lines.append(f"- `{cid}`")
        if len(summary["incomplete_candidate_ids"]) > 40:
            lines.append(f"- ... {len(summary['incomplete_candidate_ids']) - 40} more")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and merge a completed Qwen3 canonicalized human audit form.")
    parser.add_argument("--form", type=Path, default=DEFAULT_FORM)
    parser.add_argument("--key", type=Path, default=DEFAULT_KEY)
    parser.add_argument("--merged-output", type=Path, default=DEFAULT_MERGED)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--allow-incomplete", action="store_true")
    parser.add_argument("--skip-merged-output", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    form_rows = read_csv(resolve(args.form))
    key_rows = read_csv(resolve(args.key))
    summary, merged = validate_rows(form_rows, key_rows, args.allow_incomplete)
    merged_path: Path | None = None
    if summary["is_complete"] and not args.skip_merged_output:
        fieldnames = list(form_rows[0].keys()) + [field for field in KEY_FIELDS if field not in form_rows[0]]
        merged_path = resolve(args.merged_output)
        write_csv(merged_path, merged, fieldnames, args.overwrite)
        summary["merged_output"] = str(merged_path)
    write_json(resolve(args.summary_output), summary, args.overwrite)
    write_text(resolve(args.report_output), markdown(summary, merged_path), args.overwrite)
    print(json.dumps({"decision": summary["decision"], "is_complete": summary["is_complete"], "row_count": summary["row_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
