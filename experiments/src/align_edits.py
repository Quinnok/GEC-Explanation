from __future__ import annotations

from edit_schema import Edit


def exact_align(predicted: Edit, reference: Edit) -> bool:
    return predicted.start == reference.start and predicted.end == reference.end and predicted.operation == reference.operation

