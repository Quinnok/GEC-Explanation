from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import torch
from huggingface_hub import model_info
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from edit_schema import Edit, compare_edits
from llm_judge import build_yes_no_prompt, parse_yes_no_score
from run_faithfulness_methods import (
    direct_leak_features,
    parsed_edit,
    rule_evidence_verifier,
    surface_keyword,
    tfidf_predict,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BENCHMARK = ROOT / "data" / "faithfulness_benchmark"
DEFAULT_ROUND09 = ROOT / "results" / "round09"
DEFAULT_OUT_DIR = ROOT / "results" / "round11"
DEFAULT_DOCS = ROOT / "docs"

POSITIVE_LABELS = {
    "faithful_positive": 1.0,
    "faithful_positive_masked": 0.8,
    "partially_informative_positive": 0.6,
    "faithful_candidate": 0.7,
    "faithful_to_model_behavior_not_grammar_gold": 0.7,
}
NEGATIVE_LABELS = {
    "negative": 0.0,
    "negative_partial": 0.25,
}
SELECTED_TYPES = {
    "explicit_template",
    "masked_target_template",
    "rule_only",
    "gee_style_automatic",
    "rule_grounded_automatic",
    "wrong_span",
    "wrong_target",
    "wrong_direction",
    "wrong_rule",
    "swapped_across_sentence",
    "generic",
}


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


def stable_float(key: str) -> float:
    value = int(hashlib.sha1(key.encode("utf-8")).hexdigest(), 16) % 1_000_000
    return value / 1_000_000


def grade_for(label: str) -> Optional[float]:
    if label in POSITIVE_LABELS:
        return POSITIVE_LABELS[label]
    if label in NEGATIVE_LABELS:
        return NEGATIVE_LABELS[label]
    return None


def edit_text(edit: Dict[str, Any]) -> str:
    if edit["operation"] == "replace":
        return f'{edit.get("source_text", "")} -> {edit.get("target_text", "")}'
    if edit["operation"] == "insert":
        return f'insert {edit.get("target_text", "")}'
    if edit["operation"] == "delete":
        return f'delete {edit.get("source_text", "")}'
    return json.dumps(edit, ensure_ascii=False)


def build_candidates(edit_rows: List[Dict[str, Any]], explanation_rows: List[Dict[str, Any]], edit_limit: int) -> List[Dict[str, Any]]:
    edits = {row["edit_id"]: row for row in edit_rows}
    eligible_edit_ids = sorted(edits)[:edit_limit]
    eligible = set(eligible_edit_ids)
    candidates = []
    for exp in explanation_rows:
        if exp["edit_id"] not in eligible or exp["explanation_type"] not in SELECTED_TYPES:
            continue
        grade = grade_for(exp["label"])
        if grade is None:
            continue
        edit_record = edits[exp["edit_id"]]
        edit = Edit.from_dict(edit_record["predicted_edit"])
        edit = Edit(edit.start, edit.end, edit.source_text, edit.target_text, edit.operation, exp["error_type"])
        candidates.append(
            {
                "candidate_id": exp["instance_id"],
                "edit_id": exp["edit_id"],
                "sample_id": exp["sample_id"],
                "dataset": exp["dataset"],
                "model_key": exp["model_key"],
                "model_family": exp["model_family"],
                "behavior": exp["behavior"],
                "error_type": exp["error_type"],
                "explanation_type": exp["explanation_type"],
                "negative_type": exp["negative_type"],
                "label": exp["label"],
                "grade": grade,
                "is_positive": grade >= 0.5,
                "source": edit_record["source"],
                "prediction": edit_record["prediction"],
                "edit": edit.to_dict(),
                "explanation": exp["explanation"],
            }
        )
    return candidates


def length_score(text: str) -> float:
    words = len(text.split())
    return max(0.0, 1.0 - abs(words - 18) / 30)


def surface_score(candidate: Dict[str, Any]) -> float:
    edit = Edit.from_dict(candidate["edit"])
    hits = direct_leak_features(candidate["explanation"], edit)
    return sum(hits.values()) / len(hits)


def reconstruction_score(candidate: Dict[str, Any]) -> float:
    edit = Edit.from_dict(candidate["edit"])
    pred = parsed_edit(candidate["source"], candidate["explanation"], candidate["error_type"])
    if pred is None:
        return 0.0
    metrics = compare_edits(pred, edit)
    return (
        metrics["span_f1"]
        + metrics["target_text_match"]
        + metrics["operation_accuracy"]
        + metrics["error_type_accuracy"]
    ) / 4


def rule_score(candidate: Dict[str, Any]) -> float:
    row = {
        "explanation": candidate["explanation"],
        "edit": Edit.from_dict(candidate["edit"]),
        "error_type": candidate["error_type"],
    }
    return 1.0 if rule_evidence_verifier(row) else 0.0


def counterfactual_scores(round09_dir: Path) -> Dict[Tuple[str, str], float]:
    path = round09_dir / "counterfactual_simulator_predictions.jsonl"
    if not path.exists():
        return {}
    hits: Dict[Tuple[str, str], List[float]] = defaultdict(list)
    for row in read_jsonl(path):
        if row["method"] == "explanation_leakage_simulator":
            hits[(row["origin_edit_id"], row["explanation_type"])].append(1.0 if row["correct"] else 0.0)
    return {key: sum(values) / len(values) for key, values in hits.items()}


def llm_prompt(candidate: Dict[str, Any]) -> str:
    return build_yes_no_prompt(candidate)


def run_local_llm_judge(candidates: List[Dict[str, Any]], args: argparse.Namespace) -> Dict[str, float]:
    selected = candidates[: args.llm_judge_limit]
    if not selected:
        return {}
    started = time.time()
    try:
        revision = model_info(args.llm_judge_model).sha or "unknown"
    except Exception as exc:  # pragma: no cover - network/cache dependent metadata.
        revision = f"metadata_unavailable:{type(exc).__name__}"
    tokenizer = AutoTokenizer.from_pretrained(args.llm_judge_model)
    model = AutoModelForSeq2SeqLM.from_pretrained(args.llm_judge_model).to("cpu")
    model.eval()
    torch.set_num_threads(1)
    scores: Dict[str, float] = {}
    for start in range(0, len(selected), args.llm_batch_size):
        batch = selected[start : start + args.llm_batch_size]
        prompts = [llm_prompt(candidate) for candidate in batch]
        inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=384)
        with torch.inference_mode():
            output_ids = model.generate(**inputs, max_new_tokens=3, num_beams=1)
        decoded = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        for candidate, text in zip(batch, decoded):
            scores[candidate["candidate_id"]] = parse_yes_no_score(text)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_json(
        args.out_dir / "local_llm_judge_metadata.json",
        {
            "created_at": utc_now(),
            "model_id": args.llm_judge_model,
            "model_revision": revision,
            "candidate_count": len(selected),
            "duration_seconds": round(time.time() - started, 3),
            "score_counts": {str(key): value for key, value in Counter(scores.values()).items()},
            "important_note": "Local open-source FLAN-T5 judge; no paid API. Scores are automatic and not human judgments.",
        },
    )
    return scores


def method_scores(candidates: List[Dict[str, Any]], cf_scores: Dict[Tuple[str, str], float], llm_scores: Dict[str, float]) -> List[Dict[str, Any]]:
    rows = []
    for candidate in candidates:
        surf = surface_score(candidate)
        recon = reconstruction_score(candidate)
        rule = rule_score(candidate)
        cf = cf_scores.get((candidate["edit_id"], candidate["explanation_type"]), 0.0)
        llm = llm_scores.get(candidate["candidate_id"], 0.5)
        length = length_score(candidate["explanation"])
        scores = {
            "random_selection": stable_float(candidate["candidate_id"]),
            "length_heuristic": length,
            "surface_score": surf,
            "local_llm_judge": llm,
            "reconstruction_score": recon,
            "counterfactual_score": cf,
            "rule_evidence_score": rule,
            "combined_reranker": 0.15 * length + 0.2 * surf + 0.2 * recon + 0.2 * cf + 0.25 * rule,
        }
        for method, score in scores.items():
            rows.append({**candidate, "method": method, "score": score})
    return rows


def rank_groups(scored_rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    groups: Dict[str, Dict[str, List[Dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in scored_rows:
        groups[row["method"]][row["edit_id"]].append(row)
    for method in groups:
        for edit_id in groups[method]:
            groups[method][edit_id].sort(key=lambda row: (row["score"], stable_float(row["candidate_id"])), reverse=True)
    return groups


def pairwise_accuracy(rows: List[Dict[str, Any]]) -> float:
    total = 0
    correct = 0
    for i, left in enumerate(rows):
        for right in rows[i + 1 :]:
            if left["grade"] == right["grade"]:
                continue
            total += 1
            better, worse = (left, right) if left["grade"] > right["grade"] else (right, left)
            if better["score"] > worse["score"]:
                correct += 1
            elif better["score"] == worse["score"]:
                correct += 0.5
    return correct / total if total else 0.0


def mrr(rows: List[Dict[str, Any]]) -> float:
    for idx, row in enumerate(rows, start=1):
        if row["is_positive"]:
            return 1.0 / idx
    return 0.0


def fluency_proxy(text: str) -> float:
    words = text.split()
    if not words:
        return 0.0
    repeated = sum(1 for i in range(1, len(words)) if words[i].lower() == words[i - 1].lower())
    has_sentence_punctuation = bool(re.search(r"[.!?]$", text.strip()))
    return max(0.0, 1.0 - repeated / max(1, len(words))) * (1.0 if has_sentence_punctuation else 0.85)


def evaluate(scored_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    groups = rank_groups(scored_rows)
    metrics = {}
    reward = {}
    for method, by_edit in groups.items():
        top_rows = [rows[0] for rows in by_edit.values() if rows]
        metrics[method] = {
            "edit_count": len(by_edit),
            "pairwise_ranking_accuracy": sum(pairwise_accuracy(rows) for rows in by_edit.values()) / len(by_edit),
            "mrr": sum(mrr(rows) for rows in by_edit.values()) / len(by_edit),
            "automatic_top1_faithfulness": sum(row["grade"] for row in top_rows) / len(top_rows),
            "human_top1_preference": None,
            "human_top1_preference_status": "blocked_no_human_labels",
            "automatic_grammatical_validity_proxy": sum(1.0 for row in top_rows if row["label"] in POSITIVE_LABELS) / len(top_rows),
            "automatic_helpfulness_proxy": sum(0.0 if row["explanation_type"] == "generic" else min(1.0, len(row["explanation"].split()) / 12) for row in top_rows) / len(top_rows),
            "average_explanation_length": sum(len(row["explanation"].split()) for row in top_rows) / len(top_rows),
            "fluency_proxy": sum(fluency_proxy(row["explanation"]) for row in top_rows) / len(top_rows),
        }
        reward[method] = {
            "template_top1_rate": sum(1 for row in top_rows if "template" in row["explanation_type"]) / len(top_rows),
            "edit_copy_top1_rate": sum(1 for row in top_rows if surface_score(row) >= 0.8) / len(top_rows),
            "too_long_top1_rate": sum(1 for row in top_rows if len(row["explanation"].split()) > 35) / len(top_rows),
            "generic_top1_rate": sum(1 for row in top_rows if row["explanation_type"] == "generic") / len(top_rows),
            "unrelated_rule_top1_rate": sum(1 for row in top_rows if row["explanation_type"] == "wrong_rule") / len(top_rows),
        }
    return {"method_metrics": metrics, "reward_hacking": reward}


def tex_table(metrics: Dict[str, Any]) -> str:
    lines = [
        "\\noindent\\resizebox{0.95\\linewidth}{!}{%",
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Method & Pairwise & MRR & AutoTop1 & AvgLen \\\\",
        "\\midrule",
    ]
    for method, row in sorted(metrics.items()):
        escaped_method = method.replace("_", "\\_")
        lines.append(
            f"{escaped_method} & {row['pairwise_ranking_accuracy']:.3f} & {row['mrr']:.3f} & {row['automatic_top1_faithfulness']:.3f} & {row['average_explanation_length']:.1f} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}%", "}"])
    return "\n".join(lines)


def run(args: argparse.Namespace) -> None:
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    edit_rows = read_jsonl(args.benchmark_dir / "edit_records.jsonl")
    explanation_rows = read_jsonl(args.benchmark_dir / "explanation_instances.jsonl")
    candidates = build_candidates(edit_rows, explanation_rows, args.edit_limit)
    cf = counterfactual_scores(args.round09_dir)
    llm_scores = run_local_llm_judge(candidates, args) if args.run_local_llm_judge else {}
    scored = method_scores(candidates, cf, llm_scores)
    evaluation = evaluate(scored)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "reranking_candidates.jsonl", candidates)
    write_jsonl(args.out_dir / "reranking_scored_candidates.jsonl", scored)
    write_json(
        args.out_dir / "reranking_metrics.json",
        {
            "created_at": utc_now(),
            "edit_limit": args.edit_limit,
            "candidate_count": len(candidates),
            "local_llm_judged_candidate_count": len(llm_scores),
            "local_llm_unjudged_candidate_count": max(0, len(candidates) - len(llm_scores)),
            "candidate_type_counts": dict(Counter(row["explanation_type"] for row in candidates)),
            "method_count": len(evaluation["method_metrics"]),
            "human_top1_preference_status": "blocked_no_human_labels",
            **evaluation,
        },
    )
    write_json(args.out_dir / "reward_hacking_report.json", evaluation["reward_hacking"])
    write_text(ROOT / "results" / "tables" / "round11_reranking.tex", tex_table(evaluation["method_metrics"]))
    best = max(evaluation["method_metrics"].items(), key=lambda item: item[1]["pairwise_ranking_accuracy"])
    write_text(
        args.docs_dir / "round_11.md",
        "\n".join(
            [
                "# Round 11: Explanation Candidate Reranking",
                "",
                "## Completed",
                "",
                f"- Built reranking candidates for {args.edit_limit} model-produced edits.",
                f"- Candidate count: {len(candidates)}.",
                "- Compared random, length, surface, local open-source LLM judge, reconstruction, counterfactual, rule/evidence, and combined rerankers.",
                "- Evaluated pairwise ranking accuracy, MRR, automatic top-1 faithfulness, grammatical-validity proxy, helpfulness proxy, length, fluency proxy, and reward-hacking indicators.",
                "",
                "## Key Result",
                "",
                f"- Best automatic pairwise ranking method: `{best[0]}` with {best[1]['pairwise_ranking_accuracy']:.3f} pairwise accuracy.",
                "- Human top-1 preference remains blocked because no human labels exist.",
                "",
                "## Files",
                "",
                "- `results/round11/reranking_candidates.jsonl`",
                "- `results/round11/reranking_scored_candidates.jsonl`",
                "- `results/round11/reranking_metrics.json`",
                "- `results/round11/reward_hacking_report.json`",
                "- `results/tables/round11_reranking.tex`",
            ]
        ),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Round 11 explanation candidate reranking experiment.")
    parser.add_argument("--benchmark-dir", type=Path, default=DEFAULT_BENCHMARK)
    parser.add_argument("--round09-dir", type=Path, default=DEFAULT_ROUND09)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS)
    parser.add_argument("--edit-limit", type=int, default=80)
    parser.add_argument("--run-local-llm-judge", action="store_true")
    parser.add_argument("--llm-judge-model", default="google/flan-t5-base")
    parser.add_argument("--llm-judge-limit", type=int, default=880)
    parser.add_argument("--llm-batch-size", type=int, default=16)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)
