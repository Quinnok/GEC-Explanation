from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]

GRAMMAR_KEYWORDS = {
    "agreement",
    "article",
    "auxiliary",
    "capitalization",
    "clause",
    "collocation",
    "comma",
    "comparative",
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

GENERIC_EVIDENCE_ROLES = {"source", "target", "source_text", "target_text", "unspecified", ""}


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalize(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def text_contains(text: str, needle: str) -> bool:
    needle = normalize(needle)
    if not needle:
        return True
    return needle in normalize(text)


def diagnostic_text(row: Dict[str, Any]) -> str:
    parsed = row.get("parsed_output") or {}
    evidence_text = " ".join(str(span.get("text", "")) for span in parsed.get("evidence_spans", []) if isinstance(span, dict))
    return " ".join(
        [
            str(parsed.get("edit_description", "")),
            str(parsed.get("rule_text", "")),
            str(parsed.get("rationale", "")),
            evidence_text,
        ]
    )


def has_contextual_evidence(row: Dict[str, Any]) -> bool:
    parsed = row.get("parsed_output") or {}
    edit = row.get("model_edit") or {}
    source_text = normalize(edit.get("source_text", ""))
    target_text = normalize(edit.get("target_text", ""))
    spans = parsed.get("evidence_spans", [])
    if not isinstance(spans, list):
        return False
    for span in spans:
        if not isinstance(span, dict):
            continue
        text = normalize(span.get("text", ""))
        role = normalize(span.get("role", ""))
        if not text:
            continue
        if role in GENERIC_EVIDENCE_ROLES:
            continue
        if text in {source_text, target_text}:
            continue
        return True
    return False


def rule_is_edit_copy(row: Dict[str, Any]) -> bool:
    parsed = row.get("parsed_output") or {}
    rule = normalize(parsed.get("rule_text", ""))
    if not rule or rule in {"none", "null", "n/a", "na"}:
        return True
    has_edit_word = any(word in rule for word in ["replace", "insert", "delete", "change"])
    has_grammar_word = any(keyword in rule for keyword in GRAMMAR_KEYWORDS)
    edit = row.get("model_edit") or {}
    mentions_source = text_contains(rule, edit.get("source_text", ""))
    mentions_target = text_contains(rule, edit.get("target_text", ""))
    return has_edit_word and not has_grammar_word and (mentions_source or mentions_target)


def alignment_proxy_pass(row: Dict[str, Any]) -> bool:
    parsed = row.get("parsed_output") or {}
    edit = row.get("model_edit") or {}
    operation = normalize(edit.get("operation", ""))
    source_text = str(edit.get("source_text", ""))
    target_text = str(edit.get("target_text", ""))
    text = diagnostic_text(row)
    if operation and operation not in normalize(text):
        return False
    if source_text and not text_contains(text, source_text):
        return False
    if operation != "delete" and target_text and not text_contains(text, target_text):
        return False
    return True


def flags_for(row: Dict[str, Any]) -> Dict[str, Any]:
    parsed = row.get("parsed_output") or {}
    raw = str(row.get("raw_response", ""))
    flags = {
        "candidate_id": row.get("candidate_id"),
        "provider": row.get("provider"),
        "teacher_model": row.get("teacher_model"),
        "candidate_type": row.get("candidate_type"),
        "parse_status": row.get("parse_status"),
        "raw_markdown_json": raw.strip().startswith("```"),
        "alignment_proxy_pass": alignment_proxy_pass(row),
        "rule_is_edit_copy": rule_is_edit_copy(row),
        "has_contextual_evidence": has_contextual_evidence(row),
        "abstain": bool(parsed.get("abstain", False)),
        "edit_validity": parsed.get("edit_validity", "uncertain"),
        "rationale": parsed.get("rationale", ""),
        "rule_text": parsed.get("rule_text", ""),
    }
    flags["missing_rule_text"] = normalize(parsed.get("rule_text", "")) in {"", "none", "null", "n/a", "na"}
    flags["high_risk"] = (
        flags["parse_status"] != "parsed_json"
        or not flags["alignment_proxy_pass"]
        or flags["missing_rule_text"]
        or flags["rule_is_edit_copy"]
        or not flags["has_contextual_evidence"]
    )
    return flags


def rate(count: int, total: int) -> float:
    return round(count / total, 4) if total else 0.0


def summarize(flags: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(flags)
    by_provider: Dict[str, Dict[str, Any]] = {}
    provider_groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for item in flags:
        provider_groups[str(item.get("provider", ""))].append(item)
    for provider, group in provider_groups.items():
        n = len(group)
        by_provider[provider] = {
            "candidate_count": n,
            "parse_json_rate": rate(sum(1 for item in group if item["parse_status"] == "parsed_json"), n),
            "alignment_proxy_pass_rate": rate(sum(1 for item in group if item["alignment_proxy_pass"]), n),
            "rule_edit_copy_rate": rate(sum(1 for item in group if item["rule_is_edit_copy"]), n),
            "missing_rule_text_rate": rate(sum(1 for item in group if item["missing_rule_text"]), n),
            "contextual_evidence_rate": rate(sum(1 for item in group if item["has_contextual_evidence"]), n),
            "high_risk_rate": rate(sum(1 for item in group if item["high_risk"]), n),
            "raw_markdown_json_rate": rate(sum(1 for item in group if item["raw_markdown_json"]), n),
            "abstain_rate": rate(sum(1 for item in group if item["abstain"]), n),
            "candidate_type_counts": dict(Counter(item["candidate_type"] for item in group)),
        }
    return {
        "candidate_count": total,
        "provider_counts": dict(Counter(item.get("provider", "") for item in flags)),
        "candidate_type_counts": dict(Counter(item.get("candidate_type", "") for item in flags)),
        "parse_status_counts": dict(Counter(item.get("parse_status", "") for item in flags)),
        "by_provider": by_provider,
    }


def write_markdown(path: Path, input_path: Path, summary: Dict[str, Any], flags: List[Dict[str, Any]]) -> None:
    lines = [
        "# RuleFaith Teacher Candidate Diagnostics",
        "",
        f"Input: `{input_path}`",
        "",
        "## Summary",
        "",
        f"- Candidate count: {summary['candidate_count']}",
        f"- Provider counts: {summary['provider_counts']}",
        f"- Candidate type counts: {summary['candidate_type_counts']}",
        f"- Parse status counts: {summary['parse_status_counts']}",
        "",
        "## Provider Metrics",
        "",
        "| Provider | N | Parse JSON | Alignment Proxy | Missing Rule | Rule Edit-Copy | Contextual Evidence | High Risk | Markdown JSON | Abstain |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for provider, metrics in summary["by_provider"].items():
        lines.append(
            "| {provider} | {candidate_count} | {parse_json_rate:.3f} | {alignment_proxy_pass_rate:.3f} | "
            "{missing_rule_text_rate:.3f} | {rule_edit_copy_rate:.3f} | {contextual_evidence_rate:.3f} | {high_risk_rate:.3f} | "
            "{raw_markdown_json_rate:.3f} | {abstain_rate:.3f} |".format(provider=provider, **metrics)
        )
    lines.extend(["", "## Highest-Risk Examples", ""])
    for item in [flag for flag in flags if flag["high_risk"]][:30]:
        lines.append(
            f"- `{item['candidate_id']}`: alignment={item['alignment_proxy_pass']}, "
            f"missing_rule={item['missing_rule_text']}, rule_edit_copy={item['rule_is_edit_copy']}, "
            f"contextual_evidence={item['has_contextual_evidence']}; "
            f"rule={item['rule_text'][:160]!r}; rationale={item['rationale'][:180]!r}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose RuleFaith teacher candidate risks.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--md-output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = resolve(args.input)
    flags = [flags_for(row) for row in read_jsonl(input_path)]
    summary = summarize(flags)
    write_json(resolve(args.json_output), {"input": str(input_path), "summary": summary, "flags": flags})
    write_markdown(resolve(args.md_output), input_path, summary, flags)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
