from __future__ import annotations

import argparse
import csv
import json
import re
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
from experiments.rulefaith import select_qwen3_field_aware_rulefaith as field_select


DEFAULT_INPUTS = [
    ROOT / "data" / "rulefaith" / "filtering" / "qwen3_field_aware_rulefaith_accepted.jsonl",
    ROOT / "data" / "rulefaith" / "filtering" / "qwen3_field_aware_rulefaith_refine.jsonl",
]
DEFAULT_OUTPUT_DIR = ROOT / "data" / "rulefaith" / "filtering"
DEFAULT_PREFIX = "qwen3_target_masked_rulefaith"
DEFAULT_STATS = ROOT / "results" / "rulefaith" / "qwen3_target_masked_validation_stats.json"
DEFAULT_REPORT = ROOT / "results" / "rulefaith" / "qwen3_target_masked_validation_report.md"
DEFAULT_CSV = ROOT / "results" / "rulefaith" / "qwen3_target_masked_validation.csv"
TARGET_MASK = "[TARGET_MASK]"

QUALITY_FIELDS = ["rule_text", "rationale"]


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


def target_pattern(target: Any) -> re.Pattern[str] | None:
    target_text = str(target or "").strip()
    if not target_text:
        return None
    pieces = [re.escape(piece) for piece in target_text.split()]
    if not pieces:
        return None
    body = r"\s+".join(pieces)
    prefix = r"(?<!\w)" if re.match(r"\w", target_text[0]) else ""
    suffix = r"(?!\w)" if re.match(r"\w", target_text[-1]) else ""
    return re.compile(prefix + body + suffix, flags=re.IGNORECASE)


def contains_target(text: Any, target: Any) -> bool:
    pattern = target_pattern(target)
    return bool(pattern and pattern.search(str(text or "")))


def mask_target(text: Any, target: Any) -> tuple[str, int]:
    pattern = target_pattern(target)
    value = str(text or "")
    if not pattern:
        return value, 0
    return pattern.subn(TARGET_MASK, value)


def quality_text(parsed: dict[str, Any]) -> str:
    conditions = parsed.get("applicability_conditions", [])
    if isinstance(conditions, list):
        condition_text = " ".join(str(item) for item in conditions)
    else:
        condition_text = str(conditions or "")
    fields = [str(parsed.get(field, "")) for field in QUALITY_FIELDS]
    fields.append(condition_text)
    return " ".join(fields)


def grammar_keyword_hit(text: str) -> bool:
    normalized = audit.normalize(text)
    return any(keyword in normalized for keyword in audit.GRAMMAR_KEYWORDS)


def generic_hit(text: str) -> bool:
    normalized = audit.normalize(text)
    return any(phrase in normalized for phrase in audit.GENERIC_PHRASES) and not grammar_keyword_hit(text)


def rule_category_issue(row: dict[str, Any], text: str) -> str:
    normalized = audit.normalize(text)
    error_category = audit.normalize(row.get("error_category", ""))
    edit = row.get("model_edit") or {}
    error_type = audit.normalize(edit.get("error_type", row.get("error_type", "")))
    if not normalized:
        return "missing_rule_text"
    if ("noun_number" in error_category or "noun:num" in error_type) and "subject" in normalized and "verb" in normalized:
        return "noun_number_explained_as_subject_verb_agreement"
    if ("articles_determiners" in error_category or "det" in error_type) and not any(
        word in normalized for word in ["article", "determiner", "definite", "indefinite", "a ", "an ", "the "]
    ):
        return "determiner_rule_lacks_article_or_determiner_signal"
    if ("prepositions" in error_category or "prep" in error_type) and "preposition" not in normalized:
        return "preposition_rule_lacks_preposition_signal"
    if ("pronouns" in error_category or "pron" in error_type) and not any(word in normalized for word in ["pronoun", "antecedent", "reference"]):
        return "pronoun_rule_lacks_pronoun_signal"
    if ("spelling_orthography" in error_category or "orth" in error_type or "spell" in error_type) and not any(
        word in normalized for word in ["spelling", "orthograph", "capital", "punctuation", "apostrophe"]
    ):
        return "orthography_rule_lacks_spelling_signal"
    if ("verb_form" in error_category or "verb" in error_type) and not any(
        word in normalized for word in ["verb", "tense", "aspect", "infinitive", "gerund", "participle", "auxiliary"]
    ):
        return "verb_rule_lacks_verb_signal"
    return ""


def evidence_items(row: dict[str, Any]) -> list[dict[str, Any]]:
    parsed = row.get("parsed_output") or {}
    spans = parsed.get("evidence_spans", [])
    return [span for span in spans if isinstance(span, dict)] if isinstance(spans, list) else []


def specific_evidence_items(row: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    source = str(row.get("source", ""))
    prediction = str(row.get("model_prediction", ""))
    edit = row.get("model_edit") or {}
    for item in evidence_items(row):
        checks = audit.evidence_checks(source, prediction, edit, [item])
        role = audit.normalize(item.get("role", ""))
        if not checks["evidence_contextual"]:
            continue
        if role in repair.SPECIFIC_EVIDENCE_ROLES:
            items.append(item)
            continue
        if role == "modified_token" and audit.edit_token_can_be_contextual(edit):
            items.append(item)
            continue
        if role not in repair.GENERIC_EVIDENCE_ROLE_WORDS and any(word in role for word in repair.SPECIFIC_EVIDENCE_ROLE_WORDS):
            items.append(item)
    return items


def evidence_mentioned_in_text(row: dict[str, Any], text: str) -> bool:
    edit = row.get("model_edit") or {}
    source = audit.normalize(edit.get("source_text", ""))
    target = audit.normalize(edit.get("target_text", ""))
    normalized_text = audit.normalize(text)
    for item in specific_evidence_items(row):
        span_text = audit.normalize(item.get("text", ""))
        if not span_text or span_text in {source, target}:
            continue
        if span_text in normalized_text:
            return True
    return False


def target_occurrences_by_field(row: dict[str, Any]) -> dict[str, int]:
    parsed = row.get("parsed_output") or {}
    edit = row.get("model_edit") or {}
    target = edit.get("target_text", "")
    counts: dict[str, int] = {}
    for field in ["edit_description", "rule_text", "rationale"]:
        _, count = mask_target(parsed.get(field, ""), target)
        counts[field] = count
    conditions = parsed.get("applicability_conditions", [])
    condition_text = " ".join(str(item) for item in conditions) if isinstance(conditions, list) else str(conditions or "")
    _, counts["applicability_conditions"] = mask_target(condition_text, target)
    return counts


def validate_row(row: dict[str, Any]) -> dict[str, Any]:
    parsed = row.get("parsed_output") or {}
    edit = row.get("model_edit") or {}
    target = edit.get("target_text", "")
    original_quality_text = quality_text(parsed)
    masked_quality_text, masked_count = mask_target(original_quality_text, target)
    grammar_survives = grammar_keyword_hit(masked_quality_text)
    category_issue = rule_category_issue(row, masked_quality_text)
    specific_evidence = specific_evidence_items(row)
    evidence_specific_count = len(specific_evidence)
    evidence_mention_survives = evidence_mentioned_in_text(row, masked_quality_text)
    generic_after_mask = generic_hit(masked_quality_text)
    field_leakage = field_select.leakage_by_field(row)
    target_counts = target_occurrences_by_field(row)
    target_in_quality_fields = sum(target_counts[field] for field in ["rule_text", "rationale", "applicability_conditions"])
    rationale_edit_copy = field_leakage["rationale_edit_copy"]
    rule_text_edit_copy = field_leakage["rule_text_edit_copy"]
    no_specific_evidence = not repair.has_specific_source_evidence(row)
    target_dependent = bool(target_in_quality_fields and (not grammar_survives or not evidence_mention_survives))

    score = 0.0
    score += 0.35 if grammar_survives else 0.0
    score += 0.35 if evidence_specific_count else 0.0
    score += 0.15 if evidence_mention_survives else (0.05 if evidence_specific_count else 0.0)
    score += 0.15 if not generic_after_mask else 0.0
    if target_dependent:
        score -= 0.2
    if rationale_edit_copy:
        score -= 0.2
    if rule_text_edit_copy:
        score -= 0.35
    if no_specific_evidence:
        score -= 0.35
    if category_issue:
        score -= 0.3
    score = round(max(0.0, min(1.0, score)), 4)

    failures: list[str] = []
    warnings: list[str] = []
    if not grammar_survives:
        failures.append("masked_rule_lacks_grammar_signal")
    if no_specific_evidence:
        failures.append("no_specific_source_evidence")
    if not evidence_mention_survives:
        warnings.append("specific_evidence_not_mentioned_in_rule_or_rationale")
    if generic_after_mask:
        failures.append("generic_after_target_mask")
    if category_issue:
        failures.append(f"rule_category_mismatch:{category_issue}")
    if target_dependent:
        failures.append("target_dependent_quality_text")
    if rule_text_edit_copy:
        failures.append("rule_text_edit_copy")
    if rationale_edit_copy:
        warnings.append("rationale_edit_copy")

    if score >= 0.75 and not failures:
        label = "pass"
        bucket = "validated"
    elif score >= 0.5 and not any(reason in failures for reason in ["rule_text_edit_copy", "no_specific_source_evidence"]):
        label = "partial"
        bucket = "refine"
    else:
        label = "fail"
        bucket = "rejected"

    return {
        "target_masked_label": label,
        "target_masked_bucket": bucket,
        "target_masked_score": score,
        "target_occurrences_masked": masked_count,
        "target_occurrences_by_field": target_counts,
        "target_in_quality_fields": target_in_quality_fields,
        "target_dependent": target_dependent,
        "masked_rule_has_grammar_signal": grammar_survives,
        "specific_source_evidence_count": evidence_specific_count,
        "specific_evidence_mentioned_after_mask": evidence_mention_survives,
        "generic_after_target_mask": generic_after_mask,
        "rule_category_issue": category_issue,
        "field_leakage": field_leakage,
        "failures": failures,
        "warnings": warnings,
    }


def enrich_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        enriched = dict(row)
        enriched["rulefaith_target_masked_validation"] = validate_row(row)
        output.append(enriched)
    return output


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    buckets = Counter(row["rulefaith_target_masked_validation"]["target_masked_bucket"] for row in rows)
    labels = Counter(row["rulefaith_target_masked_validation"]["target_masked_label"] for row in rows)
    failures = Counter(reason for row in rows for reason in row["rulefaith_target_masked_validation"]["failures"])
    warnings = Counter(reason for row in rows for reason in row["rulefaith_target_masked_validation"]["warnings"])
    previous = Counter((row.get("rulefaith_field_aware_selection") or {}).get("bucket", "unknown") for row in rows)
    by_previous: dict[str, dict[str, int]] = {}
    for previous_bucket in sorted(previous):
        group = [row for row in rows if (row.get("rulefaith_field_aware_selection") or {}).get("bucket", "unknown") == previous_bucket]
        by_previous[previous_bucket] = dict(
            sorted(Counter(row["rulefaith_target_masked_validation"]["target_masked_bucket"] for row in group).items())
        )
    by_dataset: dict[str, dict[str, int]] = {}
    for dataset in sorted({str(row.get("dataset", "")) for row in rows}):
        group = [row for row in rows if str(row.get("dataset", "")) == dataset]
        by_dataset[dataset] = dict(
            sorted(Counter(row["rulefaith_target_masked_validation"]["target_masked_bucket"] for row in group).items())
        )
    by_model: dict[str, dict[str, int]] = {}
    for model in sorted({str(row.get("model_key", "")) for row in rows}):
        group = [row for row in rows if str(row.get("model_key", "")) == model]
        by_model[model] = dict(
            sorted(Counter(row["rulefaith_target_masked_validation"]["target_masked_bucket"] for row in group).items())
        )
    scores = [row["rulefaith_target_masked_validation"]["target_masked_score"] for row in rows]
    return {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "candidate_count": len(rows),
        "field_aware_input_bucket_counts": dict(sorted(previous.items())),
        "target_masked_bucket_counts": dict(sorted(buckets.items())),
        "target_masked_label_counts": dict(sorted(labels.items())),
        "target_masked_bucket_rates": {key: round(value / len(rows), 4) if rows else 0.0 for key, value in sorted(buckets.items())},
        "score_mean": round(sum(scores) / len(scores), 4) if scores else 0.0,
        "score_min": min(scores) if scores else 0.0,
        "score_max": max(scores) if scores else 0.0,
        "failure_counts": dict(sorted(failures.items())),
        "warning_counts": dict(sorted(warnings.items())),
        "by_previous_field_aware_bucket": by_previous,
        "by_dataset": by_dataset,
        "by_model_key": by_model,
        "decision": "use_target_masked_validated_bucket_for_manual_or_stronger_validation_only",
        "policy": {
            "validated": "masked quality score >= 0.75 with grammar signal, specific source evidence, no genericness, no target-dependence, and no rule/rationale edit-copy hard failure",
            "refine": "target-masked quality is partial or has non-hard warnings such as rationale edit-copy",
            "rejected": "target-masked quality fails because rule/evidence/genericness/target-dependence hard risks remain",
        },
    }


def write_csv(path: Path, rows: list[dict[str, Any]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "candidate_id",
        "field_aware_bucket",
        "target_masked_bucket",
        "target_masked_label",
        "target_masked_score",
        "failures",
        "warnings",
        "dataset",
        "model_key",
        "operation",
        "error_type",
        "error_category",
        "target_text",
        "target_in_quality_fields",
        "masked_rule_has_grammar_signal",
        "specific_source_evidence_count",
        "specific_evidence_mentioned_after_mask",
        "generic_after_target_mask",
        "target_dependent",
        "rule_category_issue",
        "rule_text",
        "rationale",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            validation = row["rulefaith_target_masked_validation"]
            edit = row.get("model_edit") or {}
            parsed = row.get("parsed_output") or {}
            writer.writerow(
                {
                    "candidate_id": row["candidate_id"],
                    "field_aware_bucket": (row.get("rulefaith_field_aware_selection") or {}).get("bucket", ""),
                    "target_masked_bucket": validation["target_masked_bucket"],
                    "target_masked_label": validation["target_masked_label"],
                    "target_masked_score": validation["target_masked_score"],
                    "failures": ";".join(validation["failures"]),
                    "warnings": ";".join(validation["warnings"]),
                    "dataset": row.get("dataset", ""),
                    "model_key": row.get("model_key", ""),
                    "operation": edit.get("operation", ""),
                    "error_type": edit.get("error_type", ""),
                    "error_category": row.get("error_category", ""),
                    "target_text": edit.get("target_text", ""),
                    "target_in_quality_fields": validation["target_in_quality_fields"],
                    "masked_rule_has_grammar_signal": validation["masked_rule_has_grammar_signal"],
                    "specific_source_evidence_count": validation["specific_source_evidence_count"],
                    "specific_evidence_mentioned_after_mask": validation["specific_evidence_mentioned_after_mask"],
                    "generic_after_target_mask": validation["generic_after_target_mask"],
                    "target_dependent": validation["target_dependent"],
                    "rule_category_issue": validation["rule_category_issue"],
                    "rule_text": parsed.get("rule_text", ""),
                    "rationale": parsed.get("rationale", ""),
                }
            )


def markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Qwen3 Target-Masked RuleFaith Validation",
        "",
        "This validation hides the target edit from rule/rationale/applicability-condition text and checks whether grammar and evidence signals survive without relying on direct target copying. It is an automatic diagnostic, not human evaluation.",
        "",
        "## Summary",
        "",
        f"- Input candidates: {summary['candidate_count']}",
        f"- Field-aware input buckets: `{summary['field_aware_input_bucket_counts']}`",
        f"- Target-masked buckets: `{summary['target_masked_bucket_counts']}`",
        f"- Target-masked rates: `{summary['target_masked_bucket_rates']}`",
        f"- Score mean/min/max: `{summary['score_mean']}` / `{summary['score_min']}` / `{summary['score_max']}`",
        "",
        "## Failure Counts",
        "",
    ]
    for key, value in summary["failure_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Warning Counts", ""])
    for key, value in summary["warning_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Breakdown By Previous Bucket", ""])
    for key, value in summary["by_previous_field_aware_bucket"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Validated Examples", ""])
    shown = 0
    for row in rows:
        validation = row["rulefaith_target_masked_validation"]
        if validation["target_masked_bucket"] != "validated":
            continue
        parsed = row.get("parsed_output") or {}
        edit = row.get("model_edit") or {}
        lines.extend(
            [
                f"### {row['candidate_id']}",
                "",
                f"- score: `{validation['target_masked_score']}`",
                f"- source: {row.get('source', '')}",
                f"- edit: `{edit.get('operation', '')}` `{edit.get('source_text', '')}` -> `{edit.get('target_text', '')}`",
                f"- rule: {parsed.get('rule_text', '')}",
                f"- rationale: {parsed.get('rationale', '')[:260]}",
                f"- evidence: `{json.dumps(parsed.get('evidence_spans', []), ensure_ascii=False, sort_keys=True)}`",
                "",
            ]
        )
        shown += 1
        if shown >= 10:
            lines.append("Additional validated candidates are available in the JSONL bucket.")
            break
    lines.extend(["", "## Target-Dependence Examples", ""])
    shown = 0
    for row in rows:
        validation = row["rulefaith_target_masked_validation"]
        if not validation["target_dependent"]:
            continue
        parsed = row.get("parsed_output") or {}
        edit = row.get("model_edit") or {}
        masked_text, _ = mask_target(quality_text(parsed), edit.get("target_text", ""))
        lines.extend(
            [
                f"- `{row['candidate_id']}` score=`{validation['target_masked_score']}` failures=`{';'.join(validation['failures'])}`",
                f"  - target: `{edit.get('target_text', '')}`",
                f"  - masked quality text: {masked_text[:260]}",
            ]
        )
        shown += 1
        if shown >= 15:
            break
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- This diagnostic checks target-copy dependence heuristically; it does not prove human rule correctness.",
            "- Validated candidates remain automatic pseudo-labels and must not be used as final SFT positives without stronger validation.",
            "- Empty-target delete edits are not target-mask stress tests because there is no target string to hide.",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run target-masked validation over field-aware Qwen3 RuleFaith buckets.")
    parser.add_argument("--inputs", type=Path, nargs="*", default=DEFAULT_INPUTS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--stats-output", type=Path, default=DEFAULT_STATS)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--csv-output", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in args.inputs:
        for row in read_jsonl(resolve(path)):
            candidate_id = row.get("candidate_id")
            if not candidate_id:
                raise ValueError(f"Missing candidate_id in {path}")
            if candidate_id in seen:
                raise ValueError(f"Duplicate candidate_id across inputs: {candidate_id}")
            seen.add(candidate_id)
            rows.append(row)
    enriched = enrich_rows(rows)
    buckets: dict[str, list[dict[str, Any]]] = {"validated": [], "refine": [], "rejected": []}
    for row in enriched:
        buckets[row["rulefaith_target_masked_validation"]["target_masked_bucket"]].append(row)
    output_dir = resolve(args.output_dir)
    for bucket, bucket_rows in buckets.items():
        write_jsonl(output_dir / f"{args.prefix}_{bucket}.jsonl", bucket_rows, args.overwrite)
    summary = summarize(enriched)
    write_json(resolve(args.stats_output), summary, args.overwrite)
    write_text(resolve(args.report_output), markdown(summary, enriched), args.overwrite)
    write_csv(resolve(args.csv_output), enriched, args.overwrite)
    print(json.dumps({"bucket_counts": summary["target_masked_bucket_counts"], "decision": summary["decision"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
