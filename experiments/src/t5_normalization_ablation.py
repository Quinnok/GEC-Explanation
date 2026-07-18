from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Tuple

import errant

from analyze_model_edits import align_predicted_edits, extract_edits


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PREDICTIONS = ROOT / "results" / "model_predictions" / "expect_v1_model_predictions.jsonl"
DEFAULT_OUT_DIR = ROOT / "results" / "model_edits"


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


def normalize_spacing(text: str) -> str:
    text = " ".join(text.replace("\n", " ").split())
    text = re.sub(r"\s+([,.;:!?])", r" \1", text)
    text = re.sub(r"([,.;:!?])(?=\S)", r"\1 ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_punctuation(text: str) -> str:
    text = normalize_spacing(text)
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"\b([A-Za-z]+)'s\b", r"\1 's", text)
    text = re.sub(r"\b([A-Za-z]+)n't\b", r"\1 n't", text)
    text = re.sub(r"\b([A-Za-z]+)'m\b", r"\1 'm", text)
    text = re.sub(r"\b([A-Za-z]+)'re\b", r"\1 're", text)
    text = re.sub(r"\b([A-Za-z]+)'ve\b", r"\1 've", text)
    text = re.sub(r"\b([A-Za-z]+)'ll\b", r"\1 'll", text)
    text = re.sub(r'\s*"\s*', ' " ', text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_case(text: str) -> str:
    return normalize_punctuation(text).lower()


def noise_like(edit: Dict[str, Any]) -> bool:
    if "ORTH" in edit["error_type"] or "PUNCT" in edit["error_type"]:
        return True
    source = re.sub(r"[\s`'\".,!?;:()\[\]{}-]+", "", edit.get("source_text", "").lower())
    target = re.sub(r"[\s`'\".,!?;:()\[\]{}-]+", "", edit.get("target_text", "").lower())
    return source == target and edit.get("source_text", "") != edit.get("target_text", "")


def keep_edit(edit: Dict[str, Any], mode: str) -> bool:
    etype = edit["error_type"]
    if mode == "all":
        return True
    if mode == "exclude_orth":
        return "ORTH" not in etype
    if mode == "exclude_punct":
        return "PUNCT" not in etype
    if mode == "exclude_orth_punct":
        return "ORTH" not in etype and "PUNCT" not in etype
    if mode == "substantive":
        return "ORTH" not in etype and "PUNCT" not in etype and not noise_like(edit)
    raise ValueError(f"Unknown filter mode: {mode}")


def f05(precision: float, recall: float) -> float:
    beta2 = 0.25
    if precision == 0.0 and recall == 0.0:
        return 0.0
    return (1 + beta2) * precision * recall / (beta2 * precision + recall)


def summarize_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts = Counter(event["behavior"] for row in rows for event in row["events"])
    correct = counts["correct_correction"]
    wrong = counts["wrong_correction"]
    over = counts["overcorrection"]
    missed = counts["missed_correction"]
    pred_edit_count = sum(row["pred_edit_count"] for row in rows)
    precision = correct / (correct + wrong + over) if correct + wrong + over else 0.0
    recall = correct / (correct + wrong + missed) if correct + wrong + missed else 0.0
    return {
        "sentence_count": len(rows),
        "behavior_counts": dict(counts),
        "correct": correct,
        "wrong": wrong,
        "overcorrection": over,
        "missed": missed,
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f0_5": round(f05(precision, recall), 6),
        "predicted_edit_count": pred_edit_count,
        "reference_edit_count": sum(row["ref_edit_count"] for row in rows),
        "avg_predicted_edits_per_sentence": round(pred_edit_count / len(rows), 6) if rows else 0.0,
        "avg_reference_edits_per_sentence": round(sum(row["ref_edit_count"] for row in rows) / len(rows), 6) if rows else 0.0,
    }


def row_events(alignments: List[Dict[str, Any]], missed: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "behavior": item["behavior"],
            "predicted_edit": item["predicted_edit"],
            "reference_edit": item["reference_edit"],
            "score": item["score"],
        }
        for item in alignments
    ] + [
        {
            "behavior": "missed_correction",
            "predicted_edit": None,
            "reference_edit": item["reference_edit"],
            "score": 0.0,
        }
        for item in missed
    ]


def evaluate_variant(
    annotator: Any,
    rows: List[Dict[str, Any]],
    variant_name: str,
    text_transform: Callable[[str], str],
    filter_mode: str,
    transform_source_reference: bool = False,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    sentence_rows = []
    for row in rows:
        source = text_transform(row["source"]) if transform_source_reference else row["source"]
        reference = text_transform(row["reference"]) if transform_source_reference else row["reference"]
        prediction = text_transform(row["prediction"])
        ref_edits = [edit for edit in extract_edits(annotator, source, reference) if keep_edit(edit, filter_mode)]
        pred_edits = [edit for edit in extract_edits(annotator, source, prediction) if keep_edit(edit, filter_mode)]
        alignments, missed, failures = align_predicted_edits(ref_edits, pred_edits)
        sentence_rows.append(
            {
                "sample_id": row["sample_id"],
                "variant": variant_name,
                "source": source,
                "reference": reference,
                "prediction": prediction,
                "ref_edit_count": len(ref_edits),
                "pred_edit_count": len(pred_edits),
                "events": row_events(alignments, missed),
                "alignment_failure_count": len(failures),
            }
        )
    stats = summarize_rows(sentence_rows)
    stats["variant"] = variant_name
    stats["filter_mode"] = filter_mode
    stats["text_transform"] = text_transform.__name__
    stats["transform_source_reference"] = transform_source_reference
    return stats, sentence_rows


def build_changes(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    changes = []
    for row in rows:
        spacing = normalize_spacing(row["prediction"])
        punctuation = normalize_punctuation(row["prediction"])
        case = normalize_case(row["prediction"])
        if spacing != row["prediction"] or punctuation != row["prediction"] or case != row["prediction"]:
            changes.append(
                {
                    "sample_id": row["sample_id"],
                    "model_key": row["model_key"],
                    "raw_prediction": row["prediction"],
                    "normalized_spacing_prediction": spacing,
                    "normalized_punctuation_prediction": punctuation,
                    "normalized_case_prediction": case,
                    "changed_by_spacing": spacing != row["prediction"],
                    "changed_by_punctuation": punctuation != row["prediction"],
                    "changed_by_case": case != row["prediction"],
                }
            )
    return changes


def run(args: argparse.Namespace) -> None:
    annotator = errant.load("en")
    rows = [row for row in read_jsonl(args.predictions) if row["model_key"] == "t5_base_grammar"]
    variants = [
        ("raw", lambda x: x, "all", False),
        ("normalized_spacing", normalize_spacing, "all", False),
        ("normalized_punctuation", normalize_punctuation, "all", False),
        ("normalized_case", normalize_case, "all", True),
        ("excluding_orth", lambda x: x, "exclude_orth", False),
        ("excluding_punct", lambda x: x, "exclude_punct", False),
        ("excluding_orth_punct", lambda x: x, "exclude_orth_punct", False),
        ("substantive_grammatical_edits_only", lambda x: x, "substantive", False),
    ]
    stats_by_variant: Dict[str, Any] = {}
    detailed_rows: List[Dict[str, Any]] = []
    for name, transform, filter_mode, transform_source_reference in variants:
        stats, variant_rows = evaluate_variant(
            annotator,
            rows,
            name,
            transform,
            filter_mode,
            transform_source_reference,
        )
        stats_by_variant[name] = stats
        detailed_rows.extend(variant_rows)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    raw_stats = stats_by_variant["raw"] | {"normalization_rules": NORMALIZATION_RULES}
    write_json(args.out_dir / "raw_behavior_stats.json", raw_stats)
    write_json(args.out_dir / "normalized_behavior_stats.json", {"variants": stats_by_variant, "normalization_rules": NORMALIZATION_RULES})
    write_json(args.out_dir / "substantive_behavior_stats.json", stats_by_variant["substantive_grammatical_edits_only"])
    write_jsonl(args.out_dir / "normalization_changes.jsonl", build_changes(rows))
    write_jsonl(args.out_dir / "normalization_variant_events.jsonl", detailed_rows)


NORMALIZATION_RULES = {
    "raw": "Use original T5 predictions without modifying source, reference, or prediction.",
    "normalized_spacing": "Normalize whitespace and punctuation spacing in the T5 prediction only.",
    "normalized_punctuation": "Apply spacing normalization plus quote/apostrophe and contraction tokenization to the T5 prediction only.",
    "normalized_case": "Apply punctuation normalization and lowercase source, reference, and prediction to isolate case-only effects.",
    "excluding_orth": "Run raw extraction and drop ERRANT edits whose type contains ORTH before alignment.",
    "excluding_punct": "Run raw extraction and drop ERRANT edits whose type contains PUNCT before alignment.",
    "excluding_orth_punct": "Run raw extraction and drop ERRANT edits whose type contains ORTH or PUNCT before alignment.",
    "substantive_grammatical_edits_only": "Drop ORTH/PUNCT and punctuation/case-only edits before alignment; keep likely grammatical edits.",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="T5 normalization and edit-filtering ablation.")
    parser.add_argument("--predictions", type=Path, default=DEFAULT_PREDICTIONS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
