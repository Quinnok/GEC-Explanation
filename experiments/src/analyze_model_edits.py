from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import errant

from edit_schema import Edit, span_positions


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PREDICTIONS = ROOT / "results" / "model_predictions" / "expect_v1_model_predictions.jsonl"
DEFAULT_OUT_DIR = ROOT / "results" / "model_edits"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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


def errant_operation(start: int, end: int, c_start: int, c_end: int) -> str:
    if start == end and c_start < c_end:
        return "insert"
    if start < end and c_start == c_end:
        return "delete"
    return "replace"


def errant_edit_to_dict(edit: Any) -> Dict[str, Any]:
    return Edit(
        start=int(edit.o_start),
        end=int(edit.o_end),
        source_text=str(edit.o_str).strip(),
        target_text=str(edit.c_str).strip(),
        operation=errant_operation(edit.o_start, edit.o_end, edit.c_start, edit.c_end),
        error_type=str(edit.type),
    ).to_dict()


def extract_edits(annotator: Any, source: str, target: str) -> List[Dict[str, Any]]:
    if source.strip() == target.strip():
        return []
    original = annotator.parse(source)
    corrected = annotator.parse(target)
    return [errant_edit_to_dict(edit) for edit in annotator.annotate(original, corrected) if edit.type != "noop"]


def edit_signature(edit: Dict[str, Any], include_type: bool = False) -> Tuple[Any, ...]:
    base = (
        int(edit["start"]),
        int(edit["end"]),
        edit.get("source_text", ""),
        edit.get("target_text", ""),
        edit.get("operation", ""),
    )
    if include_type:
        return (*base, edit.get("error_type", "UNK"))
    return base


def span_f1(pred: Dict[str, Any], ref: Dict[str, Any]) -> float:
    pred_set = span_positions(Edit.from_dict(pred))
    ref_set = span_positions(Edit.from_dict(ref))
    if not pred_set and not ref_set:
        return 1.0
    if not pred_set or not ref_set:
        return 0.0
    overlap = len(pred_set & ref_set)
    if overlap == 0:
        return 0.0
    precision = overlap / len(pred_set)
    recall = overlap / len(ref_set)
    return 2 * precision * recall / (precision + recall)


def align_score(pred: Dict[str, Any], ref: Dict[str, Any]) -> float:
    score = span_f1(pred, ref)
    if pred["start"] == ref["start"]:
        score = max(score, 0.51)
    if pred.get("source_text") and pred.get("source_text") == ref.get("source_text"):
        score = max(score, 0.75)
    return score


def exact_match(pred: Dict[str, Any], ref: Dict[str, Any]) -> bool:
    return edit_signature(pred) == edit_signature(ref)


def align_predicted_edits(
    ref_edits: Sequence[Dict[str, Any]],
    pred_edits: Sequence[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    matched_refs: set[int] = set()
    alignments: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []

    for pred_index, pred in enumerate(pred_edits):
        exact_candidates = [
            idx for idx, ref in enumerate(ref_edits) if idx not in matched_refs and exact_match(pred, ref)
        ]
        if exact_candidates:
            ref_index = exact_candidates[0]
            matched_refs.add(ref_index)
            alignments.append(
                {
                    "pred_index": pred_index,
                    "ref_index": ref_index,
                    "behavior": "correct_correction",
                    "score": 1.0,
                    "predicted_edit": pred,
                    "reference_edit": ref_edits[ref_index],
                }
            )
            continue

        scored = [
            (idx, align_score(pred, ref))
            for idx, ref in enumerate(ref_edits)
            if idx not in matched_refs
        ]
        scored = [(idx, score) for idx, score in scored if score > 0.0]
        if not scored:
            alignments.append(
                {
                    "pred_index": pred_index,
                    "ref_index": None,
                    "behavior": "overcorrection",
                    "score": 0.0,
                    "predicted_edit": pred,
                    "reference_edit": None,
                }
            )
            continue

        scored.sort(key=lambda item: item[1], reverse=True)
        best_score = scored[0][1]
        tied = [idx for idx, score in scored if score == best_score]
        if len(tied) > 1:
            failures.append(
                {
                    "kind": "ambiguous_alignment",
                    "pred_index": pred_index,
                    "candidate_ref_indices": tied,
                    "score": best_score,
                    "predicted_edit": pred,
                }
            )
        ref_index = scored[0][0]
        matched_refs.add(ref_index)
        alignments.append(
            {
                "pred_index": pred_index,
                "ref_index": ref_index,
                "behavior": "wrong_correction",
                "score": best_score,
                "predicted_edit": pred,
                "reference_edit": ref_edits[ref_index],
            }
        )

    missed = [
        {
            "ref_index": idx,
            "behavior": "missed_correction",
            "reference_edit": ref,
        }
        for idx, ref in enumerate(ref_edits)
        if idx not in matched_refs
    ]
    return alignments, missed, failures


def model_edit_record(row: Dict[str, Any], alignment: Dict[str, Any]) -> Dict[str, Any]:
    ref_edit = alignment["reference_edit"]
    predicted_edit = alignment["predicted_edit"]
    error_type = ref_edit["error_type"] if ref_edit else predicted_edit["error_type"]
    return {
        "sample_id": row["sample_id"],
        "source": row["source"],
        "reference": row["reference"],
        "prediction": row["prediction"],
        "model": row["model"],
        "model_key": row["model_key"],
        "model_family": row["model_family"],
        "model_id": row["model_id"],
        "model_version": row["model_version"],
        "decoding_config": row["decoding_config"],
        "predicted_edit": predicted_edit,
        "aligned_reference_edit": ref_edit,
        "alignment_score": alignment["score"],
        "behavior": alignment["behavior"],
        "error_type": error_type,
    }


def missing_record(row: Dict[str, Any], missed: Dict[str, Any]) -> Dict[str, Any]:
    ref_edit = missed["reference_edit"]
    return {
        "sample_id": row["sample_id"],
        "source": row["source"],
        "reference": row["reference"],
        "prediction": row["prediction"],
        "model": row["model"],
        "model_key": row["model_key"],
        "model_family": row["model_family"],
        "model_id": row["model_id"],
        "model_version": row["model_version"],
        "decoding_config": row["decoding_config"],
        "reference_edit": ref_edit,
        "behavior": "missed_correction",
        "error_type": ref_edit["error_type"],
    }


def render_check_sample(index: int, row: Dict[str, Any], ref_edits: List[Dict[str, Any]], pred_edits: List[Dict[str, Any]], alignments: List[Dict[str, Any]], missed: List[Dict[str, Any]]) -> List[str]:
    compact_alignments = [
        {
            "pred_index": item["pred_index"],
            "ref_index": item["ref_index"],
            "behavior": item["behavior"],
            "score": round(item["score"], 3),
        }
        for item in alignments
    ]
    return [
        f"## {index}. {row['model_key']}::{row['sample_id']}",
        "",
        f"- Source: `{row['source']}`",
        f"- Reference: `{row['reference']}`",
        f"- Prediction: `{row['prediction']}`",
        f"- Reference edits: `{json.dumps(ref_edits, ensure_ascii=False)}`",
        f"- Predicted edits: `{json.dumps(pred_edits, ensure_ascii=False)}`",
        f"- Alignment: `{json.dumps(compact_alignments, ensure_ascii=False)}`",
        f"- Missed edits: `{json.dumps(missed, ensure_ascii=False)}`",
        "",
    ]


def summarize(
    model_edit_rows: List[Dict[str, Any]],
    missing_rows: List[Dict[str, Any]],
    per_sentence_rows: List[Dict[str, Any]],
    failures: List[Dict[str, Any]],
) -> Dict[str, Any]:
    model_behavior: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    type_behavior: Dict[str, Dict[str, Dict[str, int]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for row in model_edit_rows:
        model_behavior[row["model_key"]][row["behavior"]] += 1
        type_behavior[row["model_key"]][row["error_type"]][row["behavior"]] += 1
    for row in missing_rows:
        model_behavior[row["model_key"]][row["behavior"]] += 1
        type_behavior[row["model_key"]][row["error_type"]][row["behavior"]] += 1

    sentence_counts = defaultdict(lambda: {"sentences": 0, "changed_sentences": 0})
    for row in per_sentence_rows:
        item = sentence_counts[row["model_key"]]
        item["sentences"] += 1
        if row["pred_edit_count"] > 0:
            item["changed_sentences"] += 1

    return {
        "created_at": utc_now(),
        "model_edit_count": len(model_edit_rows),
        "missing_edit_count": len(missing_rows),
        "per_sentence_count": len(per_sentence_rows),
        "model_behavior_distribution": {model: dict(counts) for model, counts in model_behavior.items()},
        "error_type_behavior_distribution": {
            model: {etype: dict(counts) for etype, counts in etypes.items()}
            for model, etypes in type_behavior.items()
        },
        "sentence_counts": dict(sentence_counts),
        "alignment_failure_count": len(failures),
        "alignment_failure_examples": failures[:30],
        "alignment_policy": "Predicted edits are correct when span/source/target/operation match an unmatched reference edit. Non-exact overlapping edits are wrong corrections. Predicted edits with no aligned reference edit are overcorrections. Unmatched reference edits are missed corrections.",
    }


def analyze(args: argparse.Namespace) -> None:
    annotator = errant.load("en")
    predictions = read_jsonl(args.predictions)
    model_keys = sorted({row["model_key"] for row in predictions})
    per_model_check_limit = max(1, args.check_size // max(1, len(model_keys)))
    check_counts: Counter[str] = Counter()
    rendered_checks = 0
    model_edit_rows: List[Dict[str, Any]] = []
    missing_rows: List[Dict[str, Any]] = []
    per_sentence_rows: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []
    report_lines = [
        "# Model Edit Alignment Check",
        "",
        "This report compares source-reference ERRANT edits against source-prediction ERRANT edits for real model outputs.",
        "",
    ]

    for idx, row in enumerate(predictions):
        ref_edits = extract_edits(annotator, row["source"], row["reference"])
        pred_edits = extract_edits(annotator, row["source"], row["prediction"])
        alignments, missed, row_failures = align_predicted_edits(ref_edits, pred_edits)
        for failure in row_failures:
            failures.append({"sample_id": row["sample_id"], "model_key": row["model_key"], **failure})
        model_edit_rows.extend(model_edit_record(row, alignment) for alignment in alignments)
        missing_rows.extend(missing_record(row, item) for item in missed)
        per_sentence_rows.append(
            {
                "sample_id": row["sample_id"],
                "model_key": row["model_key"],
                "model": row["model"],
                "source": row["source"],
                "reference": row["reference"],
                "prediction": row["prediction"],
                "ref_edit_count": len(ref_edits),
                "pred_edit_count": len(pred_edits),
                "alignment_counts": dict(Counter(item["behavior"] for item in alignments) + Counter(item["behavior"] for item in missed)),
            }
        )
        if check_counts[row["model_key"]] < per_model_check_limit and rendered_checks < args.check_size:
            rendered_checks += 1
            check_counts[row["model_key"]] += 1
            report_lines.extend(render_check_sample(rendered_checks, row, ref_edits, pred_edits, alignments, missed))

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "model_edit_dataset.jsonl", model_edit_rows)
    write_jsonl(args.out_dir / "missing_edit_diagnosis.jsonl", missing_rows)
    write_jsonl(args.out_dir / "per_sentence_alignment.jsonl", per_sentence_rows)
    write_jsonl(args.out_dir / "alignment_failures.jsonl", failures)
    summary = summarize(model_edit_rows, missing_rows, per_sentence_rows, failures)
    write_json(args.out_dir / "behavior_summary.json", summary)
    (args.out_dir / "model_edit_alignment_check_30.md").write_text("\n".join(report_lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ERRANT alignment and behavior classification for model predictions.")
    parser.add_argument("--predictions", type=Path, default=DEFAULT_PREDICTIONS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--check-size", type=int, default=30)
    return parser.parse_args()


if __name__ == "__main__":
    analyze(parse_args())
