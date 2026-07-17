from __future__ import annotations

from edit_schema import Edit


def wrong_target_negative(edit: Edit, wrong_target: str = "the") -> str:
    if edit.operation == "replace":
        return f'Replace "{edit.source_text}" with "{wrong_target}" because the original phrase is not grammatical.'
    if edit.operation == "insert":
        return f'Insert "{wrong_target}" because the sentence is missing a required word.'
    return "This explanation intentionally describes the wrong target edit."


def generic_negative() -> str:
    return "The sentence has a grammar issue and should be improved."

