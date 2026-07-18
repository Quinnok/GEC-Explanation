from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = ROOT / "data" / "faithfulness_benchmark"


RULE_HINTS = {
    "VERB": "Use the verb form required by the subject and tense.",
    "NOUN": "Use the noun number or noun form required by the sentence.",
    "DET": "Use an article or determiner licensed by the noun phrase.",
    "PREP": "Use the preposition required by the surrounding phrase.",
    "PRON": "Use a pronoun form that matches its grammatical role or antecedent.",
    "ORTH": "Correct spelling, casing, spacing, or another orthographic form.",
    "PUNCT": "Use punctuation that matches the sentence structure.",
    "WO": "Use the word order required by the sentence.",
    "MORPH": "Use the correct morphological form.",
}


WRONG_TYPES = ["R:VERB:SVA", "R:NOUN:NUM", "R:DET", "R:PREP", "R:ORTH", "R:PUNCT"]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def split_for(row: Dict[str, Any]) -> str:
    key = f"{row.get('dataset')}::{row.get('sample_id')}::{row.get('source')}"
    bucket = int(hashlib.sha1(key.encode("utf-8")).hexdigest(), 16) % 10
    if bucket < 7:
        return "train"
    if bucket < 8:
        return "dev"
    return "test"


def canonical_edit_id(row: Dict[str, Any], index: int) -> str:
    edit = row["predicted_edit"]
    dataset = row.get("dataset", "UNKNOWN")
    model_key = row.get("model_key", "model")
    return f"{dataset}::{row['sample_id']}::{model_key}::{index:05d}::{edit['start']}-{edit['end']}::{edit['operation']}"


def edit_text(edit: Dict[str, Any]) -> str:
    op = edit["operation"]
    src = edit.get("source_text", "")
    tgt = edit.get("target_text", "")
    if op == "replace":
        return f'replace "{src}" with "{tgt}"'
    if op == "insert":
        return f'insert "{tgt}"'
    if op == "delete":
        return f'delete "{src}"'
    return f"{op} {src} {tgt}".strip()


def type_rule(error_type: str) -> str:
    for key, hint in RULE_HINTS.items():
        if key in error_type:
            return hint
    return "Apply the grammar rule indicated by the local context."


def masked(text: str, target: str) -> str:
    if not target:
        return text
    return text.replace(f'"{target}"', '"[MASK]"').replace(target, "[MASK]", 1)


def wrong_target(edit: Dict[str, Any]) -> str:
    tgt = edit.get("target_text", "")
    if tgt.lower() != "the":
        return "the"
    return "a"


def wrong_operation(edit: Dict[str, Any]) -> str:
    return {"replace": "insert", "insert": "delete", "delete": "replace"}.get(edit["operation"], "replace")


def wrong_type(error_type: str) -> str:
    for candidate in WRONG_TYPES:
        if candidate != error_type:
            return candidate
    return "R:OTHER"


def source_token(row: Dict[str, Any], offset: int = 1) -> str:
    tokens = row["source"].split()
    if not tokens:
        return "token"
    edit = row["predicted_edit"]
    idx = min(max(int(edit["start"]) + offset, 0), len(tokens) - 1)
    return tokens[idx]


def load_flan_candidates(paths: List[Path]) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for path in paths:
        for row in read_jsonl(path):
            edit = row.get("predicted_edit", {})
            key = f"{row.get('sample_id')}::{row.get('model_key')}::{edit.get('start')}::{edit.get('end')}::{edit.get('operation')}::{edit.get('target_text')}"
            explanation = row.get("open_source_explanation_candidate", "")
            if explanation:
                mapping[key] = explanation
    return mapping


def flan_for(row: Dict[str, Any], candidates: Dict[str, str]) -> Optional[str]:
    edit = row["predicted_edit"]
    key = f"{row.get('sample_id')}::{row.get('model_key')}::{edit.get('start')}::{edit.get('end')}::{edit.get('operation')}::{edit.get('target_text')}"
    return candidates.get(key)


def explanation_rows(row: Dict[str, Any], edit_id: str, flan_text: Optional[str], swap_pool: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    edit = row["predicted_edit"]
    error_type = row["error_type"]
    explicit = f'This edit should {edit_text(edit)} at source span [{edit["start"]},{edit["end"]}) for {error_type}.'
    rule = type_rule(error_type)
    rule_only = f"{rule} The explanation intentionally omits the target edit."
    gee_style = f"The phrase near span [{edit['start']},{edit['end']}) violates {error_type}; {rule.lower()}"
    rule_grounded = f"{rule} In this sentence, the evidence is around \"{source_token(row, 0)}\"."
    wrong_tgt = wrong_target(edit)
    wrong_op = wrong_operation(edit)
    wrong_et = wrong_type(error_type)
    swap = next((item for item in swap_pool if item is not row and item.get("sample_id") != row.get("sample_id")), None)
    swap_text = (
        f'This edit should {edit_text(swap["predicted_edit"])} for {swap["error_type"]}.'
        if swap
        else "This explanation was swapped from another edit."
    )
    rows = [
        ("explicit_template", explicit, "faithful_positive", False, "leakage_upper_control"),
        ("masked_target_template", masked(explicit, edit.get("target_text", "")), "faithful_positive_masked", False, "target_mask_control"),
        ("rule_only", rule_only, "partially_informative_positive", False, "automatic_rule_template"),
        ("gee_style_automatic", gee_style, "faithful_candidate", False, "automatic_gee_style_template"),
        ("rule_grounded_automatic", rule_grounded, "faithful_candidate", False, "automatic_rule_grounded_template"),
        ("wrong_span", f'The edit applies to source span [{edit["start"] + 1},{edit["end"] + 1}).', "negative", True, "wrong_span"),
        ("wrong_source_token", f'The error is caused by the token "{source_token(row, 1)}".', "negative", True, "wrong_source_token"),
        ("wrong_target", f'This edit should {edit["operation"]} "{wrong_tgt}".', "negative", True, "wrong_target"),
        ("wrong_operation", f'This edit should {wrong_op} the relevant phrase.', "negative", True, "wrong_operation"),
        ("wrong_direction", f'The sentence should change from "{edit.get("target_text", "")}" back to "{edit.get("source_text", "")}".', "negative", True, "wrong_direction"),
        ("wrong_error_type", f"This correction fixes {wrong_et}, not {error_type}.", "negative", True, "wrong_error_type"),
        ("wrong_rule", "Use a comma because every grammar error here is punctuation-related.", "negative", True, "wrong_rule"),
        ("wrong_evidence", f'The evidence is the unrelated token "{source_token(row, 2)}".', "negative", True, "wrong_evidence"),
        ("swapped_across_sentence", swap_text, "negative", True, "swapped_across_sentence"),
        ("generic", "The sentence has a grammar issue and should be improved.", "negative", True, "generic"),
        ("partially_correct", f"The explanation identifies {error_type} but does not identify the edit target.", "negative_partial", True, "partially_correct"),
        ("counterfactually_inconsistent_seed", "This same edit should always be made even if the grammatical condition changes.", "pending_counterfactual_label", True, "counterfactual_inconsistent_pending"),
    ]
    if flan_text:
        rows.append(("flan_t5_candidate", flan_text, "candidate_not_gold", False, "open_source_generation"))
    if row["behavior"] in {"wrong_correction", "overcorrection"}:
        rows.append(
            (
                "faithful_wrong_model_edit",
                f"The model actually decided to {edit_text(edit)}, regardless of whether the correction is grammatically valid.",
                "faithful_to_model_behavior_not_grammar_gold",
                False,
                "behavior_faithfulness_positive",
            )
        )
    return [
        {
            "instance_id": f"{edit_id}::{kind}",
            "edit_id": edit_id,
            "sample_id": row["sample_id"],
            "dataset": row.get("dataset", "UNKNOWN"),
            "split": split_for(row),
            "model_key": row["model_key"],
            "model_family": row.get("model_family", "unknown"),
            "behavior": row["behavior"],
            "error_type": error_type,
            "explanation_type": kind,
            "explanation": text,
            "label": label,
            "is_negative": is_negative,
            "negative_type": negative_type if is_negative else None,
            "is_human_gold": False,
            "label_source": "automatic_construction_not_human_gold",
            "template_family": negative_type,
        }
        for kind, text, label, is_negative, negative_type in rows
    ]


def read_with_dataset(path: Path) -> List[Dict[str, Any]]:
    rows = read_jsonl(path)
    inferred = "JFLEG" if "jfleg" in str(path).lower() else "EXPECT"
    for row in rows:
        row.setdefault("dataset", inferred)
    return rows


def select_edits(rows: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    buckets: Dict[tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[(row.get("dataset", "UNKNOWN"), row.get("model_key", "model"))].append(row)
    selected: List[Dict[str, Any]] = []
    seen_ids: set[int] = set()
    per_bucket = max(1, limit // max(1, len(buckets)))
    for key in sorted(buckets):
        for row in buckets[key][:per_bucket]:
            selected.append(row)
            seen_ids.add(id(row))
    for row in rows:
        if len(selected) >= limit:
            break
        if id(row) not in seen_ids:
            selected.append(row)
            seen_ids.add(id(row))
    return selected[:limit]


def build(args: argparse.Namespace) -> None:
    edit_rows: List[Dict[str, Any]] = []
    for path in args.edit_files:
        edit_rows.extend(read_with_dataset(path))
    if len(edit_rows) < args.min_edits:
        raise SystemExit(f"Need at least {args.min_edits} model-produced edits, found {len(edit_rows)}")
    selected = select_edits(edit_rows, args.max_edits)
    flan_candidates = load_flan_candidates(args.explanation_files)
    indexed_edits = []
    instances = []
    for idx, row in enumerate(selected):
        edit_id = canonical_edit_id(row, idx)
        row = dict(row)
        row["edit_id"] = edit_id
        row["split"] = split_for(row)
        row["is_human_gold"] = False
        row["label_source"] = "ERRANT_alignment_automatic"
        indexed_edits.append(row)
    for row in indexed_edits:
        instances.extend(explanation_rows(row, row["edit_id"], flan_for(row, flan_candidates), indexed_edits))

    missing_rows: List[Dict[str, Any]] = []
    for path in args.missing_files:
        missing_rows.extend(read_with_dataset(path))
    missing_rows = missing_rows[: args.max_missing]
    for idx, row in enumerate(missing_rows):
        row["diagnosis_id"] = f"{row.get('dataset', 'UNKNOWN')}::{row['sample_id']}::{row['model_key']}::missing::{idx:05d}"
        row["split"] = split_for(row)
        row["is_human_gold"] = False
        row["label_source"] = "ERRANT_alignment_automatic"

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "edit_records.jsonl", indexed_edits)
    write_jsonl(args.out_dir / "explanation_instances.jsonl", instances)
    write_jsonl(args.out_dir / "missing_edit_diagnosis.jsonl", missing_rows)
    stats = {
        "created_at": utc_now(),
        "edit_count": len(indexed_edits),
        "missing_edit_count": len(missing_rows),
        "explanation_instance_count": len(instances),
        "dataset_counts": dict(Counter(row.get("dataset", "UNKNOWN") for row in indexed_edits)),
        "model_counts": dict(Counter(row["model_key"] for row in indexed_edits)),
        "model_family_counts": dict(Counter(row.get("model_family", "unknown") for row in indexed_edits)),
        "behavior_counts": dict(Counter(row["behavior"] for row in indexed_edits)),
        "operation_counts": dict(Counter(row["predicted_edit"]["operation"] for row in indexed_edits)),
        "error_type_counts": dict(Counter(row["error_type"] for row in indexed_edits)),
        "error_type_count": len({row["error_type"] for row in indexed_edits}),
        "split_counts": dict(Counter(row["split"] for row in indexed_edits)),
        "explanation_type_counts": dict(Counter(row["explanation_type"] for row in instances)),
        "negative_type_counts": dict(Counter(row["negative_type"] for row in instances if row["is_negative"])),
        "human_gold_count": 0,
        "important_note": "All labels are automatic. Generated/template explanations are not human gold. Explicit templates are leakage upper controls.",
    }
    write_json(args.out_dir / "benchmark_stats.json", stats)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Round 07 faithfulness benchmark.")
    parser.add_argument("--edit-files", type=Path, nargs="+", required=True)
    parser.add_argument("--missing-files", type=Path, nargs="+", default=[])
    parser.add_argument("--explanation-files", type=Path, nargs="+", default=[])
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--min-edits", type=int, default=500)
    parser.add_argument("--max-edits", type=int, default=700)
    parser.add_argument("--max-missing", type=int, default=160)
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
