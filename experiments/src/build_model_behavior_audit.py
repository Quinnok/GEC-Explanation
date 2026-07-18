from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import errant

from analyze_model_edits import align_predicted_edits, extract_edits


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


def compact_alignment(alignments: List[Dict[str, Any]], missed: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = [
        {
            "pred_index": item["pred_index"],
            "ref_index": item["ref_index"],
            "behavior": item["behavior"],
            "score": round(float(item["score"]), 3),
            "predicted_edit": item["predicted_edit"],
            "reference_edit": item["reference_edit"],
        }
        for item in alignments
    ]
    rows.extend(
        {
            "pred_index": None,
            "ref_index": item["ref_index"],
            "behavior": "missed_correction",
            "score": 0.0,
            "predicted_edit": None,
            "reference_edit": item["reference_edit"],
        }
        for item in missed
    )
    return rows


def noise_flag(edit: Dict[str, Any] | None) -> bool:
    if not edit:
        return False
    if "ORTH" in edit["error_type"] or "PUNCT" in edit["error_type"]:
        return True
    source = re.sub(r"[\s`'\".,!?;:()\[\]{}-]+", "", edit.get("source_text", "").lower())
    target = re.sub(r"[\s`'\".,!?;:()\[\]{}-]+", "", edit.get("target_text", "").lower())
    return source == target and edit.get("source_text", "") != edit.get("target_text", "")


def span_mismatch(source: str, edit: Dict[str, Any] | None) -> bool:
    if not edit or edit["operation"] == "insert":
        return False
    span = " ".join(source.split()[int(edit["start"]) : int(edit["end"])])
    return " ".join(span.split()).lower() != " ".join(edit.get("source_text", "").split()).lower()


def sentence_length_bucket(source: str) -> str:
    length = len(source.split())
    if length < 15:
        return "short"
    if length > 45:
        return "long"
    return "medium"


def make_event_records(row: Dict[str, Any], ref_edits: List[Dict[str, Any]], pred_edits: List[Dict[str, Any]], alignments: List[Dict[str, Any]], missed: List[Dict[str, Any]], failures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    compact = compact_alignment(alignments, missed)
    records = []
    for event_index, event in enumerate(compact):
        edit = event["predicted_edit"] or event["reference_edit"]
        records.append(
            {
                "audit_type": "researcher_readable_automatic_audit_not_human_annotation",
                "record_id": f"{row['sample_id']}::{row['model_key']}::{event_index}::{event['behavior']}",
                "sample_id": row["sample_id"],
                "model_key": row["model_key"],
                "model": row["model"],
                "source": row["source"],
                "reference": row["reference"],
                "prediction": row["prediction"],
                "gold_edits": ref_edits,
                "predicted_edits": pred_edits,
                "alignment": compact,
                "behavior": event["behavior"],
                "error_type": edit["error_type"],
                "operation": edit["operation"],
                "event_edit": edit,
                "aligned_reference_edit": event["reference_edit"],
                "predicted_edit": event["predicted_edit"],
                "multi_reference_equivalent_correction": "unknown_single_reference_only",
                "errant_boundary_issue_auto": span_mismatch(row["source"], event["predicted_edit"]) or span_mismatch(row["source"], event["reference_edit"]),
                "model_format_noise_auto": noise_flag(event["predicted_edit"]) or noise_flag(event["reference_edit"]),
                "suitable_for_explanation_experiment_auto": event["behavior"] != "missed_correction" and not noise_flag(event["predicted_edit"]),
                "single_or_multi_edit_sentence": "multi_edit" if len(ref_edits) > 1 or len(pred_edits) > 1 else "single_edit",
                "sentence_length_bucket": sentence_length_bucket(row["source"]),
                "alignment_failure_in_sentence": bool(failures),
            }
        )
    return records


def select(records: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
    selected: List[Dict[str, Any]] = []
    used: set[str] = set()

    def add_matching(predicate, limit: int) -> None:
        for record in records:
            if len(selected) >= count or limit <= 0:
                break
            if record["record_id"] not in used and predicate(record):
                selected.append(record)
                used.add(record["record_id"])
                limit -= 1

    strata = [(model, behavior) for model in sorted({r["model_key"] for r in records}) for behavior in ["correct_correction", "wrong_correction", "overcorrection", "missed_correction"]]
    per_stratum = max(1, count // max(1, len(strata)))
    for model, behavior in strata:
        add_matching(lambda r, m=model, b=behavior: r["model_key"] == m and r["behavior"] == b, per_stratum)

    for op in ["replace", "insert", "delete"]:
        add_matching(lambda r, op=op: r["operation"] == op, 3)
    for flag in [True, False]:
        add_matching(lambda r, flag=flag: r["model_format_noise_auto"] == flag, 8)
    for bucket in ["short", "long"]:
        add_matching(lambda r, bucket=bucket: r["sentence_length_bucket"] == bucket, 5)
    for mode in ["single_edit", "multi_edit"]:
        add_matching(lambda r, mode=mode: r["single_or_multi_edit_sentence"] == mode, 8)

    common_types = [etype for etype, _ in Counter(r["error_type"] for r in records).most_common(12)]
    for etype in common_types:
        add_matching(lambda r, etype=etype: r["error_type"] == etype, 2)

    for record in records:
        if len(selected) >= count:
            break
        if record["record_id"] not in used:
            selected.append(record)
            used.add(record["record_id"])
    return selected[:count]


def summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    correct = sum(1 for row in rows if row["behavior"] == "correct_correction")
    wrong = sum(1 for row in rows if row["behavior"] == "wrong_correction")
    over = sum(1 for row in rows if row["behavior"] == "overcorrection")
    missed = sum(1 for row in rows if row["behavior"] == "missed_correction")
    return {
        "audit_type": "researcher_readable_automatic_audit_not_human_annotation",
        "audit_count": len(rows),
        "model_counts": dict(Counter(row["model_key"] for row in rows)),
        "behavior_counts": dict(Counter(row["behavior"] for row in rows)),
        "operation_counts": dict(Counter(row["operation"] for row in rows)),
        "error_type_counts": dict(Counter(row["error_type"] for row in rows).most_common(30)),
        "sentence_length_buckets": dict(Counter(row["sentence_length_bucket"] for row in rows)),
        "single_multi_counts": dict(Counter(row["single_or_multi_edit_sentence"] for row in rows)),
        "model_format_noise_count": sum(1 for row in rows if row["model_format_noise_auto"]),
        "errant_boundary_issue_count": sum(1 for row in rows if row["errant_boundary_issue_auto"]),
        "suitable_for_explanation_experiment_count": sum(1 for row in rows if row["suitable_for_explanation_experiment_auto"]),
        "precision_in_audit": round(correct / (correct + wrong + over), 6) if correct + wrong + over else 0.0,
        "recall_in_audit": round(correct / (correct + wrong + missed), 6) if correct + wrong + missed else 0.0,
        "notes": [
            "Multi-reference equivalence cannot be adjudicated from EXPECT single-reference records.",
            "Boundary, noise, and suitability fields are automatic screening flags, not human judgments.",
        ],
    }


def render(rows: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
    lines = [
        "# Round 04 Model Behavior Audit",
        "",
        "This is a researcher-readable automatic audit, not human annotation.",
        "",
        "## Summary",
        "",
        f"- Rows: {summary['audit_count']}",
        f"- Model counts: `{json.dumps(summary['model_counts'], sort_keys=True)}`",
        f"- Behavior counts: `{json.dumps(summary['behavior_counts'], sort_keys=True)}`",
        f"- Operation counts: `{json.dumps(summary['operation_counts'], sort_keys=True)}`",
        f"- Format-noise flags: {summary['model_format_noise_count']}",
        f"- Suitable for explanation experiment: {summary['suitable_for_explanation_experiment_count']}",
        "",
    ]
    for idx, row in enumerate(rows, 1):
        lines.extend(
            [
                f"## {idx}. {row['record_id']}",
                "",
                f"- Source: `{row['source']}`",
                f"- Reference: `{row['reference']}`",
                f"- Prediction: `{row['prediction']}`",
                f"- Gold edits: `{json.dumps(row['gold_edits'], ensure_ascii=False)}`",
                f"- Predicted edits: `{json.dumps(row['predicted_edits'], ensure_ascii=False)}`",
                f"- Alignment: `{json.dumps(row['alignment'], ensure_ascii=False)}`",
                f"- Behavior: `{row['behavior']}`",
                f"- Error type: `{row['error_type']}`",
                f"- Operation: `{row['operation']}`",
                f"- Multi-reference equivalent correction: `{row['multi_reference_equivalent_correction']}`",
                f"- ERRANT boundary issue auto: `{row['errant_boundary_issue_auto']}`",
                f"- Model format noise auto: `{row['model_format_noise_auto']}`",
                f"- Suitable for explanation experiment auto: `{row['suitable_for_explanation_experiment_auto']}`",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def build(args: argparse.Namespace) -> None:
    annotator = errant.load("en")
    records: List[Dict[str, Any]] = []
    for row in read_jsonl(args.predictions):
        ref_edits = extract_edits(annotator, row["source"], row["reference"])
        pred_edits = extract_edits(annotator, row["source"], row["prediction"])
        alignments, missed, failures = align_predicted_edits(ref_edits, pred_edits)
        records.extend(make_event_records(row, ref_edits, pred_edits, alignments, missed, failures))
    selected = select(records, args.count)
    summary = summarize(selected)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "model_behavior_audit_100.jsonl", selected)
    write_json(args.out_dir / "model_behavior_audit_summary.json", summary)
    (args.out_dir / "model_behavior_audit_100.md").write_text(render(selected, summary))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a 100-row model behavior audit from real GEC predictions.")
    parser.add_argument("--predictions", type=Path, default=DEFAULT_PREDICTIONS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--count", type=int, default=100)
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
