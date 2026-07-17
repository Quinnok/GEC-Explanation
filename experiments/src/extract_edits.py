from __future__ import annotations

import difflib
from typing import List

from edit_schema import Edit


def tokenize(sentence: str) -> List[str]:
    return sentence.split()


def extract_token_diff_edits(source: str, target: str, error_type: str = "UNK") -> List[Edit]:
    source_tokens = tokenize(source)
    target_tokens = tokenize(target)
    matcher = difflib.SequenceMatcher(a=source_tokens, b=target_tokens)
    edits: List[Edit] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        source_text = " ".join(source_tokens[i1:i2])
        target_text = " ".join(target_tokens[j1:j2])
        if tag == "replace":
            operation = "replace"
        elif tag == "insert":
            operation = "insert"
        elif tag == "delete":
            operation = "delete"
        else:
            operation = tag
        edits.append(
            Edit(
                start=i1,
                end=i2,
                source_text=source_text,
                target_text=target_text,
                operation=operation,
                error_type=error_type,
            )
        )
    return edits


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()
    print(json.dumps([edit.to_dict() for edit in extract_token_diff_edits(args.source, args.target)], indent=2))

