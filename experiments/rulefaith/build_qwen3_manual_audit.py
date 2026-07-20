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
DEFAULT_BLIND_FORM = ROOT / "annotation" / "rulefaith_qwen3_audit" / "manual_audit_form.csv"
DEFAULT_BLIND_KEY = ROOT / "annotation" / "rulefaith_qwen3_audit" / "manual_audit_key.csv"
DEFAULT_GUIDELINES = ROOT / "annotation" / "rulefaith_qwen3_audit" / "guidelines.md"

FORBIDDEN_GENERATOR_FIELDS = {"reference", "behavior", "model_behavior", "human_label", "final_label", "gold_label"}
GENERIC_EVIDENCE_ROLES = {"", "source", "source_text", "original", "edit", "error", "error_span"}
PREDICTION_EVIDENCE_ROLES = {"target", "target_text", "modified", "correction", "corrected", "corrected_span"}
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
    "evidence_all_spans_source_index_match",
    "evidence_text_found_in_source",
    "evidence_text_found_in_prediction_only",
    "evidence_contextual",
    "evidence_valid_source_span_count",
    "evidence_invalid_source_span_count",
    "evidence_contextual_source_count",
    "evidence_edit_token_only_count",
    "evidence_error_types",
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

BLIND_FORM_FIELDS = [
    "candidate_id",
    "dataset",
    "sample_id",
    "model_key",
    "source",
    "model_prediction",
    "operation",
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

BLIND_KEY_FIELDS = [
    "candidate_id",
    "bucket",
    "audit_priority",
    "candidate_type",
    "dataset",
    "model_key",
    "behavior",
    "operation",
    "error_type",
    "risk_count",
    "risk_reasons",
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


def write_csv(path: Path, rows: Iterable[dict[str, Any]], overwrite: bool, fieldnames: list[str] | None = None) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fieldnames or CSV_FIELDS
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "").strip() if isinstance(row.get(field, ""), str) else row.get(field, "") for field in fields})


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def normalize(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def content_tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", normalize(text))


def normalized_ws_tokens(text: str) -> list[str]:
    return [normalize(token) for token in str(text or "").split() if normalize(token)]


def token_sequence_found(needle: str, haystack_tokens: list[str]) -> bool:
    needle_tokens = normalized_ws_tokens(needle)
    if not needle_tokens:
        return False
    if len(needle_tokens) > len(haystack_tokens):
        return False
    return any(haystack_tokens[i : i + len(needle_tokens)] == needle_tokens for i in range(len(haystack_tokens) - len(needle_tokens) + 1))


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


def edit_token_can_be_contextual(edit: dict[str, Any]) -> bool:
    error_type = normalize(edit.get("error_type", ""))
    source_text = normalize(edit.get("source_text", ""))
    target_text = normalize(edit.get("target_text", ""))
    if not source_text:
        return False
    source_content = "".join(content_tokens(source_text))
    target_content = "".join(content_tokens(target_text))
    if source_content and source_content == target_content and source_text != target_text:
        return True
    if error_type.startswith(("r:orth", "m:orth", "u:orth", "r:spell", "m:spell", "u:spell")):
        return True
    return "punct" in error_type or "capital" in error_type


def evidence_checks(source: str, prediction: str, edit: dict[str, Any], spans: Any) -> dict[str, Any]:
    if not isinstance(spans, list) or not spans:
        return {
            "evidence_span_index_match": False,
            "evidence_all_spans_source_index_match": False,
            "evidence_text_found_in_source": False,
            "evidence_text_found_in_prediction_only": False,
            "evidence_contextual": False,
            "evidence_valid_source_span_count": 0,
            "evidence_invalid_source_span_count": 0,
            "evidence_contextual_source_count": 0,
            "evidence_edit_token_only_count": 0,
            "evidence_error_types": "missing_evidence",
            "missing_evidence": True,
            "wrong_evidence_auto": False,
        }

    source_tokens = source.split()
    normalized_source_tokens = normalized_ws_tokens(source)
    normalized_prediction_tokens = normalized_ws_tokens(prediction)
    edit_source = normalize(edit.get("source_text", ""))
    edit_target = normalize(edit.get("target_text", ""))
    allow_edit_token_evidence = edit_token_can_be_contextual(edit)
    valid_source_span_count = 0
    invalid_source_span_count = 0
    contextual_source_count = 0
    edit_token_only_count = 0
    prediction_only_count = 0
    text_found_count = 0
    errors: Counter[str] = Counter()

    for span in spans:
        if not isinstance(span, dict):
            errors["malformed_span"] += 1
            invalid_source_span_count += 1
            continue
        text = normalize(span.get("text", ""))
        role = normalize(span.get("role", ""))
        start = span.get("start")
        end = span.get("end")
        if not text:
            errors["empty_text"] += 1
            invalid_source_span_count += 1
            continue

        text_in_source = token_sequence_found(text, normalized_source_tokens)
        text_in_prediction = token_sequence_found(text, normalized_prediction_tokens)
        if text_in_source:
            text_found_count += 1

        index_valid = isinstance(start, int) and isinstance(end, int) and 0 <= start <= end <= len(source_tokens)
        index_match = False
        if index_valid:
            indexed_text = normalize(" ".join(source_tokens[start:end]))
            index_match = indexed_text == text
        else:
            errors["invalid_indices"] += 1

        if index_match:
            valid_source_span_count += 1
        else:
            invalid_source_span_count += 1
            if index_valid:
                errors["index_text_mismatch"] += 1

        edit_token_only = text in {edit_source, edit_target} or role in (GENERIC_EVIDENCE_ROLES | PREDICTION_EVIDENCE_ROLES)
        if edit_token_only:
            edit_token_only_count += 1

        prediction_only = text_in_prediction and not text_in_source
        if prediction_only or role in PREDICTION_EVIDENCE_ROLES:
            prediction_only_count += 1
            if prediction_only:
                errors["prediction_only_text"] += 1
            else:
                errors["prediction_or_target_role"] += 1

        if not text_in_source and not any(token in set(normalized_source_tokens) for token in content_tokens(text)):
            errors["text_not_in_source"] += 1

        contextual = text_in_source and index_match and not prediction_only and (not edit_token_only or allow_edit_token_evidence)
        if contextual:
            contextual_source_count += 1

    any_index_match = valid_source_span_count > 0
    all_index_match = valid_source_span_count == len(spans) and len(spans) > 0
    any_text_found = text_found_count > 0
    any_prediction_only = prediction_only_count > 0
    any_contextual = contextual_source_count > 0
    wrong_evidence = bool(errors) or any_prediction_only or invalid_source_span_count > 0
    return {
        "evidence_span_index_match": any_index_match,
        "evidence_all_spans_source_index_match": all_index_match,
        "evidence_text_found_in_source": any_text_found,
        "evidence_text_found_in_prediction_only": any_prediction_only,
        "evidence_contextual": any_contextual,
        "evidence_valid_source_span_count": valid_source_span_count,
        "evidence_invalid_source_span_count": invalid_source_span_count,
        "evidence_contextual_source_count": contextual_source_count,
        "evidence_edit_token_only_count": edit_token_only_count,
        "evidence_error_types": ";".join(sorted(errors)) if errors else "",
        "missing_evidence": not any_contextual,
        "wrong_evidence_auto": wrong_evidence,
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
    evidence = evidence_checks(row.get("source", ""), row.get("model_prediction", ""), edit, parsed.get("evidence_spans", []))
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
    if not flags["evidence_all_spans_source_index_match"]:
        risk_reasons.append("evidence_not_all_source_index_matched")
    if not flags["evidence_text_found_in_source"]:
        risk_reasons.append("evidence_text_not_found_in_source")
    if flags["evidence_text_found_in_prediction_only"]:
        risk_reasons.append("evidence_prediction_only_text")
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
        "evidence_all_spans_source_index_match",
        "evidence_text_found_in_source",
        "evidence_text_found_in_prediction_only",
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
        "evidence_all_spans_index_mismatch_count": len(rows) - flag_counts["evidence_all_spans_source_index_match"],
        "evidence_prediction_only_count": flag_counts["evidence_text_found_in_prediction_only"],
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
        "evidence_error_type_counts": dict(
            Counter(
                error
                for row in rows
                for error in str(row.get("evidence_error_types", "")).split(";")
                if error
            )
        ),
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
        f"- Evidence error type counts: `{summary.get('evidence_error_type_counts', {})}`",
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
                f"- Source: {str(row['source']).strip()}",
                f"- Prediction: {str(row['model_prediction']).strip()}",
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


def blind_guidelines(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Qwen3-8B RuleFaith Manual Audit Guidelines",
            "",
            "You are auditing model-generated explanation candidates for edit-level GEC explanations.",
            "",
            "## Scope",
            "",
            f"- Audit rows: {summary['selected_manual_audit_count']}",
            "- Each row evaluates one model-produced atomic edit and one Qwen3-8B explanation candidate.",
            "- The file is blind: it does not show accepted/refine/rejected bucket labels or automatic risk flags.",
            "- These explanations are teacher-generated candidates, not human gold.",
            "",
            "## What To Check",
            "",
            "Fill each issue column with `yes`, `no`, or `uncertain`.",
            "",
            "- `human_alignment_error`: yes if the explanation describes a different edit, wrong operation, wrong source text, wrong target text, or wrong direction.",
            "- `human_validity_error`: yes if the explanation says or implies the model edit is valid when the edit is invalid, unnecessary, or only stylistic.",
            "- `human_wrong_rule`: yes if the stated linguistic rule is false.",
            "- `human_inapplicable_rule`: yes if the rule is true in general but does not justify this edit in this sentence.",
            "- `human_missing_evidence`: yes if no sentence-specific contextual evidence is provided.",
            "- `human_wrong_evidence`: yes if the cited evidence span, token index, trigger, subject, antecedent, governor, or contextual relation is wrong.",
            "- `human_generic_explanation`: yes if the explanation could apply to many unrelated sentences and does not identify this case's concrete trigger.",
            "- `human_edit_copy`: yes if the explanation mainly copies the source-target edit without rule or evidence grounding.",
            "- `human_semantic_distortion`: yes if the explanation changes the intended meaning or rationalizes a semantically wrong correction.",
            "- `human_unsupported_confidence`: yes if the confidence is high despite missing evidence, weak rule support, invalid edit, or uncertainty.",
            "",
            "## Evidence Rules",
            "",
            "- Evidence spans must refer to text in the original SOURCE, not the model prediction.",
            "- The `start` and `end` fields are whitespace-token offsets in SOURCE.",
            "- A target phrase that only appears in MODEL_PREDICTION is not source evidence.",
            "- The modified token alone is usually not enough evidence for grammar rules.",
            "- For spelling, capitalization, and punctuation, the edited token itself may be sufficient only if the explanation explicitly concerns that orthographic property.",
            "- Subject-verb agreement should cite the subject and verb.",
            "- Article/determiner explanations should cite the head noun and definiteness/countability/number cue when available.",
            "- Tense explanations should cite the time cue or relevant event context when available.",
            "- Preposition explanations should cite the governing verb/adjective/noun or collocation when available.",
            "",
            "## Decision",
            "",
            "Use `human_decision`:",
            "",
            "- `accept`: explanation is aligned and has no serious rule/evidence/validity issue.",
            "- `refine`: explanation is useful but needs targeted repair.",
            "- `reject`: explanation is misleading, wrong, too generic, or mostly edit-copy.",
            "- `abstain`: there is not enough information to judge or the edit itself is too ambiguous.",
            "",
            "Keep notes concise. Do not use automatic labels or previous audit outputs while filling the blind form.",
            "",
        ]
    )


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
    parser.add_argument("--blind-form-output", type=Path, default=DEFAULT_BLIND_FORM)
    parser.add_argument("--blind-key-output", type=Path, default=DEFAULT_BLIND_KEY)
    parser.add_argument("--guidelines-output", type=Path, default=DEFAULT_GUIDELINES)
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
    selected_rows = [row for row in annotated if row["selected_for_manual_audit"]]
    write_csv(resolve(args.csv_output), annotated, args.overwrite)
    write_csv(resolve(args.blind_form_output), selected_rows, args.overwrite, BLIND_FORM_FIELDS)
    write_csv(resolve(args.blind_key_output), selected_rows, args.overwrite, BLIND_KEY_FIELDS)
    write_json(resolve(args.summary_output), summary, args.overwrite)
    write_text(resolve(args.guidelines_output), blind_guidelines(summary), args.overwrite)
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
                "blind_form_output": str(resolve(args.blind_form_output)),
                "guidelines_output": str(resolve(args.guidelines_output)),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
