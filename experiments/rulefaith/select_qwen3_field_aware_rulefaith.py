from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.rulefaith import build_qwen3_manual_audit as audit
from experiments.rulefaith import repair_qwen3_structured_evidence as repair


DEFAULT_CANDIDATES = ROOT / "results" / "rulefaith" / "qwen3_structured_evidence_repaired_candidates.jsonl"
DEFAULT_EDIT_POOL = ROOT / "data" / "rulefaith" / "edit_pool.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "rulefaith" / "filtering"
DEFAULT_PREFIX = "qwen3_field_aware_rulefaith"
DEFAULT_STATS = ROOT / "results" / "rulefaith" / "qwen3_field_aware_rulefaith_selection_stats.json"
DEFAULT_REPORT = ROOT / "results" / "rulefaith" / "qwen3_field_aware_rulefaith_selection_report.md"
DEFAULT_CSV = ROOT / "results" / "rulefaith" / "qwen3_field_aware_rulefaith_selection.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Bad JSON in {path}:{lineno}: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"JSONL row is not an object in {path}:{lineno}")
            rows.append(row)
    if not rows:
        raise ValueError(f"Input file is empty: {path}")
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


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


def field_edit_copy(text: Any, edit: dict[str, Any]) -> bool:
    normalized = audit.normalize(text)
    operation = audit.normalize(edit.get("operation", ""))
    source = audit.normalize(edit.get("source_text", ""))
    target = audit.normalize(edit.get("target_text", ""))
    operation_hit = bool(operation and (operation in normalized or any(word in normalized for word in ["replace", "insert", "delete", "change", "remove"])))
    source_hit = not source or source in normalized
    target_hit = operation == "delete" or not target or target in normalized
    return bool(operation_hit and source_hit and target_hit)


def field_target_copy(text: Any, edit: dict[str, Any]) -> bool:
    target = audit.normalize(edit.get("target_text", ""))
    return bool(target and target in audit.normalize(text))


def leakage_by_field(row: dict[str, Any]) -> dict[str, bool]:
    parsed = row.get("parsed_output") or {}
    edit = row.get("model_edit") or {}
    return {
        "edit_description_edit_copy": field_edit_copy(parsed.get("edit_description", ""), edit),
        "edit_description_target_copy": field_target_copy(parsed.get("edit_description", ""), edit),
        "rule_text_edit_copy": field_edit_copy(parsed.get("rule_text", ""), edit),
        "rule_text_target_copy": field_target_copy(parsed.get("rule_text", ""), edit),
        "rationale_edit_copy": field_edit_copy(parsed.get("rationale", ""), edit),
        "rationale_target_copy": field_target_copy(parsed.get("rationale", ""), edit),
    }


def select_candidate(row: dict[str, Any], flags: dict[str, Any]) -> tuple[str, list[str], list[str], dict[str, bool]]:
    leakage = leakage_by_field(row)
    hard: list[str] = []
    refine: list[str] = []
    if row.get("parse_status") != "parsed_json":
        hard.append("parse_not_json")
    for key in [
        "alignment_error",
        "validity_error_auto",
        "possible_false_rationalization",
        "missing_rule",
        "rule_edit_copy",
        "missing_evidence",
        "wrong_evidence_auto",
        "evidence_text_found_in_prediction_only",
    ]:
        if flags.get(key) is True:
            hard.append(key)
    if not repair.has_specific_source_evidence(row):
        hard.append("no_specific_source_evidence")
    if leakage["rationale_edit_copy"]:
        refine.append("rationale_edit_copy")
    if flags.get("unsupported_confidence") is True:
        refine.append("unsupported_confidence")
    if flags.get("generic_explanation") is True:
        refine.append("generic_explanation")
    if hard:
        return "rejected", hard, refine, leakage
    if refine:
        return "refine", hard, refine, leakage
    return "accepted", hard, refine, leakage


def write_selection_csv(path: Path, rows: list[dict[str, Any]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "candidate_id",
        "bucket",
        "hard_reasons",
        "refine_reasons",
        "dataset",
        "model_key",
        "operation",
        "error_type",
        "edit_description_edit_copy",
        "rule_text_edit_copy",
        "rationale_edit_copy",
        "rule_text_target_copy",
        "rationale_target_copy",
        "specific_source_evidence",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            edit = row.get("model_edit") or {}
            selection = row["rulefaith_field_aware_selection"]
            leakage = selection["field_leakage"]
            writer.writerow(
                {
                    "candidate_id": row["candidate_id"],
                    "bucket": selection["bucket"],
                    "hard_reasons": ";".join(selection["hard_reasons"]),
                    "refine_reasons": ";".join(selection["refine_reasons"]),
                    "dataset": row.get("dataset", ""),
                    "model_key": row.get("model_key", ""),
                    "operation": edit.get("operation", ""),
                    "error_type": edit.get("error_type", ""),
                    "edit_description_edit_copy": leakage["edit_description_edit_copy"],
                    "rule_text_edit_copy": leakage["rule_text_edit_copy"],
                    "rationale_edit_copy": leakage["rationale_edit_copy"],
                    "rule_text_target_copy": leakage["rule_text_target_copy"],
                    "rationale_target_copy": leakage["rationale_target_copy"],
                    "specific_source_evidence": repair.has_specific_source_evidence(row),
                }
            )


def summarize(selected_rows: list[dict[str, Any]], previous_strict_counts: dict[str, int] | None = None) -> dict[str, Any]:
    bucket_counts = Counter(row["rulefaith_field_aware_selection"]["bucket"] for row in selected_rows)
    hard_reasons = Counter(reason for row in selected_rows for reason in row["rulefaith_field_aware_selection"]["hard_reasons"])
    refine_reasons = Counter(reason for row in selected_rows for reason in row["rulefaith_field_aware_selection"]["refine_reasons"])
    active_refine_reasons = Counter(
        reason
        for row in selected_rows
        if row["rulefaith_field_aware_selection"]["bucket"] == "refine"
        for reason in row["rulefaith_field_aware_selection"]["refine_reasons"]
    )
    leakage_counts = Counter()
    for row in selected_rows:
        for key, value in row["rulefaith_field_aware_selection"]["field_leakage"].items():
            if value:
                leakage_counts[key] += 1
    summary = {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "candidate_count": len(selected_rows),
        "bucket_counts": dict(sorted(bucket_counts.items())),
        "bucket_rates": {bucket: round(count / len(selected_rows), 4) if selected_rows else 0.0 for bucket, count in sorted(bucket_counts.items())},
        "hard_reason_counts": dict(sorted(hard_reasons.items())),
        "refine_trigger_counts_all_rows": dict(sorted(refine_reasons.items())),
        "active_refine_reason_counts": dict(sorted(active_refine_reasons.items())),
        "field_leakage_counts": dict(sorted(leakage_counts.items())),
        "previous_strict_bucket_counts": previous_strict_counts or {},
        "decision": "use_field_aware_gate_for_target_masked_validation_pool",
        "policy": {
            "accepted": "passes parse/alignment/validity/rule/evidence/specific-source hard gates; no rationale edit-copy, genericness, or unsupported-confidence refine risk",
            "refine": "passes hard gates but has rationale edit-copy, genericness, or unsupported-confidence risk",
            "rejected": "fails parse/alignment/validity/false-rationalization/rule/evidence/specific-source hard gate",
            "allowed_copy": "edit_description may mention the atomic edit because it is the structured edit-description field; this is reported but not treated as leakage by itself",
        },
    }
    return summary


def markdown(summary: dict[str, Any], selected_rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Qwen3 Field-Aware RuleFaith Selection",
        "",
        "This gate separates required edit description from leakage in rule/rationale fields. It does not treat `edit_description` edit-copy as a direct failure, but it still rejects alignment, validity, false-rationalization, rule, and evidence hard failures.",
        "",
        "## Bucket Counts",
        "",
        f"- current: `{summary['bucket_counts']}`",
        f"- previous strict: `{summary['previous_strict_bucket_counts']}`",
        "",
        "## Field Leakage Counts",
        "",
    ]
    for key, value in summary["field_leakage_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Hard Failure Reasons", ""])
    for key, value in summary["hard_reason_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Refine Reasons", ""])
    lines.append("Active refine bucket:")
    lines.append("")
    for key, value in summary["active_refine_reason_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.append("")
    lines.append("All refine triggers before hard-reject override:")
    lines.append("")
    for key, value in summary["refine_trigger_counts_all_rows"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Accepted Examples", ""])
    shown = 0
    for row in selected_rows:
        selection = row["rulefaith_field_aware_selection"]
        if selection["bucket"] != "accepted":
            continue
        parsed = row.get("parsed_output") or {}
        lines.extend(
            [
                f"### {row['candidate_id']}",
                "",
                f"- source: {row.get('source', '')}",
                f"- edit: `{row.get('model_edit', {}).get('operation', '')}` `{row.get('model_edit', {}).get('source_text', '')}` -> `{row.get('model_edit', {}).get('target_text', '')}`",
                f"- rule: {parsed.get('rule_text', '')}",
                f"- rationale: {parsed.get('rationale', '')[:240]}",
                f"- evidence: `{json.dumps(parsed.get('evidence_spans', []), ensure_ascii=False, sort_keys=True)}`",
                "",
            ]
        )
        shown += 1
        if shown >= 12:
            lines.append("Additional accepted candidates are available in the JSONL bucket.")
            break
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- Accepted means suitable for target-masked validation, not ready for SFT positive construction.",
            "- These are automatic pseudo-label decisions, not human evaluation.",
            "- Rule correctness still requires human or stronger verifier confirmation.",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run field-aware RuleFaith selection over repaired Qwen3 candidates.")
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--edit-pool", type=Path, default=DEFAULT_EDIT_POOL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--stats-output", type=Path, default=DEFAULT_STATS)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--csv-output", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    candidates = read_jsonl(resolve(args.candidates))
    edit_pool = read_jsonl(resolve(args.edit_pool))
    flags = repair.annotated_flags(candidates, edit_pool)
    flags_by_id = {row["candidate_id"]: row for row in flags}
    buckets: dict[str, list[dict[str, Any]]] = {"accepted": [], "refine": [], "rejected": []}
    selected_rows: list[dict[str, Any]] = []
    for row in candidates:
        flag_row = flags_by_id[row["candidate_id"]]
        bucket, hard, refine_reasons, leakage = select_candidate(row, flag_row)
        enriched = dict(row)
        enriched["rulefaith_field_aware_selection"] = {
            "bucket": bucket,
            "hard_reasons": hard,
            "refine_reasons": refine_reasons,
            "field_leakage": leakage,
            "specific_source_evidence": repair.has_specific_source_evidence(row),
        }
        buckets[bucket].append(enriched)
        selected_rows.append(enriched)
    output_dir = resolve(args.output_dir)
    for bucket, rows in buckets.items():
        write_jsonl(output_dir / f"{args.prefix}_{bucket}.jsonl", rows, args.overwrite)
    previous = {}
    strict_stats_path = ROOT / "results" / "rulefaith" / "qwen3_structured_evidence_repair_stats.json"
    if strict_stats_path.exists():
        previous = json.loads(strict_stats_path.read_text(encoding="utf-8")).get("strict_selection", {}).get("bucket_counts", {})
    summary = summarize(selected_rows, previous)
    write_json(resolve(args.stats_output), summary, args.overwrite)
    write_text(resolve(args.report_output), markdown(summary, selected_rows), args.overwrite)
    write_selection_csv(resolve(args.csv_output), selected_rows, args.overwrite)
    print(json.dumps({"bucket_counts": summary["bucket_counts"], "decision": summary["decision"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
