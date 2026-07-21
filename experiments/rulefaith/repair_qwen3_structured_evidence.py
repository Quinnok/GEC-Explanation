from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.rulefaith import build_qwen3_manual_audit as audit


DEFAULT_INPUT = ROOT / "data" / "rulefaith" / "teacher_candidates_qwen3_8b_canonicalized.jsonl"
DEFAULT_EDIT_POOL = ROOT / "data" / "rulefaith" / "edit_pool.jsonl"
DEFAULT_OUTPUT = ROOT / "results" / "rulefaith" / "qwen3_structured_evidence_repaired_candidates.jsonl"
DEFAULT_STATS = ROOT / "results" / "rulefaith" / "qwen3_structured_evidence_repair_stats.json"
DEFAULT_REPORT = ROOT / "results" / "rulefaith" / "qwen3_structured_evidence_repair_report.md"
DEFAULT_BEFORE_AFTER = ROOT / "results" / "rulefaith" / "qwen3_structured_evidence_repair_before_after.csv"
DEFAULT_SELECTION_DIR = ROOT / "data" / "rulefaith" / "filtering"

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "being",
    "but",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "were",
    "with",
}

SPECIFIC_EVIDENCE_ROLES = {
    "grammatical_subject",
    "subject",
    "head_noun",
    "noun",
    "preposition_governor",
    "preposition_complement",
    "governor",
    "complement",
    "pronoun_antecedent_context",
    "antecedent",
    "noun_number_context",
    "countability_context",
    "time_expression",
}
GENERIC_EVIDENCE_ROLE_WORDS = {"source", "target", "original", "error", "error_span", "left_context", "right_context", "modified_token"}
SPECIFIC_EVIDENCE_ROLE_WORDS = {"subject", "head", "noun", "governor", "complement", "antecedent", "count", "time"}


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


def token_is_content(token: str) -> bool:
    normalized = audit.normalize(token)
    if not normalized or normalized in STOPWORDS:
        return False
    return any(char.isalnum() for char in normalized)


def span(tokens: list[str], start: int, end: int, role: str, source: str = "structured_heuristic") -> dict[str, Any]:
    return {"text": " ".join(tokens[start:end]), "start": start, "end": end, "role": role, "source": source}


def prev_content_indices(tokens: list[str], start: int, window: int) -> list[int]:
    return [idx for idx in range(max(0, start - window), start) if token_is_content(tokens[idx])][::-1]


def next_content_indices(tokens: list[str], end: int, window: int) -> list[int]:
    return [idx for idx in range(end, min(len(tokens), end + window)) if token_is_content(tokens[idx])]


def add_if_valid(spans: list[dict[str, Any]], tokens: list[str], idx: int, role: str) -> None:
    if 0 <= idx < len(tokens):
        spans.append(span(tokens, idx, idx + 1, role))


def valid_existing_spans(record: dict[str, Any]) -> list[dict[str, Any]]:
    parsed = record.get("parsed_output") or {}
    edit = record.get("model_edit") or {}
    source = str(record.get("source", ""))
    prediction = str(record.get("model_prediction", ""))
    tokens = source.split()
    spans = parsed.get("evidence_spans", []) if isinstance(parsed, dict) else []
    if not isinstance(spans, list):
        return []
    kept: list[dict[str, Any]] = []
    for item in spans:
        if not isinstance(item, dict):
            continue
        try:
            start = int(item.get("start", -1))
            end = int(item.get("end", -1))
        except (TypeError, ValueError):
            continue
        text = str(item.get("text", "")).strip()
        role = str(item.get("role", "context")).strip() or "context"
        if not (0 <= start <= end <= len(tokens)):
            continue
        if audit.normalize(" ".join(tokens[start:end])) != audit.normalize(text):
            continue
        checks = audit.evidence_checks(source, prediction, edit, [{"text": text, "start": start, "end": end, "role": role}])
        if checks["evidence_text_found_in_prediction_only"]:
            continue
        kept.append({"text": " ".join(tokens[start:end]), "start": start, "end": end, "role": role, "source": "kept_existing"})
    return kept


def inferred_spans(record: dict[str, Any], window: int) -> tuple[list[dict[str, Any]], Counter[str]]:
    source = str(record.get("source", ""))
    tokens = source.split()
    edit = record.get("model_edit") or {}
    error_type = audit.normalize(edit.get("error_type", ""))
    operation = audit.normalize(edit.get("operation", ""))
    try:
        start = int(edit.get("start", 0))
        end = int(edit.get("end", start))
    except (TypeError, ValueError):
        start, end = 0, 0
    start = max(0, min(start, len(tokens)))
    end = max(start, min(end, len(tokens)))
    prevs = prev_content_indices(tokens, start, window)
    nexts = next_content_indices(tokens, end, window)
    spans: list[dict[str, Any]] = []
    actions: Counter[str] = Counter()

    if audit.edit_token_can_be_contextual(edit) and operation != "insert" and start < end:
        spans.append(span(tokens, start, end, "modified_token"))
        actions["added_modified_token_evidence"] += 1

    if "sva" in error_type or "subject_verb_agreement" in audit.normalize(record.get("error_category", "")):
        if prevs:
            add_if_valid(spans, tokens, prevs[0], "grammatical_subject")
            actions["added_sva_subject"] += 1
        if start < len(tokens):
            add_if_valid(spans, tokens, start, "finite_verb")
            actions["added_sva_verb"] += 1
    elif "verb" in error_type:
        if prevs:
            add_if_valid(spans, tokens, prevs[0], "verb_context")
            actions["added_verb_left_context"] += 1
        if nexts:
            add_if_valid(spans, tokens, nexts[0], "verb_complement_or_time_context")
            actions["added_verb_right_context"] += 1
    elif "det" in error_type or "article" in audit.normalize(record.get("error_category", "")):
        if nexts:
            add_if_valid(spans, tokens, nexts[0], "head_noun")
            actions["added_determiner_head_noun"] += 1
        elif prevs:
            add_if_valid(spans, tokens, prevs[0], "noun_context")
            actions["added_determiner_left_context"] += 1
    elif "prep" in error_type:
        if prevs:
            add_if_valid(spans, tokens, prevs[0], "preposition_governor")
            actions["added_preposition_governor"] += 1
        if nexts:
            add_if_valid(spans, tokens, nexts[0], "preposition_complement")
            actions["added_preposition_complement"] += 1
    elif "noun" in error_type:
        if prevs:
            add_if_valid(spans, tokens, prevs[0], "noun_number_context")
            actions["added_noun_left_context"] += 1
        if nexts:
            add_if_valid(spans, tokens, nexts[0], "noun_phrase_context")
            actions["added_noun_right_context"] += 1
    elif "pron" in error_type:
        if prevs:
            add_if_valid(spans, tokens, prevs[0], "pronoun_antecedent_context")
            actions["added_pronoun_context"] += 1
    elif "wo" in error_type or "clause" in audit.normalize(record.get("error_category", "")) or "conj" in error_type:
        if prevs:
            add_if_valid(spans, tokens, prevs[0], "left_clause_context")
            actions["added_left_clause_context"] += 1
        if nexts:
            add_if_valid(spans, tokens, nexts[0], "right_clause_context")
            actions["added_right_clause_context"] += 1
    else:
        if prevs:
            add_if_valid(spans, tokens, prevs[0], "left_context")
            actions["added_left_context"] += 1
        if nexts:
            add_if_valid(spans, tokens, nexts[0], "right_context")
            actions["added_right_context"] += 1

    return spans, actions


def dedupe_spans(spans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen: set[tuple[int, int, str]] = set()
    for item in spans:
        key = (int(item["start"]), int(item["end"]), audit.normalize(item.get("role", "")))
        if key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


def has_specific_source_evidence(record: dict[str, Any]) -> bool:
    parsed = record.get("parsed_output") or {}
    edit = record.get("model_edit") or {}
    source = str(record.get("source", ""))
    prediction = str(record.get("model_prediction", ""))
    spans = parsed.get("evidence_spans", []) if isinstance(parsed, dict) else []
    if not isinstance(spans, list):
        return False
    for item in spans:
        if not isinstance(item, dict):
            continue
        role = audit.normalize(item.get("role", ""))
        checks = audit.evidence_checks(source, prediction, edit, [item])
        if not checks["evidence_contextual"]:
            continue
        if role in SPECIFIC_EVIDENCE_ROLES:
            return True
        if role not in GENERIC_EVIDENCE_ROLE_WORDS and any(word in role for word in SPECIFIC_EVIDENCE_ROLE_WORDS):
            return True
        if role == "modified_token" and audit.edit_token_can_be_contextual(edit):
            return True
    return False


def repair_record(record: dict[str, Any], window: int) -> tuple[dict[str, Any], Counter[str]]:
    parsed = dict(record.get("parsed_output") or {})
    before_checks = audit.evidence_checks(
        str(record.get("source", "")),
        str(record.get("model_prediction", "")),
        record.get("model_edit") or {},
        parsed.get("evidence_spans", []),
    )
    kept = valid_existing_spans(record)
    inferred, actions = inferred_spans(record, window)
    repaired_spans = dedupe_spans(kept + inferred)
    if kept:
        actions["kept_existing_valid_source_spans"] += len(kept)
    parsed["evidence_spans"] = repaired_spans
    after_checks = audit.evidence_checks(
        str(record.get("source", "")),
        str(record.get("model_prediction", "")),
        record.get("model_edit") or {},
        repaired_spans,
    )
    output = dict(record)
    output["candidate_id"] = f"{record['candidate_id']}::structured_evidence_repaired"
    output["original_candidate_id"] = record.get("candidate_id")
    output["original_candidate_type"] = record.get("candidate_type")
    output["candidate_type"] = "structured_evidence_repaired"
    output["provider"] = "rulefaith_structured_evidence_repair"
    output["prompt_version"] = "rulefaith_structured_evidence_repair_v1_no_llm"
    output["parsed_output"] = parsed
    output["before_evidence_checks"] = before_checks
    output["after_evidence_checks"] = after_checks
    output["structured_evidence_repair_actions"] = dict(actions)
    output["evidence_contextual_improved"] = bool(not before_checks["evidence_contextual"] and after_checks["evidence_contextual"])
    output["wrong_evidence_fixed"] = bool(before_checks["wrong_evidence_auto"] and not after_checks["wrong_evidence_auto"])
    output["prediction_only_evidence_regressed"] = bool(not before_checks["evidence_text_found_in_prediction_only"] and after_checks["evidence_text_found_in_prediction_only"])
    output["created_at"] = utc_now()
    output["label_source"] = "deterministic_structured_evidence_repair_not_human_gold"
    return output, actions


def annotated_flags(rows: list[dict[str, Any]], edit_pool: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pool_by_id = {row["rulefaith_pool_id"]: row for row in edit_pool}
    return [audit.annotate_row(row, "structured_repair", pool_by_id) for row in rows]


def count_flags(rows: list[dict[str, Any]]) -> dict[str, int]:
    keys = [
        "evidence_contextual",
        "missing_evidence",
        "wrong_evidence_auto",
        "evidence_text_found_in_prediction_only",
        "edit_copy",
        "rule_edit_copy",
        "possible_false_rationalization",
        "unsupported_confidence",
        "alignment_error",
        "validity_error_auto",
    ]
    return {key: sum(1 for row in rows if row.get(key) is True) for key in keys}


def selection_for(row: dict[str, Any], flags: dict[str, Any]) -> tuple[str, list[str]]:
    hard_reasons: list[str] = []
    refine_reasons: list[str] = []
    if row.get("parse_status") != "parsed_json":
        hard_reasons.append("parse_not_json")
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
            hard_reasons.append(key)
    if not has_specific_source_evidence(row):
        hard_reasons.append("no_specific_source_evidence")
    for key in ["edit_copy", "unsupported_confidence", "generic_explanation"]:
        if flags.get(key) is True:
            refine_reasons.append(key)
    if hard_reasons:
        return "rejected", hard_reasons
    if refine_reasons:
        return "refine", refine_reasons
    return "accepted", []


def write_selection_buckets(
    output_dir: Path,
    prefix: str,
    repaired: list[dict[str, Any]],
    after_flags: list[dict[str, Any]],
    overwrite: bool,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    flags_by_id = {row["candidate_id"]: row for row in after_flags}
    buckets: dict[str, list[dict[str, Any]]] = {"accepted": [], "refine": [], "rejected": []}
    reason_counts: Counter[str] = Counter()
    for row in repaired:
        flags = flags_by_id[row["candidate_id"]]
        bucket, reasons = selection_for(row, flags)
        enriched = dict(row)
        enriched["rulefaith_strict_selection"] = {"bucket": bucket, "reasons": reasons}
        buckets[bucket].append(enriched)
        reason_counts.update(reasons)
    for bucket, rows in buckets.items():
        write_jsonl(output_dir / f"{prefix}_{bucket}.jsonl", rows, overwrite)
    total = sum(len(rows) for rows in buckets.values())
    return {
        "bucket_counts": {bucket: len(rows) for bucket, rows in buckets.items()},
        "bucket_rates": {bucket: round(len(rows) / total, 4) if total else 0.0 for bucket, rows in buckets.items()},
        "reason_counts": dict(sorted(reason_counts.items())),
        "policy": {
            "accepted": "parsed JSON, no alignment/validity/rule/evidence hard failures, specific source evidence present, and no edit-copy/unsupported-confidence refine risk",
            "refine": "passes hard gates but has edit-copy, genericness, or unsupported-confidence risk",
            "rejected": "parse, alignment, validity, false-rationalization, rule, wrong-evidence, missing-evidence, or no-specific-evidence hard failure",
        },
    }


def summarize(
    original: list[dict[str, Any]],
    repaired: list[dict[str, Any]],
    before_flags: list[dict[str, Any]],
    after_flags: list[dict[str, Any]],
    action_counts: Counter[str],
    input_path: Path,
    strict_selection: dict[str, Any],
) -> dict[str, Any]:
    improved = sum(1 for row in repaired if row["evidence_contextual_improved"])
    regressed = sum(1 for row in repaired if row["prediction_only_evidence_regressed"])
    fixed_wrong = sum(1 for row in repaired if row["wrong_evidence_fixed"])
    before_counts = count_flags(before_flags)
    after_counts = count_flags(after_flags)
    before_specific = sum(1 for row in original if has_specific_source_evidence(row))
    after_specific = sum(1 for row in repaired if has_specific_source_evidence(row))
    return {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "input": str(input_path),
        "label_source": "deterministic_structured_evidence_repair_not_human_gold",
        "candidate_count": len(original),
        "repaired_count": len(repaired),
        "action_counts": dict(sorted(action_counts.items())),
        "before_flag_counts": before_counts,
        "after_flag_counts": after_counts,
        "delta_flag_counts": {key: after_counts[key] - before_counts[key] for key in before_counts},
        "specific_source_evidence": {
            "before": before_specific,
            "after": after_specific,
            "delta": after_specific - before_specific,
            "after_generic_context_only": after_counts["evidence_contextual"] - after_specific,
        },
        "improvement_counts": {
            "evidence_contextual_improved": improved,
            "wrong_evidence_fixed": fixed_wrong,
            "prediction_only_evidence_regressed": regressed,
        },
        "strict_selection": strict_selection,
        "decision": (
            "keep_structured_evidence_repair_for_refiner_inputs_not_final_scoring"
            if after_counts["evidence_contextual"] > before_counts["evidence_contextual"] and regressed == 0
            else "revise_structured_evidence_repair"
        ),
        "limitations": [
            "This repair adds source-grounded candidate evidence spans but does not prove linguistic rule correctness.",
            "These labels and repairs are automatic and must not be reported as human evaluation.",
            "False-rationalization and invalid-edit risks require a separate edit-validity/rule verifier.",
        ],
    }


def write_before_after(path: Path, before: list[dict[str, Any]], after: list[dict[str, Any]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "candidate_id",
        "before_evidence_contextual",
        "after_evidence_contextual",
        "before_missing_evidence",
        "after_missing_evidence",
        "before_wrong_evidence_auto",
        "after_wrong_evidence_auto",
        "before_prediction_only",
        "after_prediction_only",
        "before_risk_count",
        "after_risk_count",
        "actions",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        import csv

        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for before_row, after_row in zip(before, after):
            actions = after_row.get("structured_evidence_repair_actions", {})
            writer.writerow(
                {
                    "candidate_id": before_row["candidate_id"],
                    "before_evidence_contextual": before_row.get("evidence_contextual"),
                    "after_evidence_contextual": after_row["after_evidence_checks"].get("evidence_contextual"),
                    "before_missing_evidence": before_row.get("missing_evidence"),
                    "after_missing_evidence": after_row["after_evidence_checks"].get("missing_evidence"),
                    "before_wrong_evidence_auto": before_row.get("wrong_evidence_auto"),
                    "after_wrong_evidence_auto": after_row["after_evidence_checks"].get("wrong_evidence_auto"),
                    "before_prediction_only": before_row.get("evidence_text_found_in_prediction_only"),
                    "after_prediction_only": after_row["after_evidence_checks"].get("evidence_text_found_in_prediction_only"),
                    "before_risk_count": before_row.get("risk_count"),
                    "after_risk_count": after_row.get("risk_count", ""),
                    "actions": json.dumps(actions, ensure_ascii=False, sort_keys=True),
                }
            )


def markdown(summary: dict[str, Any], repaired: list[dict[str, Any]]) -> str:
    lines = [
        "# Qwen3 Structured Evidence Repair",
        "",
        "This deterministic repair pass adds source-grounded evidence spans inferred from the edit, error type, and nearby source context. It uses no reference correction, no behavior label for generation, and no human label.",
        "",
        "## Summary",
        "",
        f"- Candidate count: {summary['candidate_count']}",
        f"- Decision: `{summary['decision']}`",
        f"- Label source: `{summary['label_source']}`",
        "",
        "## Before / After Flag Counts",
        "",
        "| Flag | Before | After | Delta |",
        "|---|---:|---:|---:|",
    ]
    for key, before_value in summary["before_flag_counts"].items():
        after_value = summary["after_flag_counts"][key]
        delta = summary["delta_flag_counts"][key]
        lines.append(f"| `{key}` | {before_value} | {after_value} | {delta:+d} |")
    lines.extend(["", "## Repair Actions", ""])
    for key, value in summary["action_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Stricter Evidence Check", ""])
    strict = summary["specific_source_evidence"]
    lines.extend(
        [
            f"- `specific_source_evidence_before`: {strict['before']}",
            f"- `specific_source_evidence_after`: {strict['after']}",
            f"- `specific_source_evidence_delta`: {strict['delta']:+d}",
            f"- `after_generic_context_only`: {strict['after_generic_context_only']}",
            "",
            "The stricter count excludes generic left/right context roles. It is the safer number to use when deciding whether a repaired candidate is suitable for a later human audit or positive-data construction.",
        ]
    )
    lines.extend(["", "## Strict RuleFaith Selection", ""])
    selection = summary["strict_selection"]
    lines.append(f"- bucket counts: `{selection['bucket_counts']}`")
    lines.append(f"- reason counts: `{selection['reason_counts']}`")
    lines.extend(["", "This stricter gate is intentionally more conservative than `filter_teacher_candidates.py`: it treats false rationalization, validity errors, alignment errors, and lack of specific source evidence as hard failures. Edit-copy and unsupported-confidence risks are routed to `refine`, not direct `accepted`.", ""])
    lines.extend(["", "## Examples With Improved Contextual Evidence", ""])
    shown = 0
    for row in repaired:
        if not row.get("evidence_contextual_improved"):
            continue
        parsed = row.get("parsed_output") or {}
        lines.extend(
            [
                f"### {row['candidate_id']}",
                "",
                f"- source: {row.get('source', '')}",
                f"- edit: `{row.get('model_edit', {}).get('operation', '')}` `{row.get('model_edit', {}).get('source_text', '')}` -> `{row.get('model_edit', {}).get('target_text', '')}`",
                f"- error type: `{row.get('model_edit', {}).get('error_type', '')}`",
                f"- evidence: `{json.dumps(parsed.get('evidence_spans', []), ensure_ascii=False, sort_keys=True)}`",
                f"- actions: `{row.get('structured_evidence_repair_actions', {})}`",
                "",
            ]
        )
        shown += 1
        if shown >= 20:
            lines.append("Additional improved cases are available in the JSONL output.")
            break
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- Automatic source evidence repair does not prove the rule is linguistically correct.",
            "- The repaired candidates remain pseudo-labelled artifacts, not human-gold data.",
            "- Edit-validity and false-rationalization risks require a separate verifier.",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repair missing Qwen3 evidence spans with deterministic source-context heuristics.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--edit-pool", type=Path, default=DEFAULT_EDIT_POOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stats-output", type=Path, default=DEFAULT_STATS)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--before-after-output", type=Path, default=DEFAULT_BEFORE_AFTER)
    parser.add_argument("--selection-output-dir", type=Path, default=DEFAULT_SELECTION_DIR)
    parser.add_argument("--selection-prefix", default="qwen3_structured_rulefaith")
    parser.add_argument("--window", type=int, default=6)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = resolve(args.input)
    original = read_jsonl(input_path)
    edit_pool = read_jsonl(resolve(args.edit_pool))
    before_flags = annotated_flags(original, edit_pool)
    repaired: list[dict[str, Any]] = []
    action_counts: Counter[str] = Counter()
    for record in original:
        repaired_row, actions = repair_record(record, args.window)
        action_counts.update(actions)
        repaired.append(repaired_row)
    after_flags = annotated_flags(repaired, edit_pool)
    after_by_id = {row["candidate_id"]: row for row in after_flags}
    enriched_repaired: list[dict[str, Any]] = []
    for row in repaired:
        flags = after_by_id[row["candidate_id"]]
        enriched = dict(row)
        enriched["risk_count"] = flags.get("risk_count")
        enriched["risk_reasons"] = flags.get("risk_reasons")
        enriched_repaired.append(enriched)
    strict_selection = write_selection_buckets(
        resolve(args.selection_output_dir),
        args.selection_prefix,
        enriched_repaired,
        after_flags,
        args.overwrite,
    )
    summary = summarize(original, enriched_repaired, before_flags, after_flags, action_counts, input_path, strict_selection)
    write_jsonl(resolve(args.output), enriched_repaired, args.overwrite)
    write_json(resolve(args.stats_output), summary, args.overwrite)
    write_before_after(resolve(args.before_after_output), before_flags, enriched_repaired, args.overwrite)
    write_text(resolve(args.report_output), markdown(summary, enriched_repaired), args.overwrite)
    print(json.dumps({"decision": summary["decision"], "before": summary["before_flag_counts"], "after": summary["after_flag_counts"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
