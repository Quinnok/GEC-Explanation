from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EXPLANATIONS = ROOT / "data" / "processed" / "model_edit_explanation_candidates.jsonl"
DEFAULT_PER_SENTENCE = ROOT / "results" / "model_edits" / "per_sentence_alignment.jsonl"
DEFAULT_OUT_DIR = ROOT / "results" / "audit"


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def tokens(text: str) -> List[str]:
    return text.split()


def span_text(source: str, edit: Dict[str, Any]) -> str:
    toks = tokens(source)
    start = int(edit["start"])
    end = int(edit["end"])
    if start == end:
        return ""
    return " ".join(toks[start:end])


def punctuation_case_only(source_text: str, target_text: str) -> bool:
    def strip_noise(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[\s`'\".,!?;:()\[\]{}-]+", "", text)
        return text

    return strip_noise(source_text) == strip_noise(target_text) and source_text != target_text


def explanation_flags(row: Dict[str, Any]) -> Dict[str, Any]:
    edit = row["predicted_edit"]
    explanation = row["open_source_explanation_candidate"]
    low = normalize_text(explanation)
    source_text = normalize_text(edit.get("source_text", ""))
    target_text = normalize_text(edit.get("target_text", ""))
    operation = edit.get("operation", "")
    error_type = edit.get("error_type", "")
    generic_patterns = [
        "the following is a list",
        "the verb should agree with the singular subject",
        "grammatical errors",
        "same meaning",
    ]
    mentions_source = bool(source_text and source_text in low)
    mentions_target = bool(target_text and target_text in low)
    mentions_operation = operation in low or {
        "replace": "instead",
        "insert": "missing",
        "delete": "remove",
    }.get(operation, "###") in low
    mentions_type_hint = any(part.lower() in low for part in error_type.split(":") if len(part) > 2)
    direct_target_restatement = bool(target_text and target_text == low)
    prediction_first_clause = normalize_text(row["prediction"]).split(" . ")[0]
    repeats_prediction_clause = bool(prediction_first_clause and prediction_first_clause[:80] in low)
    generic = any(pattern in low for pattern in generic_patterns) or len(low.split()) < 4
    corresponds_current_edit = mentions_source or mentions_target or mentions_operation or mentions_type_hint
    return {
        "explanation_mentions_source_text": mentions_source,
        "explanation_mentions_target_text": mentions_target,
        "explanation_mentions_operation_hint": mentions_operation,
        "explanation_mentions_error_type_hint": mentions_type_hint,
        "explanation_corresponds_to_current_edit_auto": corresponds_current_edit and not generic,
        "explanation_directly_restates_target_auto": direct_target_restatement,
        "explanation_repeats_prediction_clause_auto": repeats_prediction_clause,
        "explanation_generic_auto": generic,
        "explanation_rule_correctness_auto": "unknown_requires_human",
        "explanation_omits_key_condition_auto": generic or not corresponds_current_edit,
    }


def audit_flags(row: Dict[str, Any], multi_edit_lookup: Dict[Tuple[str, str], bool]) -> Dict[str, Any]:
    edit = row["predicted_edit"]
    extracted_span = span_text(row["source"], edit)
    span_ok = normalize_text(extracted_span) == normalize_text(edit.get("source_text", ""))
    if edit["operation"] == "insert":
        span_ok = edit.get("source_text", "") == "" and int(edit["start"]) == int(edit["end"])
    orth_punct = "ORTH" in edit["error_type"] or "PUNCT" in edit["error_type"]
    orth_punct = orth_punct or punctuation_case_only(edit.get("source_text", ""), edit.get("target_text", ""))
    alignment_score = row.get("alignment_score")
    behavior_label_auto_consistent = (
        (row["behavior"] == "correct_correction" and row["aligned_reference_edit"] is not None and (alignment_score in (None, 1.0)))
        or (row["behavior"] == "wrong_correction" and row["aligned_reference_edit"] is not None)
        or (row["behavior"] == "overcorrection" and row["aligned_reference_edit"] is None)
    )
    return {
        "audit_type": "researcher_readable_automatic_audit_not_human_annotation",
        "edit_extraction_source_span_matches_auto": span_ok,
        "edit_boundary_auto_check": "pass" if span_ok else "needs_review",
        "behavior_label_auto_consistent": behavior_label_auto_consistent,
        "orth_or_punct_noise_auto": orth_punct,
        "multi_edit_sentence": multi_edit_lookup.get((row["sample_id"], row["model_key"]), False),
    } | explanation_flags(row)


def stratum_key(row: Dict[str, Any]) -> Tuple[str, str]:
    return row["model_key"], row["behavior"]


def select_rows(rows: List[Dict[str, Any]], target_count: int) -> List[Dict[str, Any]]:
    selected: List[Dict[str, Any]] = []
    selected_ids: set[str] = set()
    by_stratum: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_stratum[stratum_key(row)].append(row)

    strata = [
        ("gector_roberta_base", "correct_correction"),
        ("gector_roberta_base", "wrong_correction"),
        ("gector_roberta_base", "overcorrection"),
        ("t5_base_grammar", "correct_correction"),
        ("t5_base_grammar", "wrong_correction"),
        ("t5_base_grammar", "overcorrection"),
    ]
    per_stratum = max(1, target_count // len(strata))
    for key in strata:
        for row in by_stratum.get(key, [])[:per_stratum]:
            selected.append(row)
            selected_ids.add(row["record_id"])

    required_ops = {"replace", "insert", "delete"}
    required_noise = {True, False}
    required_multi = {True, False}
    for predicate in [
        lambda row: row["predicted_edit"]["operation"] in required_ops,
        lambda row: "ORTH" in row["predicted_edit"]["error_type"] or "PUNCT" in row["predicted_edit"]["error_type"],
        lambda row: row["record_id"] not in selected_ids,
    ]:
        for row in rows:
            if len(selected) >= target_count:
                break
            if row["record_id"] not in selected_ids and predicate(row):
                selected.append(row)
                selected_ids.add(row["record_id"])

    for row in rows:
        if len(selected) >= target_count:
            break
        if row["record_id"] not in selected_ids:
            selected.append(row)
            selected_ids.add(row["record_id"])

    return selected[:target_count]


def render_markdown(rows: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
    lines = [
        "# Round 04 Model Edit and Explanation Audit",
        "",
        "This is a researcher-readable automatic audit, not human annotation. It flags likely extraction, alignment, detokenization, and explanation-quality issues for manual review.",
        "",
        "## Summary",
        "",
        f"- Audited rows: {summary['audit_count']}",
        f"- Model counts: `{json.dumps(summary['model_counts'], sort_keys=True)}`",
        f"- Behavior counts: `{json.dumps(summary['behavior_counts'], sort_keys=True)}`",
        f"- Operation counts: `{json.dumps(summary['operation_counts'], sort_keys=True)}`",
        f"- ORTH/PUNCT noise flags: {summary['orth_or_punct_noise_count']}",
        f"- Generic explanation flags: {summary['generic_explanation_count']}",
        "",
    ]
    for index, row in enumerate(rows, 1):
        flags = row["audit_flags"]
        lines.extend(
            [
                f"## {index}. {row['record_id']}",
                "",
                f"- Model: `{row['model_key']}`",
                f"- Behavior: `{row['behavior']}`",
                f"- Source: `{row['source']}`",
                f"- Reference: `{row['reference']}`",
                f"- Prediction: `{row['prediction']}`",
                f"- Predicted edit: `{json.dumps(row['predicted_edit'], ensure_ascii=False)}`",
                f"- Aligned reference edit: `{json.dumps(row['aligned_reference_edit'], ensure_ascii=False)}`",
                f"- FLAN explanation: `{row['open_source_explanation_candidate']}`",
                f"- Automatic audit flags: `{json.dumps(flags, ensure_ascii=False, sort_keys=True)}`",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def build(args: argparse.Namespace) -> None:
    rows = read_jsonl(args.explanations)
    per_sentence = read_jsonl(args.per_sentence)
    multi_edit_lookup = {
        (row["sample_id"], row["model_key"]): row["pred_edit_count"] > 1 or row["ref_edit_count"] > 1
        for row in per_sentence
    }
    selected = select_rows(rows, args.count)
    audited = []
    for row in selected:
        row = dict(row)
        row["audit_flags"] = audit_flags(row, multi_edit_lookup)
        audited.append(row)

    summary = {
        "audit_type": "researcher_readable_automatic_audit_not_human_annotation",
        "audit_count": len(audited),
        "model_counts": dict(Counter(row["model_key"] for row in audited)),
        "behavior_counts": dict(Counter(row["behavior"] for row in audited)),
        "operation_counts": dict(Counter(row["predicted_edit"]["operation"] for row in audited)),
        "error_type_counts": dict(Counter(row["predicted_edit"]["error_type"] for row in audited).most_common(20)),
        "multi_edit_sentence_count": sum(1 for row in audited if row["audit_flags"]["multi_edit_sentence"]),
        "orth_or_punct_noise_count": sum(1 for row in audited if row["audit_flags"]["orth_or_punct_noise_auto"]),
        "generic_explanation_count": sum(1 for row in audited if row["audit_flags"]["explanation_generic_auto"]),
        "target_restatement_count": sum(1 for row in audited if row["audit_flags"]["explanation_directly_restates_target_auto"]),
        "prediction_clause_repeat_count": sum(1 for row in audited if row["audit_flags"]["explanation_repeats_prediction_clause_auto"]),
        "span_auto_check_fail_count": sum(1 for row in audited if not row["audit_flags"]["edit_extraction_source_span_matches_auto"]),
        "behavior_auto_inconsistent_count": sum(1 for row in audited if not row["audit_flags"]["behavior_label_auto_consistent"]),
        "notes": [
            "Automatic flags are screening signals only.",
            "Rule correctness and explanation faithfulness require human review or a stronger validated evaluator.",
        ],
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "round04_sample_audit.jsonl", audited)
    write_json(args.out_dir / "round04_audit_summary.json", summary)
    (args.out_dir / "round04_sample_audit.md").write_text(render_markdown(audited, summary))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a stratified Round 04 audit over model edits and FLAN explanations.")
    parser.add_argument("--explanations", type=Path, default=DEFAULT_EXPLANATIONS)
    parser.add_argument("--per-sentence", type=Path, default=DEFAULT_PER_SENTENCE)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--count", type=int, default=60)
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
