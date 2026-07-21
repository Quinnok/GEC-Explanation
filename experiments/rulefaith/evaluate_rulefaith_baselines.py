from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_READY_VALIDATION = (
    ROOT
    / "annotation"
    / "rulefaith_qwen3_ready_validation_v2"
    / "ready_validation_completed_by_codex_merged_with_key.csv"
)
DEFAULT_OUTPUT_DIR = ROOT / "results" / "rulefaith"
DEFAULT_ASSET_DIR = ROOT / "results" / "paper_assets"
DEFAULT_DOC = ROOT / "docs" / "rulefaith_loop_O_baseline_results.md"

UTILITY = {"accept": 1.0, "refine": 0.5, "reject": 0.0}


@dataclass(frozen=True)
class TeacherSpec:
    system: str
    provider: str
    diagnostic_path: Path
    filtering_path: Path
    label_source: str


TEACHER_SPECS = [
    TeacherSpec(
        system="FLAN-T5-base direct",
        provider="open_teacher",
        diagnostic_path=ROOT / "results" / "rulefaith" / "open_teacher_diagnostic_metrics.json",
        filtering_path=ROOT / "results" / "rulefaith" / "open_teacher_filtering_statistics.json",
        label_source="automatic_prefilter",
    ),
    TeacherSpec(
        system="Qwen2.5-0.5B direct",
        provider="qwen_small",
        diagnostic_path=ROOT / "results" / "rulefaith" / "qwen_teacher_diagnostic_metrics.json",
        filtering_path=ROOT / "results" / "rulefaith" / "qwen_filtering_statistics.json",
        label_source="automatic_prefilter",
    ),
    TeacherSpec(
        system="Qwen2.5-1.5B probe",
        provider="qwen_small",
        diagnostic_path=ROOT / "results" / "rulefaith" / "qwen15_probe_diagnostic_metrics.json",
        filtering_path=ROOT / "results" / "rulefaith" / "qwen15_probe_filtering_statistics.json",
        label_source="automatic_prefilter_probe20",
    ),
    TeacherSpec(
        system="Qwen3-8B direct",
        provider="qwen3_8b",
        diagnostic_path=ROOT / "results" / "rulefaith" / "qwen3_8b_teacher_diagnostic_metrics.json",
        filtering_path=ROOT / "results" / "rulefaith" / "qwen3_8b_filtering_statistics.json",
        label_source="automatic_prefilter",
    ),
]


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Empty CSV: {path}")
    return rows


def current_git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def get_provider_summary(metrics: dict[str, Any], provider: str) -> dict[str, Any]:
    if isinstance(metrics.get("summary"), dict):
        metrics = metrics["summary"]
    by_provider = metrics.get("by_provider")
    if isinstance(by_provider, dict) and provider in by_provider:
        summary = by_provider[provider]
        if isinstance(summary, dict):
            return summary
    return metrics


def fmt_float(value: Any, places: int = 3) -> str:
    if value is None or value == "":
        return ""
    try:
        return f"{float(value):.{places}f}"
    except (TypeError, ValueError):
        return ""


def pct(value: float) -> str:
    return f"{100 * value:.1f}"


def teacher_baseline_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for spec in TEACHER_SPECS:
        diagnostics = get_provider_summary(read_json(spec.diagnostic_path), spec.provider)
        filtering = read_json(spec.filtering_path)
        buckets = filtering.get("bucket_counts", {})
        n = int(filtering.get("candidate_count", diagnostics.get("candidate_count", 0)))
        accepted = int(buckets.get("accepted", 0))
        refine = int(buckets.get("refine", 0))
        rejected = int(buckets.get("rejected", 0))
        rows.append(
            {
                "system": spec.system,
                "n": str(n),
                "parse_json_rate": fmt_float(diagnostics.get("parse_json_rate")),
                "alignment_proxy_pass_rate": fmt_float(diagnostics.get("alignment_proxy_pass_rate")),
                "missing_rule_text_rate": fmt_float(diagnostics.get("missing_rule_text_rate")),
                "rule_edit_copy_rate": fmt_float(diagnostics.get("rule_edit_copy_rate")),
                "contextual_evidence_rate": fmt_float(diagnostics.get("contextual_evidence_rate")),
                "high_risk_rate": fmt_float(diagnostics.get("high_risk_rate")),
                "accepted": str(accepted),
                "refine": str(refine),
                "rejected": str(rejected),
                "accepted_rate": fmt_float(accepted / n if n else 0.0),
                "non_rejected_rate": fmt_float((accepted + refine) / n if n else 0.0),
                "label_source": spec.label_source,
            }
        )
    return rows


def method_gate_rows() -> list[dict[str, str]]:
    field_aware = read_json(ROOT / "results" / "rulefaith" / "qwen3_field_aware_rulefaith_selection_stats.json")
    target_masked = read_json(ROOT / "results" / "rulefaith" / "qwen3_target_masked_validation_stats.json")
    rule_audit = read_json(ROOT / "results" / "rulefaith" / "qwen3_rule_plausibility_audit_stats.json")
    repair = read_json(ROOT / "results" / "rulefaith" / "qwen3_targeted_repair_stats.json")
    pseudo = read_json(ROOT / "results" / "rulefaith" / "qwen3_ready_validation_codex_summary.json")

    row_specs = [
        (
            "Qwen3 direct prefilter",
            "qwen3_8b_filtering_statistics.json",
            read_json(ROOT / "results" / "rulefaith" / "qwen3_8b_filtering_statistics.json")["candidate_count"],
            read_json(ROOT / "results" / "rulefaith" / "qwen3_8b_filtering_statistics.json")["bucket_counts"]["accepted"],
            read_json(ROOT / "results" / "rulefaith" / "qwen3_8b_filtering_statistics.json")["bucket_counts"]["refine"],
            read_json(ROOT / "results" / "rulefaith" / "qwen3_8b_filtering_statistics.json")["bucket_counts"]["rejected"],
            "automatic_prefilter",
        ),
        (
            "Field-aware RuleFaith gate",
            "qwen3_field_aware_rulefaith_selection_stats.json",
            field_aware["candidate_count"],
            field_aware["bucket_counts"]["accepted"],
            field_aware["bucket_counts"]["refine"],
            field_aware["bucket_counts"]["rejected"],
            "automatic_gate",
        ),
        (
            "Target-masked validation",
            "qwen3_target_masked_validation_stats.json",
            target_masked["candidate_count"],
            target_masked["target_masked_bucket_counts"]["validated"],
            target_masked["target_masked_bucket_counts"]["refine"],
            target_masked["target_masked_bucket_counts"]["rejected"],
            "automatic_gate",
        ),
        (
            "Rule/evidence audit",
            "qwen3_rule_plausibility_audit_stats.json",
            rule_audit["candidate_count"],
            rule_audit["decision_counts"]["ready_for_human_spotcheck"],
            rule_audit["decision_counts"]["needs_refinement"],
            rule_audit["decision_counts"]["reject"],
            "automatic_rule_evidence_audit",
        ),
        (
            "Targeted deterministic repair",
            "qwen3_targeted_repair_stats.json",
            repair["candidate_count"],
            repair["candidate_count"],
            0,
            0,
            "deterministic_repair_revalidated",
        ),
        (
            "Codex pseudo-validation",
            "qwen3_ready_validation_codex_summary.json",
            pseudo["candidate_count"],
            pseudo["validator_overall_decision_counts"]["accept"],
            pseudo["validator_overall_decision_counts"]["refine"],
            pseudo["validator_overall_decision_counts"]["reject"],
            "codex_ai_pseudo_validation_not_human",
        ),
    ]
    rows = []
    for stage, source_file, n, accepted, refine, rejected, label_source in row_specs:
        n_int = int(n)
        rows.append(
            {
                "stage": stage,
                "source_file": source_file,
                "n": str(n_int),
                "accepted_or_ready": str(int(accepted)),
                "refine": str(int(refine)),
                "rejected": str(int(rejected)),
                "accepted_or_ready_rate": fmt_float(int(accepted) / n_int if n_int else 0.0),
                "non_rejected_rate": fmt_float((int(accepted) + int(refine)) / n_int if n_int else 0.0),
                "label_source": label_source,
            }
        )
    return rows


def candidate_style(candidate_id: str) -> str:
    if "::natural::" in candidate_id:
        return "natural"
    if "::rule_grounded::" in candidate_id:
        return "rule_grounded"
    return candidate_id.split("::")[-1]


def edit_group_id(candidate_id: str) -> str:
    return candidate_id.split("::")[0]


def row_utility(row: dict[str, str]) -> float:
    return UTILITY[row["validator_overall_decision"]]


def group_ready_rows(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for index, row in enumerate(rows):
        row = dict(row)
        row["_index"] = str(index)
        row["_style"] = candidate_style(row["candidate_id"])
        row["_edit_group"] = edit_group_id(row["candidate_id"])
        groups[row["_edit_group"]].append(row)
    return dict(groups)


def sorted_group(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(rows, key=lambda row: int(row["_index"]))


def choose_first(rows: list[dict[str, str]]) -> dict[str, str] | None:
    return sorted_group(rows)[0]


def choose_style(style: str) -> Callable[[list[dict[str, str]]], dict[str, str] | None]:
    def choose(rows: list[dict[str, str]]) -> dict[str, str] | None:
        ordered = sorted_group(rows)
        return next((row for row in ordered if row["_style"] == style), ordered[0])

    return choose


def choose_highest_confidence(rows: list[dict[str, str]]) -> dict[str, str] | None:
    return max(sorted_group(rows), key=lambda row: (float(row.get("confidence") or 0.0), -int(row["_index"])))


def choose_longest_rationale(rows: list[dict[str, str]]) -> dict[str, str] | None:
    return max(sorted_group(rows), key=lambda row: len((row.get("rationale") or "").split()))


def choose_shortest_rationale(rows: list[dict[str, str]]) -> dict[str, str] | None:
    return min(sorted_group(rows), key=lambda row: len((row.get("rationale") or "").split()))


def choose_pseudo_selective(rows: list[dict[str, str]]) -> dict[str, str] | None:
    ordered = sorted_group(rows)
    return next((row for row in ordered if row["validator_overall_decision"] == "accept"), None)


def summarize_selected(
    name: str,
    groups: dict[str, list[dict[str, str]]],
    chooser: Callable[[list[dict[str, str]]], dict[str, str] | None],
    label_source: str,
) -> dict[str, str]:
    selected = []
    abstained = 0
    for rows in groups.values():
        choice = chooser(rows)
        if choice is None:
            abstained += 1
        else:
            selected.append(choice)
    counts = Counter(row["validator_overall_decision"] for row in selected)
    covered = len(selected)
    group_count = len(groups)
    return {
        "strategy": name,
        "edit_groups": str(group_count),
        "covered_groups": str(covered),
        "abstained_groups": str(abstained),
        "coverage": fmt_float(covered / group_count if group_count else 0.0),
        "accept_selected": fmt_float(counts["accept"], 1),
        "refine_selected": fmt_float(counts["refine"], 1),
        "reject_selected": fmt_float(counts["reject"], 1),
        "accept_rate": fmt_float(counts["accept"] / covered if covered else 0.0),
        "non_reject_rate": fmt_float((counts["accept"] + counts["refine"]) / covered if covered else 0.0),
        "mean_utility": fmt_float(sum(row_utility(row) for row in selected) / covered if covered else 0.0),
        "label_source": label_source,
    }


def summarize_random_expected(groups: dict[str, list[dict[str, str]]]) -> dict[str, str]:
    group_count = len(groups)
    accept = refine = reject = utility = 0.0
    for rows in groups.values():
        n = len(rows)
        counts = Counter(row["validator_overall_decision"] for row in rows)
        accept += counts["accept"] / n
        refine += counts["refine"] / n
        reject += counts["reject"] / n
        utility += sum(row_utility(row) for row in rows) / n
    return {
        "strategy": "Random candidate (expected)",
        "edit_groups": str(group_count),
        "covered_groups": str(group_count),
        "abstained_groups": "0",
        "coverage": "1.000",
        "accept_selected": fmt_float(accept, 1),
        "refine_selected": fmt_float(refine, 1),
        "reject_selected": fmt_float(reject, 1),
        "accept_rate": fmt_float(accept / group_count if group_count else 0.0),
        "non_reject_rate": fmt_float((accept + refine) / group_count if group_count else 0.0),
        "mean_utility": fmt_float(utility / group_count if group_count else 0.0),
        "label_source": "codex_ai_pseudo_validation_expected_value",
    }


def selection_baseline_rows(ready_validation_path: Path = DEFAULT_READY_VALIDATION) -> list[dict[str, str]]:
    rows = read_csv(ready_validation_path)
    groups = group_ready_rows(rows)
    strategy_specs: list[tuple[str, Callable[[list[dict[str, str]]], dict[str, str] | None], str]] = [
        ("First candidate", choose_first, "codex_ai_pseudo_validation"),
        ("Natural candidate", choose_style("natural"), "codex_ai_pseudo_validation"),
        ("Rule-grounded candidate", choose_style("rule_grounded"), "codex_ai_pseudo_validation"),
        ("Highest confidence", choose_highest_confidence, "codex_ai_pseudo_validation"),
        ("Longest rationale", choose_longest_rationale, "codex_ai_pseudo_validation"),
        ("Shortest rationale", choose_shortest_rationale, "codex_ai_pseudo_validation"),
        ("Pseudo-validator selective accept", choose_pseudo_selective, "codex_ai_pseudo_validation_upper_bound"),
    ]
    output = [summarize_random_expected(groups)]
    output.extend(summarize_selected(name, groups, chooser, source) for name, chooser, source in strategy_specs)
    return output


def write_csv(path: Path, rows: list[dict[str, str]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    if not rows:
        raise ValueError(f"No rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def latex_escape(value: str) -> str:
    return (
        value.replace("\\", "\\textbackslash{}")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("_", "\\_")
        .replace("#", "\\#")
    )


def write_teacher_tex(path: Path, rows: list[dict[str, str]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{lrrrrrrrr}",
        "\\toprule",
        "System & $N$ & Parse & Align & Missing rule & Edit-copy & Evidence & Accept & Reject \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(
            f"{latex_escape(row['system'])} & {row['n']} & {row['parse_json_rate']} & "
            f"{row['alignment_proxy_pass_rate']} & {row['missing_rule_text_rate']} & "
            f"{row['rule_edit_copy_rate']} & {row['contextual_evidence_rate']} & "
            f"{row['accepted']} & {row['rejected']} \\\\"
        )
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\caption{Open-teacher candidate quality under the same 80-edit RuleFaith pilot setting. Rates are automatic diagnostics; accepted/refine/rejected counts come from the frozen conservative prefilter and are not human labels.}",
            "\\label{tab:rulefaith-open-teacher-baselines}",
            "\\end{table*}",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_selection_tex(path: Path, rows: list[dict[str, str]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    keep = [
        row
        for row in rows
        if row["strategy"]
        in {
            "Random candidate (expected)",
            "First candidate",
            "Natural candidate",
            "Rule-grounded candidate",
            "Highest confidence",
            "Longest rationale",
            "Pseudo-validator selective accept",
        }
    ]
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Strategy & Cov. & Accept & Non-rej. & Utility \\\\",
        "\\midrule",
    ]
    for row in keep:
        lines.append(
            f"{latex_escape(row['strategy'])} & {row['coverage']} & {row['accept_rate']} & "
            f"{row['non_reject_rate']} & {row['mean_utility']} \\\\"
        )
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\caption{Selection baselines on 23 edit groups and 41 Qwen3 candidates. Accept/refine/reject labels are Codex/AI pseudo-validation for internal method triage; the selective row is an upper-bound diagnostic, not a deployable human result.}",
            "\\label{tab:rulefaith-selection-baselines}",
            "\\end{table}",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_markdown_report(
    path: Path,
    teacher_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    selection_rows: list[dict[str, str]],
    overwrite: bool,
) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)

    def table(rows: Iterable[dict[str, str]]) -> list[str]:
        rows = list(rows)
        header = list(rows[0].keys())
        lines = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * len(header)) + " |"]
        for row in rows:
            lines.append("| " + " | ".join(row.get(col, "") for col in header) + " |")
        return lines

    lines = [
        "# RuleFaith Loop O: Baseline Result Fill-In",
        "",
        "## Status",
        "",
        "- Loop ID: O",
        "- Current bottleneck: paper method section had Qwen3 pilot results but lacked a compact baseline comparison and candidate-selection ablation.",
        "- Hypothesis: under the same 80-edit teacher setting, Qwen3-8B is a stronger local teacher than FLAN-T5 and Qwen2.5, but simple candidate-selection rules remain weak under pseudo-validation.",
        "- Required evidence: same-setting teacher diagnostic files, frozen RuleFaith gate statistics, and the 41-row Codex/AI pseudo-validation package.",
        "- Success criterion: generated tables are fully derived from repository result files and do not claim human validation for pseudo labels.",
        "- Failure criterion: missing result provenance, unlabeled pseudo-validation boundaries, or table numbers not matching JSON/CSV sources.",
        "",
        "## Teacher Baselines",
        "",
        *table(teacher_rows),
        "",
        "## RuleFaith Gate Funnel",
        "",
        *table(gate_rows),
        "",
        "## Candidate-Selection Baselines",
        "",
        *table(selection_rows),
        "",
        "## Interpretation",
        "",
        "- Qwen2.5-0.5B ran in the same setting but produced only 1 accepted candidate out of 160 under the conservative prefilter; it is therefore a weak baseline/negative source, not a positive-teacher source.",
        "- Qwen3-8B produced a non-trivial direct accepted pool, but later pseudo-validation still rejected 11 of the 41 automatically ready candidates.",
        "- Rule-grounded candidate choice is the best simple non-oracle top-1 strategy in this ready pool by accept rate, but the selective pseudo-validator diagnostic shows that many edit groups still need abstention or further refinement.",
        "- These results can fill the method-pilot baseline section. They are not a replacement for real-human natural explanation evaluation.",
        "",
        "## Artifacts Produced",
        "",
        "- `results/rulefaith/rulefaith_teacher_baselines.csv`",
        "- `results/rulefaith/rulefaith_method_gate_funnel.csv`",
        "- `results/rulefaith/rulefaith_selection_baselines.csv`",
        "- `results/rulefaith/rulefaith_selection_baselines.json`",
        "- `results/paper_assets/rulefaith_open_teacher_baselines.tex`",
        "- `results/paper_assets/rulefaith_selection_baselines.tex`",
        "",
        "## Provenance",
        "",
        f"- Generated at: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Git commit at generation time: `{current_git_commit()}`",
        "- Label boundary: `codex_ai_pseudo_validation` is AI pseudo-validation for internal triage only.",
        "",
        "## Next Highest-Priority Loop",
        "",
        "Prepare the next natural-explanation validation package or add a non-oracle deployable scorer for the 41-row ready pool; do not treat the pseudo-selective diagnostic as a final method result.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate RuleFaith same-setting baselines and selection diagnostics.")
    parser.add_argument("--ready-validation", type=Path, default=DEFAULT_READY_VALIDATION)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--asset-dir", type=Path, default=DEFAULT_ASSET_DIR)
    parser.add_argument("--report", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ready_path = resolve(args.ready_validation)
    output_dir = resolve(args.output_dir)
    asset_dir = resolve(args.asset_dir)
    report = resolve(args.report)

    teacher_rows = teacher_baseline_rows()
    gate_rows = method_gate_rows()
    selection_rows = selection_baseline_rows(ready_path)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": current_git_commit(),
        "ready_validation_path": str(ready_path),
        "label_boundary": "Codex/AI pseudo-validation labels are internal triage labels, not human gold.",
        "teacher_baselines": teacher_rows,
        "method_gate_funnel": gate_rows,
        "selection_baselines": selection_rows,
    }

    write_csv(output_dir / "rulefaith_teacher_baselines.csv", teacher_rows, args.overwrite)
    write_csv(output_dir / "rulefaith_method_gate_funnel.csv", gate_rows, args.overwrite)
    write_csv(output_dir / "rulefaith_selection_baselines.csv", selection_rows, args.overwrite)
    write_json(output_dir / "rulefaith_selection_baselines.json", payload, args.overwrite)
    write_teacher_tex(asset_dir / "rulefaith_open_teacher_baselines.tex", teacher_rows, args.overwrite)
    write_selection_tex(asset_dir / "rulefaith_selection_baselines.tex", selection_rows, args.overwrite)
    write_markdown_report(report, teacher_rows, gate_rows, selection_rows, args.overwrite)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
