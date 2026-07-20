from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.rulefaith import build_qwen3_manual_audit as audit


DEFAULT_FORM = ROOT / "annotation" / "rulefaith_qwen3_audit_canonicalized" / "manual_audit_form.csv"
DEFAULT_DIAGNOSTICS = ROOT / "results" / "rulefaith" / "qwen3_manual_audit_after_canonicalization.csv"
DEFAULT_OUTPUT = ROOT / "annotation" / "rulefaith_qwen3_audit_canonicalized" / "manual_audit_codex_prelabeled.csv"
DEFAULT_SUMMARY = ROOT / "results" / "rulefaith" / "qwen3_codex_prelabeled_audit_summary.json"
DEFAULT_REPORT = ROOT / "results" / "rulefaith" / "qwen3_codex_prelabeled_audit_report.md"

ISSUE_FIELDS = [
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
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if not rows:
        raise ValueError(f"CSV has no rows: {path}")
    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


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


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def confidence(row: dict[str, str]) -> float:
    try:
        return float(row.get("confidence", "0") or 0.0)
    except ValueError:
        return 0.0


def label(value: bool) -> str:
    return "yes" if value else "no"


def diag_for(form_rows: list[dict[str, str]], diagnostics: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    selected_ids = {row["candidate_id"] for row in form_rows}
    diag = {row["candidate_id"]: row for row in diagnostics if row.get("candidate_id") in selected_ids}
    missing = selected_ids - set(diag)
    if missing:
        raise ValueError(f"Diagnostics missing candidate IDs: {sorted(missing)[:10]}")
    return diag


def prelabel_row(row: dict[str, str], diag: dict[str, str]) -> dict[str, str]:
    output = dict(row)
    alignment_error = truthy(diag.get("alignment_error")) or not truthy(diag.get("source_span_match")) or not truthy(diag.get("target_present_in_prediction"))
    validity_error = truthy(diag.get("validity_error_auto")) or truthy(diag.get("possible_false_rationalization"))
    wrong_rule = truthy(diag.get("possible_false_rationalization")) or (truthy(diag.get("semantic_distortion_auto")) and "valid" in diag.get("edit_validity", "").lower())
    inapplicable_rule = truthy(diag.get("semantic_distortion_auto")) or truthy(diag.get("validity_error_auto"))
    missing_evidence = truthy(diag.get("missing_evidence"))
    wrong_evidence = truthy(diag.get("wrong_evidence_auto")) or truthy(diag.get("evidence_text_found_in_prediction_only"))
    generic = truthy(diag.get("generic_explanation"))
    edit_copy = truthy(diag.get("edit_copy")) or truthy(diag.get("rule_edit_copy"))
    semantic_distortion = truthy(diag.get("semantic_distortion_auto"))
    unsupported_conf = truthy(diag.get("unsupported_confidence")) or (
        confidence(diag) >= 0.85 and (missing_evidence or wrong_evidence or validity_error or wrong_rule)
    )

    assignments = {
        "human_alignment_error": alignment_error,
        "human_validity_error": validity_error,
        "human_wrong_rule": wrong_rule,
        "human_inapplicable_rule": inapplicable_rule,
        "human_missing_evidence": missing_evidence,
        "human_wrong_evidence": wrong_evidence,
        "human_generic_explanation": generic,
        "human_edit_copy": edit_copy,
        "human_semantic_distortion": semantic_distortion,
        "human_unsupported_confidence": unsupported_conf,
    }
    for field, value in assignments.items():
        output[field] = label(value)

    severe = alignment_error or validity_error or wrong_rule or inapplicable_rule or semantic_distortion
    repairable = missing_evidence or wrong_evidence or generic or edit_copy or unsupported_conf
    if alignment_error and not truthy(diag.get("source_span_match")):
        decision = "abstain"
    elif severe:
        decision = "reject"
    elif repairable:
        decision = "refine"
    else:
        decision = "accept"
    output["human_decision"] = decision
    reasons = [field.replace("human_", "") for field, value in output.items() if field in ISSUE_FIELDS and value == "yes"]
    if reasons:
        output["human_notes"] = "Codex prelabel from automatic diagnostics: " + ", ".join(reasons[:5]) + ("." if len(reasons) <= 5 else ", ...")
    else:
        output["human_notes"] = "Codex prelabel: no automatic issue triggered."
    return output


def summarize(rows: list[dict[str, str]]) -> dict[str, Any]:
    decision_counts = Counter(row["human_decision"] for row in rows)
    issue_counts = {field: Counter(row[field] for row in rows) for field in ISSUE_FIELDS}
    return {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "row_count": len(rows),
        "label_source": "codex_ai_assisted_prelabelling_not_human_gold",
        "decision_counts": dict(sorted(decision_counts.items())),
        "issue_counts": {field: dict(sorted(counter.items())) for field, counter in issue_counts.items()},
        "accept_count": decision_counts.get("accept", 0),
        "refine_count": decision_counts.get("refine", 0),
        "reject_count": decision_counts.get("reject", 0),
        "abstain_count": decision_counts.get("abstain", 0),
        "decision": "usable_as_ai_assisted_prelabelling_only_not_human_audit",
    }


def markdown(summary: dict[str, Any], rows: list[dict[str, str]]) -> str:
    lines = [
        "# Qwen3 Canonicalized Audit Codex Prelabels",
        "",
        "These labels are generated by Codex-assisted rules over the blind form and automatic diagnostics. They are not human labels, not human gold, and must not be reported as human evaluation.",
        "",
        "## Summary",
        "",
    ]
    for key in ["row_count", "accept_count", "refine_count", "reject_count", "abstain_count", "decision"]:
        lines.append(f"- `{key}`: `{summary[key]}`")
    lines.extend(["", "## Issue Counts", ""])
    for field, counts in summary["issue_counts"].items():
        lines.append(f"- `{field}`: `{counts}`")
    lines.extend(["", "## High-Risk Examples", ""])
    for row in rows:
        if row["human_decision"] not in {"reject", "abstain"}:
            continue
        lines.extend(
            [
                f"### {row['candidate_id']}",
                "",
                f"- decision: `{row['human_decision']}`",
                f"- issues: `{', '.join(field for field in ISSUE_FIELDS if row[field] == 'yes')}`",
                f"- source: {row.get('source', '')}",
                f"- edit: `{row.get('operation')}` `{row.get('source_text')}` -> `{row.get('target_text')}`",
                f"- rule: {row.get('rule_text', '')}",
                f"- evidence: `{row.get('evidence_spans_json', '')}`",
                f"- notes: {row.get('human_notes', '')}",
                "",
            ]
        )
        if sum(1 for item in rows[: rows.index(row) + 1] if item["human_decision"] in {"reject", "abstain"}) >= 20:
            lines.append("Additional high-risk rows are available in the CSV.")
            break
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prefill the Qwen3 canonicalized audit form with Codex-assisted labels.")
    parser.add_argument("--form", type=Path, default=DEFAULT_FORM)
    parser.add_argument("--diagnostics", type=Path, default=DEFAULT_DIAGNOSTICS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    form_rows = read_csv(resolve(args.form))
    diagnostics = read_csv(resolve(args.diagnostics))
    diagnostics_by_id = diag_for(form_rows, diagnostics)
    prelabels = [prelabel_row(row, diagnostics_by_id[row["candidate_id"]]) for row in form_rows]
    summary = summarize(prelabels)
    summary["input_form"] = str(resolve(args.form))
    summary["diagnostics"] = str(resolve(args.diagnostics))
    summary["output"] = str(resolve(args.output))
    write_csv(resolve(args.output), prelabels, list(form_rows[0].keys()), args.overwrite)
    write_json(resolve(args.summary_output), summary, args.overwrite)
    write_text(resolve(args.report_output), markdown(summary, prelabels), args.overwrite)
    print(json.dumps({"decision": summary["decision"], "decision_counts": summary["decision_counts"], "row_count": summary["row_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
