from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_TEX = ROOT / "results" / "paper_assets" / "rulefaith_qwen3_method_funnel.tex"
DEFAULT_OUTPUT_CSV = ROOT / "results" / "paper_assets" / "rulefaith_qwen3_method_funnel.csv"


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data


def rows_from_results() -> list[dict[str, str]]:
    field_aware = read_json(ROOT / "results" / "rulefaith" / "qwen3_field_aware_rulefaith_selection_stats.json")
    target_masked = read_json(ROOT / "results" / "rulefaith" / "qwen3_target_masked_validation_stats.json")
    rule_audit = read_json(ROOT / "results" / "rulefaith" / "qwen3_rule_plausibility_audit_stats.json")
    repair = read_json(ROOT / "results" / "rulefaith" / "qwen3_targeted_repair_stats.json")
    pseudo = read_json(ROOT / "results" / "rulefaith" / "qwen3_ready_validation_codex_summary.json")
    return [
        {
            "stage": "Field-aware gate",
            "input": str(field_aware["candidate_count"]),
            "kept": str(field_aware["bucket_counts"]["accepted"] + field_aware["bucket_counts"]["refine"]),
            "revise": str(field_aware["bucket_counts"]["refine"]),
            "reject": str(field_aware["bucket_counts"]["rejected"]),
            "evidence": "Automatic field-aware RuleFaith gate",
        },
        {
            "stage": "Target-masked validation",
            "input": str(target_masked["candidate_count"]),
            "kept": str(target_masked["target_masked_bucket_counts"]["validated"]),
            "revise": str(target_masked["target_masked_bucket_counts"]["refine"]),
            "reject": str(target_masked["target_masked_bucket_counts"]["rejected"]),
            "evidence": "Automatic target-masked gate",
        },
        {
            "stage": "Rule/evidence audit",
            "input": str(rule_audit["candidate_count"]),
            "kept": str(rule_audit["decision_counts"]["ready_for_human_spotcheck"]),
            "revise": str(rule_audit["decision_counts"]["needs_refinement"]),
            "reject": str(rule_audit["decision_counts"]["reject"]),
            "evidence": "Automatic rule/evidence audit",
        },
        {
            "stage": "Targeted repair",
            "input": str(repair["candidate_count"]),
            "kept": str(repair["candidate_count"]),
            "revise": "0",
            "reject": "0",
            "evidence": "Deterministic repair plus revalidation",
        },
        {
            "stage": "Codex pseudo-validation",
            "input": str(pseudo["candidate_count"]),
            "kept": str(pseudo["validator_overall_decision_counts"]["accept"]),
            "revise": str(pseudo["validator_overall_decision_counts"]["refine"]),
            "reject": str(pseudo["validator_overall_decision_counts"]["reject"]),
            "evidence": "AI pseudo-validation, not human gold",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, str]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["stage", "input", "kept", "revise", "reject", "evidence"])
        writer.writeheader()
        writer.writerows(rows)


def latex_escape(value: str) -> str:
    return (
        value.replace("\\", "\\textbackslash{}")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("_", "\\_")
        .replace("#", "\\#")
    )


def write_tex(path: Path, rows: list[dict[str, str]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Stage & Input & Kept & Refine & Reject \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(
            f"{latex_escape(row['stage'])} & {row['input']} & {row['kept']} & {row['revise']} & {row['reject']} \\\\"
        )
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\caption{Qwen3-8B RuleFaith method-pilot funnel. The final row uses Codex/AI pseudo-validation for internal triage, not human-gold evidence.}",
            "\\label{tab:rulefaith-qwen3-funnel}",
            "\\end{table}",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate RuleFaith method-pilot paper assets from result JSON files.")
    parser.add_argument("--output-tex", type=Path, default=DEFAULT_OUTPUT_TEX)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = rows_from_results()
    write_csv(resolve(args.output_csv), rows, args.overwrite)
    write_tex(resolve(args.output_tex), rows, args.overwrite)
    print(json.dumps({"rows": rows, "output_tex": str(resolve(args.output_tex)), "output_csv": str(resolve(args.output_csv))}, indent=2))


if __name__ == "__main__":
    main()
