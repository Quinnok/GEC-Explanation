from __future__ import annotations

import argparse
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


DEFAULT_INPUT = ROOT / "results" / "rulefaith" / "qwen3_v2_smoke10_candidates.jsonl"
DEFAULT_OUTPUT = ROOT / "results" / "rulefaith" / "qwen3_v2_smoke10_evidence_canonicalized_candidates.jsonl"
DEFAULT_STATS = ROOT / "results" / "rulefaith" / "qwen3_v2_smoke10_evidence_canonicalization_stats.json"
DEFAULT_AUDIT_MD = ROOT / "results" / "rulefaith" / "qwen3_v2_smoke10_evidence_canonicalization_audit.md"


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


def normalize_token(token: str) -> str:
    return audit.normalize(token)


def normalized_tokens(text: str) -> list[str]:
    return [normalize_token(token) for token in str(text or "").split() if normalize_token(token)]


def find_token_sequence(source: str, text: str) -> list[tuple[int, int]]:
    source_tokens = normalized_tokens(source)
    needle = normalized_tokens(text)
    if not needle or len(needle) > len(source_tokens):
        return []
    spans: list[tuple[int, int]] = []
    for idx in range(len(source_tokens) - len(needle) + 1):
        if source_tokens[idx : idx + len(needle)] == needle:
            spans.append((idx, idx + len(needle)))
    return spans


def canonicalize_spans(record: dict[str, Any], drop_prediction_only: bool) -> tuple[list[dict[str, Any]], Counter[str]]:
    parsed = record.get("parsed_output") or {}
    spans = parsed.get("evidence_spans", []) if isinstance(parsed, dict) else []
    if not isinstance(spans, list):
        return [], Counter({"malformed_evidence_spans": 1})
    source = str(record.get("source", ""))
    prediction = str(record.get("model_prediction", ""))
    edit = record.get("model_edit") or {}
    source_token_count = len(source.split())
    counters: Counter[str] = Counter()
    canonical: list[dict[str, Any]] = []
    seen: set[tuple[str, int, int, str]] = set()
    for span in spans:
        if not isinstance(span, dict):
            counters["dropped_malformed_span"] += 1
            continue
        text = str(span.get("text", "")).strip()
        role = str(span.get("role", "unspecified")).strip() or "unspecified"
        if not text:
            counters["dropped_empty_span"] += 1
            continue
        matches = find_token_sequence(source, text)
        prediction_only = audit.token_sequence_found(text, audit.normalized_ws_tokens(prediction)) and not matches
        if prediction_only and drop_prediction_only:
            counters["dropped_prediction_only_span"] += 1
            continue
        if len(matches) == 1:
            start, end = matches[0]
            old_start, old_end = span.get("start"), span.get("end")
            if old_start != start or old_end != end:
                counters["corrected_indices"] += 1
        elif len(matches) > 1:
            start, end = choose_nearest_match(matches, edit)
            counters["corrected_ambiguous_indices"] += 1
        else:
            try:
                start = int(span.get("start", -1))
                end = int(span.get("end", -1))
            except (TypeError, ValueError):
                counters["dropped_unlocatable_span"] += 1
                continue
            if not (0 <= start <= end <= source_token_count):
                counters["dropped_unlocatable_span"] += 1
                continue
            counters["kept_unverified_span"] += 1
        key = (audit.normalize(text), start, end, audit.normalize(role))
        if key in seen:
            counters["dropped_duplicate_span"] += 1
            continue
        seen.add(key)
        canonical.append({"text": " ".join(source.split()[start:end]) if 0 <= start <= end <= source_token_count else text, "start": start, "end": end, "role": role})
    return canonical, counters


def choose_nearest_match(matches: list[tuple[int, int]], edit: dict[str, Any]) -> tuple[int, int]:
    try:
        edit_start = int(edit.get("start", 0))
    except (TypeError, ValueError):
        edit_start = 0
    return min(matches, key=lambda span: min(abs(span[0] - edit_start), abs(span[1] - edit_start)))


def checks_for(record: dict[str, Any], parsed: dict[str, Any] | None = None) -> dict[str, Any]:
    parsed_output = parsed if parsed is not None else record.get("parsed_output") or {}
    if not isinstance(parsed_output, dict):
        parsed_output = {}
    return audit.evidence_checks(
        str(record.get("source", "")),
        str(record.get("model_prediction", "")),
        record.get("model_edit") or {},
        parsed_output.get("evidence_spans", []),
    )


def canonicalize_record(record: dict[str, Any], drop_prediction_only: bool) -> tuple[dict[str, Any], Counter[str]]:
    parsed = dict(record.get("parsed_output") or {})
    before_checks = checks_for(record, parsed)
    spans, counters = canonicalize_spans(record, drop_prediction_only)
    parsed["evidence_spans"] = spans
    after_checks = checks_for(record, parsed)
    output = dict(record)
    output["candidate_id"] = f"{record['candidate_id']}::evidence_canonicalized"
    output["original_candidate_id"] = record.get("candidate_id")
    output["candidate_type"] = "evidence_canonicalized"
    output["original_candidate_type"] = record.get("candidate_type")
    output["provider"] = "rulefaith_deterministic_evidence_canonicalizer"
    output["prompt_version"] = "rulefaith_deterministic_evidence_canonicalizer_v1"
    output["parsed_output"] = parsed
    output["before_evidence_checks"] = before_checks
    output["after_evidence_checks"] = after_checks
    output["canonicalization_actions"] = dict(counters)
    output["evidence_contextual_improved"] = bool(not before_checks["evidence_contextual"] and after_checks["evidence_contextual"])
    output["wrong_evidence_fixed"] = bool(before_checks["wrong_evidence_auto"] and not after_checks["wrong_evidence_auto"])
    output["prediction_only_evidence_regressed"] = bool(not before_checks["evidence_text_found_in_prediction_only"] and after_checks["evidence_text_found_in_prediction_only"])
    output["created_at"] = utc_now()
    output["label_source"] = "deterministic_span_repair_not_human_gold"
    return output, counters


def summarize(original: list[dict[str, Any]], canonicalized: list[dict[str, Any]], action_counts: Counter[str]) -> dict[str, Any]:
    before = [checks_for(row) for row in original]
    after = [row["after_evidence_checks"] for row in canonicalized]

    def count(checks: list[dict[str, Any]], key: str) -> int:
        return sum(1 for item in checks if item.get(key))

    summary = {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "input_count": len(original),
        "canonicalized_count": len(canonicalized),
        "action_counts": dict(action_counts),
        "before": {
            "contextual_source_evidence": count(before, "evidence_contextual"),
            "missing_evidence": count(before, "missing_evidence"),
            "prediction_only_evidence": count(before, "evidence_text_found_in_prediction_only"),
            "wrong_evidence_auto": count(before, "wrong_evidence_auto"),
        },
        "after": {
            "contextual_source_evidence": count(after, "evidence_contextual"),
            "missing_evidence": count(after, "missing_evidence"),
            "prediction_only_evidence": count(after, "evidence_text_found_in_prediction_only"),
            "wrong_evidence_auto": count(after, "wrong_evidence_auto"),
        },
        "improvement_counts": {
            "evidence_contextual_improved": sum(1 for row in canonicalized if row["evidence_contextual_improved"]),
            "wrong_evidence_fixed": sum(1 for row in canonicalized if row["wrong_evidence_fixed"]),
            "prediction_only_evidence_regressed": sum(1 for row in canonicalized if row["prediction_only_evidence_regressed"]),
        },
    }
    if summary["after"]["contextual_source_evidence"] > summary["before"]["contextual_source_evidence"]:
        summary["decision"] = "keep_canonicalizer_as_span_normalization_step_before_model_refinement"
    else:
        summary["decision"] = "canonicalizer_only_repairs_offsets_not_missing_contextual_evidence"
    return summary


def markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Evidence Span Canonicalization Audit",
        "",
        "This deterministic pass repairs evidence span offsets when the cited text can be located in SOURCE. It does not judge whether the rule is linguistically correct.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Changed Cases", ""])
    for row in rows:
        actions = row.get("canonicalization_actions", {})
        if not actions:
            continue
        parsed = row.get("parsed_output") or {}
        lines.extend(
            [
                f"### {row['candidate_id']}",
                "",
                f"- original: `{row.get('original_candidate_id')}`",
                f"- actions: `{actions}`",
                f"- before: `{row.get('before_evidence_checks')}`",
                f"- after: `{row.get('after_evidence_checks')}`",
                f"- evidence: `{json.dumps(parsed.get('evidence_spans', []), ensure_ascii=False, sort_keys=True)}`",
                "",
            ]
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Canonicalize evidence span offsets in RuleFaith candidate JSONL files.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stats-output", type=Path, default=DEFAULT_STATS)
    parser.add_argument("--audit-md-output", type=Path, default=DEFAULT_AUDIT_MD)
    parser.add_argument("--drop-prediction-only", action="store_true", default=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = read_jsonl(resolve(args.input))
    ids = [row.get("candidate_id") for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate candidate_id in input")
    canonicalized: list[dict[str, Any]] = []
    action_counts: Counter[str] = Counter()
    for row in rows:
        output, counters = canonicalize_record(row, args.drop_prediction_only)
        canonicalized.append(output)
        action_counts.update(counters)
    summary = summarize(rows, canonicalized, action_counts)
    summary["input_file"] = str(resolve(args.input))
    summary["output_file"] = str(resolve(args.output))
    write_jsonl(resolve(args.output), canonicalized, args.overwrite)
    write_json(resolve(args.stats_output), summary, args.overwrite)
    write_text(resolve(args.audit_md_output), markdown(summary, canonicalized), args.overwrite)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
