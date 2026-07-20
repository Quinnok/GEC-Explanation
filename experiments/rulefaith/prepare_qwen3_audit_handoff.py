from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.rulefaith import build_qwen3_manual_audit as audit


DEFAULT_AUDIT_DIR = ROOT / "annotation" / "rulefaith_qwen3_audit_canonicalized"
DEFAULT_OUTPUT_DIR = DEFAULT_AUDIT_DIR / "handoff_package"
DEFAULT_ZIP = DEFAULT_AUDIT_DIR / "qwen3_canonicalized_human_audit_package.zip"
DEFAULT_MANIFEST = DEFAULT_AUDIT_DIR / "handoff_manifest.json"
DEFAULT_REPORT = DEFAULT_AUDIT_DIR / "handoff_manifest.md"

AUDITOR_FILES = {
    "README_FOR_AUDITOR.md": "README_HANDOFF.md",
    "guidelines.md": "guidelines.md",
    "manual_audit_form.csv": "manual_audit_form.csv",
}

FORBIDDEN_KEY_COLUMNS = {
    "bucket",
    "audit_priority",
    "risk_count",
    "risk_reasons",
    "behavior",
    "error_type",
    "selected_for_manual_audit",
}

HUMAN_FIELDS = [
    "human_alignment_error",
    "human_validity_error",
    "human_wrong_rule",
    "human_inapplicable_rule",
    "human_missing_evidence",
    "human_wrong_evidence",
    "human_generic_explanation",
    "human_edit_copy",
    "human_semantic_distortion",
    "human_unsupported_confidence",
    "human_notes",
    "human_decision",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if not rows:
        raise ValueError(f"CSV has no rows: {path}")
    return rows


def write_json(path: Path, obj: Any, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def copy_file(source: Path, target: Path, overwrite: bool) -> None:
    if target.exists() and not overwrite:
        raise FileExistsError(f"{target} exists; pass --overwrite")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())


def validate_form(form: Path, key: Path, expected_rows: int) -> dict[str, Any]:
    form_rows = read_csv(form)
    key_rows = read_csv(key)
    form_ids = [row["candidate_id"] for row in form_rows]
    key_ids = [row["candidate_id"] for row in key_rows]
    if len(form_rows) != expected_rows:
        raise ValueError(f"Expected {expected_rows} audit rows, found {len(form_rows)}")
    if len(form_ids) != len(set(form_ids)):
        raise ValueError("Duplicate candidate_id in blind audit form")
    if set(form_ids) != set(key_ids):
        raise ValueError("Blind audit form candidate_id set does not match hidden key")
    leaked_columns = sorted(FORBIDDEN_KEY_COLUMNS.intersection(form_rows[0].keys()))
    if leaked_columns:
        raise ValueError(f"Blind audit form contains hidden key columns: {leaked_columns}")
    missing_human_fields = [field for field in HUMAN_FIELDS if field not in form_rows[0]]
    if missing_human_fields:
        raise ValueError(f"Blind audit form is missing human fields: {missing_human_fields}")
    filled_human_cells = sum(1 for row in form_rows for field in HUMAN_FIELDS if row.get(field, "").strip())
    return {
        "row_count": len(form_rows),
        "candidate_id_count": len(set(form_ids)),
        "key_row_count": len(key_rows),
        "hidden_key_columns_in_form": leaked_columns,
        "human_annotation_cells_filled": filled_human_cells,
        "human_annotation_cells_blank": len(form_rows) * len(HUMAN_FIELDS) - filled_human_cells,
    }


def build_zip(package_dir: Path, zip_path: Path, overwrite: bool) -> None:
    if zip_path.exists() and not overwrite:
        raise FileExistsError(f"{zip_path} exists; pass --overwrite")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(package_dir.iterdir()):
            if path.is_file():
                archive.write(path, arcname=path.name)


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    audit_dir = resolve(args.audit_dir)
    output_dir = resolve(args.output_dir)
    zip_path = resolve(args.zip_output)
    manifest_path = resolve(args.manifest_output)
    report_path = resolve(args.report_output)
    form = audit_dir / "manual_audit_form.csv"
    key = audit_dir / "manual_audit_key.csv"
    validation = validate_form(form, key, args.expected_rows)

    output_dir.mkdir(parents=True, exist_ok=True)
    copied_files: list[dict[str, Any]] = []
    for target_name, source_name in AUDITOR_FILES.items():
        source = audit_dir / source_name
        if not source.exists():
            raise FileNotFoundError(source)
        target = output_dir / target_name
        copy_file(source, target, args.overwrite)
        copied_files.append({"filename": target.name, "size_bytes": target.stat().st_size, "sha256": sha256(target)})

    forbidden_in_package = sorted(path.name for path in output_dir.iterdir() if "key" in path.name.lower())
    if forbidden_in_package:
        raise ValueError(f"Package contains hidden key-like files: {forbidden_in_package}")
    build_zip(output_dir, zip_path, args.overwrite)

    return {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "audit_dir": str(audit_dir),
        "package_dir": str(output_dir),
        "zip_file": str(zip_path),
        "manifest_file": str(manifest_path),
        "report_file": str(report_path),
        "expected_rows": args.expected_rows,
        "validation": validation,
        "auditor_files": copied_files,
        "zip_sha256": sha256(zip_path),
        "zip_size_bytes": zip_path.stat().st_size,
        "hidden_key_file_kept_out_of_package": str(key),
        "decision": "ready_for_human_auditor_handoff",
    }


def markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 Canonicalized Human Audit Handoff Manifest",
        "",
        "This package is the blind human-audit handoff for Qwen3-8B teacher candidates after deterministic evidence-span canonicalization.",
        "",
        "## Package",
        "",
        f"- Package directory: `{manifest['package_dir']}`",
        f"- Zip file: `{manifest['zip_file']}`",
        f"- Zip SHA256: `{manifest['zip_sha256']}`",
        f"- Zip size bytes: `{manifest['zip_size_bytes']}`",
        "",
        "## Validation",
        "",
    ]
    for key, value in manifest["validation"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Files Included For Auditor",
            "",
        ]
    )
    for item in manifest["auditor_files"]:
        lines.append(f"- `{item['filename']}`: {item['size_bytes']} bytes, sha256 `{item['sha256']}`")
    lines.extend(
        [
            "",
            "## Files Not Included",
            "",
            f"- Hidden key file: `{manifest['hidden_key_file_kept_out_of_package']}`",
            "",
            "## Next Step",
            "",
            "Send only the zip file or package directory contents to a real human auditor. After the completed CSV returns, validate it with `experiments/rulefaith/validate_qwen3_human_audit.py`.",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare the blind Qwen3 canonicalized audit handoff package.")
    parser.add_argument("--audit-dir", type=Path, default=DEFAULT_AUDIT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--zip-output", type=Path, default=DEFAULT_ZIP)
    parser.add_argument("--manifest-output", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--expected-rows", type=int, default=80)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_manifest(args)
    write_json(resolve(args.manifest_output), manifest, args.overwrite)
    write_text(resolve(args.report_output), markdown(manifest), args.overwrite)
    print(json.dumps({"decision": manifest["decision"], "zip_file": manifest["zip_file"], "zip_sha256": manifest["zip_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
