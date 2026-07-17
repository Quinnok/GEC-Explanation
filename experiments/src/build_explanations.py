from __future__ import annotations

from edit_schema import Edit


def explicit_explanation(edit: Edit) -> str:
    if edit.operation == "replace":
        return f'Replace "{edit.source_text}" with "{edit.target_text}" to correct the {edit.error_type} error.'
    if edit.operation == "insert":
        return f'Insert "{edit.target_text}" to correct the {edit.error_type} error.'
    if edit.operation == "delete":
        return f'Delete "{edit.source_text}" to correct the {edit.error_type} error.'
    return f"The edit addresses a {edit.error_type} error."


def generic_explanation() -> str:
    return "This sentence contains a grammar issue and should be revised."

