from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.rulefaith import build_qwen3_manual_audit as audit
from experiments.rulefaith import refine_qwen3_evidence as refine


DEFAULT_BASELINE = ROOT / "data" / "rulefaith" / "qwen3_evidence_refinement_probe20.jsonl"
DEFAULT_REFINED = ROOT / "results" / "rulefaith" / "qwen3_evidence_refinement_probe20_refined_candidates.jsonl"
DEFAULT_REFINED_CANON = ROOT / "results" / "rulefaith" / "qwen3_evidence_refinement_probe20_refined_canonicalized_candidates.jsonl"
DEFAULT_OUTPUT = ROOT / "results" / "rulefaith" / "qwen3_evidence_refinement_probe20_comparison.json"
DEFAULT_MD = ROOT / "results" / "rulefaith" / "qwen3_evidence_refinement_probe20_comparison.md"


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


def base_id(row: dict[str, Any]) -> str:
    current = str(row.get("candidate_id") or "")
    original = str(row.get("original_candidate_id") or "")
    if "::evidence_refined" in current:
        return current.split("::evidence_refined", 1)[0]
    if "::evidence_refined" in original:
        return original.split("::evidence_refined", 1)[0]
    if current.endswith("::evidence_canonicalized"):
        return current
    return original or current


def checks(row: dict[str, Any]) -> dict[str, Any]:
    return refine.evidence_checks_for_record(row)


def count_flags(rows: list[dict[str, Any]]) -> dict[str, int]:
    all_checks = [checks(row) for row in rows]

    def count(key: str) -> int:
        return sum(1 for item in all_checks if item.get(key))

    return {
        "contextual_source_evidence": count("evidence_contextual"),
        "missing_evidence": count("missing_evidence"),
        "prediction_only_evidence": count("evidence_text_found_in_prediction_only"),
        "wrong_evidence_auto": count("wrong_evidence_auto"),
        "all_spans_source_index_match": count("evidence_all_spans_source_index_match"),
    }


def row_summary(row: dict[str, Any]) -> dict[str, Any]:
    parsed = row.get("parsed_output") or {}
    return {
        "candidate_id": row.get("candidate_id"),
        "original_candidate_id": row.get("original_candidate_id"),
        "dataset": row.get("dataset"),
        "model_key": row.get("model_key"),
        "rulefaith_split": row.get("rulefaith_split"),
        "candidate_type": row.get("candidate_type"),
        "original_candidate_type": row.get("original_candidate_type"),
        "checks": checks(row),
        "rule_text": parsed.get("rule_text", ""),
        "evidence_spans": parsed.get("evidence_spans", []),
        "abstain": parsed.get("abstain", False),
        "confidence": parsed.get("confidence", None),
    }


def compare_rows(baseline: list[dict[str, Any]], refined: list[dict[str, Any]], refined_canon: list[dict[str, Any]]) -> dict[str, Any]:
    refined_by_base = {base_id(row): row for row in refined}
    canon_by_base = {base_id(row): row for row in refined_canon}
    missing_refined = [row.get("candidate_id") for row in baseline if row.get("candidate_id") not in refined_by_base]
    missing_canon = [row.get("candidate_id") for row in baseline if row.get("candidate_id") not in canon_by_base]
    cases: list[dict[str, Any]] = []
    transitions: Counter[str] = Counter()
    for row in baseline:
        cid = str(row.get("candidate_id"))
        refined_row = refined_by_base.get(cid)
        canon_row = canon_by_base.get(cid)
        if not refined_row or not canon_row:
            continue
        before = checks(row)
        after_refined = checks(refined_row)
        after_canon = checks(canon_row)
        transition = (
            f"ctx:{int(bool(before['evidence_contextual']))}->{int(bool(after_refined['evidence_contextual']))}"
            f"->{int(bool(after_canon['evidence_contextual']))};"
            f"wrong:{int(bool(before['wrong_evidence_auto']))}->{int(bool(after_refined['wrong_evidence_auto']))}"
            f"->{int(bool(after_canon['wrong_evidence_auto']))}"
        )
        transitions[transition] += 1
        cases.append(
            {
                "base_candidate_id": cid,
                "baseline": row_summary(row),
                "refined": row_summary(refined_row),
                "refined_canonicalized": row_summary(canon_row),
            }
        )
    return {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "counts": {
            "baseline": len(baseline),
            "refined": len(refined),
            "refined_canonicalized": len(refined_canon),
            "aligned_triples": len(cases),
        },
        "coverage": {
            "missing_refined_candidate_ids": missing_refined,
            "missing_refined_canonicalized_candidate_ids": missing_canon,
        },
        "flag_counts": {
            "canonicalized_only": count_flags(baseline),
            "qwen3_refined": count_flags(refined),
            "qwen3_refined_then_canonicalized": count_flags(refined_canon),
        },
        "transition_counts": dict(sorted(transitions.items())),
        "cases": cases,
    }


def markdown(report: dict[str, Any]) -> str:
    counts = report["counts"]
    flags = report["flag_counts"]
    lines = [
        "# Qwen3 Evidence Refinement Probe20 Comparison",
        "",
        "This report compares the same 20 canonicalized evidence-failure candidates before refinement, after Qwen3 targeted refinement, and after re-canonicalizing refined outputs.",
        "",
        "## Summary",
        "",
        f"- aligned triples: `{counts['aligned_triples']}/{counts['baseline']}`",
        f"- canonicalized only: `{flags['canonicalized_only']}`",
        f"- Qwen3 refined: `{flags['qwen3_refined']}`",
        f"- Qwen3 refined then canonicalized: `{flags['qwen3_refined_then_canonicalized']}`",
        f"- transition counts: `{report['transition_counts']}`",
        "",
        "## Decision",
        "",
    ]
    before_ctx = flags["canonicalized_only"]["contextual_source_evidence"]
    after_ctx = flags["qwen3_refined_then_canonicalized"]["contextual_source_evidence"]
    before_wrong = flags["canonicalized_only"]["wrong_evidence_auto"]
    after_wrong = flags["qwen3_refined_then_canonicalized"]["wrong_evidence_auto"]
    if after_ctx > before_ctx and after_wrong <= before_wrong:
        lines.append("Keep this refinement direction for a larger manually audited pilot, but do not treat the outputs as positives until human audit passes.")
    else:
        lines.append("Do not scale this refinement prompt yet; it does not improve strict contextual evidence over canonicalized-only outputs.")
    lines.extend(["", "## Cases", ""])
    for case in report["cases"]:
        lines.extend(
            [
                f"### {case['base_candidate_id']}",
                "",
                f"- baseline checks: `{case['baseline']['checks']}`",
                f"- refined checks: `{case['refined']['checks']}`",
                f"- refined+canonicalized checks: `{case['refined_canonicalized']['checks']}`",
                f"- refined rule: {case['refined']['rule_text']}",
                f"- refined evidence: `{json.dumps(case['refined']['evidence_spans'], ensure_ascii=False, sort_keys=True)}`",
                "",
            ]
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare canonicalized-only and Qwen3-refined evidence probe outputs.")
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--refined", type=Path, default=DEFAULT_REFINED)
    parser.add_argument("--refined-canonicalized", type=Path, default=DEFAULT_REFINED_CANON)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--md-output", type=Path, default=DEFAULT_MD)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    baseline = read_jsonl(resolve(args.baseline))
    refined = read_jsonl(resolve(args.refined))
    refined_canon = read_jsonl(resolve(args.refined_canonicalized))
    report = compare_rows(baseline, refined, refined_canon)
    write_json(resolve(args.output), report, args.overwrite)
    write_text(resolve(args.md_output), markdown(report), args.overwrite)
    print(json.dumps({key: report[key] for key in ("counts", "flag_counts", "transition_counts")}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
