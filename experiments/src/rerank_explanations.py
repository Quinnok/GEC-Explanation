"""Reranking placeholder.

Real reranking requires multiple candidate explanations per edit and human or
structured supervision. This file keeps the expected entry point explicit.
"""


def rerank_by_score(candidates):
    return sorted(candidates, key=lambda item: item.get("score", 0.0), reverse=True)

