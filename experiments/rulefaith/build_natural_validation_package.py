from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import subprocess
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIRECT = ROOT / "data" / "rulefaith" / "teacher_candidates_qwen3_8b_pilot.jsonl"
DEFAULT_READY = (
    ROOT
    / "annotation"
    / "rulefaith_qwen3_ready_validation_v2"
    / "ready_validation_completed_by_codex_merged_with_key.csv"
)
DEFAULT_SCORES = ROOT / "results" / "rulefaith" / "rulefaith_ready_candidate_scores.csv"
DEFAULT_OUTPUT_DIR = ROOT / "annotation" / "rulefaith_natural"
LABEL_COLUMNS = [
    "edit_alignment_label",
    "edit_validity_label",
    "rule_correctness_label",
    "evidence_label",
    "overall_faithfulness_label",
    "learner_helpfulness_label",
    "fluency_label",
    "preference_label",
    "notes",
]


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows = []
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
    if not rows:
        raise ValueError(f"Empty JSONL file: {path}")
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Empty CSV file: {path}")
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


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


def edit_group(candidate_id: str) -> str:
    return candidate_id.split("::")[0]


def parsed_text(row: dict[str, Any] | dict[str, str], key: str) -> str:
    parsed = row.get("parsed_output")
    if isinstance(parsed, dict):
        return str(parsed.get(key, ""))
    return str(row.get(key, ""))


def parsed_evidence(row: dict[str, Any] | dict[str, str]) -> str:
    parsed = row.get("parsed_output")
    if isinstance(parsed, dict):
        return json.dumps(parsed.get("evidence_spans", []), ensure_ascii=False)
    return str(row.get("evidence_spans_json", ""))


def candidate_record(
    source_row: dict[str, Any] | dict[str, str],
    system_id: str,
    system_label: str,
    group_id: str,
    candidate_id: str,
    score_row: dict[str, str] | None = None,
) -> dict[str, Any]:
    if "model_edit" in source_row and isinstance(source_row.get("model_edit"), dict):
        edit = source_row["model_edit"]
        operation = edit.get("operation", "")
        edit_start = edit.get("start", "")
        edit_end = edit.get("end", "")
        source_text = edit.get("source_text", "")
        target_text = edit.get("target_text", "")
        error_type = edit.get("error_type", source_row.get("error_type", ""))
    else:
        operation = source_row.get("operation", "")
        edit_start = source_row.get("edit_start", "")
        edit_end = source_row.get("edit_end", "")
        source_text = source_row.get("source_text", "")
        target_text = source_row.get("target_text", "")
        error_type = source_row.get("error_type", "")
    model_edit_display = f"{operation} [{edit_start}, {edit_end}) '{source_text}' -> '{target_text}'"
    return {
        "annotation_item_id": "",
        "edit_group_id": group_id,
        "candidate_id_blind": "",
        "dataset": source_row.get("dataset", ""),
        "sample_id": source_row.get("sample_id", ""),
        "model_key": source_row.get("model_key", ""),
        "model_family": source_row.get("model_family", ""),
        "error_type": error_type,
        "error_category": source_row.get("error_category", ""),
        "source": source_row.get("source", ""),
        "model_prediction": source_row.get("model_prediction", ""),
        "model_edit": model_edit_display,
        "edit_description": parsed_text(source_row, "edit_description"),
        "edit_validity_claim": parsed_text(source_row, "edit_validity"),
        "rule_text": parsed_text(source_row, "rule_text"),
        "evidence_spans_json": parsed_evidence(source_row),
        "rationale": parsed_text(source_row, "rationale"),
        "confidence": parsed_text(source_row, "confidence") or source_row.get("confidence", ""),
        "system_id": system_id,
        "system_label": system_label,
        "source_candidate_id": candidate_id,
        "rulefaith_score": score_row.get("rulefaith_score", "") if score_row else "",
        "rulefaith_bucket": score_row.get("rulefaith_bucket", "") if score_row else "",
    }


def build_items(
    direct_rows: list[dict[str, Any]],
    ready_rows: list[dict[str, str]],
    score_rows: list[dict[str, str]],
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    direct_by_group: dict[str, dict[str, Any]] = {}
    for row in direct_rows:
        if row.get("provider") != "qwen3_8b" or row.get("parse_status") != "parsed_json":
            continue
        if row.get("candidate_type") not in {"natural", "rule_grounded"}:
            continue
        group = row.get("rulefaith_pool_id") or edit_group(row["candidate_id"])
        current = direct_by_group.get(group)
        if current is None or (current.get("candidate_type") != "natural" and row.get("candidate_type") == "natural"):
            direct_by_group[group] = row
    ready_by_id = {row["candidate_id"]: row for row in ready_rows}
    score_by_id = {row["candidate_id"]: row for row in score_rows}
    by_group: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in score_rows:
        by_group[row["edit_group"]].append(row)

    items: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for group_id, rows in sorted(by_group.items()):
        direct = direct_by_group.get(group_id)
        if direct is None:
            skipped.append({"edit_group_id": group_id, "reason": "missing_parsed_direct_candidate"})
            continue
        selected_score = max(rows, key=lambda row: (float(row["rulefaith_score"]), row["candidate_id"]))
        ready = ready_by_id.get(selected_score["candidate_id"])
        if ready is None:
            skipped.append({"edit_group_id": group_id, "reason": "missing_ready_candidate"})
            continue
        group_label = f"rf-natural-{len(items)//2 + 1:04d}"
        direct_system = f"qwen3_direct_{direct.get('candidate_type', 'candidate')}"
        direct_label = f"Qwen3 direct {direct.get('candidate_type', 'candidate')}"
        items.append(candidate_record(direct, direct_system, direct_label, group_label, direct["candidate_id"]))
        items.append(
            candidate_record(
                ready,
                "rulefaith_score_top1",
                "RuleFaith deployable top-1",
                group_label,
                ready["candidate_id"],
                score_by_id.get(ready["candidate_id"]),
            )
        )

    rng = random.Random(seed)
    rng.shuffle(items)
    for index, row in enumerate(items, 1):
        row["annotation_item_id"] = f"rf-nat-{index:04d}"
        row["candidate_id_blind"] = f"candidate-{index:04d}"
    key_rows = [
        {
            "annotation_item_id": row["annotation_item_id"],
            "edit_group_id": row["edit_group_id"],
            "candidate_id_blind": row["candidate_id_blind"],
            "system_id": row["system_id"],
            "system_label": row["system_label"],
            "source_candidate_id": row["source_candidate_id"],
            "rulefaith_score": row["rulefaith_score"],
            "rulefaith_bucket": row["rulefaith_bucket"],
        }
        for row in items
    ]
    stats = {
        "item_count": len(items),
        "edit_group_count": len({row["edit_group_id"] for row in items}),
        "system_counts": dict(Counter(row["system_id"] for row in items)),
        "dataset_counts": dict(Counter(row["dataset"] for row in items)),
        "model_key_counts": dict(Counter(row["model_key"] for row in items)),
        "operation_counts": dict(Counter(row["model_edit"].split(" ", 1)[0] for row in items)),
        "skipped": skipped,
    }
    return items, key_rows, stats


def annotation_rows(items: list[dict[str, Any]], seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    rows = []
    for item in items:
        public = {k: v for k, v in item.items() if k not in {"system_id", "system_label", "source_candidate_id", "rulefaith_score", "rulefaith_bucket"}}
        for label in LABEL_COLUMNS:
            public[label] = ""
        rows.append(public)
    rng.shuffle(rows)
    return rows


def adjudication_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for item in items:
        public = {k: v for k, v in item.items() if k not in {"system_id", "system_label", "source_candidate_id", "rulefaith_score", "rulefaith_bucket"}}
        for prefix in ["annotator_a", "annotator_b", "final"]:
            for label in LABEL_COLUMNS:
                public[f"{prefix}_{label}"] = ""
        rows.append(public)
    return rows


def public_fields() -> list[str]:
    return [
        "annotation_item_id",
        "edit_group_id",
        "candidate_id_blind",
        "dataset",
        "sample_id",
        "model_key",
        "model_family",
        "error_type",
        "error_category",
        "source",
        "model_prediction",
        "model_edit",
        "edit_description",
        "edit_validity_claim",
        "rule_text",
        "evidence_spans_json",
        "rationale",
        "confidence",
        *LABEL_COLUMNS,
    ]


def key_fields() -> list[str]:
    return [
        "annotation_item_id",
        "edit_group_id",
        "candidate_id_blind",
        "system_id",
        "system_label",
        "source_candidate_id",
        "rulefaith_score",
        "rulefaith_bucket",
    ]


def adjudication_fields() -> list[str]:
    base = [field for field in public_fields() if field not in LABEL_COLUMNS]
    labels = [f"{prefix}_{label}" for prefix in ["annotator_a", "annotator_b", "final"] for label in LABEL_COLUMNS]
    return base + labels


def guidelines_text() -> str:
    return """# RuleFaith Natural Explanation Annotation Guidelines

You are evaluating natural edit-level explanations for Grammatical Error Correction (GEC).

For each row, judge only the displayed source sentence, model prediction, atomic model edit, and explanation fields. Do not infer hidden model reasoning. Do not assume the edit is correct.

Fill these labels:

- `edit_alignment_label`: correct, partially_correct, incorrect, uncertain.
- `edit_validity_label`: valid, acceptable_alternative, invalid, stylistic, uncertain.
- `rule_correctness_label`: correct, partially_correct, incorrect, not_applicable, uncertain.
- `evidence_label`: correct, partially_correct, incorrect, not_provided, uncertain.
- `overall_faithfulness_label`: faithful, partially_faithful, unfaithful, uncertain.
- `learner_helpfulness_label`: helpful, partially_helpful, unhelpful, uncertain.
- `fluency_label`: fluent, mostly_fluent, disfluent, uncertain.
- `preference_label`: best_in_group, acceptable_not_best, not_preferred, uncertain.
- `notes`: concise explanation when needed.

Important rules:

1. Evaluate only the current atomic edit, not every edit in the full model prediction.
2. A wrong model edit can be faithfully described if the explanation honestly identifies the problem.
3. Pure edit-copy is at most partially faithful unless it also gives a correct rule and contextual evidence.
4. Evidence must be source-grounded. Mentioning only the changed token is not automatically contextual evidence.
5. Do not reward long explanations unless they are specific, correct, and evidence-grounded.
6. Do not use system identity. The rows are randomized and anonymized.
7. Rows sharing the same `edit_group_id` are alternative explanations for the same edit. Use `preference_label` relative to other rows in the same group after reviewing the group.
"""


def data_card_text(stats: dict[str, Any], seed: int) -> str:
    return f"""# RuleFaith Natural Explanation Validation Data Card

Generated: {now_utc()}
Git commit: {git_commit()}
Seed: {seed}

## Purpose

This package supports blinded evaluation of natural GEC edit explanations. It compares Qwen3 direct natural explanations with RuleFaith deployable top-1 outputs for the same model-produced edits.

## Scope

- Items: {stats['item_count']}
- Edit groups: {stats['edit_group_count']}
- Systems per group: 2
- System identities are hidden from annotators and stored only in `hidden_system_key.csv`.

## Counts

- Systems: {stats['system_counts']}
- Datasets: {stats['dataset_counts']}
- Correctors: {stats['model_key_counts']}
- Operations: {stats['operation_counts']}

## Label Boundary

This package contains model-generated explanations. It does not contain human labels yet. It does not expose Codex/AI pseudo-validation decisions to annotators.

## Known Limitations

This is a small validation package derived from the current 41-row Qwen3 ready pool and 23 edit groups. It is suitable for a method-pilot validation pass, not for final AAAI-scale human evaluation by itself.
"""


def readme_text() -> str:
    return """# RuleFaith Natural Explanation Validation Package

Annotators should use:

- `form_annotator_a.csv`
- `form_annotator_b.csv`
- `guidelines.md`
- `data_card.md`

Do not open `hidden_system_key.csv`; it is not included in the handoff zip.

After two independent annotations are complete, use `adjudication_form.csv` for final adjudication.
"""


def write_package(output_dir: Path, items: list[dict[str, Any]], key_rows: list[dict[str, Any]], stats: dict[str, Any], seed: int, overwrite: bool) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    form_a = output_dir / "form_annotator_a.csv"
    form_b = output_dir / "form_annotator_b.csv"
    adjudication = output_dir / "adjudication_form.csv"
    key = output_dir / "hidden_system_key.csv"
    guidelines = output_dir / "guidelines.md"
    data_card = output_dir / "data_card.md"
    readme = output_dir / "README.md"
    manifest_json = output_dir / "manifest.json"
    manifest_md = output_dir / "manifest.md"
    zip_path = output_dir / "rulefaith_natural_validation_handoff.zip"

    write_csv(form_a, annotation_rows(items, seed + 1), public_fields(), overwrite)
    write_csv(form_b, annotation_rows(items, seed + 2), public_fields(), overwrite)
    write_csv(adjudication, adjudication_rows(items), adjudication_fields(), overwrite)
    write_csv(key, key_rows, key_fields(), overwrite)
    guidelines.write_text(guidelines_text(), encoding="utf-8")
    data_card.write_text(data_card_text(stats, seed), encoding="utf-8")
    readme.write_text(readme_text(), encoding="utf-8")

    public_files = [form_a, form_b, adjudication, guidelines, data_card, readme]
    if zip_path.exists() and not overwrite:
        raise FileExistsError(f"{zip_path} exists; pass --overwrite")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in public_files:
            zf.write(file, arcname=file.name)

    manifest = {
        "generated_at": now_utc(),
        "git_commit": git_commit(),
        "seed": seed,
        "stats": stats,
        "files": {file.name: {"sha256": sha256(file), "bytes": file.stat().st_size} for file in [*public_files, key, zip_path]},
        "hidden_files_not_in_zip": ["hidden_system_key.csv"],
        "handoff_zip": zip_path.name,
    }
    write_json(manifest_json, manifest, overwrite)
    manifest_md.write_text(
        "\n".join(
            [
                "# RuleFaith Natural Validation Manifest",
                "",
                f"- generated_at: `{manifest['generated_at']}`",
                f"- git_commit: `{manifest['git_commit']}`",
                f"- items: `{stats['item_count']}`",
                f"- edit_groups: `{stats['edit_group_count']}`",
                f"- handoff_zip: `{zip_path.name}`",
                "- hidden key excluded from zip: `hidden_system_key.csv`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a blinded natural-explanation annotation package for RuleFaith.")
    parser.add_argument("--direct", type=Path, default=DEFAULT_DIRECT)
    parser.add_argument("--ready", type=Path, default=DEFAULT_READY)
    parser.add_argument("--scores", type=Path, default=DEFAULT_SCORES)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    direct = read_jsonl(resolve(args.direct))
    ready = read_csv(resolve(args.ready))
    scores = read_csv(resolve(args.scores))
    items, key_rows, stats = build_items(direct, ready, scores, args.seed)
    manifest = write_package(resolve(args.output_dir), items, key_rows, stats, args.seed, args.overwrite)
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
