from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from baselines import structured_explicit_edit_baseline, surface_keyword_predict
from edit_schema import Edit, compare_edits


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BENCHMARK_DIR = ROOT / "data" / "faithfulness_benchmark"
DEFAULT_OUT_DIR = ROOT / "results" / "round08"

POSITIVE_LABELS = {
    "faithful_positive",
    "faithful_positive_masked",
    "partially_informative_positive",
    "faithful_candidate",
    "faithful_to_model_behavior_not_grammar_gold",
}
NEGATIVE_LABELS = {"negative", "negative_partial"}
SKIP_LABELS = {"candidate_not_gold", "pending_counterfactual_label"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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


def label_to_bool(label: str) -> Optional[bool]:
    if label in POSITIVE_LABELS:
        return True
    if label in NEGATIVE_LABELS:
        return False
    if label in SKIP_LABELS:
        return None
    return None


def stable_random_bool(key: str) -> bool:
    bucket = int(hashlib.sha1(key.encode("utf-8")).hexdigest(), 16) % 2
    return bool(bucket)


def canonical_template(edit: Edit, error_type: str) -> str:
    if edit.operation == "replace":
        action = f'replace "{edit.source_text}" with "{edit.target_text}"'
    elif edit.operation == "insert":
        action = f'insert "{edit.target_text}"'
    elif edit.operation == "delete":
        action = f'delete "{edit.source_text}"'
    else:
        action = edit.operation
    return f"The correction should {action} because it fixes {error_type}."


def mask_target(explanation: str, edit: Edit) -> str:
    if not edit.target_text:
        return explanation
    escaped = re.escape(edit.target_text)
    return re.sub(escaped, "[MASK]", explanation, count=1, flags=re.IGNORECASE)


def direct_leak_features(explanation: str, edit: Edit) -> Dict[str, bool]:
    text = explanation.lower()
    return {
        "operation": edit.operation.lower() in text,
        "source": (not edit.source_text) or edit.source_text.lower() in text,
        "target": (not edit.target_text) or edit.target_text.lower() in text,
        "type": edit.error_type.lower() in text,
        "span": bool(re.search(r"\[\s*\d+\s*,\s*\d+\s*\)", explanation)),
    }


def parsed_edit(source: str, explanation: str, default_error_type: str) -> Optional[Edit]:
    return structured_explicit_edit_baseline(source, explanation, error_type=default_error_type)


def edit_exact(source: str, explanation: str, gold: Edit, default_error_type: str) -> Tuple[bool, Optional[Edit]]:
    pred = parsed_edit(source, explanation, default_error_type)
    if pred is None:
        return False, None
    return bool(compare_edits(pred, gold)["full_edit_exact"]), pred


def surface_keyword(example: Dict[str, Any]) -> bool:
    return surface_keyword_predict(example["edit"], example["explanation"])


def structured_extraction(example: Dict[str, Any]) -> bool:
    ok, _ = edit_exact(example["source"], example["explanation"], example["edit"], example["error_type"])
    return ok


def reverse_reconstruction(example: Dict[str, Any]) -> bool:
    ok, pred = edit_exact(example["source"], example["explanation"], example["edit"], example["error_type"])
    if ok:
        return True
    if pred is not None:
        scores = compare_edits(pred, example["edit"])
        return scores["span_f1"] >= 0.5 and scores["operation_accuracy"] == 1.0 and scores["target_text_match"] == 1.0
    return surface_keyword(example)


def target_masked_reconstruction(example: Dict[str, Any]) -> bool:
    masked = dict(example)
    masked["explanation"] = mask_target(example["explanation"], example["edit"])
    ok, _ = edit_exact(masked["source"], masked["explanation"], masked["edit"], masked["error_type"])
    return ok


def no_source_reconstruction(example: Dict[str, Any]) -> bool:
    ok, _ = edit_exact("", example["explanation"], example["edit"], example["error_type"])
    return ok


def no_rule_verifier(example: Dict[str, Any]) -> bool:
    text = example["explanation"].lower()
    if "unrelated token" in text or "grammar issue and should be improved" in text:
        return False
    source_hit = bool(example["edit"].source_text and example["edit"].source_text.lower() in text)
    target_hit = bool(example["edit"].target_text and example["edit"].target_text.lower() in text)
    operation_hit = example["edit"].operation.lower() in text
    return operation_hit or source_hit or target_hit


def no_evidence_verifier(example: Dict[str, Any]) -> bool:
    text = example["explanation"].lower()
    if "every grammar error here is punctuation-related" in text and "PUNCT" not in example["error_type"]:
        return False
    if "fixes " in text:
        mentioned_types = re.findall(r"[MRU]:[A-Z0-9_:]+", example["explanation"])
        if mentioned_types and example["error_type"] not in mentioned_types:
            return False
    type_key = next((key for key in RULE_KEYWORDS if key in example["error_type"]), "")
    if not type_key:
        return example["error_type"].lower() in text
    return any(keyword in text for keyword in RULE_KEYWORDS[type_key]) or example["error_type"].lower() in text


def current_edit_only(example: Dict[str, Any]) -> bool:
    return example["edit"].operation in {"replace", "insert", "delete"}


def leakage_adjusted_reconstruction(example: Dict[str, Any]) -> bool:
    if not reverse_reconstruction(example):
        return False
    leaks = direct_leak_features(example["explanation"], example["edit"])
    direct_answer = leaks["operation"] and leaks["source"] and leaks["target"] and (leaks["type"] or leaks["span"])
    return not direct_answer


def nli_proxy(example: Dict[str, Any]) -> bool:
    text = example["explanation"].lower()
    contradiction_markers = [
        "back to",
        "not ",
        "wrong",
        "unrelated",
        "every grammar error",
        "always be made",
    ]
    if any(marker in text for marker in contradiction_markers):
        return False
    if "grammar issue" in text and "should be improved" in text and len(text.split()) < 12:
        return False
    leaks = direct_leak_features(example["explanation"], example["edit"])
    return leaks["type"] or leaks["operation"] or any(word in text for word in ["rule", "span", "evidence", "phrase"])


RULE_KEYWORDS = {
    "VERB": ["verb", "tense", "subject"],
    "NOUN": ["noun", "number", "count"],
    "DET": ["article", "determiner", "noun phrase"],
    "PREP": ["preposition", "phrase"],
    "PRON": ["pronoun", "antecedent"],
    "ORTH": ["spelling", "casing", "spacing", "orthographic"],
    "PUNCT": ["punctuation", "comma"],
    "WO": ["word order"],
    "MORPH": ["morphological", "form"],
}


def rule_evidence_verifier(example: Dict[str, Any]) -> bool:
    text = example["explanation"].lower()
    if "grammar issue and should be improved" in text:
        return False
    if "every grammar error here is punctuation-related" in text and "PUNCT" not in example["error_type"]:
        return False
    if "unrelated token" in text:
        return False
    if "fixes " in text:
        mentioned_types = re.findall(r"[MRU]:[A-Z0-9_:]+", example["explanation"])
        if mentioned_types and example["error_type"] not in mentioned_types:
            return False
    type_key = next((key for key in RULE_KEYWORDS if key in example["error_type"]), "")
    if not type_key:
        return surface_keyword(example)
    keyword_hit = any(keyword in text for keyword in RULE_KEYWORDS[type_key])
    source_hit = bool(example["edit"].source_text and example["edit"].source_text.lower() in text)
    target_hit = bool(example["edit"].target_text and example["edit"].target_text.lower() in text)
    return keyword_hit or source_hit or target_hit


def confusion(predictions: List[Tuple[bool, bool]]) -> Dict[str, float]:
    tp = sum(1 for pred, gold in predictions if pred and gold)
    tn = sum(1 for pred, gold in predictions if not pred and not gold)
    fp = sum(1 for pred, gold in predictions if pred and not gold)
    fn = sum(1 for pred, gold in predictions if not pred and gold)
    total = len(predictions)
    pos_precision = tp / (tp + fp) if tp + fp else 0.0
    pos_recall = tp / (tp + fn) if tp + fn else 0.0
    pos_f1 = 0.0 if pos_precision + pos_recall == 0 else 2 * pos_precision * pos_recall / (pos_precision + pos_recall)
    neg_precision = tn / (tn + fn) if tn + fn else 0.0
    neg_recall = tn / (tn + fp) if tn + fp else 0.0
    neg_f1 = 0.0 if neg_precision + neg_recall == 0 else 2 * neg_precision * neg_recall / (neg_precision + neg_recall)
    return {
        "n": total,
        "accuracy": (tp + tn) / total if total else 0.0,
        "positive_precision": pos_precision,
        "positive_recall": pos_recall,
        "positive_f1": pos_f1,
        "negative_precision": neg_precision,
        "negative_recall": neg_recall,
        "negative_f1": neg_f1,
        "macro_f1": (pos_f1 + neg_f1) / 2,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


def average_metric_dict(rows: List[Dict[str, float]]) -> Dict[str, float]:
    if not rows:
        return {}
    keys = sorted(rows[0].keys())
    return {key: sum(row[key] for row in rows) / len(rows) for key in keys}


def fit_tfidf(train_examples: List[Dict[str, Any]]) -> Tuple[TfidfVectorizer, float]:
    texts = []
    labels = []
    for example in train_examples:
        texts.append(example["explanation"])
        texts.append(canonical_template(example["edit"], example["error_type"]))
        labels.append(example["gold_label"])
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    vectorizer.fit(texts)
    candidates = [round(value, 2) for value in [i / 100 for i in range(5, 96, 5)]]
    scored = []
    for threshold in candidates:
        preds = [(tfidf_predict(example, vectorizer, threshold), example["gold_label"]) for example in train_examples]
        scored.append((confusion(preds)["macro_f1"], threshold))
    scored.sort(reverse=True)
    return vectorizer, scored[0][1]


def tfidf_predict(example: Dict[str, Any], vectorizer: TfidfVectorizer, threshold: float) -> bool:
    query = vectorizer.transform([example["explanation"]])
    template = vectorizer.transform([canonical_template(example["edit"], example["error_type"])])
    score = float(cosine_similarity(query, template)[0, 0])
    return score >= threshold


def build_examples(edit_rows: List[Dict[str, Any]], explanation_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    edits = {row["edit_id"]: row for row in edit_rows}
    examples = []
    for row in explanation_rows:
        gold = label_to_bool(row["label"])
        if gold is None:
            continue
        edit_record = edits[row["edit_id"]]
        edit = Edit.from_dict(edit_record["predicted_edit"])
        edit = Edit(edit.start, edit.end, edit.source_text, edit.target_text, edit.operation, row["error_type"])
        examples.append(
            {
                "instance_id": row["instance_id"],
                "edit_id": row["edit_id"],
                "sample_id": row["sample_id"],
                "dataset": row["dataset"],
                "split": row["split"],
                "model_key": row["model_key"],
                "model_family": row["model_family"],
                "behavior": row["behavior"],
                "error_type": row["error_type"],
                "explanation_type": row["explanation_type"],
                "negative_type": row["negative_type"],
                "label": row["label"],
                "gold_label": gold,
                "source": edit_record["source"],
                "prediction": edit_record["prediction"],
                "edit": edit,
                "explanation": row["explanation"],
            }
        )
    return examples


def evaluate(args: argparse.Namespace) -> None:
    edit_rows = read_jsonl(args.benchmark_dir / "edit_records.jsonl")
    explanation_rows = read_jsonl(args.benchmark_dir / "explanation_instances.jsonl")
    examples = build_examples(edit_rows, explanation_rows)
    train_examples = [item for item in examples if item["split"] == "train"]
    tfidf_vectorizer, tfidf_threshold = fit_tfidf(train_examples)
    train_majority = Counter(item["gold_label"] for item in train_examples).most_common(1)[0][0]

    methods: Dict[str, Callable[[Dict[str, Any]], bool]] = {
        "random": lambda ex: stable_random_bool(ex["instance_id"]),
        "majority_train": lambda ex: train_majority,
        "no_explanation_majority": lambda ex: train_majority,
        "current_edit_only": current_edit_only,
        "surface_keyword": surface_keyword,
        "structured_explicit_extraction": structured_extraction,
        "reverse_reconstruction": reverse_reconstruction,
        "no_source_reconstruction": no_source_reconstruction,
        "target_masked_reconstruction": target_masked_reconstruction,
        "leakage_adjusted_reconstruction": leakage_adjusted_reconstruction,
        "tfidf_embedding_similarity": lambda ex: tfidf_predict(ex, tfidf_vectorizer, tfidf_threshold),
        "nli_lexical_proxy": nli_proxy,
        "rule_evidence_verifier": rule_evidence_verifier,
        "no_rule_verifier": no_rule_verifier,
        "no_evidence_verifier": no_evidence_verifier,
    }

    detailed = []
    method_pairs: Dict[str, List[Tuple[bool, bool]]] = defaultdict(list)
    method_pairs_by_type: Dict[str, Dict[str, List[Tuple[bool, bool]]]] = defaultdict(lambda: defaultdict(list))
    reconstruction_metrics: Dict[str, List[Dict[str, float]]] = defaultdict(list)

    for example in examples:
        for method, fn in methods.items():
            pred = bool(fn(example))
            gold = bool(example["gold_label"])
            method_pairs[method].append((pred, gold))
            method_pairs_by_type[method][example["explanation_type"]].append((pred, gold))
            if method in {
                "structured_explicit_extraction",
                "reverse_reconstruction",
                "no_source_reconstruction",
                "target_masked_reconstruction",
                "leakage_adjusted_reconstruction",
            }:
                explanation = example["explanation"]
                if method == "target_masked_reconstruction":
                    explanation = mask_target(explanation, example["edit"])
                source = "" if method == "no_source_reconstruction" else example["source"]
                parsed = parsed_edit(source, explanation, example["error_type"])
                if parsed is None or (method == "leakage_adjusted_reconstruction" and not pred):
                    reconstruction_metrics[method].append(
                        {
                            "span_exact": 0.0,
                            "span_precision": 0.0,
                            "span_recall": 0.0,
                            "span_f1": 0.0,
                            "source_text_match": 0.0,
                            "target_text_match": 0.0,
                            "operation_accuracy": 0.0,
                            "error_type_accuracy": 0.0,
                            "full_edit_exact": 0.0,
                        }
                    )
                else:
                    reconstruction_metrics[method].append(compare_edits(parsed, example["edit"]))
            detailed.append(
                {
                    "instance_id": example["instance_id"],
                    "edit_id": example["edit_id"],
                    "split": example["split"],
                    "dataset": example["dataset"],
                    "model_key": example["model_key"],
                    "behavior": example["behavior"],
                    "error_type": example["error_type"],
                    "explanation_type": example["explanation_type"],
                    "negative_type": example["negative_type"],
                    "label": example["label"],
                    "gold_label": gold,
                    "method": method,
                    "prediction": pred,
                    "direct_leak_features": direct_leak_features(example["explanation"], example["edit"]),
                }
            )

    metrics = {
        "created_at": utc_now(),
        "example_count": len(examples),
        "skipped_label_counts": dict(Counter(row["label"] for row in explanation_rows if label_to_bool(row["label"]) is None)),
        "positive_label_counts": dict(Counter(item["label"] for item in examples if item["gold_label"])),
        "negative_label_counts": dict(Counter(item["label"] for item in examples if not item["gold_label"])),
        "tfidf_threshold": tfidf_threshold,
        "train_majority_label": train_majority,
        "method_metrics": {method: confusion(pairs) for method, pairs in method_pairs.items()},
        "method_by_explanation_type": {
            method: {etype: confusion(pairs) for etype, pairs in type_map.items()}
            for method, type_map in method_pairs_by_type.items()
        },
        "reconstruction_metrics": {
            method: average_metric_dict(rows)
            for method, rows in reconstruction_metrics.items()
        },
    }

    negative_rejection: Dict[str, Dict[str, float]] = {}
    for method in methods:
        by_negative_type: Dict[str, List[bool]] = defaultdict(list)
        for row in detailed:
            if row["method"] == method and row["negative_type"] and not row["gold_label"]:
                by_negative_type[row["negative_type"]].append(not row["prediction"])
        negative_rejection[method] = {
            key: sum(values) / len(values) if values else math.nan
            for key, values in sorted(by_negative_type.items())
        }
    metrics["negative_rejection_rates"] = negative_rejection

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.out_dir / "l1_method_metrics.json", metrics)
    write_jsonl(args.out_dir / "l1_detailed_predictions.jsonl", detailed)
    with (args.out_dir / "l1_condition_metrics.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["method", "explanation_type", "n", "accuracy", "macro_f1", "positive_f1", "negative_f1"])
        writer.writeheader()
        for method, type_map in metrics["method_by_explanation_type"].items():
            for etype, result in type_map.items():
                writer.writerow(
                    {
                        "method": method,
                        "explanation_type": etype,
                        "n": result["n"],
                        "accuracy": result["accuracy"],
                        "macro_f1": result["macro_f1"],
                        "positive_f1": result["positive_f1"],
                        "negative_f1": result["negative_f1"],
                    }
                )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Round 08 L1/L3 faithfulness methods on benchmark instances.")
    parser.add_argument("--benchmark-dir", type=Path, default=DEFAULT_BENCHMARK_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


if __name__ == "__main__":
    evaluate(parse_args())
