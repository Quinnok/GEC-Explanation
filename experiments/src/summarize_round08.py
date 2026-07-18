from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULTS = ROOT / "results" / "round08"
DEFAULT_DOCS = ROOT / "docs"
DEFAULT_TABLES = ROOT / "results" / "tables"


L1_DISPLAY = [
    "random",
    "majority_train",
    "current_edit_only",
    "surface_keyword",
    "structured_explicit_extraction",
    "reverse_reconstruction",
    "target_masked_reconstruction",
    "leakage_adjusted_reconstruction",
    "tfidf_embedding_similarity",
    "nli_lexical_proxy",
    "rule_evidence_verifier",
    "no_rule_verifier",
    "no_evidence_verifier",
    "no_source_reconstruction",
    "no_explanation_majority",
]


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def tex_escape(value: str) -> str:
    return value.replace("_", "\\_")


def fmt(value: float) -> str:
    return f"{value:.3f}"


def l1_rows(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = []
    for method in L1_DISPLAY:
        if method not in metrics["method_metrics"]:
            continue
        item = metrics["method_metrics"][method]
        rows.append(
            {
                "method": method,
                "n": item["n"],
                "accuracy": item["accuracy"],
                "macro_f1": item["macro_f1"],
                "positive_f1": item["positive_f1"],
                "negative_f1": item["negative_f1"],
            }
        )
    return rows


def l1_markdown(rows: List[Dict[str, Any]]) -> str:
    lines = ["| Method | N | Accuracy | Macro-F1 | Positive F1 | Negative F1 |", "|---|---:|---:|---:|---:|---:|"]
    for row in rows:
        lines.append(
            f"| `{row['method']}` | {row['n']} | {fmt(row['accuracy'])} | {fmt(row['macro_f1'])} | {fmt(row['positive_f1'])} | {fmt(row['negative_f1'])} |"
        )
    return "\n".join(lines)


def l1_latex(rows: List[Dict[str, Any]]) -> str:
    lines = [
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Method & Acc. & Macro-F1 & Pos. F1 & Neg. F1 \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(
            f"{tex_escape(row['method'])} & {fmt(row['accuracy'])} & {fmt(row['macro_f1'])} & {fmt(row['positive_f1'])} & {fmt(row['negative_f1'])} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    return "\n".join(lines)


def cf_markdown(metrics: Dict[str, Any]) -> str:
    lines = [
        "| Method | N | Accuracy | Macro-F1 |",
        "|---|---:|---:|---:|",
    ]
    for method, item in sorted(metrics["method_metrics"].items()):
        lines.append(f"| `{method}` | {item['n']} | {fmt(item['accuracy'])} | {fmt(item['macro_f1'])} |")
    return "\n".join(lines)


def cf_latex(metrics: Dict[str, Any]) -> str:
    lines = [
        "\\begin{tabular}{lrr}",
        "\\toprule",
        "Method & Acc. & Macro-F1 \\\\",
        "\\midrule",
    ]
    for method, item in sorted(metrics["method_metrics"].items()):
        lines.append(f"{tex_escape(method)} & {fmt(item['accuracy'])} & {fmt(item['macro_f1'])} \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    return "\n".join(lines)


def build(args: argparse.Namespace) -> None:
    l1 = read_json(args.results_dir / "l1_method_metrics.json")
    cf = read_json(args.results_dir / "counterfactual_method_metrics.json")
    l1_table_rows = l1_rows(l1)

    report = "\n".join(
        [
            "# Round 08: Methods and Counterfactual Pilot",
            "",
            "## Completed",
            "",
            "- Implemented L1 edit-correspondence/leakage methods over the Round 07 benchmark.",
            "- Implemented L3-style rule/evidence lexical verifier and ablations.",
            "- Built 48 counterfactual source variants from 24 model-produced edits across GECToR, T5, and CoEdIT.",
            "- Reran the original public GEC models on counterfactual sources and assigned labels from actual model behavior.",
            "- Added regression coverage for `source span` parsing.",
            "",
            "## L1/L3 Method Results",
            "",
            f"- Evaluated examples: {l1['example_count']}",
            f"- Skipped labels: `{json.dumps(l1['skipped_label_counts'], sort_keys=True)}`",
            f"- TF-IDF similarity threshold selected on train split: {l1['tfidf_threshold']}",
            "",
            l1_markdown(l1_table_rows),
            "",
            "## Reconstruction Metrics",
            "",
            "| Method | Full Exact | Span F1 | Target Match | Operation Acc. |",
            "|---|---:|---:|---:|---:|",
            *[
                f"| `{method}` | {fmt(item.get('full_edit_exact', 0.0))} | {fmt(item.get('span_f1', 0.0))} | {fmt(item.get('target_text_match', 0.0))} | {fmt(item.get('operation_accuracy', 0.0))} |"
                for method, item in sorted(l1["reconstruction_metrics"].items())
            ],
            "",
            "## Counterfactual Pilot",
            "",
            f"- Counterfactual instances: {cf['counterfactual_count']}",
            f"- Model counts: `{json.dumps(cf['model_counts'], sort_keys=True)}`",
            f"- Variant family counts: `{json.dumps(cf['variant_family_counts'], sort_keys=True)}`",
            f"- Actual behavior counts: `{json.dumps(cf['actual_behavior_counts'], sort_keys=True)}`",
            "",
            cf_markdown(cf),
            "",
            "## Interpretation Guardrails",
            "",
            "- These numbers use automatic labels and synthetic/open-model explanations; they are not human-gold faithfulness scores.",
            "- Explicit templates remain leakage upper controls.",
            "- The L2 pilot is small but real: labels come from rerunning the same public GEC models on counterfactual inputs.",
            "- Many rule-relevant variants become `competing_edit`, so Round 09 must analyze this class instead of treating all non-preserve labels as clean cancellation.",
        ]
    )

    write_text(args.docs_dir / "round_08.md", report)
    write_text(args.tables_dir / "round08_l1_methods.tex", l1_latex(l1_table_rows))
    write_text(args.tables_dir / "round08_counterfactual_methods.tex", cf_latex(cf))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Round 08 reports and tables from result JSON.")
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS)
    parser.add_argument("--tables-dir", type=Path, default=DEFAULT_TABLES)
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
