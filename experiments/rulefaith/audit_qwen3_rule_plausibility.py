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
from experiments.rulefaith import validate_qwen3_target_masked as target_masked


DEFAULT_INPUT = ROOT / "data" / "rulefaith" / "filtering" / "qwen3_target_masked_rulefaith_validated.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "rulefaith" / "filtering"
DEFAULT_PREFIX = "qwen3_rule_plausibility"
DEFAULT_STATS = ROOT / "results" / "rulefaith" / "qwen3_rule_plausibility_audit_stats.json"
DEFAULT_REPORT = ROOT / "results" / "rulefaith" / "qwen3_rule_plausibility_audit_report.md"
DEFAULT_CSV = ROOT / "results" / "rulefaith" / "qwen3_rule_plausibility_audit.csv"


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


def evidence_roles(row: dict[str, Any]) -> set[str]:
    roles: set[str] = set()
    for item in target_masked.specific_evidence_items(row):
        roles.add(audit.normalize(item.get("role", "")))
    return roles


def role_hit(roles: set[str], choices: set[str]) -> bool:
    for role in roles:
        if role in choices:
            return True
        if any(choice in role for choice in choices):
            return True
    return False


def required_evidence_groups(row: dict[str, Any]) -> list[tuple[str, set[str]]]:
    edit = row.get("model_edit") or {}
    error_type = audit.normalize(edit.get("error_type", row.get("error_type", "")))
    category = audit.normalize(row.get("error_category", ""))
    if "sva" in error_type or "subject_verb_agreement" in category:
        return [("subject", {"grammatical_subject", "subject"})]
    if "prep" in error_type or "prepositions" in category:
        return [
            ("governor", {"preposition_governor", "governor"}),
            ("complement", {"preposition_complement", "complement"}),
        ]
    if "det" in error_type or "articles_determiners" in category:
        return [("head_noun", {"head_noun", "noun", "noun_context", "noun_phrase_context"})]
    if "pron" in error_type or "pronouns" in category:
        return [("antecedent", {"antecedent", "pronoun_antecedent_context", "reference"})]
    if "noun:num" in error_type or "noun_number" in category:
        return [("noun_number_context", {"head_noun", "noun_number_context", "noun_phrase_context", "noun"})]
    if "verb" in error_type or "verb_form" in category:
        return [("verb_context", {"verb_context", "verb_complement_or_time_context", "finite_verb", "time_expression", "subject"})]
    if "orth" in error_type or "spell" in error_type or "punct" in error_type or "spelling_orthography" in category:
        return [("orthographic_context", {"modified_token", "head_noun", "punctuation_context"})]
    return [("specific_source_evidence", repair.SPECIFIC_EVIDENCE_ROLES)]


def evidence_sufficiency(row: dict[str, Any]) -> tuple[str, list[str]]:
    roles = evidence_roles(row)
    missing = [name for name, choices in required_evidence_groups(row) if not role_hit(roles, choices)]
    if not roles:
        return "insufficient", ["no_specific_source_evidence"]
    if not missing:
        return "sufficient", []
    if len(missing) < len(required_evidence_groups(row)):
        return "partial", [f"missing_required_evidence:{name}" for name in missing]
    return "insufficient", [f"missing_required_evidence:{name}" for name in missing]


def rule_plausibility(row: dict[str, Any]) -> tuple[str, list[str]]:
    validation = row.get("rulefaith_target_masked_validation") or target_masked.validate_row(row)
    parsed = row.get("parsed_output") or {}
    text = target_masked.quality_text(parsed)
    masked, _ = target_masked.mask_target(text, (row.get("model_edit") or {}).get("target_text", ""))
    reasons: list[str] = []
    if validation.get("generic_after_target_mask"):
        reasons.append("generic_rule_after_mask")
    if not validation.get("masked_rule_has_grammar_signal"):
        reasons.append("missing_grammar_signal_after_mask")
    if validation.get("target_dependent"):
        reasons.append("target_dependent_rule_or_rationale")
    if validation.get("rule_category_issue"):
        reasons.append(f"rule_category_mismatch:{validation['rule_category_issue']}")
    if not repair.has_specific_source_evidence(row):
        reasons.append("no_specific_source_evidence")
    if target_masked.generic_hit(masked):
        reasons.append("generic_quality_text")
    if any(reason.startswith("rule_category_mismatch") for reason in reasons):
        return "implausible", reasons
    if any(reason in reasons for reason in ["missing_grammar_signal_after_mask", "generic_rule_after_mask", "target_dependent_rule_or_rationale"]):
        return "weak", reasons
    return "plausible", reasons


def unsupported_confidence(row: dict[str, Any], rule_label: str, evidence_label: str) -> bool:
    parsed = row.get("parsed_output") or {}
    try:
        confidence = float(parsed.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0
    return confidence >= 0.9 and (rule_label != "plausible" or evidence_label != "sufficient")


def audit_row(row: dict[str, Any]) -> dict[str, Any]:
    validation = row.get("rulefaith_target_masked_validation") or target_masked.validate_row(row)
    rule_label, rule_reasons = rule_plausibility(row)
    evidence_label, evidence_reasons = evidence_sufficiency(row)
    warnings = list(validation.get("warnings", []))
    reasons = rule_reasons + evidence_reasons
    if "specific_evidence_not_mentioned_in_rule_or_rationale" in warnings:
        reasons.append("evidence_not_mentioned_in_rule_or_rationale")
    if "rationale_edit_copy" in warnings:
        reasons.append("rationale_edit_copy")
    if unsupported_confidence(row, rule_label, evidence_label):
        reasons.append("unsupported_high_confidence")

    if rule_label == "implausible":
        decision = "reject"
    elif evidence_label == "insufficient":
        decision = "reject"
    elif reasons:
        decision = "needs_refinement"
    else:
        decision = "ready_for_human_spotcheck"
    return {
        "rule_plausibility_label": rule_label,
        "evidence_sufficiency_label": evidence_label,
        "decision": decision,
        "reasons": reasons,
        "target_masked_score": validation.get("target_masked_score", 0.0),
        "target_masked_bucket": validation.get("target_masked_bucket", ""),
    }


def enrich_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        enriched = dict(row)
        enriched["rulefaith_rule_plausibility_audit"] = audit_row(row)
        output.append(enriched)
    return output


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    decisions = Counter(row["rulefaith_rule_plausibility_audit"]["decision"] for row in rows)
    rules = Counter(row["rulefaith_rule_plausibility_audit"]["rule_plausibility_label"] for row in rows)
    evidence = Counter(row["rulefaith_rule_plausibility_audit"]["evidence_sufficiency_label"] for row in rows)
    reasons = Counter(reason for row in rows for reason in row["rulefaith_rule_plausibility_audit"]["reasons"])
    by_dataset: dict[str, dict[str, int]] = {}
    for dataset in sorted({str(row.get("dataset", "")) for row in rows}):
        group = [row for row in rows if str(row.get("dataset", "")) == dataset]
        by_dataset[dataset] = dict(sorted(Counter(row["rulefaith_rule_plausibility_audit"]["decision"] for row in group).items()))
    by_model: dict[str, dict[str, int]] = {}
    for model in sorted({str(row.get("model_key", "")) for row in rows}):
        group = [row for row in rows if str(row.get("model_key", "")) == model]
        by_model[model] = dict(sorted(Counter(row["rulefaith_rule_plausibility_audit"]["decision"] for row in group).items()))
    return {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "candidate_count": len(rows),
        "decision_counts": dict(sorted(decisions.items())),
        "decision_rates": {key: round(value / len(rows), 4) if rows else 0.0 for key, value in sorted(decisions.items())},
        "rule_plausibility_counts": dict(sorted(rules.items())),
        "evidence_sufficiency_counts": dict(sorted(evidence.items())),
        "reason_counts": dict(sorted(reasons.items())),
        "by_dataset": by_dataset,
        "by_model_key": by_model,
        "decision": "use_ready_bucket_for_blind_human_or_stronger_validation_package_only",
        "policy": {
            "ready_for_human_spotcheck": "target-masked validated candidate with plausible rule, sufficient source evidence, evidence mentioned in rule/rationale, no rationale edit-copy, and no unsupported high confidence",
            "needs_refinement": "rule/evidence mostly usable but explanation needs targeted repair before human package or positive construction",
            "reject": "implausible rule or insufficient evidence after target-masked validation",
        },
    }


def write_csv(path: Path, rows: list[dict[str, Any]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "candidate_id",
        "decision",
        "rule_plausibility_label",
        "evidence_sufficiency_label",
        "reasons",
        "target_masked_score",
        "dataset",
        "model_key",
        "operation",
        "error_type",
        "error_category",
        "source_text",
        "target_text",
        "rule_text",
        "rationale",
        "evidence_spans_json",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            result = row["rulefaith_rule_plausibility_audit"]
            edit = row.get("model_edit") or {}
            parsed = row.get("parsed_output") or {}
            writer.writerow(
                {
                    "candidate_id": row["candidate_id"],
                    "decision": result["decision"],
                    "rule_plausibility_label": result["rule_plausibility_label"],
                    "evidence_sufficiency_label": result["evidence_sufficiency_label"],
                    "reasons": ";".join(result["reasons"]),
                    "target_masked_score": result["target_masked_score"],
                    "dataset": row.get("dataset", ""),
                    "model_key": row.get("model_key", ""),
                    "operation": edit.get("operation", ""),
                    "error_type": edit.get("error_type", ""),
                    "error_category": row.get("error_category", ""),
                    "source_text": edit.get("source_text", ""),
                    "target_text": edit.get("target_text", ""),
                    "rule_text": parsed.get("rule_text", ""),
                    "rationale": parsed.get("rationale", ""),
                    "evidence_spans_json": json.dumps(parsed.get("evidence_spans", []), ensure_ascii=False, sort_keys=True),
                }
            )


def markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Qwen3 Rule Plausibility and Evidence Sufficiency Audit",
        "",
        "This automatic audit runs after target-masked validation. It checks whether the rule type is plausible for the edit category and whether evidence spans are sufficient for that rule type. It is not human evaluation.",
        "",
        "## Summary",
        "",
        f"- Candidate count: {summary['candidate_count']}",
        f"- Decision counts: `{summary['decision_counts']}`",
        f"- Decision rates: `{summary['decision_rates']}`",
        f"- Rule plausibility: `{summary['rule_plausibility_counts']}`",
        f"- Evidence sufficiency: `{summary['evidence_sufficiency_counts']}`",
        "",
        "## Reason Counts",
        "",
    ]
    for key, value in summary["reason_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Ready Examples", ""])
    shown = 0
    for row in rows:
        result = row["rulefaith_rule_plausibility_audit"]
        if result["decision"] != "ready_for_human_spotcheck":
            continue
        edit = row.get("model_edit") or {}
        parsed = row.get("parsed_output") or {}
        lines.extend(
            [
                f"### {row['candidate_id']}",
                "",
                f"- source: {row.get('source', '')}",
                f"- edit: `{edit.get('operation', '')}` `{edit.get('source_text', '')}` -> `{edit.get('target_text', '')}`",
                f"- rule: {parsed.get('rule_text', '')}",
                f"- evidence: `{json.dumps(parsed.get('evidence_spans', []), ensure_ascii=False, sort_keys=True)}`",
                "",
            ]
        )
        shown += 1
        if shown >= 12:
            lines.append("Additional ready candidates are available in the JSONL bucket.")
            break
    lines.extend(["", "## Refinement / Reject Examples", ""])
    shown = 0
    for row in rows:
        result = row["rulefaith_rule_plausibility_audit"]
        if result["decision"] == "ready_for_human_spotcheck":
            continue
        parsed = row.get("parsed_output") or {}
        lines.extend(
            [
                f"- `{row['candidate_id']}` decision=`{result['decision']}` reasons=`{';'.join(result['reasons'])}`",
                f"  - rule: {parsed.get('rule_text', '')[:220]}",
            ]
        )
        shown += 1
        if shown >= 20:
            break
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- This audit uses deterministic heuristics and ERRANT-style category assumptions.",
            "- It can catch obvious category/evidence issues but may miss subtle grammatical invalidity.",
            "- Ready candidates are only ready for human or stronger validation, not final positive training data.",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit target-masked Qwen3 candidates for rule plausibility and evidence sufficiency.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--stats-output", type=Path, default=DEFAULT_STATS)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--csv-output", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = read_jsonl(resolve(args.input))
    enriched = enrich_rows(rows)
    buckets: dict[str, list[dict[str, Any]]] = {"ready_for_human_spotcheck": [], "needs_refinement": [], "reject": []}
    for row in enriched:
        buckets[row["rulefaith_rule_plausibility_audit"]["decision"]].append(row)
    output_dir = resolve(args.output_dir)
    for bucket, bucket_rows in buckets.items():
        write_jsonl(output_dir / f"{args.prefix}_{bucket}.jsonl", bucket_rows, args.overwrite)
    summary = summarize(enriched)
    write_json(resolve(args.stats_output), summary, args.overwrite)
    write_text(resolve(args.report_output), markdown(summary, enriched), args.overwrite)
    write_csv(resolve(args.csv_output), enriched, args.overwrite)
    print(json.dumps({"decision_counts": summary["decision_counts"], "decision": summary["decision"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
