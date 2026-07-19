from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "data" / "rulefaith" / "teacher_candidates_pilot.jsonl"
DEFAULT_JSON = ROOT / "results" / "rulefaith" / "teacher_candidate_quality_flags.json"
DEFAULT_MD = ROOT / "results" / "rulefaith" / "teacher_candidate_quality_report.md"


GENERIC_PATTERNS = [
    r"\bgrammatical error\b",
    r"\bgrammar correction model\b",
    r"\bgrammatical error correction model\b",
    r"\bthe word .{0,20} is a grammatical\b",
    r"^\(?[A-D]\)?(?:\s+\(?[A-D]\)?)+$",
]


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def token_set(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9']+", text.lower()))


def source_overlap_ratio(rationale: str, source: str) -> float:
    r_tokens = token_set(rationale)
    if not r_tokens:
        return 0.0
    return len(r_tokens & token_set(source)) / len(r_tokens)


def flags_for(row: Dict[str, Any]) -> Dict[str, Any]:
    rationale = row.get("parsed_output", {}).get("rationale", "")
    raw = row.get("raw_response", "")
    source = row.get("source", "")
    norm = normalize(rationale)
    generic = any(re.search(pattern, norm) for pattern in GENERIC_PATTERNS)
    prompt_contamination = "grammar correction model" in norm or norm.startswith("source:")
    source_copy_like = len(rationale.split()) >= 25 and source_overlap_ratio(rationale, source) >= 0.75
    too_short = len(rationale.split()) < 4
    return {
        "candidate_id": row["candidate_id"],
        "provider": row.get("provider"),
        "teacher_model": row.get("teacher_model"),
        "candidate_type": row.get("candidate_type"),
        "parse_status": row.get("parse_status"),
        "generic": generic,
        "prompt_contamination": prompt_contamination,
        "source_copy_like": source_copy_like,
        "too_short": too_short,
        "low_quality": generic or prompt_contamination or source_copy_like or too_short,
        "source_overlap_ratio": round(source_overlap_ratio(rationale, source), 4),
        "word_count": len(rationale.split()),
        "raw_response": raw,
    }


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def audit(args: argparse.Namespace) -> None:
    rows = read_jsonl(args.input)
    flags = [flags_for(row) for row in rows]
    counts = {
        "candidate_count": len(rows),
        "provider_counts": dict(Counter(row.get("provider") for row in rows)),
        "teacher_model_counts": dict(Counter(row.get("teacher_model") for row in rows)),
        "candidate_type_counts": dict(Counter(row.get("candidate_type") for row in rows)),
        "parse_status_counts": dict(Counter(row.get("parse_status") for row in rows)),
        "generic_count": sum(1 for row in flags if row["generic"]),
        "prompt_contamination_count": sum(1 for row in flags if row["prompt_contamination"]),
        "source_copy_like_count": sum(1 for row in flags if row["source_copy_like"]),
        "too_short_count": sum(1 for row in flags if row["too_short"]),
        "low_quality_count": sum(1 for row in flags if row["low_quality"]),
    }
    counts["low_quality_rate"] = round(counts["low_quality_count"] / len(rows), 4) if rows else 0.0
    output = {"input": str(args.input), "counts": counts, "flags": flags}
    write_json(args.json_output, output)

    lines = [
        "# Teacher Candidate Quality Report",
        "",
        f"Input: `{args.input}`",
        "",
        "## Summary",
        "",
    ]
    for key, value in counts.items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Highest-Risk Examples", ""])
    for row in sorted(flags, key=lambda item: (not item["low_quality"], -item["word_count"]))[:20]:
        lines.append(f"- `{row['candidate_id']}`: {row['raw_response'][:240]}")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The open-teacher candidates are useful as a weak baseline and failure signal, but they are not strong enough to replace the GPT-5.5 teacher pilot.",
        ]
    )
    args.md_output.parent.mkdir(parents=True, exist_ok=True)
    args.md_output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--md-output", type=Path, default=DEFAULT_MD)
    return parser.parse_args()


if __name__ == "__main__":
    audit(parse_args())
