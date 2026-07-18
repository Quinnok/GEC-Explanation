from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "paper_assets"


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def esc(value: Any) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def pct(value: float) -> str:
    return f"{100 * value:.1f}"


def top_items(counts: Dict[str, int], n: int = 6) -> str:
    return ", ".join(f"{esc(k)} {v}" for k, v in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:n])


def table_env(caption: str, label: str, columns: str, header: str, rows: Iterable[str], *, wide: bool = False) -> str:
    env = "table*" if wide else "table"
    width = r"\textwidth" if wide else r"\linewidth"
    return "\n".join(
        [
            f"\\begin{{{env}}}[t]",
            "\\centering",
            "\\footnotesize",
            f"\\resizebox{{{width}}}{{!}}{{%",
            f"\\begin{{tabular}}{{{columns}}}",
            "\\toprule",
            header,
            "\\midrule",
            *rows,
            "\\bottomrule",
            "\\end{tabular}%",
            "}",
            f"\\caption{{{caption}}}",
            f"\\label{{{label}}}",
            f"\\end{{{env}}}",
        ]
    )


def figure_env(caption: str, label: str, body: List[str], *, wide: bool = False) -> str:
    env = "figure*" if wide else "figure"
    return "\n".join(
        [
            f"\\begin{{{env}}}[t]",
            "\\centering",
            "\\footnotesize",
            *body,
            f"\\caption{{{caption}}}",
            f"\\label{{{label}}}",
            f"\\end{{{env}}}",
        ]
    )


def main_result_rows(stat: Dict[str, Any]) -> List[str]:
    l1 = stat["method_bootstrap_macro_f1"]
    l2 = stat["counterfactual_simulator_bootstrap_macro_f1"]
    wanted_l1 = [
        "surface_keyword",
        "reverse_reconstruction",
        "target_masked_reconstruction",
        "leakage_adjusted_reconstruction",
        "tfidf_embedding_similarity",
        "nli_lexical_proxy",
        "rule_evidence_verifier",
    ]
    rows = []
    for name in wanted_l1:
        row = l1[name]
        rows.append(
            f"L1/L3 & {esc(name)} & {row['macro_f1']:.3f} & [{row['ci_low']:.3f}, {row['ci_high']:.3f}] \\\\"
        )
    for name in ["random", "variant_family_prior", "explanation_leakage_simulator", "trained_explanation_type_prior"]:
        row = l2[name]
        rows.append(
            f"L2 & {esc(name)} & {row['macro_f1']:.3f} & [{row['ci_low']:.3f}, {row['ci_high']:.3f}] \\\\"
        )
    return rows


def leakage_rows(stat: Dict[str, Any], round11: Dict[str, Any]) -> List[str]:
    l1 = stat["method_bootstrap_macro_f1"]
    reward = read_json(ROOT / "results" / "round11" / "reward_hacking_report.json")
    return [
        f"Reverse reconstruction & {l1['reverse_reconstruction']['macro_f1']:.3f} & target visible & -- \\\\",
        f"Target-masked reconstruction & {l1['target_masked_reconstruction']['macro_f1']:.3f} & target masked & -- \\\\",
        f"Leakage-adjusted reconstruction & {l1['leakage_adjusted_reconstruction']['macro_f1']:.3f} & direct leakage penalized & -- \\\\",
        f"Round 11 combined reranker & {round11['method_metrics']['combined_reranker']['pairwise_ranking_accuracy']:.3f} & automatic ranking & {reward['combined_reranker']['edit_copy_top1_rate']:.3f} \\\\",
        f"Round 11 local LLM judge & {round11['method_metrics']['local_llm_judge']['pairwise_ranking_accuracy']:.3f} & local FLAN-T5 & {reward['local_llm_judge']['edit_copy_top1_rate']:.3f} \\\\",
    ]


def behavior_rows(edit_rows: List[Dict[str, Any]]) -> List[str]:
    counts: Dict[str, Counter] = defaultdict(Counter)
    for row in edit_rows:
        counts[row["model_key"]][row["behavior"]] += 1
    rows = []
    for model in sorted(counts):
        total = sum(counts[model].values())
        rows.append(
            f"{esc(model)} & {total} & {counts[model]['correct_correction']} & {counts[model]['wrong_correction']} & {counts[model]['overcorrection']} \\\\"
        )
    return rows


def find_case_study(counterfactual_rows: List[Dict[str, Any]], explanation_rows: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    by_origin: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in counterfactual_rows:
        by_origin[row["origin_edit_id"]].append(row)
    explanations = {
        (row["edit_id"], row["explanation_type"]): row["explanation"]
        for row in explanation_rows
        if row["explanation_type"] in {"rule_grounded_automatic", "gee_style_automatic", "masked_target_template"}
    }
    for edit_id, rows in by_origin.items():
        preserve = next((row for row in rows if row["actual_behavior_label"] == "preserve"), None)
        cancel = next((row for row in rows if row["actual_behavior_label"] == "cancel"), None)
        explanation = explanations.get((edit_id, "rule_grounded_automatic")) or explanations.get((edit_id, "gee_style_automatic"))
        if preserve and cancel and explanation:
            return preserve, cancel, explanation
    first = counterfactual_rows[0]
    return first, first, explanations.get((first["origin_edit_id"], "rule_grounded_automatic"), "No explanation candidate found.")


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    stats = read_json(ROOT / "data" / "faithfulness_benchmark" / "benchmark_stats.json")
    stat09 = read_json(ROOT / "results" / "round09" / "statistical_analysis.json")
    ann = read_json(ROOT / "results" / "round10" / "annotation_package_stats.json")
    human = read_json(ROOT / "results" / "round10" / "human_annotation_status.json")
    rerank = read_json(ROOT / "results" / "round11" / "reranking_metrics.json")
    edit_rows = read_jsonl(ROOT / "data" / "faithfulness_benchmark" / "edit_records.jsonl")
    cf_rows = read_jsonl(ROOT / "results" / "round09" / "counterfactual_labels.jsonl")
    explanation_rows = read_jsonl(ROOT / "data" / "faithfulness_benchmark" / "explanation_instances.jsonl")

    write_text(
        OUT / "framework_figure.tex",
        figure_env(
            "Three-layer evaluation framework instantiated with real pilot counts.",
            "fig:framework",
            [
                r"\fbox{\begin{minipage}{0.96\linewidth}\raggedright",
                f"\\textbf{{Input:}} {stats['edit_count']} model-produced edits from {len(stats['dataset_counts'])} datasets and {len(stats['model_family_counts'])} model families.\\\\[2pt]",
                r"\textbf{L1 Edit correspondence:} reconstruct span, operation, target, and ERRANT type from explanations.\\",
                r"\textbf{L2 Counterfactual edit simulatability:} rerun the same GEC model on controlled variants and predict preserve/change/cancel/competing behavior.\\",
                r"\textbf{L3 Rule/evidence grounding:} verify rule claims and evidence spans against the produced edit.",
                r"\end{minipage}}",
            ],
        ),
    )
    write_text(
        OUT / "data_pipeline_figure.tex",
        figure_env(
            "Data construction pipeline with counts generated from benchmark metadata.",
            "fig:data-pipeline",
            [
                r"\fbox{\begin{minipage}{0.96\linewidth}\raggedright",
                f"Public GEC sources ({top_items(stats['dataset_counts'])}) $\\rightarrow$ model predictions ({top_items(stats['model_counts'])}) $\\rightarrow$ ERRANT model edits ({stats['edit_count']}) $\\rightarrow$ explanation/control instances ({stats['explanation_instance_count']}) $\\rightarrow$ counterfactual reruns ({len(cf_rows)} variants).",
                r"\end{minipage}}",
            ],
        ),
    )
    preserve, cancel, explanation = find_case_study(cf_rows, explanation_rows)
    edit = preserve["original_predicted_edit"]
    write_text(
        OUT / "counterfactual_pair_figure.tex",
        figure_env(
            "Counterfactual pair illustration sampled from actual model reruns.",
            "fig:counterfactual-pair",
            [
                r"\fbox{\begin{minipage}{0.96\linewidth}\raggedright\scriptsize",
                f"\\textbf{{Original source:}} {esc(preserve['original_source'])}\\\\",
                f"\\textbf{{Original edit:}} {esc(edit['operation'])} ``{esc(edit['source_text'])}'' $\\rightarrow$ ``{esc(edit['target_text'])}'' ({esc(preserve['original_error_type'])}).\\\\",
                f"\\textbf{{Explanation candidate:}} {esc(explanation[:220])}\\\\",
                f"\\textbf{{Irrelevant variant:}} {esc(preserve['source'])} $\\Rightarrow$ {esc(preserve['actual_behavior_label'])}.\\\\",
                f"\\textbf{{Rule-relevant variant:}} {esc(cancel['source'])} $\\Rightarrow$ {esc(cancel['actual_behavior_label'])}.",
                r"\end{minipage}}",
            ],
            wide=True,
        ),
    )
    write_text(
        OUT / "method_comparison_figure.tex",
        figure_env(
            "Method comparison summary generated from Round 09 and Round 11 metrics.",
            "fig:method-comparison",
            [
                r"\resizebox{\linewidth}{!}{%",
                r"\begin{tabular}{llr}",
                r"\toprule",
                r"Layer/Application & Best current automatic method & Score \\",
                r"\midrule",
                f"L1 edit correspondence & rule/evidence verifier & {stat09['method_bootstrap_macro_f1']['rule_evidence_verifier']['macro_f1']:.3f} Macro-F1 \\\\",
                f"L2 counterfactual simulator & trained explanation-type prior & {stat09['counterfactual_simulator_bootstrap_macro_f1']['trained_explanation_type_prior']['macro_f1']:.3f} Macro-F1 \\\\",
                f"Reranking application & combined reranker & {rerank['method_metrics']['combined_reranker']['pairwise_ranking_accuracy']:.3f} pairwise \\\\",
                r"\bottomrule",
                r"\end{tabular}%",
                r"}",
            ],
        ),
    )
    write_text(
        OUT / "main_results_table.tex",
        table_env(
            "Main automatic pilot results with grouped bootstrap confidence intervals.",
            "tab:main-results",
            "llrr",
            r"Layer & Method & Macro-F1 / Pairwise & 95\% CI \\",
            main_result_rows(stat09),
            wide=True,
        ),
    )
    write_text(
        OUT / "leakage_ablation_table.tex",
        table_env(
            "Leakage and reward-hacking controls.",
            "tab:leakage",
            "llrr",
            r"Condition & Score & Control & Edit-copy top-1 \\",
            leakage_rows(stat09, rerank),
        ),
    )
    write_text(
        OUT / "model_behavior_breakdown_table.tex",
        table_env(
            "Model-produced edit behavior distribution in the benchmark.",
            "tab:model-behavior",
            "lrrrr",
            r"Model & Edits & Correct & Wrong & Over \\",
            behavior_rows(edit_rows),
        ),
    )
    write_text(
        OUT / "human_correlation_table.tex",
        table_env(
            "Human-evaluation status; no human correlation is reported without labels.",
            "tab:human-status",
            "lrrl",
            r"Item set & Items & Human labels & Status \\",
            [
                f"Faithfulness & {ann['faithfulness_item_count']} & {human['completed_label_count']} & {esc(human['status'])} \\\\",
                f"Counterfactual & {ann['counterfactual_item_count']} & {human['completed_label_count']} & {esc(human['status'])} \\\\",
                f"Agreement & {human['paired_overlap_count']} overlap & -- & Cohen's $\\kappa$ unavailable \\\\",
            ],
        ),
    )
    error_paths = {
        "success": ROOT / "results" / "round09" / "error_analysis" / "success_cases_50.jsonl",
        "failure": ROOT / "results" / "round09" / "error_analysis" / "failure_cases_50.jsonl",
        "model instability": ROOT / "results" / "round09" / "error_analysis" / "model_instability_cases_20.jsonl",
        "invalid/competing CF": ROOT / "results" / "round09" / "error_analysis" / "counterfactual_invalid_or_competing_20.jsonl",
        "multi-reference": ROOT / "results" / "round09" / "error_analysis" / "multi_reference_equivalence_candidates_20.jsonl",
        "ERRANT alignment": ROOT / "results" / "round09" / "error_analysis" / "errant_alignment_issues_20.jsonl",
        "simulator confusion": ROOT / "results" / "round09" / "error_analysis" / "simulator_confusion_cases_20.jsonl",
    }
    write_text(
        OUT / "error_analysis_table.tex",
        table_env(
            "Error-analysis packet inventory generated from saved JSONL files.",
            "tab:error-analysis",
            "lr",
            r"Packet & Cases \\",
            [f"{esc(name)} & {len(read_jsonl(path))} \\\\" for name, path in error_paths.items()],
        ),
    )
    write_text(
        OUT / "benchmark_stats_table.tex",
        table_env(
            "Benchmark statistics generated from the data card JSON.",
            "tab:benchmark-stats",
            "lr",
            r"Statistic & Value \\",
            [
                f"Model-produced edits & {stats['edit_count']} \\\\",
                f"Explanation/control instances & {stats['explanation_instance_count']} \\\\",
                f"Missed-edit diagnoses & {stats['missing_edit_count']} \\\\",
                f"ERRANT error types & {stats['error_type_count']} \\\\",
                f"Datasets & {top_items(stats['dataset_counts'])} \\\\",
                f"Operations & {top_items(stats['operation_counts'])} \\\\",
                f"Human gold labels & {stats['human_gold_count']} \\\\",
            ],
        ),
    )
    write_text(
        OUT / "case_study_figure.tex",
        figure_env(
            "Case study for a real model edit and two counterfactual outcomes.",
            "fig:case-study",
            [
                r"\fbox{\begin{minipage}{0.96\linewidth}\raggedright\scriptsize",
                f"Model: {esc(preserve['model_key'])}; dataset: {esc(preserve['origin_dataset'])}; behavior: {esc(preserve['original_behavior'])}.\\\\",
                f"Source: {esc(preserve['original_source'])}\\\\",
                f"Prediction: {esc(preserve['original_prediction'])}\\\\",
                f"Edit: {esc(edit['source_text'])} $\\rightarrow$ {esc(edit['target_text'])}; ERRANT type: {esc(preserve['original_error_type'])}.\\\\",
                f"Counterfactual labels from reruns: irrelevant={esc(preserve['actual_behavior_label'])}; rule-relevant={esc(cancel['actual_behavior_label'])}.",
                r"\end{minipage}}",
            ],
            wide=True,
        ),
    )
    manifest = {
        "generated_files": sorted(path.name for path in OUT.glob("*.tex")),
        "benchmark_edit_count": stats["edit_count"],
        "explanation_instance_count": stats["explanation_instance_count"],
        "counterfactual_variant_count": len(cf_rows),
        "human_gold_count": stats["human_gold_count"],
        "source_files": [
            "data/faithfulness_benchmark/benchmark_stats.json",
            "results/round09/statistical_analysis.json",
            "results/round10/annotation_package_stats.json",
            "results/round10/human_annotation_status.json",
            "results/round11/reranking_metrics.json",
        ],
    }
    write_text(OUT / "manifest.json", json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    build()
