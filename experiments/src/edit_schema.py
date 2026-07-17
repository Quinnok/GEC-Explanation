from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, Set


@dataclass(frozen=True)
class Edit:
    start: int
    end: int
    source_text: str
    target_text: str
    operation: str
    error_type: str = "UNK"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Edit":
        return cls(
            start=int(data["start"]),
            end=int(data["end"]),
            source_text=str(data.get("source_text", "")),
            target_text=str(data.get("target_text", "")),
            operation=str(data.get("operation", "")),
            error_type=str(data.get("error_type", "UNK")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def span_positions(edit: Edit) -> Set[int]:
    if edit.end > edit.start:
        return set(range(edit.start, edit.end))
    return {edit.start}


def prf(predicted: Iterable[int], gold: Iterable[int]) -> Dict[str, float]:
    pred_set = set(predicted)
    gold_set = set(gold)
    if not pred_set and not gold_set:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}
    if not pred_set or not gold_set:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    overlap = len(pred_set & gold_set)
    precision = overlap / len(pred_set)
    recall = overlap / len(gold_set)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return {"precision": precision, "recall": recall, "f1": f1}


def compare_edits(pred: Edit, gold: Edit) -> Dict[str, float]:
    span_scores = prf(span_positions(pred), span_positions(gold))
    return {
        "span_exact": float(pred.start == gold.start and pred.end == gold.end),
        "span_precision": span_scores["precision"],
        "span_recall": span_scores["recall"],
        "span_f1": span_scores["f1"],
        "source_text_match": float(pred.source_text == gold.source_text),
        "target_text_match": float(pred.target_text == gold.target_text),
        "operation_accuracy": float(pred.operation == gold.operation),
        "error_type_accuracy": float(pred.error_type == gold.error_type),
        "full_edit_exact": float(pred == gold),
    }

