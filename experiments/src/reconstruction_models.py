from __future__ import annotations

from typing import Dict, Optional

from baselines import explicit_edit_baseline
from edit_schema import Edit


class ExplicitEditPatternReconstructor:
    name = "explicit_edit_pattern"

    def reconstruct(self, source: str, explanation: str, error_type: str = "UNK") -> Optional[Edit]:
        return explicit_edit_baseline(source, explanation, error_type=error_type)


def get_reconstructor(name: str):
    if name == ExplicitEditPatternReconstructor.name:
        return ExplicitEditPatternReconstructor()
    raise ValueError(f"Unknown reconstructor: {name}")


def reconstruction_to_json(edit: Optional[Edit]) -> Dict[str, object]:
    if edit is None:
        return {"reconstructable": False}
    return {"reconstructable": True, **edit.to_dict()}

