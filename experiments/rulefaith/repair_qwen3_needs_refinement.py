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
from experiments.rulefaith import select_qwen3_field_aware_rulefaith as field_select
from experiments.rulefaith import validate_qwen3_target_masked as target_masked


DEFAULT_INPUT = ROOT / "data" / "rulefaith" / "filtering" / "qwen3_rule_plausibility_needs_refinement.jsonl"
DEFAULT_OUTPUT = ROOT / "results" / "rulefaith" / "qwen3_targeted_repaired_candidates.jsonl"
DEFAULT_STATS = ROOT / "results" / "rulefaith" / "qwen3_targeted_repair_stats.json"
DEFAULT_REPORT = ROOT / "results" / "rulefaith" / "qwen3_targeted_repair_report.md"
DEFAULT_CSV = ROOT / "results" / "rulefaith" / "qwen3_targeted_repair_before_after.csv"


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


def evidence_clause(row: dict[str, Any]) -> str:
    spans = target_masked.specific_evidence_items(row)
    if not spans:
        return "The available source sentence does not provide enough specific evidence for a reliable explanation."
    parts: list[str] = []
    for item in spans[:3]:
        text = str(item.get("text", "")).strip()
        role = str(item.get("role", "evidence")).replace("_", " ").strip() or "evidence"
        if text:
            parts.append(f'"{text}" as {role}')
    joined = "; ".join(parts)
    return f"The cited source evidence is {joined}."


def repair_rationale(row: dict[str, Any], reasons: list[str]) -> tuple[str, list[str]]:
    parsed = row.get("parsed_output") or {}
    rule_text = str(parsed.get("rule_text", "")).strip()
    rationale = str(parsed.get("rationale", "")).strip()
    clause = evidence_clause(row)
    actions: list[str] = []
    leakage = field_select.leakage_by_field(row)
    if "rationale_edit_copy" in reasons or leakage["rationale_edit_copy"]:
        actions.append("replaced_rationale_edit_copy")
        if rule_text:
            return f"{clause} This evidence supports the rule that {rule_text.rstrip('.')}.", actions
        return clause, actions
    if "evidence_not_mentioned_in_rule_or_rationale" in reasons:
        actions.append("appended_source_evidence_to_rationale")
        return f"{rationale.rstrip()} {clause}".strip(), actions
    return rationale, actions


def repair_confidence(parsed: dict[str, Any], actions: list[str]) -> None:
    try:
        confidence = float(parsed.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0
    if confidence > 0.85:
        parsed["confidence"] = 0.8
        actions.append("capped_confidence_at_0.8")


def repair_row(row: dict[str, Any]) -> dict[str, Any]:
    result = row.get("rulefaith_rule_plausibility_audit") or {}
    reasons = list(result.get("reasons", []))
    parsed = dict(row.get("parsed_output") or {})
    actions: list[str] = []
    new_rationale, rationale_actions = repair_rationale(row, reasons)
    actions.extend(rationale_actions)
    parsed["rationale"] = new_rationale
    repair_confidence(parsed, actions)
    output = dict(row)
    output["candidate_id"] = f"{row['candidate_id']}::targeted_repaired"
    output["original_candidate_id"] = row.get("candidate_id")
    output["parsed_output"] = parsed
    output["rulefaith_targeted_repair"] = {
        "reasons": reasons,
        "actions": actions,
        "repair_source": "deterministic_rulefaith_repair_not_human",
    }
    return output


def summarize(before: list[dict[str, Any]], after: list[dict[str, Any]]) -> dict[str, Any]:
    before_rationale_copy = sum(1 for row in before if field_select.leakage_by_field(row)["rationale_edit_copy"])
    after_rationale_copy = sum(1 for row in after if field_select.leakage_by_field(row)["rationale_edit_copy"])
    before_evidence_mentioned = sum(1 for row in before if target_masked.evidence_mentioned_in_text(row, target_masked.quality_text(row.get("parsed_output") or {})))
    after_evidence_mentioned = sum(1 for row in after if target_masked.evidence_mentioned_in_text(row, target_masked.quality_text(row.get("parsed_output") or {})))
    actions = Counter(action for row in after for action in row["rulefaith_targeted_repair"]["actions"])
    return {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "candidate_count": len(after),
        "before_rationale_edit_copy": before_rationale_copy,
        "after_rationale_edit_copy": after_rationale_copy,
        "before_evidence_mentioned_in_quality_text": before_evidence_mentioned,
        "after_evidence_mentioned_in_quality_text": after_evidence_mentioned,
        "action_counts": dict(sorted(actions.items())),
        "decision": "rerun_target_masked_and_rule_plausibility_audit_on_repaired_candidates",
        "label_source": "deterministic_repair_not_human_label",
    }


def write_csv(path: Path, before: list[dict[str, Any]], after: list[dict[str, Any]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "original_candidate_id",
        "repaired_candidate_id",
        "actions",
        "before_rationale_edit_copy",
        "after_rationale_edit_copy",
        "before_rationale",
        "after_rationale",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for old, new in zip(before, after):
            writer.writerow(
                {
                    "original_candidate_id": old["candidate_id"],
                    "repaired_candidate_id": new["candidate_id"],
                    "actions": ";".join(new["rulefaith_targeted_repair"]["actions"]),
                    "before_rationale_edit_copy": field_select.leakage_by_field(old)["rationale_edit_copy"],
                    "after_rationale_edit_copy": field_select.leakage_by_field(new)["rationale_edit_copy"],
                    "before_rationale": (old.get("parsed_output") or {}).get("rationale", ""),
                    "after_rationale": (new.get("parsed_output") or {}).get("rationale", ""),
                }
            )


def markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Qwen3 Targeted Repair",
        "",
        "This deterministic repair pass uses Loop K audit reasons to connect cited source evidence back into the rationale and remove rationale-level edit-copy wording. It is not a model-generated or human-authored revision.",
        "",
        "## Summary",
        "",
        f"- Candidate count: {summary['candidate_count']}",
        f"- Rationale edit-copy before/after: {summary['before_rationale_edit_copy']} -> {summary['after_rationale_edit_copy']}",
        f"- Evidence mentioned in rule/rationale before/after: {summary['before_evidence_mentioned_in_quality_text']} -> {summary['after_evidence_mentioned_in_quality_text']}",
        f"- Action counts: `{summary['action_counts']}`",
        "",
        "## Examples",
        "",
    ]
    for row in rows[:12]:
        parsed = row.get("parsed_output") or {}
        lines.extend(
            [
                f"### {row['candidate_id']}",
                "",
                f"- actions: `{';'.join(row['rulefaith_targeted_repair']['actions'])}`",
                f"- rationale: {parsed.get('rationale', '')[:320]}",
                "",
            ]
        )
    lines.extend(
        [
            "## Limitations",
            "",
            "- This repair improves structural evidence integration, but it does not prove grammatical correctness.",
            "- Repaired candidates must pass the target-masked and rule/evidence gates again.",
            "- Repaired candidates remain automatic pseudo-label artifacts, not human gold.",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministically repair Qwen3 needs-refinement explanations.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stats-output", type=Path, default=DEFAULT_STATS)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--csv-output", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    before = read_jsonl(resolve(args.input))
    after = [repair_row(row) for row in before]
    write_jsonl(resolve(args.output), after, args.overwrite)
    summary = summarize(before, after)
    write_json(resolve(args.stats_output), summary, args.overwrite)
    write_text(resolve(args.report_output), markdown(summary, after), args.overwrite)
    write_csv(resolve(args.csv_output), before, after, args.overwrite)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
