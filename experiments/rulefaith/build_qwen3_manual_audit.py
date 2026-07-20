from __future__ import annotations

import argparse
import csv
import json
import random
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]

DEFAULT_BUCKETS = {
    "accepted": ROOT / "data" / "rulefaith" / "filtering" / "qwen3_8b_accepted.jsonl",
    "refine": ROOT / "data" / "rulefaith" / "filtering" / "qwen3_8b_refine.jsonl",
    "rejected": ROOT / "data" / "rulefaith" / "filtering" / "qwen3_8b_rejected.jsonl",
}
DEFAULT_EDIT_POOL = ROOT / "data" / "rulefaith" / "edit_pool.jsonl"
DEFAULT_CSV = ROOT / "results" / "rulefaith" / "qwen3_manual_audit.csv"
DEFAULT_SUMMARY = ROOT / "results" / "rulefaith" / "qwen3_manual_audit_summary.json"
DEFAULT_CASES = ROOT / "results" / "rulefaith" / "qwen3_manual_audit_cases.md"

FORBIDDEN_GENERATOR_FIELDS = {"reference", "behavior", "model_behavior", "human_label", "final_label", "gold_label"}
GENERIC_EVIDENCE_ROLES = {"", "source", "target", "source_text", "target_text", "original", "modified", "edit"}
GENERIC_PHRASES = [
    "grammar issue",
    "grammar problem",
    "grammatical error",
    "should be improved",
    "more natural",
    "more appropriate",
    "make the sentence correct",
    "makes the sentence grammatically correct",
]
GRAMMAR_KEYWORDS = {
    "agreement",
    "article",
    "auxiliary",
    "capitalization",
    "clause",
    "collocation",
    "comma",
    "count",
    "countable",
    "determiner",
    "gerund",
    "infinitive",
    "morphology",
    "noun",
    "plural",
    "possessive",
    "preposition",
    "pronoun",
    "punctuation",
    "singular",
    "spelling",
    "subject",
    "tense",
    "verb",
    "word order",
}
INVALID_EDIT_BEHAVIORS = {"wrong_correction", "overcorrection"}
VALIDITY_CAVEATS = {
    "invalid",
    "not valid",
    "ungrammatical",
    "incorrect",
    "wrong",
    "unnecessary",
    "optional",
    "stylistic",
    "may not",
    "might not",
    "uncertain",
    "acceptable alternative",
}

CSV_FIELDS = [
    "candidate_id",
    "bucket",
    "selected_for_manual_audit",
    "audit_priority",
    "dataset",
    "sample_id",
    "model_key",
    "model_family",
    "behavior",
    "operation",
    "error_type",
    "error_category",
    "candidate_type",
    "rulefaith_split",
    "source",
    "model_prediction",
    "edit_start",
    "edit_end",
    "source_text",
    "target_text",
    "edit_description",
    "edit_validity",
    "rule_text",
    "evidence_spans_json",
    "rationale",
    "confidence",
    "abstain",
    "abstain_reason",
    "generator_input_fields",
    "leakage_input_violation",
    "source_span_match",
    "target_present_in_prediction",
    "evidence_span_index_match",
    "evidence_text_found_in_source",
    "evidence_contextual",
    "missing_evidence",
    "wrong_evidence_auto",
    "missing_rule",
    "rule_edit_copy",
    "target_copy",
    "edit_copy",
    "generic_explanation",
    "possible_false_rationalization",
    "unsupported_confidence",
    "alignment_error",
    "validity_error_auto",
    "semantic_distortion_auto",
    "risk_count",
    "risk_reasons",
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
    "human_notes",
    "human_decision",
]


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
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Bad JSON in {path}:{lineno}: {exc}") from exc
    if not rows:
        raise ValueError(f"Input file is empty: {path}")
    return rows


def write_json(path: Path, obj: Any, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: Iterable[dict[str, Any]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in CSV_FIELDS})


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def normalize(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def content_tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", normalize(text))


def text_contains(text: str, needle: Any) -> bool:
    needle_norm = normalize(needle)
    if not needle_norm:
        return True
    return needle_norm in normalize(text)


def compact_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


def model_edit(row: dict[str, Any]) -> dict[str, Any]:
    edit = row.get("model_edit") or row.get("predicted_edit") or {}
    if not isinstance(edit, dict):
        raise ValueError(f"Malformed model_edit in {row.get('candidate_id')}")
    return edit


def source_span_match(source: str, edit: dict[str, Any]) -> bool:
    operation = normalize(edit.get("operation", ""))
    source_text = normalize(edit.get("source_text", ""))
    start = edit.get("start")
    end = edit.get("end")
    if operation == "insert":
        return source_text == ""
    if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end < start:
        return False
    tokens = source.split()
    if end > len(tokens):
        return False
    return normalize(" ".join(tokens[start:end])) == source_text


def target_present_in_prediction(prediction: str, edit: dict[str, Any]) -> bool:
    operation = normalize(edit.get("operation", ""))
    target_text = normalize(edit.get("target_text", ""))
    if operation == "delete" or not target_text:
        return True
    return target_text in normalize(prediction)


def evidence_checks(source: str, edit: dict[str, Any], spans: Any) -> dict[str, Any]:
    if not isinstance(spans, list) or not spans:
        return {
            "evidence_span_index_match": False,
            "evidence_text_found_in_source": False,
            "evidence_contextual": False,
            "missing_evidence": True,
            "wrong_evidence_auto": False,
        }

    source_norm = normalize(source)
    source_tokens = source.split()
    edit_source = normalize(edit.get("source_text", ""))
    edit_target = normalize(edit.get("target_text", ""))
    any_index_match = False
    any_text_found = False
    any_contextual = False
    any_wrong_explicit = False

    for span in spans:
        if not isinstance(span, dict):
            any_wrong_explicit = True
            continue
        text = normalize(span.get("text", ""))
        role = normalize(span.get("role", ""))
        start = span.get("start")
        end = span.get("end")
        if text and text in source_norm:
            any_text_found = True
        if isinstance(start, int) and isinstance(end, int) and 0 <= start <= end <= len(source_tokens):
            indexed_text = normalize(" ".join(source_tokens[start:end]))
            if text and indexed_text == text:
                any_index_match = True
        if text and role not in GENERIC_EVIDENCE_ROLES and text not in {edit_source, edit_target}:
            any_contextual = True
        if text and text not in source_norm and not any(token in source_norm for token in content_tokens(text)):
            any_wrong_explicit = True

    return {
        "evidence_span_index_match": any_index_match,
        "evidence_text_found_in_source": any_text_found,
        "evidence_contextual": any_contextual,
        "missing_evidence": not any_contextual,
        "wrong_evidence_auto": any_wrong_explicit or (not any_index_match and any_text_found),
    }


def missing_rule(rule_text: Any) -> bool:
    return normalize(rule_text) in {"", "none", "null", "n/a", "na", "not applicable"}


def rule_edit_copy(rule_text: Any, edit: dict[str, Any]) -> bool:
    rule = normalize(rule_text)
    if missing_rule(rule):
        return False
    has_edit_verb = any(word in rule for word in ["replace", "insert", "delete", "change", "remove"])
    has_grammar_keyword = any(keyword in rule for keyword in GRAMMAR_KEYWORDS)
    mentions_source = bool(normalize(edit.get("source_text", ""))) and text_contains(rule, edit.get("source_text", ""))
    mentions_target = bool(normalize(edit.get("target_text", ""))) and text_contains(rule, edit.get("target_text", ""))
    return has_edit_verb and (mentions_source or mentions_target) and not has_grammar_keyword


def diagnostic_text(parsed: dict[str, Any]) -> str:
    evidence = parsed.get("evidence_spans", [])
    evidence_text = ""
    if isinstance(evidence, list):
        evidence_text = " ".join(str(span.get("text", "")) for span in evidence if isinstance(span, dict))
    return " ".join(
        [
            str(parsed.get("edit_description", "")),
            str(parsed.get("rule_text", "")),
            str(parsed.get("rationale", "")),
            evidence_text,
        ]
    )


def target_copy(parsed: dict[str, Any], edit: dict[str, Any]) -> bool:
    target = normalize(edit.get("target_text", ""))
    if not target:
        return False
    return target in normalize(diagnostic_text(parsed))


def edit_copy(parsed: dict[str, Any], edit: dict[str, Any]) -> bool:
    text = normalize(diagnostic_text(parsed))
    source = normalize(edit.get("source_text", ""))
    target = normalize(edit.get("target_text", ""))
    operation = normalize(edit.get("operation", ""))
    operation_mentioned = operation in text or any(word in text for word in ["replace", "insert", "delete", "change", "remove"])
    source_mentioned = not source or source in text
    target_mentioned = operation == "delete" or not target or target in text
    return operation_mentioned and source_mentioned and target_mentioned


def generic_explanation(parsed: dict[str, Any]) -> bool:
    text = normalize(" ".join([str(parsed.get("rule_text", "")), str(parsed.get("rationale", ""))]))
    if not text:
        return True
    phrase_hit = any(phrase in text for phrase in GENERIC_PHRASES)
    has_keyword = any(keyword in text for keyword in GRAMMAR_KEYWORDS)
    return phrase_hit and not has_keyword


def possible_false_rationalization(parsed: dict[str, Any], behavior: str) -> bool:
    if behavior not in INVALID_EDIT_BEHAVIORS:
        return False
    validity = normalize(parsed.get("edit_validity", ""))
    text = normalize(" ".join([str(parsed.get("rule_text", "")), str(parsed.get("rationale", ""))]))
    caveat_present = any(caveat in text or caveat in validity for caveat in VALIDITY_CAVEATS)
    return validity == "valid" and not caveat_present


def alignment_error(row: dict[str, Any], parsed: dict[str, Any], edit: dict[str, Any]) -> bool:
    prefilter = row.get("rulefaith_prefilter") or {}
    if prefilter.get("alignment_proxy_pass") is False:
        return True
    text = diagnostic_text(parsed)
    operation = normalize(edit.get("operation", ""))
    source = normalize(edit.get("source_text", ""))
    target = normalize(edit.get("target_text", ""))
    if operation and operation not in normalize(text) and operation not in {"replace"}:
        return True
    if source and source not in normalize(text):
        return True
    if operation != "delete" and target and target not in normalize(text):
        return True
    return False


def leakage_input_violation(row: dict[str, Any]) -> bool:
    fields = {normalize(field) for field in row.get("generator_input_fields", []) if isinstance(field, str)}
    forbidden_field_used = bool(fields & FORBIDDEN_GENERATOR_FIELDS)
    explicit_flags = any(
        bool(row.get(flag))
        for flag in [
            "uses_reference_in_generator",
            "uses_behavior_label_in_generator",
            "uses_human_label_in_generator",
            "uses_gold_edit_in_generator",
        ]
    )
    return forbidden_field_used or explicit_flags


def annotate_row(row: dict[str, Any], bucket: str, pool_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    pool_row = pool_by_id.get(row.get("rulefaith_pool_id"), {})
    edit = model_edit(row)
    parsed = row.get("parsed_output") or {}
    if not isinstance(parsed, dict):
        parsed = {}
    evidence = evidence_checks(row.get("source", ""), edit, parsed.get("evidence_spans", []))
    missing_rule_flag = missing_rule(parsed.get("rule_text", ""))
    rule_copy_flag = rule_edit_copy(parsed.get("rule_text", ""), edit)
    target_copy_flag = target_copy(parsed, edit)
    edit_copy_flag = edit_copy(parsed, edit)
    generic_flag = generic_explanation(parsed)
    behavior = str(pool_row.get("behavior") or row.get("behavior") or "")
    false_rationalization_flag = possible_false_rationalization(parsed, behavior)
    source_span_ok = source_span_match(row.get("source", ""), edit)
    target_in_prediction = target_present_in_prediction(row.get("model_prediction", ""), edit)
    alignment_flag = alignment_error(row, parsed, edit) or not source_span_ok or not target_in_prediction
    validity_error = normalize(parsed.get("edit_validity", "")) == "valid" and behavior in INVALID_EDIT_BEHAVIORS
    semantic_distortion = validity_error or false_rationalization_flag
    unsupported_conf = float(parsed.get("confidence") or 0.0) >= 0.9 and (
        alignment_flag
        or missing_rule_flag
        or evidence["missing_evidence"]
        or evidence["wrong_evidence_auto"]
        or false_rationalization_flag
    )

    flags = {
        "leakage_input_violation": leakage_input_violation(row),
        "source_span_match": source_span_ok,
        "target_present_in_prediction": target_in_prediction,
        **evidence,
        "missing_rule": missing_rule_flag,
        "rule_edit_copy": rule_copy_flag,
        "target_copy": target_copy_flag,
        "edit_copy": edit_copy_flag,
        "generic_explanation": generic_flag,
        "possible_false_rationalization": false_rationalization_flag,
        "unsupported_confidence": unsupported_conf,
        "alignment_error": alignment_flag,
        "validity_error_auto": validity_error,
        "semantic_distortion_auto": semantic_distortion,
    }
    risk_reasons: list[str] = []
    if flags["leakage_input_violation"]:
        risk_reasons.append("leakage_input_violation")
    if not flags["source_span_match"]:
        risk_reasons.append("source_span_mismatch")
    if not flags["target_present_in_prediction"]:
        risk_reasons.append("target_missing_from_prediction")
    if not flags["evidence_span_index_match"]:
        risk_reasons.append("evidence_span_index_mismatch")
    if not flags["evidence_text_found_in_source"]:
        risk_reasons.append("evidence_text_not_found_in_source")
    for flag_name in [
        "missing_evidence",
        "wrong_evidence_auto",
        "missing_rule",
        "rule_edit_copy",
        "target_copy",
        "edit_copy",
        "generic_explanation",
        "possible_false_rationalization",
        "unsupported_confidence",
        "alignment_error",
        "validity_error_auto",
        "semantic_distortion_auto",
    ]:
        if flags[flag_name]:
            risk_reasons.append(flag_name)

    audit_row = {
        "candidate_id": row.get("candidate_id", ""),
        "bucket": bucket,
        "selected_for_manual_audit": False,
        "audit_priority": "",
        "dataset": row.get("dataset", ""),
        "sample_id": row.get("sample_id", ""),
        "model_key": row.get("model_key", ""),
        "model_family": row.get("model_family", ""),
        "behavior": behavior,
        "operation": edit.get("operation", ""),
        "error_type": edit.get("error_type", row.get("error_type", "")),
        "error_category": row.get("error_category", pool_row.get("error_category", "")),
        "candidate_type": row.get("candidate_type", ""),
        "rulefaith_split": row.get("rulefaith_split", pool_row.get("rulefaith_split", "")),
        "source": row.get("source", ""),
        "model_prediction": row.get("model_prediction", ""),
        "edit_start": edit.get("start", ""),
        "edit_end": edit.get("end", ""),
        "source_text": edit.get("source_text", ""),
        "target_text": edit.get("target_text", ""),
        "edit_description": parsed.get("edit_description", ""),
        "edit_validity": parsed.get("edit_validity", ""),
        "rule_text": parsed.get("rule_text", ""),
        "evidence_spans_json": compact_json(parsed.get("evidence_spans", [])),
        "rationale": parsed.get("rationale", ""),
        "confidence": parsed.get("confidence", ""),
        "abstain": parsed.get("abstain", ""),
        "abstain_reason": parsed.get("abstain_reason", ""),
        "generator_input_fields": compact_json(row.get("generator_input_fields", [])),
        "risk_count": len(risk_reasons),
        "risk_reasons": ";".join(risk_reasons),
        **flags,
        "human_alignment_error": "",
        "human_validity_error": "",
        "human_wrong_rule": "",
        "human_inapplicable_rule": "",
        "human_missing_evidence": "",
        "human_wrong_evidence": "",
        "human_generic_explanation": "",
        "human_edit_copy": "",
        "human_semantic_distortion": "",
        "human_unsupported_confidence": "",
        "human_notes": "",
        "human_decision": "",
    }
    return audit_row


def select_manual_rows(rows: list[dict[str, Any]], target_size: int, seed: int) -> None:
    rng = random.Random(seed)
    by_key: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    dimensions = ["bucket", "dataset", "model_key", "behavior", "operation"]
    for row in rows:
        for dim in dimensions:
            by_key[(dim, str(row.get(dim, "")))].append(row)

    selected: set[str] = set()

    def add(row: dict[str, Any], priority: str) -> None:
        cid = str(row["candidate_id"])
        if cid not in selected:
            selected.add(cid)
            row["selected_for_manual_audit"] = True
            row["audit_priority"] = priority

    # First cover required strata.
    for key, group in sorted(by_key.items()):
        if not group:
            continue
        group_sorted = sorted(group, key=lambda item: (-int(item["risk_count"]), str(item["candidate_id"])))
        add(group_sorted[0], f"stratum:{key[0]}={key[1]}")

    # Then prioritize risky accepted/refine rows and a rejected sanity subset.
    risky = sorted(rows, key=lambda item: (-int(item["risk_count"]), item["bucket"] != "accepted", str(item["candidate_id"])))
    for row in risky:
        if len(selected) >= target_size:
            break
        add(row, "risk")

    if len(selected) < target_size:
        remaining = [row for row in rows if row["candidate_id"] not in selected]
        rng.shuffle(remaining)
        for row in remaining[: target_size - len(selected)]:
            add(row, "random_fill")


def summarize(rows: list[dict[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    bool_flags = [
        "leakage_input_violation",
        "source_span_match",
        "target_present_in_prediction",
        "evidence_span_index_match",
        "evidence_text_found_in_source",
        "evidence_contextual",
        "missing_evidence",
        "wrong_evidence_auto",
        "missing_rule",
        "rule_edit_copy",
        "target_copy",
        "edit_copy",
        "generic_explanation",
        "possible_false_rationalization",
        "unsupported_confidence",
        "alignment_error",
        "validity_error_auto",
        "semantic_distortion_auto",
    ]
    selected = [row for row in rows if row["selected_for_manual_audit"]]
    bucket_counts = Counter(row["bucket"] for row in rows)
    selected_bucket_counts = Counter(row["bucket"] for row in selected)
    flag_counts = {flag: sum(1 for row in rows if row.get(flag) is True) for flag in bool_flags}
    selected_flag_counts = {flag: sum(1 for row in selected if row.get(flag) is True) for flag in bool_flags}

    strata = {
        "dataset": sorted(set(row["dataset"] for row in selected)),
        "model_key": sorted(set(row["model_key"] for row in selected)),
        "behavior": sorted(set(row["behavior"] for row in selected)),
        "operation": sorted(set(row["operation"] for row in selected)),
        "bucket": sorted(set(row["bucket"] for row in selected)),
    }
    hard_failures = {
        "input_leakage_detected": flag_counts["leakage_input_violation"] > 0,
        "source_span_mismatches": len(rows) - flag_counts["source_span_match"],
        "target_prediction_mismatches": len(rows) - flag_counts["target_present_in_prediction"],
        "evidence_index_mismatch_count": len(rows) - flag_counts["evidence_span_index_match"],
        "possible_false_rationalization_count": flag_counts["possible_false_rationalization"],
    }
    if hard_failures["input_leakage_detected"]:
        decision = "revise_teacher_inputs_before_refinement"
    elif flag_counts["evidence_span_index_match"] < len(rows) * 0.5 or flag_counts["missing_evidence"] > len(rows) * 0.4:
        decision = "fix_evidence_verifier_and_evidence_prompt_before_targeted_refinement"
    elif flag_counts["possible_false_rationalization"] > 0:
        decision = "add_edit_validity_gate_before_targeted_refinement"
    else:
        decision = "can_enter_targeted_refinement_with_manual_spot_check"

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "input_files": {
            "accepted": str(resolve(args.accepted)),
            "refine": str(resolve(args.refine)),
            "rejected": str(resolve(args.rejected)),
            "edit_pool": str(resolve(args.edit_pool)),
        },
        "candidate_count": len(rows),
        "manual_audit_target_size": args.manual_sample_size,
        "selected_manual_audit_count": len(selected),
        "bucket_counts": dict(bucket_counts),
        "selected_bucket_counts": dict(selected_bucket_counts),
        "dataset_counts": dict(Counter(row["dataset"] for row in rows)),
        "model_key_counts": dict(Counter(row["model_key"] for row in rows)),
        "behavior_counts": dict(Counter(row["behavior"] for row in rows)),
        "operation_counts": dict(Counter(row["operation"] for row in rows)),
        "flag_counts": flag_counts,
        "selected_flag_counts": selected_flag_counts,
        "selected_coverage": strata,
        "hard_failures": hard_failures,
        "decision": decision,
        "interpretation": (
            "This is an automatic pre-audit for Qwen3-8B teacher candidates. "
            "Rows marked for manual audit should be judged by humans before these candidates are used as positives."
        ),
    }


def cases_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# Qwen3-8B Manual Audit Cases",
        "",
        "## Loop Setup",
        "",
        "- Loop ID: Loop A / Qwen3-8B candidate audit",
        "- Current bottleneck: evidence grounding and false-rationalization risk in natural teacher candidates.",
        "- Hypothesis: the current prefilter accepts some useful Qwen3 candidates, but automatic flags will reveal evidence-span and validity risks that must be audited before targeted refinement.",
        "- Required evidence: stratified manual audit file plus automatic leakage/span/rule/evidence/rationalization checks.",
        "- Success criterion: no generator-input leakage; audit file covers accepted/refine/rejected, EXPECT/JFLEG, all corrector families, operations, and behaviors.",
        "- Failure criterion: reference/human-label leakage or pervasive span/evidence failures that make candidates unusable without prompt/verifier repair.",
        "",
        "## Summary",
        "",
        f"- Candidate count: {summary['candidate_count']}",
        f"- Selected for manual audit: {summary['selected_manual_audit_count']}",
        f"- Bucket counts: `{summary['bucket_counts']}`",
        f"- Flag counts: `{summary['flag_counts']}`",
        f"- Decision: `{summary['decision']}`",
        "",
        "## High-Risk Selected Cases",
        "",
    ]
    selected = [row for row in rows if row["selected_for_manual_audit"]]
    high_risk = sorted(selected, key=lambda item: (-int(item["risk_count"]), str(item["candidate_id"])))[:30]
    for row in high_risk:
        lines.extend(
            [
                f"### {row['candidate_id']}",
                "",
                f"- Bucket: `{row['bucket']}`; dataset: `{row['dataset']}`; model: `{row['model_key']}`; behavior: `{row['behavior']}`; operation: `{row['operation']}`",
                f"- Risks: `{row['risk_reasons']}`",
                f"- Source: {row['source']}",
                f"- Prediction: {row['model_prediction']}",
                f"- Edit: `{row['operation']}` `{row['source_text']}` -> `{row['target_text']}` at {row['edit_start']}:{row['edit_end']}",
                f"- Rule: {row['rule_text']}",
                f"- Evidence: `{row['evidence_spans_json']}`",
                f"- Rationale: {row['rationale']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Loop Result",
            "",
            "- Commands executed: see `docs/rulefaith_loop_A_qwen3_audit.md`.",
            "- Artifacts produced: `results/rulefaith/qwen3_manual_audit.csv`, `results/rulefaith/qwen3_manual_audit_summary.json`, and this case report.",
            f"- Hypothesis status: `revise` because the selected audit file is usable, but the automatic evidence-span checks show that the evidence verifier/prompt should be tightened before using accepted candidates as final positives.",
            "- Next highest-priority loop: implement targeted refinement only after adding stricter evidence-span validation and manual spot-checking the selected rows.",
            "",
        ]
    )
    return "\n".join(lines)


def load_all_rows(args: argparse.Namespace) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    seen: set[str] = set()
    for bucket, path in [
        ("accepted", resolve(args.accepted)),
        ("refine", resolve(args.refine)),
        ("rejected", resolve(args.rejected)),
    ]:
        for row in read_jsonl(path):
            cid = str(row.get("candidate_id", ""))
            if not cid:
                raise ValueError(f"Candidate without candidate_id in {path}")
            if cid in seen:
                raise ValueError(f"Duplicate candidate_id across buckets: {cid}")
            seen.add(cid)
            rows.append((bucket, row))
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Qwen3-8B RuleFaith manual audit package.")
    parser.add_argument("--accepted", type=Path, default=DEFAULT_BUCKETS["accepted"])
    parser.add_argument("--refine", type=Path, default=DEFAULT_BUCKETS["refine"])
    parser.add_argument("--rejected", type=Path, default=DEFAULT_BUCKETS["rejected"])
    parser.add_argument("--edit-pool", type=Path, default=DEFAULT_EDIT_POOL)
    parser.add_argument("--csv-output", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--cases-output", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--manual-sample-size", type=int, default=80)
    parser.add_argument("--seed", type=int, default=20260720)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.manual_sample_size <= 0:
        raise ValueError("--manual-sample-size must be positive")

    pool_rows = read_jsonl(resolve(args.edit_pool))
    pool_by_id = {str(row["rulefaith_pool_id"]): row for row in pool_rows}
    if len(pool_by_id) != len(pool_rows):
        raise ValueError("Duplicate rulefaith_pool_id values in edit pool")

    annotated = [annotate_row(row, bucket, pool_by_id) for bucket, row in load_all_rows(args)]
    select_manual_rows(annotated, min(args.manual_sample_size, len(annotated)), args.seed)
    annotated = sorted(
        annotated,
        key=lambda row: (
            not bool(row["selected_for_manual_audit"]),
            str(row["bucket"]),
            -int(row["risk_count"]),
            str(row["candidate_id"]),
        ),
    )

    summary = summarize(annotated, args)
    write_csv(resolve(args.csv_output), annotated, args.overwrite)
    write_json(resolve(args.summary_output), summary, args.overwrite)
    write_text(resolve(args.cases_output), cases_markdown(annotated, summary), args.overwrite)
    print(
        json.dumps(
            {
                "candidate_count": summary["candidate_count"],
                "selected_manual_audit_count": summary["selected_manual_audit_count"],
                "decision": summary["decision"],
                "csv_output": str(resolve(args.csv_output)),
                "summary_output": str(resolve(args.summary_output)),
                "cases_output": str(resolve(args.cases_output)),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
