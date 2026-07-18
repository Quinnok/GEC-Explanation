"""Utilities for explanation candidate reranking.

Round 11 uses these primitives through ``run_reranking_experiment.py``. Scores
are automatic pilot signals unless real human preference labels are supplied.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List


def rerank_by_score(candidates: Iterable[Dict[str, Any]], score_key: str = "score") -> List[Dict[str, Any]]:
    return sorted(candidates, key=lambda item: item.get("score", 0.0), reverse=True)
