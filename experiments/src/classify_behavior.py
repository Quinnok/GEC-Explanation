from __future__ import annotations

from edit_schema import Edit


def classify_behavior(predicted: Edit, reference: Edit | None) -> str:
    if reference is None:
        return "overcorrection"
    if predicted == reference:
        return "correct_correction"
    if predicted.start == reference.start and predicted.end == reference.end:
        return "wrong_correction"
    return "wrong_correction"

