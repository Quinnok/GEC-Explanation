from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.rulefaith import build_qwen3_manual_audit as audit
from experiments.rulefaith import refine_qwen3_evidence as refine


DEFAULT_INPUT = ROOT / "data" / "rulefaith" / "teacher_candidates_qwen3_8b_canonicalized.jsonl"
DEFAULT_OUTPUT = ROOT / "data" / "rulefaith" / "qwen3_evidence_refinement_probe20.jsonl"
DEFAULT_STATS = ROOT / "results" / "rulefaith" / "qwen3_evidence_refinement_probe20_stats.json"
DEFAULT_CARD = ROOT / "results" / "rulefaith" / "qwen3_evidence_refinement_probe20_card.md"

DIVERSITY_FIELDS = (
    "dataset",
    "model_key",
    "model_family",
    "operation",
    "original_candidate_type",
    "rulefaith_split",
)


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


def group_key(row: dict[str, Any]) -> str:
    for key in ("rulefaith_pool_id", "edit_id", "sample_id"):
        value = row.get(key)
        if value:
            return str(value)
    edit = row.get("model_edit") or {}
    return "::".join(
        [
            str(row.get("source", "")),
            str(edit.get("start", "")),
            str(edit.get("end", "")),
            str(edit.get("source_text", "")),
            str(edit.get("target_text", "")),
            str(edit.get("operation", "")),
        ]
    )


def candidate_type(row: dict[str, Any]) -> str:
    return str(row.get("original_candidate_type") or row.get("candidate_type") or "unknown")


def operation(row: dict[str, Any]) -> str:
    edit = row.get("model_edit") or {}
    return str(edit.get("operation") or row.get("operation") or "unknown")


def diversity_value(row: dict[str, Any], field: str) -> str:
    if field == "operation":
        return operation(row)
    if field == "original_candidate_type":
        return candidate_type(row)
    return str(row.get(field) or "unknown")


def row_with_probe_metadata(row: dict[str, Any]) -> dict[str, Any]:
    checks = refine.evidence_checks_for_record(row)
    output = dict(row)
    output["operation"] = operation(row)
    output["probe_selection_reason"] = "remaining_missing_contextual_evidence_after_canonicalization"
    output["probe_evidence_checks"] = checks
    output["probe_group_key"] = group_key(row)
    return output


def eligible_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    eligible: list[dict[str, Any]] = []
    for row in rows:
        checks = refine.evidence_checks_for_record(row)
        if checks.get("missing_evidence") or checks.get("wrong_evidence_auto") or checks.get("evidence_text_found_in_prediction_only"):
            enriched = dict(row)
            enriched["operation"] = operation(row)
            eligible.append(enriched)
    return eligible


def severity(row: dict[str, Any]) -> int:
    checks = refine.evidence_checks_for_record(row)
    return int(bool(checks.get("wrong_evidence_auto"))) + int(bool(checks.get("evidence_text_found_in_prediction_only"))) + int(
        bool(checks.get("missing_evidence"))
    )


def diversity_score(row: dict[str, Any], counters: dict[str, Counter[str]], used_groups: set[str]) -> float:
    if group_key(row) in used_groups:
        return -1_000_000.0
    score = float(severity(row))
    for field in DIVERSITY_FIELDS:
        value = diversity_value(row, field)
        score += 1.0 / (1.0 + counters[field][str(value)])
    return score


def select_probe(rows: list[dict[str, Any]], limit: int, seed: int) -> list[dict[str, Any]]:
    candidates = eligible_rows(rows)
    rng = random.Random(seed)
    rng.shuffle(candidates)
    selected: list[dict[str, Any]] = []
    used_groups: set[str] = set()
    counters: dict[str, Counter[str]] = {field: Counter() for field in DIVERSITY_FIELDS}

    while candidates and len(selected) < limit:
        best = max(
            candidates,
            key=lambda row: (
                diversity_score(row, counters, used_groups),
                str(row.get("candidate_id", "")),
            ),
        )
        if group_key(best) in used_groups:
            break
        selected.append(row_with_probe_metadata(best))
        used_groups.add(group_key(best))
        for field in DIVERSITY_FIELDS:
            value = diversity_value(best, field)
            counters[field][str(value)] += 1
        candidates = [row for row in candidates if group_key(row) not in used_groups]

    return selected


def count_by(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        value = diversity_value(row, field)
        counter[str(value)] += 1
    return dict(sorted(counter.items()))


def summarize(rows: list[dict[str, Any]], eligible: list[dict[str, Any]], selected: list[dict[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    checks = [refine.evidence_checks_for_record(row) for row in rows]
    eligible_checks = [refine.evidence_checks_for_record(row) for row in eligible]
    selected_checks = [refine.evidence_checks_for_record(row) for row in selected]

    def count(items: list[dict[str, Any]], key: str) -> int:
        return sum(1 for item in items if item.get(key))

    return {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "seed": args.seed,
        "limit": args.limit,
        "input_file": str(resolve(args.input)),
        "output_file": str(resolve(args.output)),
        "input_count": len(rows),
        "eligible_candidate_count": len(eligible),
        "eligible_edit_group_count": len({group_key(row) for row in eligible}),
        "selected_candidate_count": len(selected),
        "selected_edit_group_count": len({group_key(row) for row in selected}),
        "input_evidence_flags": {
            "contextual_source_evidence": count(checks, "evidence_contextual"),
            "missing_evidence": count(checks, "missing_evidence"),
            "prediction_only_evidence": count(checks, "evidence_text_found_in_prediction_only"),
            "wrong_evidence_auto": count(checks, "wrong_evidence_auto"),
        },
        "eligible_evidence_flags": {
            "contextual_source_evidence": count(eligible_checks, "evidence_contextual"),
            "missing_evidence": count(eligible_checks, "missing_evidence"),
            "prediction_only_evidence": count(eligible_checks, "evidence_text_found_in_prediction_only"),
            "wrong_evidence_auto": count(eligible_checks, "wrong_evidence_auto"),
        },
        "selected_evidence_flags": {
            "contextual_source_evidence": count(selected_checks, "evidence_contextual"),
            "missing_evidence": count(selected_checks, "missing_evidence"),
            "prediction_only_evidence": count(selected_checks, "evidence_text_found_in_prediction_only"),
            "wrong_evidence_auto": count(selected_checks, "wrong_evidence_auto"),
        },
        "selected_breakdown": {field: count_by(selected, field) for field in DIVERSITY_FIELDS},
        "selected_candidate_ids": [str(row.get("candidate_id")) for row in selected],
        "decision": "run_targeted_qwen3_refinement_probe_before_scaling",
    }


def markdown(summary: dict[str, Any], selected: list[dict[str, Any]]) -> str:
    lines = [
        "# Qwen3 Evidence Refinement Probe20 Card",
        "",
        "## Loop",
        "",
        "- Loop ID: Loop D / 20-edit canonicalization-plus-refinement probe.",
        "- Bottleneck: 78/160 canonicalized Qwen3 candidates still lack contextual source evidence or retain evidence-risk flags.",
        "- Hypothesis: targeted Qwen3 refinement may repair a stratified subset of remaining evidence failures beyond deterministic span canonicalization.",
        "- Success criterion: refined+canonicalized outputs improve contextual source evidence without increasing prediction-only evidence or edit-copy-only behavior.",
        "- Failure criterion: refinement clears evidence or changes wording without adding source-grounded contextual evidence.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Selected Rows", ""])
    for row in selected:
        parsed = row.get("parsed_output") or {}
        edit = row.get("model_edit") or {}
        lines.extend(
            [
                f"### {row.get('candidate_id')}",
                "",
                f"- dataset/model: `{row.get('dataset')}` / `{row.get('model_key')}`",
                f"- split/type/op: `{row.get('rulefaith_split')}` / `{candidate_type(row)}` / `{operation(row)}`",
                f"- edit: `{edit}`",
                f"- checks: `{row.get('probe_evidence_checks')}`",
                f"- rule: {parsed.get('rule_text', '')}",
                f"- evidence: `{json.dumps(parsed.get('evidence_spans', []), ensure_ascii=False, sort_keys=True)}`",
                "",
            ]
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a stratified 20-edit probe from remaining Qwen3 evidence failures.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stats-output", type=Path, default=DEFAULT_STATS)
    parser.add_argument("--card-output", type=Path, default=DEFAULT_CARD)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260720)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.limit <= 0:
        raise ValueError("--limit must be positive")
    rows = read_jsonl(resolve(args.input))
    ids = [row.get("candidate_id") for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate candidate_id in input")
    eligible = eligible_rows(rows)
    selected = select_probe(rows, args.limit, args.seed)
    if len(selected) < min(args.limit, len({group_key(row) for row in eligible})):
        raise RuntimeError("Probe selection ended before reaching the requested unique-edit limit")
    summary = summarize(rows, eligible, selected, args)
    write_jsonl(resolve(args.output), selected, args.overwrite)
    write_json(resolve(args.stats_output), summary, args.overwrite)
    write_text(resolve(args.card_output), markdown(summary, selected), args.overwrite)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
