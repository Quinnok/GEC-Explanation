from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Tuple

from run_faithfulness_methods import confusion
from analyze_counterfactuals import multiclass_metrics


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BENCHMARK_DIR = ROOT / "data" / "faithfulness_benchmark"
DEFAULT_ROUND08 = ROOT / "results" / "round08"
DEFAULT_ROUND09 = ROOT / "results" / "round09"
DEFAULT_DOCS = ROOT / "docs"
DEFAULT_TABLES = ROOT / "results" / "tables"


METHODS_OF_INTEREST = [
    "surface_keyword",
    "structured_explicit_extraction",
    "reverse_reconstruction",
    "target_masked_reconstruction",
    "leakage_adjusted_reconstruction",
    "tfidf_embedding_similarity",
    "nli_lexical_proxy",
    "rule_evidence_verifier",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def fmt(value: float) -> str:
    return f"{value:.3f}"


def tex_escape(value: str) -> str:
    return value.replace("_", "\\_")


def write_latex_tables(args: argparse.Namespace, method_bootstrap: Dict[str, Any], cf_bootstrap: Dict[str, Any]) -> None:
    l1_lines = [
        "\\noindent\\resizebox{0.95\\linewidth}{!}{%",
        "\\begin{tabular}{lrrr}",
        "\\toprule",
        "Method & Macro-F1 & CI low & CI high \\\\",
        "\\midrule",
    ]
    for method in METHODS_OF_INTEREST:
        item = method_bootstrap[method]
        l1_lines.append(f"{tex_escape(method)} & {fmt(item['macro_f1'])} & {fmt(item['ci_low'])} & {fmt(item['ci_high'])} \\\\")
    l1_lines.extend(["\\bottomrule", "\\end{tabular}%", "}"])
    write_text(args.tables_dir / "round09_l1_bootstrap.tex", "\n".join(l1_lines))

    cf_lines = [
        "\\noindent\\resizebox{0.95\\linewidth}{!}{%",
        "\\begin{tabular}{lrrr}",
        "\\toprule",
        "Simulator & Macro-F1 & CI low & CI high \\\\",
        "\\midrule",
    ]
    for method, item in sorted(cf_bootstrap.items()):
        cf_lines.append(f"{tex_escape(method)} & {fmt(item['macro_f1'])} & {fmt(item['ci_low'])} & {fmt(item['ci_high'])} \\\\")
    cf_lines.extend(["\\bottomrule", "\\end{tabular}%", "}"])
    write_text(args.tables_dir / "round09_counterfactual_bootstrap.tex", "\n".join(cf_lines))


def percentile(values: List[float], p: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    idx = min(len(values) - 1, max(0, round((len(values) - 1) * p)))
    return values[idx]


def grouped_bootstrap_binary(rows: List[Dict[str, Any]], group_key: str, seed: int, n_boot: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row[group_key])].append(row)
    group_ids = sorted(groups)
    scores = []
    for _ in range(n_boot):
        sample_rows = []
        for group_id in (rng.choice(group_ids) for _ in group_ids):
            sample_rows.extend(groups[group_id])
        scores.append(confusion([(row["prediction"], row["gold_label"]) for row in sample_rows])["macro_f1"])
    original = confusion([(row["prediction"], row["gold_label"]) for row in rows])["macro_f1"]
    return {
        "n_groups": len(group_ids),
        "n_rows": len(rows),
        "macro_f1": original,
        "ci_low": percentile(scores, 0.025),
        "ci_high": percentile(scores, 0.975),
        "bootstrap_samples": n_boot,
    }


def grouped_bootstrap_multiclass(rows: List[Dict[str, Any]], group_key: str, seed: int, n_boot: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row[group_key])].append(row)
    group_ids = sorted(groups)
    scores = []
    for _ in range(n_boot):
        sample_rows = []
        for group_id in (rng.choice(group_ids) for _ in group_ids):
            sample_rows.extend(groups[group_id])
        scores.append(multiclass_metrics([(row["prediction"], row["actual_behavior_label"]) for row in sample_rows])["macro_f1"])
    original = multiclass_metrics([(row["prediction"], row["actual_behavior_label"]) for row in rows])["macro_f1"]
    return {
        "n_groups": len(group_ids),
        "n_rows": len(rows),
        "macro_f1": original,
        "ci_low": percentile(scores, 0.025),
        "ci_high": percentile(scores, 0.975),
        "bootstrap_samples": n_boot,
    }


def paired_bootstrap_delta(rows: List[Dict[str, Any]], method_a: str, method_b: str, group_key: str, seed: int, n_boot: int) -> Dict[str, Any]:
    by_instance: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_instance[row["instance_id"]][row["method"]] = row
    paired = [
        (items[method_a], items[method_b])
        for items in by_instance.values()
        if method_a in items and method_b in items
    ]
    groups: Dict[str, List[Tuple[Dict[str, Any], Dict[str, Any]]]] = defaultdict(list)
    for left, right in paired:
        groups[str(left[group_key])].append((left, right))
    group_ids = sorted(groups)
    rng = random.Random(seed)

    def score(pairs: List[Tuple[Dict[str, Any], Dict[str, Any]]]) -> float:
        left_score = confusion([(left["prediction"], left["gold_label"]) for left, _ in pairs])["macro_f1"]
        right_score = confusion([(right["prediction"], right["gold_label"]) for _, right in pairs])["macro_f1"]
        return left_score - right_score

    deltas = []
    for _ in range(n_boot):
        sample_pairs = []
        for group_id in (rng.choice(group_ids) for _ in group_ids):
            sample_pairs.extend(groups[group_id])
        deltas.append(score(sample_pairs))
    observed = score(paired)
    p_two_sided = 2 * min(
        sum(1 for value in deltas if value <= 0) / len(deltas),
        sum(1 for value in deltas if value >= 0) / len(deltas),
    )
    return {
        "method_a": method_a,
        "method_b": method_b,
        "delta_macro_f1": observed,
        "ci_low": percentile(deltas, 0.025),
        "ci_high": percentile(deltas, 0.975),
        "p_two_sided_bootstrap": min(1.0, p_two_sided),
        "n_pairs": len(paired),
        "n_groups": len(group_ids),
    }


def holm_adjust(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    ordered = sorted(items, key=lambda item: item["p_two_sided_bootstrap"])
    m = len(ordered)
    adjusted = []
    running_max = 0.0
    for rank, item in enumerate(ordered, start=1):
        value = min(1.0, item["p_two_sided_bootstrap"] * (m - rank + 1))
        running_max = max(running_max, value)
        adjusted.append({**item, "p_holm": running_max})
    return sorted(adjusted, key=lambda item: item["method_b"])


def join_l1_rows(detailed: List[Dict[str, Any]], edit_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    edits = {row["edit_id"]: row for row in edit_rows}
    edit_counts = Counter((row["sample_id"], row["model_key"]) for row in edit_rows)
    enriched = []
    for row in detailed:
        edit = edits[row["edit_id"]]
        pred_edit = edit["predicted_edit"]
        source_len = len(edit["source"].split())
        enriched.append(
            {
                **row,
                "sample_id": edit["sample_id"],
                "operation": pred_edit["operation"],
                "sentence_length_bucket": "short" if source_len < 15 else "medium" if source_len < 35 else "long",
                "sentence_length": source_len,
                "single_vs_multi_edit": "multi_edit" if edit_counts[(edit["sample_id"], edit["model_key"])] > 1 else "single_edit",
            }
        )
    return enriched


def stratified_binary(enriched: List[Dict[str, Any]], method: str, keys: List[str]) -> Dict[str, Dict[str, Any]]:
    rows = [row for row in enriched if row["method"] == method]
    out = {}
    for key in keys:
        by_value: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for row in rows:
            value = row.get(key)
            if value is None:
                value = "NONE"
            by_value[str(value)].append(row)
        out[key] = {
            value: confusion([(item["prediction"], item["gold_label"]) for item in items])
            for value, items in sorted(by_value.items())
            if len(items) >= 10
        }
    return out


def stratified_counterfactual(rows: List[Dict[str, Any]], method: str, keys: List[str]) -> Dict[str, Dict[str, Any]]:
    method_rows = [row for row in rows if row["method"] == method]
    out = {}
    for key in keys:
        by_value: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for row in method_rows:
            by_value[str(row.get(key, "NONE"))].append(row)
        out[key] = {
            value: multiclass_metrics([(item["prediction"], item["actual_behavior_label"]) for item in items])
            for value, items in sorted(by_value.items())
            if len(items) >= 5
        }
    return out


def sample_rows(rows: List[Dict[str, Any]], predicate, limit: int) -> List[Dict[str, Any]]:
    return [row for row in rows if predicate(row)][:limit]


def render_error_markdown(title: str, rows: List[Dict[str, Any]], explanations: Dict[str, Dict[str, Any]], edits: Dict[str, Dict[str, Any]]) -> str:
    lines = [f"# {title}", ""]
    for idx, row in enumerate(rows, start=1):
        exp = explanations.get(row.get("instance_id", ""), {})
        edit = edits.get(row.get("edit_id", ""), {})
        lines.extend(
            [
                f"## {idx}. {row.get('method', 'case')}::{row.get('instance_id', row.get('counterfactual_id', 'unknown'))}",
                "",
                f"- Dataset/model: `{row.get('dataset', edit.get('dataset', 'UNKNOWN'))}` / `{row.get('model_key', edit.get('model_key', 'UNKNOWN'))}`",
                f"- Behavior/type: `{row.get('behavior', edit.get('behavior', row.get('actual_behavior_label', 'UNKNOWN')))}` / `{row.get('error_type', edit.get('error_type', row.get('original_error_type', 'UNKNOWN')))}`",
                f"- Explanation type: `{row.get('explanation_type', exp.get('explanation_type', 'NA'))}`",
                f"- Gold/prediction: `{row.get('gold_label', row.get('actual_behavior_label', 'NA'))}` / `{row.get('prediction', 'NA')}`",
                f"- Source: `{edit.get('source', row.get('source', row.get('original_source', '')) )}`",
                f"- Explanation: `{exp.get('explanation', row.get('explanation', ''))}`",
                "",
            ]
        )
    return "\n".join(lines)


def build_error_analysis(args: argparse.Namespace, enriched_l1: List[Dict[str, Any]], cf_sim_rows: List[Dict[str, Any]], cf_labels: List[Dict[str, Any]], edit_rows: List[Dict[str, Any]], explanation_rows: List[Dict[str, Any]]) -> None:
    explanations = {row["instance_id"]: row for row in explanation_rows}
    edits = {row["edit_id"]: row for row in edit_rows}
    error_dir = args.round09_dir / "error_analysis"
    method = "rule_evidence_verifier"
    success = sample_rows(enriched_l1, lambda row: row["method"] == method and row["prediction"] == row["gold_label"], 50)
    failure = sample_rows(enriched_l1, lambda row: row["method"] == method and row["prediction"] != row["gold_label"], 50)
    simulator_confusion = sample_rows(cf_sim_rows, lambda row: row["method"] == "explanation_leakage_simulator" and not row["correct"], 20)
    instability = sample_rows(
        cf_labels,
        lambda row: row["actual_behavior_label"] in {"competing_edit", "change_span", "change_target"}
        or (row["variant_family"] == "error_irrelevant" and row["actual_behavior_label"] != "preserve"),
        20,
    )
    invalid_cf = sample_rows(cf_labels, lambda row: row["variant_family"] == "rule_relevant" and row["actual_behavior_label"] == "competing_edit", 20)
    multi_reference = sample_rows(edit_rows, lambda row: row.get("dataset") == "JFLEG" and row["behavior"] in {"wrong_correction", "overcorrection"}, 20)
    alignment_issues = []
    for path in [
        ROOT / "results" / "model_edits" / "alignment_failures.jsonl",
        ROOT / "results" / "model_edits_jfleg" / "alignment_failures.jsonl",
        ROOT / "results" / "model_edits_coedit_expect" / "alignment_failures.jsonl",
    ]:
        if path.exists():
            alignment_issues.extend(read_jsonl(path))
    alignment_issues = alignment_issues[:20]

    write_jsonl(error_dir / "success_cases_50.jsonl", success)
    write_jsonl(error_dir / "failure_cases_50.jsonl", failure)
    write_jsonl(error_dir / "model_instability_cases_20.jsonl", instability)
    write_jsonl(error_dir / "counterfactual_invalid_or_competing_20.jsonl", invalid_cf)
    write_jsonl(error_dir / "multi_reference_equivalence_candidates_20.jsonl", multi_reference)
    write_jsonl(error_dir / "errant_alignment_issues_20.jsonl", alignment_issues)
    write_jsonl(error_dir / "simulator_confusion_cases_20.jsonl", simulator_confusion)
    write_text(error_dir / "success_cases_50.md", render_error_markdown("Success Cases", success, explanations, edits))
    write_text(error_dir / "failure_cases_50.md", render_error_markdown("Failure Cases", failure, explanations, edits))
    write_text(error_dir / "simulator_confusion_cases_20.md", render_error_markdown("Simulator Confusion Cases", simulator_confusion, explanations, edits))


def build(args: argparse.Namespace) -> None:
    l1_details = read_jsonl(args.round08_dir / "l1_detailed_predictions.jsonl")
    edit_rows = read_jsonl(args.benchmark_dir / "edit_records.jsonl")
    explanation_rows = read_jsonl(args.benchmark_dir / "explanation_instances.jsonl")
    cf_labels = read_jsonl(args.round09_dir / "counterfactual_labels.jsonl")
    cf_sim = read_jsonl(args.round09_dir / "counterfactual_simulator_predictions.jsonl")
    enriched_l1 = join_l1_rows(l1_details, edit_rows)

    method_bootstrap = {
        method: grouped_bootstrap_binary(
            [row for row in enriched_l1 if row["method"] == method],
            group_key="sample_id",
            seed=args.seed,
            n_boot=args.bootstrap_samples,
        )
        for method in METHODS_OF_INTEREST
    }
    paired = holm_adjust(
        [
            paired_bootstrap_delta(enriched_l1, "rule_evidence_verifier", method, "sample_id", args.seed + idx, args.bootstrap_samples)
            for idx, method in enumerate(METHODS_OF_INTEREST)
            if method != "rule_evidence_verifier"
        ]
    )
    cf_bootstrap = {
        method: grouped_bootstrap_multiclass(
            [row for row in cf_sim if row["method"] == method],
            group_key="origin_edit_id",
            seed=args.seed,
            n_boot=args.bootstrap_samples,
        )
        for method in sorted({row["method"] for row in cf_sim})
    }
    grouped = {
        "l1_rule_evidence_verifier": stratified_binary(
            enriched_l1,
            "rule_evidence_verifier",
            [
                "dataset",
                "model_key",
                "behavior",
                "error_type",
                "operation",
                "sentence_length_bucket",
                "single_vs_multi_edit",
                "explanation_type",
                "negative_type",
            ],
        ),
        "l2_explanation_leakage_simulator": stratified_counterfactual(
            cf_sim,
            "explanation_leakage_simulator",
            ["dataset", "model_key", "variant_family", "actual_behavior_label", "explanation_type", "explanation_label"],
        ),
    }
    build_error_analysis(args, enriched_l1, cf_sim, cf_labels, edit_rows, explanation_rows)

    summary = {
        "created_at": utc_now(),
        "bootstrap_samples": args.bootstrap_samples,
        "seed": args.seed,
        "method_bootstrap_macro_f1": method_bootstrap,
        "paired_bootstrap_rule_evidence_vs_others": paired,
        "counterfactual_simulator_bootstrap_macro_f1": cf_bootstrap,
        "grouped_analysis": grouped,
        "claim_answers": {
            "closest_to_human_faithfulness": "unanswered_no_human_labels",
            "reverse_reconstruction_leakage": "supported_by_drop_under_target_masked_and_leakage_adjusted_controls",
            "counterfactual_nontrivial_gain": "not_supported_yet; simulator baselines are weak in Round 09 pilot",
            "rule_relevant_more_discriminative": "partially_supported_by_higher_non_preserve_rate_but_many_competing_edits",
            "model_family_differences": "available_in_grouped_analysis_but small CoEdIT sample limits claims",
            "behavior_differences": "available_in_grouped_analysis_but automatic labels only",
        },
    }
    write_json(args.round09_dir / "statistical_analysis.json", summary)
    write_jsonl(args.round09_dir / "l1_detailed_predictions_enriched.jsonl", enriched_l1)
    write_latex_tables(args, method_bootstrap, cf_bootstrap)

    cf_label_counts = dict(Counter(row["actual_behavior_label"] for row in cf_labels))
    unique_cf_sim_instances = len({row["sim_instance_id"] for row in cf_sim})
    best_l1 = max(method_bootstrap.items(), key=lambda item: item[1]["macro_f1"])
    best_cf = max(cf_bootstrap.items(), key=lambda item: item[1]["macro_f1"])

    doc = [
        "# Round 09: Scaled Pilot Statistics and Error Analysis",
        "",
        "## Completed",
        "",
        f"- Grouped bootstrap with {args.bootstrap_samples} resamples by source sentence/edit group.",
        "- Paired bootstrap deltas with Holm correction for L1 methods.",
        "- Grouped analysis by dataset, model, behavior, error type, operation, sentence length, edit multiplicity, explanation type, and negative type.",
        "- Error-analysis packets for successes, failures, instability, invalid/competing counterfactuals, multi-reference candidates, ERRANT alignment issues, and simulator confusions.",
        "- LaTeX tables generated under `results/tables/`.",
        "",
        "## Scaled Counterfactual Run",
        "",
        f"- Counterfactual labels: `{json.dumps(cf_label_counts, sort_keys=True)}`",
        f"- Counterfactual simulator instances: {unique_cf_sim_instances} unique explanation-variant pairs; {len(cf_sim)} method prediction rows.",
        f"- Best automatic L1 method by grouped bootstrap macro-F1: `{best_l1[0]}` = {best_l1[1]['macro_f1']:.3f} [{best_l1[1]['ci_low']:.3f}, {best_l1[1]['ci_high']:.3f}]",
        f"- Best automatic L2 simulator by grouped bootstrap macro-F1: `{best_cf[0]}` = {best_cf[1]['macro_f1']:.3f} [{best_cf[1]['ci_low']:.3f}, {best_cf[1]['ci_high']:.3f}]",
        "",
        "## Claim Answers",
        "",
        "- Closest metric to human faithfulness: unanswered because no human labels exist yet.",
        "- Reverse reconstruction leakage: supported in the automatic benchmark by large drops under target masking and leakage adjustment.",
        "- Counterfactual nontrivial gain: not supported yet; current explanation-conditioned simulator baselines remain weak.",
        "- Rule-relevant counterfactuals: more likely to disrupt the original edit, but many become competing edits rather than clean cancellations.",
        "- Model-family and behavior differences: analyzable in the produced grouped files, but CoEdIT is still small and labels are automatic.",
        "",
        "## Key Files",
        "",
        "- `results/round09/statistical_analysis.json`",
        "- `results/round09/counterfactual_simulator_metrics.json`",
        "- `results/round09/error_analysis/`",
        "- `results/tables/round09_l1_bootstrap.tex`",
        "- `results/tables/round09_counterfactual_bootstrap.tex`",
    ]
    write_text(args.docs_dir / "round_09.md", "\n".join(doc))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Round 09 statistical and error analysis.")
    parser.add_argument("--benchmark-dir", type=Path, default=DEFAULT_BENCHMARK_DIR)
    parser.add_argument("--round08-dir", type=Path, default=DEFAULT_ROUND08)
    parser.add_argument("--round09-dir", type=Path, default=DEFAULT_ROUND09)
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS)
    parser.add_argument("--tables-dir", type=Path, default=DEFAULT_TABLES)
    parser.add_argument("--bootstrap-samples", type=int, default=200)
    parser.add_argument("--seed", type=int, default=9009)
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
