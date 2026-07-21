from __future__ import annotations

import argparse
import csv
import json
import math
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = (
    ROOT
    / "annotation"
    / "rulefaith_qwen3_ready_validation_v2"
    / "ready_validation_completed_by_codex_merged_with_key.csv"
)
DEFAULT_OUTPUT_CSV = ROOT / "results" / "rulefaith" / "rulefaith_ready_candidate_scores.csv"
DEFAULT_METRICS_JSON = ROOT / "results" / "rulefaith" / "rulefaith_ready_selector_metrics.json"
DEFAULT_METRICS_CSV = ROOT / "results" / "rulefaith" / "rulefaith_ready_selector_metrics.csv"
DEFAULT_CASES_MD = ROOT / "results" / "rulefaith" / "rulefaith_ready_selector_cases.md"
DEFAULT_TEX = ROOT / "results" / "paper_assets" / "rulefaith_ready_selector_metrics.tex"
DEFAULT_REPORT = ROOT / "docs" / "rulefaith_loop_P_deployable_selector.md"

PSEUDO_UTILITY = {"accept": 1.0, "refine": 0.5, "reject": 0.0}

GRAMMAR_KEYWORDS = {
    "agreement",
    "article",
    "determiner",
    "plural",
    "singular",
    "preposition",
    "pronoun",
    "antecedent",
    "verb",
    "tense",
    "aspect",
    "infinitive",
    "gerund",
    "participle",
    "auxiliary",
    "word order",
    "clause",
    "punctuation",
    "spelling",
    "orthographic",
    "collocation",
    "idiom",
    "countable",
    "uncountable",
}

GENERIC_PHRASES = {
    "grammar issue",
    "grammatical issue",
    "grammar problem",
    "more natural",
    "improves clarity",
    "sounds better",
    "correct form",
    "proper form",
}

CATEGORY_SIGNALS = {
    "articles_determiners": {"article", "determiner", "a", "an", "the", "noun", "plural", "singular", "countable"},
    "lexical_choice": {"collocation", "idiom", "word choice", "lexical", "phrase", "construction", "standard"},
    "prepositions": {"preposition", "collocation", "followed by", "governed", "object"},
    "pronouns": {"pronoun", "antecedent", "reference", "subject", "object"},
    "verb_form": {"verb", "tense", "aspect", "infinitive", "gerund", "participle", "auxiliary", "form"},
    "subject_verb_agreement": {"subject", "verb", "agreement", "plural", "singular"},
    "noun_number": {"noun", "plural", "singular", "countable", "number"},
}

SPECIFIC_ROLE_WORDS = {
    "subject",
    "head",
    "noun",
    "antecedent",
    "governor",
    "verb",
    "auxiliary",
    "determiner",
    "quantifier",
    "time",
    "tense",
    "object",
    "clause",
    "complement",
    "collocate",
}

GENERIC_EVIDENCE_ROLES = {"source", "target", "original", "modified_token", "context", "phrase"}

NECESSITY_WORDS = {
    "required",
    "requires",
    "must",
    "necessary",
    "grammatically correct",
    "corrects",
    "incorrect",
    "error",
    "standard",
    "proper",
}

HEDGING_WORDS = {
    "may",
    "optional",
    "stylistic",
    "acceptable",
    "alternative",
    "not necessary",
    "not required",
    "questionable",
    "invalid",
    "uncertain",
}


@dataclass(frozen=True)
class ScoreConfig:
    accept_threshold: float = 0.74
    refine_threshold: float = 0.56
    selector_threshold: float = 0.74


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def normalize(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "").lower()).strip()


def current_git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Empty CSV: {path}")
    candidate_ids = [row["candidate_id"] for row in rows]
    duplicates = [item for item, count in Counter(candidate_ids).items() if count > 1]
    if duplicates:
        raise ValueError(f"Duplicate candidate IDs in {path}: {duplicates[:5]}")
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], overwrite: bool) -> None:
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
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_evidence_spans(value: str) -> list[dict[str, Any]]:
    if not value.strip():
        return []
    data = json.loads(value)
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def category_signal(row: dict[str, str]) -> bool:
    text = normalize(" ".join([row.get("rule_text", ""), row.get("rationale", "")]))
    category = row.get("error_category", "")
    signals = CATEGORY_SIGNALS.get(category, set())
    return bool(signals and any(signal in text for signal in signals))


def grammar_signal(row: dict[str, str]) -> bool:
    text = normalize(" ".join([row.get("rule_text", ""), row.get("rationale", "")]))
    return any(keyword in text for keyword in GRAMMAR_KEYWORDS)


def text_in_source(text: str, source: str) -> bool:
    return bool(normalize(text) and normalize(text) in normalize(source))


def is_specific_role(role: str) -> bool:
    norm = normalize(role)
    if not norm or norm in GENERIC_EVIDENCE_ROLES:
        return False
    return any(word in norm for word in SPECIFIC_ROLE_WORDS)


def evidence_features(row: dict[str, str]) -> dict[str, Any]:
    source = row.get("source", "")
    source_text = normalize(row.get("source_text", ""))
    target_text = normalize(row.get("target_text", ""))
    quality_text = normalize(" ".join([row.get("rule_text", ""), row.get("rationale", "")]))
    spans = parse_evidence_spans(row.get("evidence_spans_json", ""))
    exact_source = 0
    specific = 0
    mentioned = 0
    for span in spans:
        text = str(span.get("text", ""))
        norm_text = normalize(text)
        if text_in_source(text, source):
            exact_source += 1
        if text_in_source(text, source) and is_specific_role(str(span.get("role", ""))) and norm_text not in {source_text, target_text}:
            specific += 1
            if norm_text and norm_text in quality_text:
                mentioned += 1
    return {
        "evidence_count": len(spans),
        "exact_source_evidence_count": exact_source,
        "specific_source_evidence_count": specific,
        "evidence_mentioned_count": mentioned,
    }


def operation_hit(row: dict[str, str], text: str) -> bool:
    op = normalize(row.get("operation", ""))
    normalized = normalize(text)
    if op and op in normalized:
        return True
    operation_words = {
        "replace": {"replace", "change", "substitute"},
        "insert": {"insert", "add"},
        "delete": {"delete", "remove", "omit"},
    }.get(op, set())
    return any(word in normalized for word in operation_words)


def edit_copy(row: dict[str, str], text: str) -> bool:
    normalized = normalize(text)
    source = normalize(row.get("source_text", ""))
    target = normalize(row.get("target_text", ""))
    if not operation_hit(row, text):
        return False
    source_hit = not source or source in normalized
    target_hit = row.get("operation") == "delete" or not target or target in normalized
    return source_hit and target_hit


def target_copy(row: dict[str, str], text: str) -> bool:
    target = normalize(row.get("target_text", ""))
    return bool(target and target in normalize(text))


def generic(row: dict[str, str]) -> bool:
    text = normalize(" ".join([row.get("rule_text", ""), row.get("rationale", "")]))
    if category_signal(row) or evidence_features(row)["specific_source_evidence_count"] > 0:
        return False
    return any(phrase in text for phrase in GENERIC_PHRASES)


def false_rationalization(row: dict[str, str]) -> bool:
    validity = normalize(row.get("edit_validity", ""))
    if validity not in {"invalid", "stylistic", "uncertain"}:
        return False
    text = normalize(" ".join([row.get("rule_text", ""), row.get("rationale", "")]))
    has_necessity = any(word in text for word in NECESSITY_WORDS)
    has_hedge = any(word in text for word in HEDGING_WORDS)
    return has_necessity and not has_hedge


def alignment_proxy(row: dict[str, str]) -> float:
    description = row.get("edit_description", "")
    score = 0.0
    if operation_hit(row, description):
        score += 0.34
    if normalize(row.get("source_text", "")) and normalize(row["source_text"]) in normalize(description):
        score += 0.33
    target = normalize(row.get("target_text", ""))
    if row.get("operation") == "delete" or not target or target in normalize(description):
        score += 0.33
    return min(score, 1.0)


def score_row(row: dict[str, str], config: ScoreConfig = ScoreConfig()) -> dict[str, Any]:
    evidence = evidence_features(row)
    rule_category = category_signal(row)
    rule_grammar = grammar_signal(row)
    rationale_edit_copy = edit_copy(row, row.get("rationale", ""))
    rule_target_copy = target_copy(row, row.get("rule_text", ""))
    rationale_target_copy = target_copy(row, row.get("rationale", ""))
    is_generic = generic(row)
    is_false_rationalization = false_rationalization(row)
    confidence = float(row.get("confidence") or 0.0)
    validity = normalize(row.get("edit_validity", ""))

    alignment_component = 0.16 * alignment_proxy(row)
    rule_component = 0.24 if rule_category else 0.14 if rule_grammar else 0.0
    evidence_component = min(
        0.25,
        0.08 * min(evidence["exact_source_evidence_count"], 1)
        + 0.11 * min(evidence["specific_source_evidence_count"], 1)
        + 0.06 * min(evidence["evidence_mentioned_count"], 1),
    )
    if validity in {"valid", "acceptable_alternative"}:
        validity_component = 0.10
    elif validity in {"invalid", "stylistic", "uncertain"} and not is_false_rationalization:
        validity_component = 0.07
    else:
        validity_component = 0.0
    specificity_component = 0.08 if not is_generic and len(normalize(row.get("rule_text", "")).split()) >= 5 else 0.0
    leakage_component = 0.12
    if rule_target_copy:
        leakage_component -= 0.05
    if rationale_target_copy:
        leakage_component -= 0.04
    if rationale_edit_copy:
        leakage_component -= 0.05
    leakage_component = max(0.0, leakage_component)
    confidence_component = 0.05 if confidence <= 0.9 or evidence["specific_source_evidence_count"] > 0 else 0.02
    penalty = 0.0
    if is_false_rationalization:
        penalty += 0.24
    if is_generic:
        penalty += 0.08
    if rule_target_copy and evidence["specific_source_evidence_count"] == 0:
        penalty += 0.05

    score = max(
        0.0,
        min(
            1.0,
            alignment_component
            + rule_component
            + evidence_component
            + validity_component
            + specificity_component
            + leakage_component
            + confidence_component
            - penalty,
        ),
    )
    if score >= config.accept_threshold and not is_false_rationalization:
        bucket = "accept"
    elif score >= config.refine_threshold:
        bucket = "refine"
    else:
        bucket = "reject"
    return {
        "rulefaith_score": round(score, 4),
        "rulefaith_bucket": bucket,
        "alignment_proxy": round(alignment_proxy(row), 4),
        "category_signal": rule_category,
        "grammar_signal": rule_grammar,
        "rationale_edit_copy": rationale_edit_copy,
        "rule_target_copy": rule_target_copy,
        "rationale_target_copy": rationale_target_copy,
        "generic": is_generic,
        "false_rationalization": is_false_rationalization,
        **evidence,
    }


def scored_rows(rows: list[dict[str, str]], config: ScoreConfig = ScoreConfig()) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        score = score_row(row, config)
        edit_group = row["candidate_id"].split("::")[0]
        candidate_style = "natural" if "::natural::" in row["candidate_id"] else "rule_grounded" if "::rule_grounded::" in row["candidate_id"] else "other"
        output.append(
            {
                "candidate_id": row["candidate_id"],
                "edit_group": edit_group,
                "candidate_style": candidate_style,
                "dataset": row.get("dataset", ""),
                "model_key": row.get("model_key", ""),
                "operation": row.get("operation", ""),
                "error_category": row.get("error_category", ""),
                "confidence": row.get("confidence", ""),
                "pseudo_overall_decision": row.get("validator_overall_decision", ""),
                "pseudo_rule_plausibility": row.get("validator_rule_plausibility", ""),
                "pseudo_evidence_sufficiency": row.get("validator_evidence_sufficiency", ""),
                **score,
            }
        )
    return output


def utility(label: str) -> float:
    return PSEUDO_UTILITY[label]


def group_by(rows: Iterable[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row[key])].append(row)
    return dict(groups)


def selection_summary(scored: list[dict[str, Any]], config: ScoreConfig = ScoreConfig()) -> dict[str, Any]:
    groups = group_by(scored, "edit_group")
    top1: list[dict[str, Any]] = []
    selective: list[dict[str, Any]] = []
    for rows in groups.values():
        selected = max(rows, key=lambda row: (float(row["rulefaith_score"]), -len(str(row["candidate_id"]))))
        top1.append(selected)
        if float(selected["rulefaith_score"]) >= config.selector_threshold and selected["rulefaith_bucket"] == "accept":
            selective.append(selected)

    def summarize_selected(name: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
        counts = Counter(row["pseudo_overall_decision"] for row in rows)
        n = len(rows)
        return {
            "strategy": name,
            "edit_groups": len(groups),
            "covered_groups": n,
            "coverage": round(n / len(groups), 4) if groups else 0.0,
            "accept_selected": counts["accept"],
            "refine_selected": counts["refine"],
            "reject_selected": counts["reject"],
            "accept_rate": round(counts["accept"] / n, 4) if n else 0.0,
            "non_reject_rate": round((counts["accept"] + counts["refine"]) / n, 4) if n else 0.0,
            "mean_utility": round(sum(utility(row["pseudo_overall_decision"]) for row in rows) / n, 4) if n else 0.0,
        }

    pairwise_total = 0
    pairwise_correct = 0.0
    for rows in groups.values():
        if len(rows) < 2:
            continue
        ordered = sorted(rows, key=lambda row: row["candidate_id"])
        for i in range(len(ordered)):
            for j in range(i + 1, len(ordered)):
                a, b = ordered[i], ordered[j]
                utility_delta = utility(a["pseudo_overall_decision"]) - utility(b["pseudo_overall_decision"])
                if utility_delta == 0:
                    continue
                score_delta = float(a["rulefaith_score"]) - float(b["rulefaith_score"])
                pairwise_total += 1
                if score_delta == 0:
                    pairwise_correct += 0.5
                elif (score_delta > 0 and utility_delta > 0) or (score_delta < 0 and utility_delta < 0):
                    pairwise_correct += 1.0

    by_pseudo: dict[str, dict[str, Any]] = {}
    for label, label_rows in group_by(scored, "pseudo_overall_decision").items():
        scores = [float(row["rulefaith_score"]) for row in label_rows]
        by_pseudo[label] = {
            "n": len(label_rows),
            "mean_score": round(sum(scores) / len(scores), 4),
            "min_score": round(min(scores), 4),
            "max_score": round(max(scores), 4),
            "bucket_counts": dict(Counter(row["rulefaith_bucket"] for row in label_rows)),
        }

    return {
        "candidate_count": len(scored),
        "edit_group_count": len(groups),
        "score_bucket_counts": dict(Counter(row["rulefaith_bucket"] for row in scored)),
        "pseudo_label_counts": dict(Counter(row["pseudo_overall_decision"] for row in scored)),
        "score_by_pseudo_label": by_pseudo,
        "top1_selection": summarize_selected("RuleFaith deployable score top-1", top1),
        "selective_selection": summarize_selected("RuleFaith deployable score selective", selective),
        "pairwise_accuracy": round(pairwise_correct / pairwise_total, 4) if pairwise_total else None,
        "pairwise_comparisons": pairwise_total,
    }


def metrics_csv_rows(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    top = metrics["top1_selection"]
    selective = metrics["selective_selection"]
    return [
        {
            "strategy": top["strategy"],
            "edit_groups": top["edit_groups"],
            "covered_groups": top["covered_groups"],
            "coverage": f"{top['coverage']:.3f}",
            "accept_rate": f"{top['accept_rate']:.3f}",
            "non_reject_rate": f"{top['non_reject_rate']:.3f}",
            "mean_utility": f"{top['mean_utility']:.3f}",
            "pairwise_accuracy": f"{metrics['pairwise_accuracy']:.3f}" if metrics["pairwise_accuracy"] is not None else "",
        },
        {
            "strategy": selective["strategy"],
            "edit_groups": selective["edit_groups"],
            "covered_groups": selective["covered_groups"],
            "coverage": f"{selective['coverage']:.3f}",
            "accept_rate": f"{selective['accept_rate']:.3f}",
            "non_reject_rate": f"{selective['non_reject_rate']:.3f}",
            "mean_utility": f"{selective['mean_utility']:.3f}",
            "pairwise_accuracy": f"{metrics['pairwise_accuracy']:.3f}" if metrics["pairwise_accuracy"] is not None else "",
        },
    ]


def write_tex(path: Path, metrics_rows: list[dict[str, Any]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Strategy & Cov. & Accept & Non-rej. & Utility \\\\",
        "\\midrule",
    ]
    for row in metrics_rows:
        strategy = str(row["strategy"]).replace("_", "\\_")
        lines.append(
            f"{strategy} & {row['coverage']} & {row['accept_rate']} & {row['non_reject_rate']} & {row['mean_utility']} \\\\"
        )
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\caption{Deployable RuleFaith scoring diagnostics on the 41-row Qwen3 ready pool. Labels are Codex/AI pseudo-validation for internal triage only.}",
            "\\label{tab:rulefaith-ready-deployable-selector}",
            "\\end{table}",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def markdown_cases(scored: list[dict[str, Any]], metrics: dict[str, Any]) -> str:
    high_reject = sorted(
        [row for row in scored if row["pseudo_overall_decision"] == "reject"],
        key=lambda row: float(row["rulefaith_score"]),
        reverse=True,
    )[:5]
    low_accept = sorted(
        [row for row in scored if row["pseudo_overall_decision"] == "accept"],
        key=lambda row: float(row["rulefaith_score"]),
    )[:5]
    false_rat = [row for row in scored if row["false_rationalization"]]

    def bullet(row: dict[str, Any]) -> str:
        return (
            f"- `{row['candidate_id']}` score={row['rulefaith_score']} bucket={row['rulefaith_bucket']} "
            f"pseudo={row['pseudo_overall_decision']} category={row['error_category']} "
            f"features: evidence={row['specific_source_evidence_count']}, target_copy={row['rationale_target_copy']}, "
            f"false_rat={row['false_rationalization']}"
        )

    lines = [
        "# RuleFaith Ready Candidate Deployable Selector Cases",
        "",
        "These cases use Codex/AI pseudo-validation only for diagnostic comparison. The deployable scorer does not use `validator_*` fields when assigning scores.",
        "",
        "## Metrics",
        "",
        f"- candidate count: `{metrics['candidate_count']}`",
        f"- edit groups: `{metrics['edit_group_count']}`",
        f"- score buckets: `{metrics['score_bucket_counts']}`",
        f"- top-1 selection: `{metrics['top1_selection']}`",
        f"- selective selection: `{metrics['selective_selection']}`",
        f"- pairwise accuracy: `{metrics['pairwise_accuracy']}` over `{metrics['pairwise_comparisons']}` comparisons",
        "",
        "## High-Scoring Pseudo-Rejects",
        "",
        *(bullet(row) for row in high_reject),
        "",
        "## Low-Scoring Pseudo-Accepts",
        "",
        *(bullet(row) for row in low_accept),
        "",
        "## False-Rationalization Flags",
        "",
    ]
    if false_rat:
        lines.extend(bullet(row) for row in false_rat[:10])
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def write_report(path: Path, metrics: dict[str, Any], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite")
    lines = [
        "# RuleFaith Loop P: Deployable Ready-Pool Selector",
        "",
        "## Status",
        "",
        "- Loop ID: P",
        "- Current bottleneck: previous selection result included a pseudo-validator upper bound but no deployable selector.",
        "- Hypothesis: a fixed RuleFaith feature scorer using edit alignment, rule signal, source evidence, leakage, specificity, and validity-risk features can improve over first-candidate and confidence heuristics without reading pseudo labels.",
        "- Required evidence: candidate-level scores, group-level top-1 selection, selective abstention, and pairwise ranking diagnostics against Codex/AI pseudo-validation for internal triage.",
        "- Success criterion: scorer is reproducible, does not use `validator_*` fields for scoring, and improves over first/highest-confidence baselines without hiding pseudo-label limitations.",
        "",
        "## Results",
        "",
        f"- score bucket counts: `{metrics['score_bucket_counts']}`",
        f"- top-1 selection: `{metrics['top1_selection']}`",
        f"- selective selection: `{metrics['selective_selection']}`",
        f"- pairwise accuracy: `{metrics['pairwise_accuracy']}` over `{metrics['pairwise_comparisons']}` comparable pairs",
        "- hypothesis status: `partially_supported_for_first_and_confidence_baselines_but_not_ready`",
        "- comparison boundary: top-1 improves over first/highest-confidence selectors from Loop O, but remains below the rule-grounded simple selector and should be revised before paper-quality claims.",
        "",
        "## Interpretation",
        "",
        "The deployable scorer is a method-pilot diagnostic. It can rank and abstain without reading pseudo labels, but the evaluation labels are still Codex/AI pseudo-validation. The current scorer is not strong enough to serve as a final selector: it beats first-candidate and highest-confidence heuristics but does not beat the rule-grounded candidate baseline, and its selective mode mostly improves non-reject rate rather than accept rate. This result is useful for engineering the RuleFaith selector and deciding which candidates require real-human validation; it is not final human evidence.",
        "",
        "## Artifacts",
        "",
        "- `results/rulefaith/rulefaith_ready_candidate_scores.csv`",
        "- `results/rulefaith/rulefaith_ready_selector_metrics.json`",
        "- `results/rulefaith/rulefaith_ready_selector_metrics.csv`",
        "- `results/rulefaith/rulefaith_ready_selector_cases.md`",
        "- `results/paper_assets/rulefaith_ready_selector_metrics.tex`",
        "",
        "## Provenance",
        "",
        f"- generated at: `{datetime.now(timezone.utc).isoformat()}`",
        f"- git commit at generation time: `{current_git_commit()}`",
        "",
        "## Next Highest-Priority Loop",
        "",
        "Use this scorer to construct a blinded natural-explanation comparison package; do not tune thresholds on the pseudo-validation labels.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score Qwen3 ready candidates with a deployable RuleFaith feature scorer.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--metrics-json", type=Path, default=DEFAULT_METRICS_JSON)
    parser.add_argument("--metrics-csv", type=Path, default=DEFAULT_METRICS_CSV)
    parser.add_argument("--cases-md", type=Path, default=DEFAULT_CASES_MD)
    parser.add_argument("--tex", type=Path, default=DEFAULT_TEX)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--accept-threshold", type=float, default=ScoreConfig.accept_threshold)
    parser.add_argument("--refine-threshold", type=float, default=ScoreConfig.refine_threshold)
    parser.add_argument("--selector-threshold", type=float, default=ScoreConfig.selector_threshold)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = ScoreConfig(
        accept_threshold=args.accept_threshold,
        refine_threshold=args.refine_threshold,
        selector_threshold=args.selector_threshold,
    )
    rows = read_csv(resolve(args.input))
    scored = scored_rows(rows, config)
    metrics = selection_summary(scored, config)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": current_git_commit(),
        "input": str(resolve(args.input)),
        "label_boundary": "Codex/AI pseudo-validation labels are diagnostic only and are not used by the scorer.",
        "config": {
            "accept_threshold": config.accept_threshold,
            "refine_threshold": config.refine_threshold,
            "selector_threshold": config.selector_threshold,
        },
        **metrics,
    }
    metrics_rows = metrics_csv_rows(metrics)
    write_csv(resolve(args.output_csv), scored, args.overwrite)
    write_json(resolve(args.metrics_json), payload, args.overwrite)
    write_csv(resolve(args.metrics_csv), metrics_rows, args.overwrite)
    write_tex(resolve(args.tex), metrics_rows, args.overwrite)
    resolve(args.cases_md).parent.mkdir(parents=True, exist_ok=True)
    if resolve(args.cases_md).exists() and not args.overwrite:
        raise FileExistsError(f"{resolve(args.cases_md)} exists; pass --overwrite")
    resolve(args.cases_md).write_text(markdown_cases(scored, metrics), encoding="utf-8")
    write_report(resolve(args.report), metrics, args.overwrite)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
