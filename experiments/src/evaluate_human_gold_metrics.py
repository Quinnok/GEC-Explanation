from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from edit_schema import Edit, compare_edits
from run_faithfulness_methods import (
    direct_leak_features,
    leakage_adjusted_reconstruction,
    mask_target,
    nli_proxy,
    parsed_edit,
    rule_evidence_verifier,
    surface_keyword,
    target_masked_reconstruction,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GOLD = ROOT / "annotation" / "round15" / "annotation_final_gold_v2.csv"
DEFAULT_EDIT_RECORDS = ROOT / "data" / "faithfulness_benchmark" / "edit_records.jsonl"
DEFAULT_RERANKING = ROOT / "results" / "round11" / "reranking_scored_candidates.jsonl"
DEFAULT_OUT_DIR = ROOT / "results" / "human_gold"
DEFAULT_ASSETS_DIR = ROOT / "results" / "paper_assets"

TARGETS = {
    "faithfulness_binary": {
        "field": "final_faithfulness",
        "positive": {"faithful", "partially_faithful"},
        "negative": {"unfaithful"},
    },
    "edit_alignment_binary": {
        "field": "final_edit_alignment",
        "positive": {"correct", "partially_correct"},
        "negative": {"incorrect"},
    },
    "rule_correctness_binary": {
        "field": "final_rule_correctness",
        "positive": {"correct", "partially_correct"},
        "negative": {"incorrect", "not_applicable"},
    },
    "evidence_binary": {
        "field": "final_evidence",
        "positive": {"correct", "partially_correct"},
        "negative": {"incorrect", "not_provided"},
    },
    "edit_validity_binary": {
        "field": "final_edit_validity",
        "positive": {"valid", "acceptable_alternative"},
        "negative": {"invalid", "stylistic"},
    },
}

ORDINAL_FAITHFULNESS = {"unfaithful": 0.0, "partially_faithful": 1.0, "faithful": 2.0}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def rank(values: List[float]) -> List[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j + 2) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def pearson(x: List[float], y: List[float]) -> Optional[float]:
    if len(x) < 2:
        return None
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    den_x = math.sqrt(sum((a - mx) ** 2 for a in x))
    den_y = math.sqrt(sum((b - my) ** 2 for b in y))
    if den_x == 0 or den_y == 0:
        return None
    return num / (den_x * den_y)


def spearman(x: List[float], y: List[float]) -> Optional[float]:
    return pearson(rank(x), rank(y))


def kendall_tau_b(x: List[float], y: List[float]) -> Optional[float]:
    n = len(x)
    if n < 2:
        return None
    concordant = discordant = ties_x = ties_y = 0
    for i in range(n):
        for j in range(i + 1, n):
            sx = (x[i] > x[j]) - (x[i] < x[j])
            sy = (y[i] > y[j]) - (y[i] < y[j])
            if sx == 0 and sy == 0:
                continue
            if sx == 0:
                ties_x += 1
                continue
            if sy == 0:
                ties_y += 1
                continue
            if sx == sy:
                concordant += 1
            else:
                discordant += 1
    den = math.sqrt((concordant + discordant + ties_x) * (concordant + discordant + ties_y))
    return None if den == 0 else (concordant - discordant) / den


def auc_roc(scores: List[float], labels: List[int]) -> Optional[float]:
    pos = [(s, y) for s, y in zip(scores, labels) if y == 1]
    neg = [(s, y) for s, y in zip(scores, labels) if y == 0]
    if not pos or not neg:
        return None
    wins = ties = 0
    for ps, _ in pos:
        for ns, _ in neg:
            if ps > ns:
                wins += 1
            elif ps == ns:
                ties += 1
    return (wins + 0.5 * ties) / (len(pos) * len(neg))


def average_precision(scores: List[float], labels: List[int]) -> Optional[float]:
    if sum(labels) == 0:
        return None
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    tp = 0
    precision_sum = 0.0
    for rank_idx, i in enumerate(order, start=1):
        if labels[i] == 1:
            tp += 1
            precision_sum += tp / rank_idx
    return precision_sum / sum(labels)


def binary_metrics(scores: List[float], labels: List[int], threshold: float = 0.5) -> Dict[str, Any]:
    preds = [1 if score >= threshold else 0 for score in scores]
    tp = sum(1 for p, y in zip(preds, labels) if p == 1 and y == 1)
    tn = sum(1 for p, y in zip(preds, labels) if p == 0 and y == 0)
    fp = sum(1 for p, y in zip(preds, labels) if p == 1 and y == 0)
    fn = sum(1 for p, y in zip(preds, labels) if p == 0 and y == 1)
    pos_precision = safe_div(tp, tp + fp)
    pos_recall = safe_div(tp, tp + fn)
    pos_f1 = safe_div(2 * pos_precision * pos_recall, pos_precision + pos_recall)
    neg_precision = safe_div(tn, tn + fn)
    neg_recall = safe_div(tn, tn + fp)
    neg_f1 = safe_div(2 * neg_precision * neg_recall, neg_precision + neg_recall)
    return {
        "n": len(labels),
        "positive_count": sum(labels),
        "negative_count": len(labels) - sum(labels),
        "accuracy": safe_div(tp + tn, len(labels)),
        "macro_f1": (pos_f1 + neg_f1) / 2,
        "positive_precision": pos_precision,
        "positive_recall": pos_recall,
        "positive_f1": pos_f1,
        "negative_precision": neg_precision,
        "negative_recall": neg_recall,
        "negative_f1": neg_f1,
        "auroc": auc_roc(scores, labels),
        "auprc": average_precision(scores, labels),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


def ci(values: List[float]) -> Tuple[Optional[float], Optional[float]]:
    cleaned = sorted(v for v in values if v is not None and not math.isnan(v))
    if not cleaned:
        return None, None
    lo = cleaned[int(0.025 * (len(cleaned) - 1))]
    hi = cleaned[int(0.975 * (len(cleaned) - 1))]
    return lo, hi


def edit_from_record(edit_record: Dict[str, Any], error_type: str) -> Edit:
    edit = Edit.from_dict(edit_record["predicted_edit"])
    return Edit(edit.start, edit.end, edit.source_text, edit.target_text, edit.operation, error_type)


def reconstruction_score(example: Dict[str, Any], explanation: str | None = None, source: str | None = None) -> float:
    text = example["explanation"] if explanation is None else explanation
    src = example["source"] if source is None else source
    pred = parsed_edit(src, text, example["error_type"])
    if pred is None:
        return 0.0
    metrics = compare_edits(pred, example["edit"])
    return (
        metrics["span_f1"]
        + metrics["target_text_match"]
        + metrics["operation_accuracy"]
        + metrics["error_type_accuracy"]
    ) / 4.0


def length_score(text: str) -> float:
    words = len(text.split())
    return max(0.0, 1.0 - abs(words - 18) / 30)


def direct_surface_score(example: Dict[str, Any]) -> float:
    hits = direct_leak_features(example["explanation"], example["edit"])
    return sum(1.0 for value in hits.values() if value) / len(hits)


def score_methods(example: Dict[str, Any], rerank_scores: Dict[Tuple[str, str], float]) -> Dict[str, Optional[float]]:
    masked = mask_target(example["explanation"], example["edit"])
    recon = reconstruction_score(example)
    surface = direct_surface_score(example)
    rule = 1.0 if rule_evidence_verifier(example) else 0.0
    local_llm = rerank_scores.get((example["instance_id"], "local_llm_judge"))
    scores: Dict[str, Optional[float]] = {
        "surface_keyword": 1.0 if surface_keyword(example) else 0.0,
        "surface_leak_score": surface,
        "structured_extraction": 1.0 if recon == 1.0 else 0.0,
        "reverse_reconstruction": recon,
        "target_masked_reconstruction": 1.0 if target_masked_reconstruction(example) else 0.0,
        "leakage_adjusted_reconstruction": 1.0 if leakage_adjusted_reconstruction(example) else 0.0,
        "target_masked_score": reconstruction_score(example, explanation=masked),
        "rule_evidence_verifier": rule,
        "nli_lexical_proxy": 1.0 if nli_proxy(example) else 0.0,
        "local_llm_judge": local_llm,
        "combined_proxy": 0.20 * length_score(example["explanation"]) + 0.25 * surface + 0.25 * recon + 0.30 * rule,
    }
    existing_combined = rerank_scores.get((example["instance_id"], "combined_reranker"))
    if existing_combined is not None:
        scores["combined_reranker_round11"] = existing_combined
    return scores


def target_value(row: Dict[str, str], target_name: str) -> Optional[int]:
    spec = TARGETS[target_name]
    value = row[spec["field"]]
    if value in spec["positive"]:
        return 1
    if value in spec["negative"]:
        return 0
    return None


def ordinal_value(row: Dict[str, str]) -> Optional[float]:
    return ORDINAL_FAITHFULNESS.get(row["final_faithfulness"])


def pairwise_accuracy(rows: List[Dict[str, Any]], method: str) -> Optional[float]:
    by_edit: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["scores"].get(method) is None or row["faithfulness_ordinal"] is None:
            continue
        by_edit[row["edit_id"]].append(row)
    correct = total = ties = 0
    for group in by_edit.values():
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                yi = group[i]["faithfulness_ordinal"]
                yj = group[j]["faithfulness_ordinal"]
                if yi == yj:
                    continue
                si = group[i]["scores"][method]
                sj = group[j]["scores"][method]
                total += 1
                if si == sj:
                    ties += 1
                    correct += 0.5
                elif (si > sj and yi > yj) or (si < sj and yi < yj):
                    correct += 1
    return None if total == 0 else correct / total


def bootstrap_ci(rows: List[Dict[str, Any]], method: str, target_name: str, iterations: int, seed: int) -> Dict[str, Any]:
    eligible = [row for row in rows if row["scores"].get(method) is not None and row["targets"].get(target_name) is not None]
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in eligible:
        groups[row["source"]].append(row)
    keys = sorted(groups)
    if not keys:
        return {"macro_f1_ci": [None, None], "auroc_ci": [None, None], "group_count": 0}
    rng = random.Random(seed)
    f1_values: List[float] = []
    auc_values: List[float] = []
    for _ in range(iterations):
        sampled: List[Dict[str, Any]] = []
        for key in (rng.choice(keys) for _ in keys):
            sampled.extend(groups[key])
        scores = [float(row["scores"][method]) for row in sampled]
        labels = [int(row["targets"][target_name]) for row in sampled]
        result = binary_metrics(scores, labels)
        f1_values.append(result["macro_f1"])
        if result["auroc"] is not None:
            auc_values.append(result["auroc"])
    f1_lo, f1_hi = ci(f1_values)
    auc_lo, auc_hi = ci(auc_values)
    return {"macro_f1_ci": [f1_lo, f1_hi], "auroc_ci": [auc_lo, auc_hi], "group_count": len(keys)}


def fmt(value: Any) -> str:
    if value is None:
        return "--"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def latex_table(path: Path, label: str, caption: str, headers: List[str], rows: List[List[Any]]) -> None:
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\scriptsize",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        "\\resizebox{\\columnwidth}{!}{%",
        "\\begin{tabular}{" + "l" + "r" * (len(headers) - 1) + "}",
        "\\toprule",
        " & ".join(headers) + " \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(fmt(value) for value in row) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}%", "}", "\\end{table}"])
    write_text(path, "\n".join(lines))


def build_examples(gold_rows: List[Dict[str, str]], edit_records: Dict[str, Dict[str, Any]], rerank_scores: Dict[Tuple[str, str], float]) -> List[Dict[str, Any]]:
    examples = []
    for row in gold_rows:
        if not row.get("instance_id") or not row.get("edit_id") or row["edit_id"] not in edit_records:
            continue
        edit_record = edit_records[row["edit_id"]]
        edit = edit_from_record(edit_record, row["error_type"])
        example = {
            **row,
            "edit": edit,
            "source": row["source"],
            "explanation": row["explanation"],
            "error_type": row["error_type"],
        }
        example["scores"] = score_methods(example, rerank_scores)
        example["targets"] = {name: target_value(row, name) for name in TARGETS}
        example["faithfulness_ordinal"] = ordinal_value(row)
        examples.append(example)
    return examples


def evaluate(args: argparse.Namespace) -> None:
    gold_rows = read_csv(args.gold)
    edit_records = {row["edit_id"]: row for row in read_jsonl(args.edit_records)}
    rerank_scores: Dict[Tuple[str, str], float] = {}
    if args.reranking.exists():
        for row in read_jsonl(args.reranking):
            rerank_scores[(row["candidate_id"], row["method"])] = float(row["score"])
    rows = build_examples(gold_rows, edit_records, rerank_scores)
    methods = sorted({method for row in rows for method, score in row["scores"].items() if score is not None})

    coverage_rows = []
    metric_rows = []
    bootstrap_results: Dict[str, Any] = {}
    for method in methods:
        covered = [row for row in rows if row["scores"].get(method) is not None]
        coverage_rows.append(
            {
                "method": method,
                "covered": len(covered),
                "total": len(rows),
                "coverage": safe_div(len(covered), len(rows)),
            }
        )
        for target_name in TARGETS:
            eligible = [row for row in covered if row["targets"].get(target_name) is not None]
            if not eligible:
                continue
            scores = [float(row["scores"][method]) for row in eligible]
            labels = [int(row["targets"][target_name]) for row in eligible]
            result = binary_metrics(scores, labels)
            metric_rows.append({"method": method, "target": target_name, **result})
        bootstrap_results[method] = bootstrap_ci(rows, method, "faithfulness_binary", args.bootstrap_iterations, args.seed)

    correlation_rows = []
    for method in methods:
        eligible = [
            row
            for row in rows
            if row["scores"].get(method) is not None and row["faithfulness_ordinal"] is not None
        ]
        scores = [float(row["scores"][method]) for row in eligible]
        labels = [float(row["faithfulness_ordinal"]) for row in eligible]
        correlation_rows.append(
            {
                "method": method,
                "n": len(eligible),
                "spearman": spearman(scores, labels),
                "kendall_b": kendall_tau_b(scores, labels),
                "pairwise_accuracy": pairwise_accuracy(rows, method),
            }
        )

    breakdown_rows = []
    for group_field in [
        "explanation_type",
        "model_behavior",
        "model_family",
        "dataset",
        "error_type",
        "final_edit_validity",
        "final_rule_correctness",
        "final_evidence",
    ]:
        for method in methods:
            by_group: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
            for row in rows:
                if row["scores"].get(method) is not None and row["targets"].get("faithfulness_binary") is not None:
                    by_group[row.get(group_field, "")].append(row)
            for group, group_rows in sorted(by_group.items()):
                if len(group_rows) < 3:
                    continue
                scores = [float(row["scores"][method]) for row in group_rows]
                labels = [int(row["targets"]["faithfulness_binary"]) for row in group_rows]
                result = binary_metrics(scores, labels)
                breakdown_rows.append(
                    {
                        "group_field": group_field,
                        "group": group,
                        "method": method,
                        "n": len(group_rows),
                        "accuracy": result["accuracy"],
                        "macro_f1": result["macro_f1"],
                        "auroc": result["auroc"],
                    }
                )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "main_metric_table.csv", metric_rows)
    write_csv(args.out_dir / "correlation_table.csv", correlation_rows)
    write_csv(args.out_dir / "stress_test_breakdown.csv", breakdown_rows)
    write_csv(args.out_dir / "coverage_report.csv", coverage_rows)
    write_json(args.out_dir / "bootstrap_results.json", bootstrap_results)
    write_json(
        args.out_dir / "coverage_report.json",
        {
            "created_at": utc_now(),
            "gold_items": len(gold_rows),
            "aligned_items": len(rows),
            "missing_alignment": len(gold_rows) - len(rows),
            "methods": coverage_rows,
            "target_counts": {
                name: dict(Counter(row["targets"][name] for row in rows if row["targets"].get(name) is not None))
                for name in TARGETS
            },
        },
    )

    summary = {
        "created_at": utc_now(),
        "gold_items": len(gold_rows),
        "aligned_items": len(rows),
        "method_count": len(methods),
        "best_by_faithfulness_macro_f1": sorted(
            [
                row
                for row in metric_rows
                if row["target"] == "faithfulness_binary"
            ],
            key=lambda row: row["macro_f1"],
            reverse=True,
        )[:5],
        "best_by_rule_macro_f1": sorted(
            [row for row in metric_rows if row["target"] == "rule_correctness_binary"],
            key=lambda row: row["macro_f1"],
            reverse=True,
        )[:5],
        "best_by_evidence_macro_f1": sorted(
            [row for row in metric_rows if row["target"] == "evidence_binary"],
            key=lambda row: row["macro_f1"],
            reverse=True,
        )[:5],
    }
    write_json(args.out_dir / "human_gold_metric_summary.json", summary)

    selected_methods = [
        "surface_leak_score",
        "reverse_reconstruction",
        "target_masked_score",
        "leakage_adjusted_reconstruction",
        "rule_evidence_verifier",
        "local_llm_judge",
        "combined_proxy",
    ]
    selected_methods = [method for method in selected_methods if method in methods]
    metric_by = {(row["method"], row["target"]): row for row in metric_rows}
    table_rows = []
    for method in selected_methods:
        faith = metric_by.get((method, "faithfulness_binary"), {})
        align = metric_by.get((method, "edit_alignment_binary"), {})
        rule = metric_by.get((method, "rule_correctness_binary"), {})
        evidence = metric_by.get((method, "evidence_binary"), {})
        boot = bootstrap_results.get(method, {})
        ci_pair = boot.get("macro_f1_ci", [None, None])
        table_rows.append(
            {
                "method": method,
                "coverage": next((row["coverage"] for row in coverage_rows if row["method"] == method), 0.0),
                "edit_alignment_macro_f1": align.get("macro_f1"),
                "rule_macro_f1": rule.get("macro_f1"),
                "evidence_macro_f1": evidence.get("macro_f1"),
                "faithfulness_macro_f1": faith.get("macro_f1"),
                "faithfulness_auroc": faith.get("auroc"),
                "faithfulness_macro_f1_ci_low": ci_pair[0],
                "faithfulness_macro_f1_ci_high": ci_pair[1],
            }
        )
    write_csv(args.out_dir / "main_metric_table_selected.csv", table_rows)

    latex_rows = [
        [
            row["method"].replace("_", "\\_"),
            row["coverage"],
            row["edit_alignment_macro_f1"],
            row["rule_macro_f1"],
            row["evidence_macro_f1"],
            row["faithfulness_macro_f1"],
            row["faithfulness_auroc"],
        ]
        for row in table_rows
    ]
    latex_table(
        args.out_dir / "main_metric_table.tex",
        "tab:human-gold-metrics",
        "Automatic metrics against adjudicated edit-explanation labels.",
        ["Method", "Cov.", "Align", "Rule", "Evid.", "Faith.", "AUROC"],
        latex_rows,
    )
    latex_table(
        args.assets_dir / "human_gold_metric_table.tex",
        "tab:human-gold-metrics",
        "Automatic metrics against adjudicated edit-explanation labels.",
        ["Method", "Cov.", "Align", "Rule", "Evid.", "Faith.", "AUROC"],
        latex_rows,
    )

    corr_by = {row["method"]: row for row in correlation_rows}
    corr_rows = [
        [
            method.replace("_", "\\_"),
            corr_by[method]["spearman"],
            corr_by[method]["kendall_b"],
            corr_by[method]["pairwise_accuracy"],
        ]
        for method in selected_methods
        if method in corr_by
    ]
    latex_table(
        args.out_dir / "correlation_table.tex",
        "tab:human-gold-correlations",
        "Correlation between automatic scores and ordinal adjudicated faithfulness.",
        ["Method", "Spearman", "Kendall", "Pairwise"],
        corr_rows,
    )
    latex_table(
        args.assets_dir / "human_gold_correlation_table.tex",
        "tab:human-gold-correlations",
        "Correlation between automatic scores and ordinal adjudicated faithfulness.",
        ["Method", "Spearman", "Kendall", "Pairwise"],
        corr_rows,
    )

    write_cases(args.out_dir / "error_cases.md", rows)
    write_text(args.out_dir / "evaluation_readme.md", build_readme(summary, table_rows, correlation_rows))


def case_line(row: Dict[str, Any], extra: str = "") -> str:
    text = [
        f"- `{row['item_id']}` `{row['explanation_type']}` `{row['model_key']}` `{row['model_behavior']}`",
        f"  - Edit: {row['model_edit']}",
        f"  - Explanation: {row['explanation']}",
        f"  - Human: alignment={row['final_edit_alignment']}, rule={row['final_rule_correctness']}, evidence={row['final_evidence']}, faithfulness={row['final_faithfulness']}",
    ]
    if extra:
        text.append(f"  - {extra}")
    return "\n".join(text)


def write_cases(path: Path, rows: List[Dict[str, Any]]) -> None:
    lines = ["# Human-Gold Stress Test Cases", ""]
    high_recon_low_rule = [
        row
        for row in rows
        if row["scores"].get("reverse_reconstruction", 0.0) >= 0.75
        and row["final_rule_correctness"] in {"incorrect", "not_applicable"}
    ][:20]
    lines.extend(["## High Reconstruction But Low Rule Correctness", ""])
    lines.extend(case_line(row, f"reverse_reconstruction={row['scores']['reverse_reconstruction']:.3f}") for row in high_recon_low_rule)
    lines.append("")

    high_recon_low_evidence = [
        row
        for row in rows
        if row["scores"].get("reverse_reconstruction", 0.0) >= 0.75
        and row["final_evidence"] in {"incorrect", "not_provided"}
    ][:20]
    lines.extend(["## High Reconstruction But Low Evidence Quality", ""])
    lines.extend(case_line(row, f"reverse_reconstruction={row['scores']['reverse_reconstruction']:.3f}") for row in high_recon_low_evidence)
    lines.append("")

    invalid_rationalization = [
        row
        for row in rows
        if row["final_edit_validity"] in {"invalid", "stylistic"}
        and row["final_faithfulness"] == "unfaithful"
    ][:20]
    lines.extend(["## Invalid Or Stylistic Edits With Unfaithful Rationales", ""])
    lines.extend(case_line(row) for row in invalid_rationalization)
    lines.append("")

    llm_disagreement = [
        row
        for row in rows
        if row["scores"].get("local_llm_judge") is not None
        and ((row["scores"]["local_llm_judge"] >= 0.5 and row["final_faithfulness"] == "unfaithful")
             or (row["scores"]["local_llm_judge"] < 0.5 and row["final_faithfulness"] != "unfaithful"))
    ][:20]
    lines.extend(["## Local LLM Judge Disagrees With Adjudicated Label", ""])
    lines.extend(case_line(row, f"local_llm_judge={row['scores']['local_llm_judge']:.3f}") for row in llm_disagreement)
    lines.append("")

    by_edit: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_edit[row["edit_id"]].append(row)
    reward_cases = []
    for group in by_edit.values():
        if len(group) < 2:
            continue
        top = max(group, key=lambda row: row["scores"].get("combined_proxy", -1))
        better = [
            row
            for row in group
            if row["faithfulness_ordinal"] is not None
            and top["faithfulness_ordinal"] is not None
            and row["faithfulness_ordinal"] > top["faithfulness_ordinal"]
        ]
        if better and top["explanation_type"] in {"explicit_template", "masked_target_template"}:
            reward_cases.append((top, better[0]))
    lines.extend(["## Combined Proxy Selects Template Despite Better Human Label", ""])
    for top, better in reward_cases[:20]:
        lines.append(case_line(top, f"combined_proxy={top['scores']['combined_proxy']:.3f}; better item `{better['item_id']}` is `{better['final_faithfulness']}`"))
    write_text(path, "\n".join(lines))


def build_readme(summary: Dict[str, Any], table_rows: List[Dict[str, Any]], correlation_rows: List[Dict[str, Any]]) -> str:
    best = summary["best_by_faithfulness_macro_f1"][0] if summary["best_by_faithfulness_macro_f1"] else {}
    return f"""# Round 15 Human-Gold Metric Evaluation

Created: `{summary['created_at']}`

Gold items aligned: `{summary['aligned_items']}` / `{summary['gold_items']}`

Best binary faithfulness Macro-F1 in this run:

- `{best.get('method', 'NA')}`: `{fmt(best.get('macro_f1'))}`

Important caveat: this is a stress-test set dominated by intentionally difficult or negative explanation types. Do not interpret the label distribution as the natural prevalence of faithful GEC explanations.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate automatic metrics against finalized Round 15 labels.")
    parser.add_argument("--gold", type=Path, default=DEFAULT_GOLD)
    parser.add_argument("--edit-records", type=Path, default=DEFAULT_EDIT_RECORDS)
    parser.add_argument("--reranking", type=Path, default=DEFAULT_RERANKING)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--assets-dir", type=Path, default=DEFAULT_ASSETS_DIR)
    parser.add_argument("--bootstrap-iterations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260719)
    return parser.parse_args()


if __name__ == "__main__":
    evaluate(parse_args())
