from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FORM = ROOT / "annotation" / "rulefaith_qwen3_ready_validation_v2" / "ready_validation_form.csv"
DEFAULT_KEY = ROOT / "annotation" / "rulefaith_qwen3_ready_validation_v2" / "ready_validation_key.csv"
DEFAULT_OUTPUT = ROOT / "annotation" / "rulefaith_qwen3_ready_validation_v2" / "ready_validation_completed_by_codex.csv"
DEFAULT_MERGED = ROOT / "annotation" / "rulefaith_qwen3_ready_validation_v2" / "ready_validation_completed_by_codex_merged_with_key.csv"
DEFAULT_SUMMARY = ROOT / "results" / "rulefaith" / "qwen3_ready_validation_codex_summary.json"
DEFAULT_CASES = ROOT / "results" / "rulefaith" / "qwen3_ready_validation_codex_cases.md"


LABEL_SOURCE = "codex_ai_pseudo_validation"

ALLOWED = {
    "validator_edit_alignment": {"pass", "partial", "fail", "uncertain"},
    "validator_edit_validity": {"valid", "acceptable_alternative", "invalid", "stylistic", "uncertain"},
    "validator_rule_plausibility": {"plausible", "weak", "implausible", "uncertain"},
    "validator_evidence_sufficiency": {"sufficient", "partial", "insufficient", "uncertain"},
    "validator_overall_decision": {"accept", "refine", "reject", "uncertain"},
}

ANNOTATION_FIELDS = [
    "validator_edit_alignment",
    "validator_edit_validity",
    "validator_rule_plausibility",
    "validator_evidence_sufficiency",
    "validator_overall_decision",
    "validator_notes",
]

# These labels are Codex/AI pseudo-validation labels over the blind v2 package.
# They are intended for internal triage and method-loop continuity, not as human gold.
CODEX_LABELS: dict[str, dict[str, str]] = {
    "rfq3-ready-0001": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "weak",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "refine",
        "validator_notes": "Rule should state that an cannot modify a plural noun.",
    },
    "rfq3-ready-0002": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Plural noun experts supports deleting an.",
    },
    "rfq3-ready-0003": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Explains the specializing in collocation.",
    },
    "rfq3-ready-0004": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Explains the specializing in collocation.",
    },
    "rfq3-ready-0005": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Pollution is used generically here.",
    },
    "rfq3-ready-0006": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Caring for the environment is the relevant collocation.",
    },
    "rfq3-ready-0007": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Caring for the environment is the relevant collocation.",
    },
    "rfq3-ready-0008": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "acceptable_alternative",
        "validator_rule_plausibility": "weak",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "refine",
        "validator_notes": "It is acceptable, but the concrete/abstract pronoun claim is weak.",
    },
    "rfq3-ready-0009": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "acceptable_alternative",
        "validator_rule_plausibility": "weak",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "refine",
        "validator_notes": "Pronoun replacement is mostly stylistic and evidence is underspecified.",
    },
    "rfq3-ready-0010": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Caring for the environment is the relevant collocation.",
    },
    "rfq3-ready-0011": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Caring for the environment is the relevant collocation.",
    },
    "rfq3-ready-0012": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "invalid",
        "validator_rule_plausibility": "implausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "reject",
        "validator_notes": "Impact on people should not be changed to impact for people.",
    },
    "rfq3-ready-0013": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "invalid",
        "validator_rule_plausibility": "implausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "reject",
        "validator_notes": "The preposition rule does not justify impact for people.",
    },
    "rfq3-ready-0014": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "weak",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "refine",
        "validator_notes": "Rule should explicitly cite plural experts rather than redundancy.",
    },
    "rfq3-ready-0015": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Plural noun experts supports deleting an.",
    },
    "rfq3-ready-0016": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Interested in is the correct collocation.",
    },
    "rfq3-ready-0017": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Interested in is the correct collocation.",
    },
    "rfq3-ready-0018": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "invalid",
        "validator_rule_plausibility": "implausible",
        "validator_evidence_sufficiency": "insufficient",
        "validator_overall_decision": "reject",
        "validator_notes": "Subject-verb agreement does not justify replacing the with they.",
    },
    "rfq3-ready-0019": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Interested in is the correct collocation.",
    },
    "rfq3-ready-0020": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Interested in is the correct collocation.",
    },
    "rfq3-ready-0021": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "invalid",
        "validator_rule_plausibility": "implausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "reject",
        "validator_notes": "Deleting is alone does not license omitting be here.",
    },
    "rfq3-ready-0022": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "refine",
        "validator_notes": "Evidence omits the implied noun side.",
    },
    "rfq3-ready-0023": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "refine",
        "validator_notes": "List punctuation is plausible, but evidence includes noisy ed token.",
    },
    "rfq3-ready-0024": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "stylistic",
        "validator_rule_plausibility": "weak",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "refine",
        "validator_notes": "Independent clauses are related but not clearly result/explanation.",
    },
    "rfq3-ready-0025": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Period separates the following sentence beginning It.",
    },
    "rfq3-ready-0026": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "implausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "reject",
        "validator_notes": "Original lacks required article; explanation falsely calls it grammatical.",
    },
    "rfq3-ready-0027": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "implausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "reject",
        "validator_notes": "Variety is not a non-count noun in this phrase.",
    },
    "rfq3-ready-0028": {
        "validator_edit_alignment": "partial",
        "validator_edit_validity": "stylistic",
        "validator_rule_plausibility": "implausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "reject",
        "validator_notes": "Civilization is not simply ending an introductory element in the source.",
    },
    "rfq3-ready-0029": {
        "validator_edit_alignment": "partial",
        "validator_edit_validity": "stylistic",
        "validator_rule_plausibility": "implausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "reject",
        "validator_notes": "Comma explanation does not match the source clause structure.",
    },
    "rfq3-ready-0030": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Period fixes a comma splice before she.",
    },
    "rfq3-ready-0031": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Period fixes a comma splice before she.",
    },
    "rfq3-ready-0032": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "implausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "reject",
        "validator_notes": "Rationale wrongly says the article modifies latter half.",
    },
    "rfq3-ready-0033": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "implausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "reject",
        "validator_notes": "Rationale wrongly treats the deleted article as tied to a time period.",
    },
    "rfq3-ready-0034": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "invalid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "reject",
        "validator_notes": "In this context the possessive should normally be people's, not peoples'.",
    },
    "rfq3-ready-0035": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "weak",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "refine",
        "validator_notes": "Needs the implied noun side, not only positive.",
    },
    "rfq3-ready-0036": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "weak",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "refine",
        "validator_notes": "Article rule is right but the evidence omits side.",
    },
    "rfq3-ready-0037": {
        "validator_edit_alignment": "partial",
        "validator_edit_validity": "invalid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "refine",
        "validator_notes": "Rule describes replacing is with are, but atomic edit is deletion.",
    },
    "rfq3-ready-0038": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "valid",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "partial",
        "validator_overall_decision": "refine",
        "validator_notes": "Rule is plausible but evidence should include the implied noun side.",
    },
    "rfq3-ready-0039": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "acceptable_alternative",
        "validator_rule_plausibility": "weak",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "refine",
        "validator_notes": "The article before streets is acceptable but not clearly required.",
    },
    "rfq3-ready-0040": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "acceptable_alternative",
        "validator_rule_plausibility": "weak",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "refine",
        "validator_notes": "The rule is too broad for this optional article choice.",
    },
    "rfq3-ready-0041": {
        "validator_edit_alignment": "pass",
        "validator_edit_validity": "stylistic",
        "validator_rule_plausibility": "plausible",
        "validator_evidence_sufficiency": "sufficient",
        "validator_overall_decision": "accept",
        "validator_notes": "Semicolon separates two related independent clauses.",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"Missing header in {path}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"Input CSV is empty: {path}")
    return rows, list(reader.fieldnames)


def write_csv(path: Path, rows: Iterable[dict[str, str]], fieldnames: list[str], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def validate_ids(rows: list[dict[str, str]]) -> None:
    ids = [row.get("validation_item_id", "") for row in rows]
    if any(not item_id for item_id in ids):
        raise ValueError("Every row must contain validation_item_id")
    duplicates = [item_id for item_id, count in Counter(ids).items() if count > 1]
    if duplicates:
        raise ValueError(f"Duplicate validation_item_id values: {duplicates}")
    expected = set(CODEX_LABELS)
    observed = set(ids)
    if observed != expected:
        missing = sorted(expected - observed)
        extra = sorted(observed - expected)
        raise ValueError(f"Validation IDs do not match label map. missing={missing} extra={extra}")


def completed_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    validate_ids(rows)
    output: list[dict[str, str]] = []
    for row in rows:
        item_id = row["validation_item_id"]
        labels = CODEX_LABELS[item_id]
        for field, values in ALLOWED.items():
            value = labels[field]
            if value not in values:
                raise ValueError(f"Illegal {field}={value} for {item_id}")
        enriched = dict(row)
        for field in ANNOTATION_FIELDS:
            enriched[field] = labels[field]
        output.append(enriched)
    return output


def merge_with_key(rows: list[dict[str, str]], key_rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[str]]:
    key_by_id = {row["validation_item_id"]: row for row in key_rows}
    if set(key_by_id) != {row["validation_item_id"] for row in rows}:
        raise ValueError("Key IDs do not match validation IDs")
    merged: list[dict[str, str]] = []
    for row in rows:
        key = key_by_id[row["validation_item_id"]]
        merged.append({**key, **row, "label_source": LABEL_SOURCE})
    key_fields = [field for field in key_rows[0] if field != "validation_item_id"]
    return merged, ["validation_item_id", *key_fields, *[field for field in rows[0] if field != "validation_item_id"], "label_source"]


def summarize(rows: list[dict[str, str]], merged: list[dict[str, str]]) -> dict[str, object]:
    return {
        "generated_at": utc_now(),
        "git_commit": git_commit(),
        "label_source": LABEL_SOURCE,
        "candidate_count": len(rows),
        "validator_overall_decision_counts": dict(sorted(Counter(row["validator_overall_decision"] for row in rows).items())),
        "validator_edit_alignment_counts": dict(sorted(Counter(row["validator_edit_alignment"] for row in rows).items())),
        "validator_edit_validity_counts": dict(sorted(Counter(row["validator_edit_validity"] for row in rows).items())),
        "validator_rule_plausibility_counts": dict(sorted(Counter(row["validator_rule_plausibility"] for row in rows).items())),
        "validator_evidence_sufficiency_counts": dict(sorted(Counter(row["validator_evidence_sufficiency"] for row in rows).items())),
        "accepted_candidate_ids": [row["candidate_id"] for row in merged if row["validator_overall_decision"] == "accept"],
        "refine_candidate_ids": [row["candidate_id"] for row in merged if row["validator_overall_decision"] == "refine"],
        "rejected_candidate_ids": [row["candidate_id"] for row in merged if row["validator_overall_decision"] == "reject"],
        "paper_use_boundary": "These labels are Codex/AI pseudo-validation for internal triage. They must not be reported as human validation or human gold.",
    }


def write_summary(path: Path, payload: dict[str, object], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_cases(path: Path, rows: list[dict[str, str]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Qwen3 Ready-Candidate Codex Pseudo-Validation Cases",
        "",
        f"Generated at: {utc_now()}",
        "",
        "These are Codex/AI pseudo-validation labels, not human annotation.",
        "",
    ]
    for decision in ["accept", "refine", "reject"]:
        group = [row for row in rows if row["validator_overall_decision"] == decision]
        lines.extend([f"## {decision.title()} ({len(group)})", ""])
        for row in group:
            lines.append(
                f"- `{row['validation_item_id']}` {row['operation']} `{row['source_text']}` -> `{row['target_text']}`: "
                f"{row['validator_notes']}"
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Complete the Qwen3 ready validation form with Codex pseudo-labels.")
    parser.add_argument("--form", type=Path, default=DEFAULT_FORM)
    parser.add_argument("--key", type=Path, default=DEFAULT_KEY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--merged-output", type=Path, default=DEFAULT_MERGED)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    form_rows, form_fields = read_csv(resolve(args.form))
    key_rows, _ = read_csv(resolve(args.key))
    for field in ANNOTATION_FIELDS:
        if field not in form_fields:
            raise ValueError(f"Missing annotation field in form: {field}")
    rows = completed_rows(form_rows)
    merged, merged_fields = merge_with_key(rows, key_rows)
    write_csv(resolve(args.output), rows, form_fields, args.overwrite)
    write_csv(resolve(args.merged_output), merged, merged_fields, args.overwrite)
    summary = summarize(rows, merged)
    write_summary(resolve(args.summary), summary, args.overwrite)
    write_cases(resolve(args.cases), rows, args.overwrite)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
