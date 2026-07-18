from __future__ import annotations

import re
from typing import Optional

from edit_schema import Edit


QUOTED = r"[\"'`“”‘’]"
SPAN_PATTERN = re.compile(r"source token span\s*\[(\d+)\s*,\s*(\d+)\)", flags=re.IGNORECASE)
TYPE_PATTERN = re.compile(r"(?:ERRANT\s+)?type\s+([A-Z]:[A-Z0-9_:]+|[A-Z][A-Za-z0-9_:-]+)", flags=re.IGNORECASE)
RAW_EDIT_PATTERN = re.compile(
    r"EDIT\s+operation=(replace|insert|delete)\s+start=(\d+)\s+end=(\d+)\s+"
    + r"source=\"(.*?)\"\s+target=\"(.*?)\"\s+type=\"(.*?)\"",
    flags=re.IGNORECASE,
)


def _find_token_span(source: str, text: str) -> Optional[tuple[int, int]]:
    source_tokens = source.split()
    text_tokens = text.split()
    if not text_tokens:
        return (0, 0)
    for i in range(0, len(source_tokens) - len(text_tokens) + 1):
        if source_tokens[i : i + len(text_tokens)] == text_tokens:
            return (i, i + len(text_tokens))
    return None


def _span_from_explanation(explanation: str) -> Optional[tuple[int, int]]:
    match = SPAN_PATTERN.search(explanation)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def _type_from_explanation(explanation: str, default: str) -> str:
    match = TYPE_PATTERN.search(explanation)
    if not match:
        return default
    return match.group(1)


def structured_explicit_edit_baseline(source: str, explanation: str, error_type: str = "UNK") -> Optional[Edit]:
    raw_match = RAW_EDIT_PATTERN.search(explanation)
    if raw_match:
        return Edit(
            start=int(raw_match.group(2)),
            end=int(raw_match.group(3)),
            source_text=raw_match.group(4),
            target_text=raw_match.group(5),
            operation=raw_match.group(1).lower(),
            error_type=raw_match.group(6),
        )

    parsed_span = _span_from_explanation(explanation)
    parsed_type = _type_from_explanation(explanation, error_type)
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
            span = parsed_span or _find_token_span(source, source_text)
            if span is None:
                return None
            return Edit(span[0], span[1], source_text, target_text, operation, parsed_type)
        if operation == "delete":
            source_text = match.group(1)
            span = parsed_span or _find_token_span(source, source_text)
            if span is None:
                return None
            return Edit(span[0], span[1], source_text, "", operation, parsed_type)
        if operation == "insert":
            target_text = match.group(1)
            span = parsed_span or (0, 0)
            return Edit(span[0], span[1], "", target_text, operation, parsed_type)
    return None


def explicit_edit_baseline(source: str, explanation: str, error_type: str = "UNK") -> Optional[Edit]:
    return structured_explicit_edit_baseline(source, explanation, error_type=error_type)


def surface_keyword_predict(gold: Edit, explanation: str) -> bool:
    text = explanation.lower()
    if not text.strip():
        return False
    operation_ok = gold.operation.lower() in text
    type_ok = gold.error_type.lower() in text
    source_ok = True if not gold.source_text else gold.source_text.lower() in text
    target_ok = True if not gold.target_text else gold.target_text.lower() in text
    return operation_ok and type_ok and source_ok and target_ok
