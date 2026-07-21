from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.rulefaith import build_qwen3_manual_audit as audit


DEFAULT_READY = ROOT / "data" / "rulefaith" / "filtering" / "qwen3_rule_plausibility_ready_for_human_spotcheck.jsonl"
DEFAULT_REFINE = ROOT / "data" / "rulefaith" / "filtering" / "qwen3_rule_plausibility_needs_refinement.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "annotation" / "rulefaith_qwen3_ready_validation"
DEFAULT_REPORT = ROOT / "results" / "rulefaith" / "qwen3_ready_validation_package_report.md"
DEFAULT_SUMMARY = ROOT / "results" / "rulefaith" / "qwen3_ready_validation_package_summary.json"

BLIND_FIELDS = [
    "validation_item_id",
    "source",
    "model_prediction",
    "operation",
    "edit_start",
    "edit_end",
    "source_text",
    "target_text",
    "edit_description",
    "edit_validity",
    "rule_text",
    "evidence_spans_json",
    "rationale",
    "confidence",
    "validator_edit_alignment",
    "validator_edit_validity",
    "validator_rule_plausibility",
    "validator_evidence_sufficiency",
    "validator_overall_decision",
    "validator_notes",
]

KEY_FIELDS = [
    "validation_item_id",
    "candidate_id",
    "dataset",
    "sample_id",
    "model_key",
    "model_family",
    "error_type",
    "error_category",
    "target_masked_score",
    "automatic_decision",
    "automatic_reasons",
]

REPAIR_FIELDS = [
    "repair_item_id",
    "candidate_id",
    "source",
    "model_prediction",
    "operation",
    "source_text",
    "target_text",
    "rule_text",
    "evidence_spans_json",
    "rationale",
    "automatic_reasons",
    "repair_instruction",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_jsonl(path: Path, allow_empty: bool = False) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Bad JSON in {path}:{lineno}: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"JSONL row is not an object in {path}:{lineno}")
            rows.append(row)
    if not rows and not allow_empty:
        raise ValueError(f"Input file is empty: {path}")
    return rows


def read_many_jsonl(paths: list[Path], allow_empty: bool = False) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in paths:
        for row in read_jsonl(path, allow_empty=allow_empty):
            candidate_id = str(row.get("candidate_id", ""))
            if not candidate_id:
                raise ValueError(f"Missing candidate_id in {path}")
            if candidate_id in seen:
                raise ValueError(f"Duplicate candidate_id across ready inputs: {candidate_id}")
            seen.add(candidate_id)
            rows.append(row)
    if not rows and not allow_empty:
        raise ValueError("All input JSONL files are empty")
    return rows


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_text(path: Path, text: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parsed(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("parsed_output") or {}


def edit(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("model_edit") or {}


def audit_result(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("rulefaith_rule_plausibility_audit") or {}


def validation_result(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("rulefaith_target_masked_validation") or {}


def blind_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for index, row in enumerate(rows, 1):
        item_id = f"rfq3-ready-{index:04d}"
        item_edit = edit(row)
        item_parsed = parsed(row)
        output.append(
            {
                "validation_item_id": item_id,
                "source": row.get("source", ""),
                "model_prediction": row.get("model_prediction", ""),
                "operation": item_edit.get("operation", ""),
                "edit_start": item_edit.get("start", ""),
                "edit_end": item_edit.get("end", ""),
                "source_text": item_edit.get("source_text", ""),
                "target_text": item_edit.get("target_text", ""),
                "edit_description": item_parsed.get("edit_description", ""),
                "edit_validity": item_parsed.get("edit_validity", ""),
                "rule_text": item_parsed.get("rule_text", ""),
                "evidence_spans_json": json.dumps(item_parsed.get("evidence_spans", []), ensure_ascii=False, sort_keys=True),
                "rationale": item_parsed.get("rationale", ""),
                "confidence": item_parsed.get("confidence", ""),
                "validator_edit_alignment": "",
                "validator_edit_validity": "",
                "validator_rule_plausibility": "",
                "validator_evidence_sufficiency": "",
                "validator_overall_decision": "",
                "validator_notes": "",
            }
        )
    return output


def key_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for index, row in enumerate(rows, 1):
        result = audit_result(row)
        output.append(
            {
                "validation_item_id": f"rfq3-ready-{index:04d}",
                "candidate_id": row.get("candidate_id", ""),
                "dataset": row.get("dataset", ""),
                "sample_id": row.get("sample_id", ""),
                "model_key": row.get("model_key", ""),
                "model_family": row.get("model_family", ""),
                "error_type": edit(row).get("error_type", row.get("error_type", "")),
                "error_category": row.get("error_category", ""),
                "target_masked_score": validation_result(row).get("target_masked_score", ""),
                "automatic_decision": result.get("decision", ""),
                "automatic_reasons": ";".join(result.get("reasons", [])),
            }
        )
    return output


def repair_instruction(reasons: list[str]) -> str:
    instructions: list[str] = []
    if "evidence_not_mentioned_in_rule_or_rationale" in reasons:
        instructions.append("Rewrite the rationale so it explicitly uses the cited source evidence span.")
    if any(reason.startswith("missing_required_evidence") for reason in reasons):
        instructions.append("Add the missing required source evidence span for the edit type.")
    if "rationale_edit_copy" in reasons:
        instructions.append("Remove edit-copy wording from the rationale and explain the grammatical condition instead.")
    if "unsupported_high_confidence" in reasons:
        instructions.append("Lower confidence or add a condition/uncertainty caveat supported by the source.")
    if not instructions:
        instructions.append("Revise the explanation to improve rule specificity and evidence grounding.")
    return " ".join(instructions)


def repair_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for index, row in enumerate(rows, 1):
        result = audit_result(row)
        item_edit = edit(row)
        item_parsed = parsed(row)
        reasons = result.get("reasons", [])
        output.append(
            {
                "repair_item_id": f"rfq3-repair-{index:04d}",
                "candidate_id": row.get("candidate_id", ""),
                "source": row.get("source", ""),
                "model_prediction": row.get("model_prediction", ""),
                "operation": item_edit.get("operation", ""),
                "source_text": item_edit.get("source_text", ""),
                "target_text": item_edit.get("target_text", ""),
                "rule_text": item_parsed.get("rule_text", ""),
                "evidence_spans_json": json.dumps(item_parsed.get("evidence_spans", []), ensure_ascii=False, sort_keys=True),
                "rationale": item_parsed.get("rationale", ""),
                "automatic_reasons": ";".join(reasons),
                "repair_instruction": repair_instruction(reasons),
            }
        )
    return output


def guidelines() -> str:
    return """# RuleFaith Qwen3 Ready-Candidate Blind Validation Guidelines

This package is for validating candidate GEC edit explanations that passed automatic RuleFaith filters.

Important boundaries:

- The candidates are automatically filtered teacher outputs, not human gold.
- The validator should not know the teacher model, automatic decision, dataset, or previous filter score.
- Judge only the displayed source sentence, model prediction, atomic edit, and explanation fields.
- Do not infer hidden model reasoning.

Fill only:

- `validator_edit_alignment`
- `validator_edit_validity`
- `validator_rule_plausibility`
- `validator_evidence_sufficiency`
- `validator_overall_decision`
- `validator_notes`

Allowed values:

- `validator_edit_alignment`: `pass`, `partial`, `fail`, `uncertain`
- `validator_edit_validity`: `valid`, `acceptable_alternative`, `invalid`, `stylistic`, `uncertain`
- `validator_rule_plausibility`: `plausible`, `weak`, `implausible`, `uncertain`
- `validator_evidence_sufficiency`: `sufficient`, `partial`, `insufficient`, `uncertain`
- `validator_overall_decision`: `accept`, `refine`, `reject`, `uncertain`

Decision rule:

- Use `accept` only when alignment passes, edit validity is understood, the rule is plausible, and evidence is sufficient.
- Use `refine` when the explanation is mostly correct but needs clearer evidence, weaker confidence, or less edit-copy wording.
- Use `reject` when the rule is implausible, evidence is insufficient, or the explanation describes the wrong edit.
- Use `uncertain` only when the item cannot be judged from the displayed information.

Notes should be short and factual.
"""


def readme() -> str:
    return """# RuleFaith Qwen3 Ready Validation Package

Files for validators:

- `guidelines.md`
- `ready_validation_form.csv`

Internal files, not for blind validators:

- `ready_validation_key.csv`
- `repair_instructions.csv`
- `handoff_manifest.json`

The blind form hides teacher/system identity and automatic filter decisions. The hidden key maps anonymized validation IDs back to candidate IDs for merging after validation.
"""


def package_zip(path: Path, files: list[Path], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in files:
            archive.write(file_path, arcname=file_path.name)


def manifest(output_dir: Path, ready_rows_count: int, refine_rows_count: int, files: list[Path], zip_path: Path) -> dict[str, Any]:
    return {
        "created_at": utc_now(),
        "git_commit": audit.git_commit(),
        "ready_candidate_count": ready_rows_count,
        "needs_refinement_count": refine_rows_count,
        "label_source": "automatic_rulefaith_filtering_ready_for_blind_validation_not_human_gold",
        "blind_validator_files": ["guidelines.md", "ready_validation_form.csv"],
        "internal_files": ["ready_validation_key.csv", "repair_instructions.csv", "handoff_manifest.json"],
        "files": {path.name: {"path": str(path), "sha256": sha256(path)} for path in files + [zip_path]},
        "output_dir": str(output_dir),
    }


def write_manifest_md(path: Path, payload: dict[str, Any], overwrite: bool) -> None:
    lines = [
        "# RuleFaith Qwen3 Ready Validation Manifest",
        "",
        f"- Created at: `{payload['created_at']}`",
        f"- Git commit: `{payload['git_commit']}`",
        f"- Ready candidates: {payload['ready_candidate_count']}",
        f"- Needs-refinement candidates: {payload['needs_refinement_count']}",
        f"- Label source: `{payload['label_source']}`",
        "",
        "## Files",
        "",
    ]
    for name, info in payload["files"].items():
        lines.append(f"- `{name}`: `{info['sha256']}`")
    write_text(path, "\n".join(lines) + "\n", overwrite)


def report(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Qwen3 Ready Validation Package Report",
            "",
            f"- Ready candidates packaged: {summary['ready_candidate_count']}",
            f"- Needs-refinement candidates packaged: {summary['needs_refinement_count']}",
            f"- Zip path: `{summary['zip_path']}`",
            f"- Zip SHA256: `{summary['zip_sha256']}`",
            "",
            "The blind form hides model/system identity and automatic filter decisions. It uses anonymized `validation_item_id` values; the candidate mapping is kept in the internal key.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a blind validation package for Qwen3 RuleFaith ready candidates.")
    parser.add_argument("--ready", type=Path, nargs="*", default=[DEFAULT_READY])
    parser.add_argument("--refine", type=Path, default=DEFAULT_REFINE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ready = read_many_jsonl([resolve(path) for path in args.ready])
    refine = read_jsonl(resolve(args.refine), allow_empty=True)
    output_dir = resolve(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    guidelines_path = output_dir / "guidelines.md"
    readme_path = output_dir / "README.md"
    form_path = output_dir / "ready_validation_form.csv"
    key_path = output_dir / "ready_validation_key.csv"
    repair_path = output_dir / "repair_instructions.csv"
    manifest_json_path = output_dir / "handoff_manifest.json"
    manifest_md_path = output_dir / "handoff_manifest.md"
    zip_path = output_dir / "rulefaith_qwen3_ready_validation_package.zip"

    write_text(guidelines_path, guidelines(), args.overwrite)
    write_text(readme_path, readme(), args.overwrite)
    write_csv(form_path, blind_rows(ready), BLIND_FIELDS, args.overwrite)
    write_csv(key_path, key_rows(ready), KEY_FIELDS, args.overwrite)
    write_csv(repair_path, repair_rows(refine), REPAIR_FIELDS, args.overwrite)
    package_zip(zip_path, [guidelines_path, readme_path, form_path], args.overwrite)
    manifest_payload = manifest(output_dir, len(ready), len(refine), [guidelines_path, readme_path, form_path, key_path, repair_path], zip_path)
    write_json(manifest_json_path, manifest_payload, args.overwrite)
    write_manifest_md(manifest_md_path, manifest_payload, args.overwrite)

    summary = {
        "created_at": manifest_payload["created_at"],
        "git_commit": manifest_payload["git_commit"],
        "ready_candidate_count": len(ready),
        "needs_refinement_count": len(refine),
        "blind_form": str(form_path),
        "hidden_key": str(key_path),
        "repair_instructions": str(repair_path),
        "zip_path": str(zip_path),
        "zip_sha256": sha256(zip_path),
        "label_source": manifest_payload["label_source"],
    }
    write_json(resolve(args.summary_output), summary, args.overwrite)
    write_text(resolve(args.report_output), report(summary), args.overwrite)
    print(json.dumps({"ready": len(ready), "needs_refinement": len(refine), "zip_sha256": summary["zip_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
