from __future__ import annotations

import re
from typing import Optional

from edit_schema import Edit


QUOTED = r"[\"'`“”‘’]"


def _find_token_span(source: str, text: str) -> Optional[tuple[int, int]]:
    source_tokens = source.split()
    text_tokens = text.split()
    if not text_tokens:
        return (0, 0)
    for i in range(0, len(source_tokens) - len(text_tokens) + 1):
        if source_tokens[i : i + len(text_tokens)] == text_tokens:
            return (i, i + len(text_tokens))
    return None


def explicit_edit_baseline(source: str, explanation: str, error_type: str = "UNK") -> Optional[Edit]:
    patterns = [
        (r"(?:replace|change)\s+" + QUOTED + r"(.+?)" + QUOTED + r"\s+(?:with|to)\s+" + QUOTED + r"(.+?)" + QUOTED, "replace"),
        (r"(?:delete|remove)\s+" + QUOTED + r"(.+?)" + QUOTED, "delete"),
        (r"(?:insert|add)\s+" + QUOTED + r"(.+?)" + QUOTED, "insert"),
    ]
    for pattern, operation in patterns:
        match = re.search(pattern, explanation, flags=re.IGNORECASE)
        if not match:
            continue
        if operation == "replace":
            source_text, target_text = match.group(1), match.group(2)
            span = _find_token_span(source, source_text)
            if span is None:
                return None
            return Edit(span[0], span[1], source_text, target_text, operation, error_type)
        if operation == "delete":
            source_text = match.group(1)
            span = _find_token_span(source, source_text)
            if span is None:
                return None
            return Edit(span[0], span[1], source_text, "", operation, error_type)
        if operation == "insert":
            target_text = match.group(1)
            return Edit(0, 0, "", target_text, operation, error_type)
    return None

