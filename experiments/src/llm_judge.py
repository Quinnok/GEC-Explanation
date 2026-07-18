"""Local, no-paid-API helpers for automatic explanation judging.

The project deliberately avoids private or paid LLM APIs. Round 11 uses a local
open-source FLAN-T5 model as an automatic baseline judge; these helpers keep the
yes/no scoring semantics explicit and reusable.
"""

from __future__ import annotations

from typing import Any, Dict


def build_yes_no_prompt(candidate: Dict[str, Any]) -> str:
    edit = candidate.get("edit", {})
    operation = edit.get("operation", "edit")
    source_text = edit.get("source_text", "")
    target_text = edit.get("target_text", "")
    edit_text = f"{operation}: {source_text} -> {target_text}".strip()
    return (
        "Answer yes or no. Is the explanation faithful to the model edit?\n"
        f"Source: {candidate.get('source', '')}\n"
        f"Model prediction: {candidate.get('prediction', '')}\n"
        f"Model edit: {edit_text}\n"
        f"Explanation: {candidate.get('explanation', '')}\n"
        "Answer:"
    )


def parse_yes_no_score(answer: str) -> float:
    normalized = answer.strip().lower()
    if normalized.startswith("yes"):
        return 1.0
    if normalized.startswith("no"):
        return 0.0
    return 0.5


def judge_faithfulness(*args, **kwargs):
    raise RuntimeError(
        "No paid or private API judge is configured. Use run_reranking_experiment.py "
        "with --run-local-llm-judge for the local open-source baseline."
    )
