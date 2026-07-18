from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import errant

from analyze_model_edits import edit_signature, exact_match, extract_edits, span_f1


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PREDICTIONS = ROOT / "results" / "model_predictions" / "expect_v1_model_predictions.jsonl"
DEFAULT_OUT_DIR = ROOT / "results" / "audit"


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def exact_only_align(ref_edits: Sequence[Dict[str, Any]], pred_edits: Sequence[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    matched_refs: set[int] = set()
    events = []
    for pred_index, pred in enumerate(pred_edits):
        match = next((idx for idx, ref in enumerate(ref_edits) if idx not in matched_refs and exact_match(pred, ref)), None)
        if match is None:
            events.append({"pred_index": pred_index, "ref_index": None, "behavior": "overcorrection", "score": 0.0, "predicted_edit": pred, "reference_edit": None})
        else:
            matched_refs.add(match)
            events.append({"pred_index": pred_index, "ref_index": match, "behavior": "correct_correction", "score": 1.0, "predicted_edit": pred, "reference_edit": ref_edits[match]})
    events.extend(
        {"pred_index": None, "ref_index": idx, "behavior": "missed_correction", "score": 0.0, "predicted_edit": None, "reference_edit": ref}
        for idx, ref in enumerate(ref_edits)
        if idx not in matched_refs
    )
    return events, []


def stable_score(pred: Dict[str, Any], ref: Dict[str, Any]) -> float:
    score = 0.45 * span_f1(pred, ref)
    score += 0.20 if pred.get("source_text") and pred.get("source_text") == ref.get("source_text") else 0.0
    score += 0.15 if pred.get("target_text") and pred.get("target_text") == ref.get("target_text") else 0.0
    score += 0.10 if pred.get("operation") == ref.get("operation") else 0.0
    score += 0.05 if pred.get("error_type") == ref.get("error_type") else 0.0
    score += 0.05 if pred.get("start") == ref.get("start") else 0.0
    return min(score, 1.0)


def relation_kind(pred: Dict[str, Any], ref: Dict[str, Any]) -> str:
    if exact_match(pred, ref):
        return "exact_match"
    sf1 = span_f1(pred, ref)
    if sf1 > 0 and pred.get("source_text") == ref.get("source_text"):
        return "partial_span_same_source"
    if sf1 > 0:
        return "partial_span_overlap"
    if pred.get("start") == ref.get("start"):
        return "same_start_no_overlap"
    if abs(int(pred.get("start", 0)) - int(ref.get("start", 0))) <= 1:
        return "adjacent_edits"
    if pred.get("target_text") == ref.get("target_text") and pred.get("target_text"):
        return "equivalent_target_text"
    return "weak_or_no_relation"


def stable_align(ref_edits: Sequence[Dict[str, Any]], pred_edits: Sequence[Dict[str, Any]], threshold: float = 0.35) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    candidates = []
    for pred_index, pred in enumerate(pred_edits):
        for ref_index, ref in enumerate(ref_edits):
            score = stable_score(pred, ref)
            if score >= threshold:
                candidates.append((score, pred_index, ref_index, relation_kind(pred, ref)))
    candidates.sort(reverse=True)
    matched_preds: set[int] = set()
    matched_refs: set[int] = set()
    events = []
    failures = []
    for score, pred_index, ref_index, relation in candidates:
        if pred_index in matched_preds or ref_index in matched_refs:
            continue
        pred = pred_edits[pred_index]
        ref = ref_edits[ref_index]
        matched_preds.add(pred_index)
        matched_refs.add(ref_index)
        behavior = "correct_correction" if exact_match(pred, ref) else "wrong_correction"
        events.append(
            {
                "pred_index": pred_index,
                "ref_index": ref_index,
                "behavior": behavior,
                "score": round(score, 6),
                "relation": relation,
                "predicted_edit": pred,
                "reference_edit": ref,
            }
        )
    for pred_index, pred in enumerate(pred_edits):
        if pred_index not in matched_preds:
            events.append({"pred_index": pred_index, "ref_index": None, "behavior": "overcorrection", "score": 0.0, "relation": "unmatched_predicted_edit", "predicted_edit": pred, "reference_edit": None})
    for ref_index, ref in enumerate(ref_edits):
        if ref_index not in matched_refs:
            events.append({"pred_index": None, "ref_index": ref_index, "behavior": "missed_correction", "score": 0.0, "relation": "unmatched_reference_edit", "predicted_edit": None, "reference_edit": ref})
    for pred_index, pred in enumerate(pred_edits):
        tied = [(ref_index, stable_score(pred, ref)) for ref_index, ref in enumerate(ref_edits) if stable_score(pred, ref) >= threshold]
        if len(tied) > 1:
            failures.append({"kind": "one_pred_many_possible_refs", "pred_index": pred_index, "candidates": tied, "predicted_edit": pred})
    return events, failures


def count_behaviors(events: List[Dict[str, Any]]) -> Counter[str]:
    return Counter(event["behavior"] for event in events)


def classify_case(old_events: List[Dict[str, Any]], new_events: List[Dict[str, Any]], failures: List[Dict[str, Any]]) -> str:
    if failures:
        return "alignment_failure"
    if count_behaviors(old_events) != count_behaviors(new_events):
        if any(event.get("relation") == "partial_span_overlap" for event in new_events):
            return "partial_span_overlap"
        if any(event.get("relation") == "partial_span_same_source" for event in new_events):
            return "partial_span_same_source"
        if any(event.get("relation") == "adjacent_edits" for event in new_events):
            return "adjacent_edits"
        return "old_new_behavior_difference"
    if any(event["behavior"] == "correct_correction" for event in new_events):
        return "exact_match"
    if len([e for e in new_events if e["predicted_edit"]]) > 1 or len([e for e in new_events if e["reference_edit"]]) > 1:
        return "one_to_many_or_many_to_one_candidate"
    return "no_match_or_stable_same"


def render(cases: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
    lines = [
        "# Round 04 ERRANT Alignment Reliability Audit",
        "",
        "This researcher-readable audit compares an exact-only alignment strategy with a more stable partial-overlap strategy.",
        "",
        "## Summary",
        "",
        f"- Audited cases: {summary['audit_count']}",
        f"- Case kinds: `{json.dumps(summary['case_kind_counts'], sort_keys=True)}`",
        f"- Old behavior totals: `{json.dumps(summary['old_behavior_counts'], sort_keys=True)}`",
        f"- Stable behavior totals: `{json.dumps(summary['stable_behavior_counts'], sort_keys=True)}`",
        "",
    ]
    for idx, case in enumerate(cases, 1):
        lines.extend(
            [
                f"## {idx}. {case['model_key']}::{case['sample_id']} ({case['case_kind']})",
                "",
                f"- Source: `{case['source']}`",
                f"- Reference: `{case['reference']}`",
                f"- Prediction: `{case['prediction']}`",
                f"- Reference edits: `{json.dumps(case['reference_edits'], ensure_ascii=False)}`",
                f"- Predicted edits: `{json.dumps(case['predicted_edits'], ensure_ascii=False)}`",
                f"- Exact-only events: `{json.dumps(case['exact_only_events'], ensure_ascii=False)}`",
                f"- Stable events: `{json.dumps(case['stable_events'], ensure_ascii=False)}`",
                f"- Alignment failures: `{json.dumps(case['stable_failures'], ensure_ascii=False)}`",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def run(args: argparse.Namespace) -> None:
    annotator = errant.load("en")
    all_cases = []
    old_counts: Counter[str] = Counter()
    stable_counts: Counter[str] = Counter()
    for row in read_jsonl(args.predictions):
        ref_edits = extract_edits(annotator, row["source"], row["reference"])
        pred_edits = extract_edits(annotator, row["source"], row["prediction"])
        old_events, _ = exact_only_align(ref_edits, pred_edits)
        new_events, failures = stable_align(ref_edits, pred_edits)
        old_counts.update(count_behaviors(old_events))
        stable_counts.update(count_behaviors(new_events))
        case_kind = classify_case(old_events, new_events, failures)
        all_cases.append(
            {
                "sample_id": row["sample_id"],
                "model_key": row["model_key"],
                "source": row["source"],
                "reference": row["reference"],
                "prediction": row["prediction"],
                "reference_edits": ref_edits,
                "predicted_edits": pred_edits,
                "exact_only_events": old_events,
                "stable_events": new_events,
                "stable_failures": failures,
                "case_kind": case_kind,
            }
        )
    priority = ["alignment_failure", "partial_span_same_source", "partial_span_overlap", "adjacent_edits", "old_new_behavior_difference", "one_to_many_or_many_to_one_candidate", "exact_match", "no_match_or_stable_same"]
    selected = []
    used = set()
    per_kind = max(1, args.count // len(priority))
    for kind in priority:
        for case in all_cases:
            if len(selected) >= args.count:
                break
            key = (case["sample_id"], case["model_key"])
            if key not in used and case["case_kind"] == kind:
                selected.append(case)
                used.add(key)
                if sum(1 for item in selected if item["case_kind"] == kind) >= per_kind:
                    break
    for case in all_cases:
        if len(selected) >= args.count:
            break
        key = (case["sample_id"], case["model_key"])
        if key not in used:
            selected.append(case)
            used.add(key)
    summary = {
        "audit_count": len(selected),
        "case_kind_counts": dict(Counter(case["case_kind"] for case in selected)),
        "old_behavior_counts": dict(old_counts),
        "stable_behavior_counts": dict(stable_counts),
        "alignment_strategy": "Stable strategy greedily matches predicted/reference edits by span F1, source text, target text, operation, type, and same-start bonuses; exact signatures remain correct corrections, non-exact matches are wrong corrections.",
        "old_strategy": "Exact-only matching: only exact span/source/target/operation matches are correct; all other predicted edits are overcorrections and all unmatched reference edits are missed corrections.",
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "alignment_reliability_audit_50.jsonl", selected)
    write_json(args.out_dir / "alignment_reliability_summary.json", summary)
    (args.out_dir / "alignment_reliability_audit_50.md").write_text(render(selected, summary))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare exact-only and stable ERRANT edit alignment strategies.")
    parser.add_argument("--predictions", type=Path, default=DEFAULT_PREDICTIONS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--count", type=int, default=50)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
