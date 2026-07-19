from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "faithfulness_benchmark" / "edit_records.jsonl"
OUT_DIR = ROOT / "data" / "rulefaith"
RESULTS_DIR = ROOT / "results" / "rulefaith"
DOCS_CARD = ROOT / "docs" / "rulefaith_edit_pool_card.md"

MODEL_TARGETS = {
    "gector_roberta_base": 120,
    "t5_base_grammar": 120,
    "coedit_large": 60,
}
MODEL_MINIMUMS = {
    "gector_roberta_base": 100,
    "t5_base_grammar": 100,
    "coedit_large": 50,
}

PUNCT_CHARS = set(".,;:!?()[]{}\"'`")


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalize_alnum(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "", text).lower()


def normalize_for_duplicate(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def stable_hash(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:12], 16)


def error_category(error_type: str) -> str:
    et = error_type.upper()
    if "VERB:SVA" in et:
        return "subject_verb_agreement"
    if "VERB:TENSE" in et:
        return "verb_tense"
    if "VERB:FORM" in et or et.endswith(":VERB") or et == "R:VERB" or et == "M:VERB" or et == "U:VERB":
        return "verb_form"
    if ":DET" in et or et.endswith("DET"):
        return "articles_determiners"
    if "NOUN:NUM" in et:
        return "noun_number"
    if "PREP" in et:
        return "prepositions"
    if "PRON" in et:
        return "pronouns"
    if "WO" in et:
        return "word_order"
    if "PUNCT" in et:
        return "punctuation"
    if "SPELL" in et or "ORTH" in et or "MORPH" in et:
        return "spelling_orthography"
    if "CONJ" in et or "PART" in et or "CONTR" in et:
        return "clause_structure"
    if "OTHER" in et or "NOUN" in et or "ADJ" in et or "ADV" in et:
        return "lexical_choice"
    return "other"


def is_detokenization_artifact(row: Dict[str, Any]) -> Tuple[bool, str]:
    edit = row["predicted_edit"]
    src = edit.get("source_text", "")
    tgt = edit.get("target_text", "")
    et = row.get("error_type", "")
    op = edit.get("operation", "")
    if not src and not tgt:
        return True, "empty_source_and_target"
    if src.strip().lower() == tgt.strip().lower() and src.strip() != tgt.strip():
        return True, "case_or_whitespace_only"
    if "PUNCT" in et or et in {"R:ORTH", "M:ORTH", "U:ORTH"}:
        if normalize_alnum(src) == normalize_alnum(tgt):
            return True, "punctuation_or_spacing_only"
    if op == "replace":
        src_chars = set(src.strip())
        tgt_chars = set(tgt.strip())
        if src_chars and tgt_chars and src_chars <= PUNCT_CHARS and tgt_chars <= PUNCT_CHARS:
            return True, "punctuation_symbol_swap"
    return False, ""


def enrich(row: Dict[str, Any], source_path: str) -> Dict[str, Any]:
    edit = row["predicted_edit"]
    noisy, reason = is_detokenization_artifact(row)
    out = dict(row)
    out["source_artifact"] = source_path
    out["operation"] = edit.get("operation", "")
    out["edit_start"] = edit.get("start")
    out["edit_end"] = edit.get("end")
    out["source_text"] = edit.get("source_text", "")
    out["target_text"] = edit.get("target_text", "")
    out["error_category"] = error_category(row.get("error_type", ""))
    out["detokenization_artifact"] = noisy
    out["artifact_reason"] = reason
    out["source_key"] = f"{row.get('dataset')}::{row.get('sample_id')}"
    out["target_key"] = normalize_for_duplicate(out["target_text"])
    out["source_norm"] = normalize_for_duplicate(row.get("source", ""))
    out["edit_key"] = "::".join(
        [
            out["source_key"],
            row.get("model_key", ""),
            str(out["edit_start"]),
            str(out["edit_end"]),
            out["operation"],
            normalize_for_duplicate(out["source_text"]),
            normalize_for_duplicate(out["target_text"]),
        ]
    )
    return out


def load_records(paths: List[Path]) -> List[Dict[str, Any]]:
    seen = set()
    rows: List[Dict[str, Any]] = []
    for path in paths:
        if not path.exists():
            continue
        for row in read_jsonl(path):
            enriched = enrich(row, str(path.relative_to(ROOT)))
            if enriched["edit_key"] in seen:
                continue
            seen.add(enriched["edit_key"])
            rows.append(enriched)
    return rows


def select_rows(rows: List[Dict[str, Any]], seed: int, target_total: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rng = random.Random(seed)
    eligible = [row for row in rows if not row["detokenization_artifact"]]
    by_model: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in eligible:
        by_model[row["model_key"]].append(row)
    selected: List[Dict[str, Any]] = []
    selected_keys = set()

    def sort_key(row: Dict[str, Any]) -> Tuple[int, int, str]:
        # Prefer non-OTHER typed edits, then balance behavior/category deterministically.
        other_penalty = 1 if row["error_category"] in {"other", "lexical_choice"} and row["error_type"] == "R:OTHER" else 0
        return (other_penalty, stable_hash(row["edit_id"]), row["edit_id"])

    for model_key, target in MODEL_TARGETS.items():
        candidates = sorted(by_model.get(model_key, []), key=sort_key)
        if len(candidates) < MODEL_MINIMUMS[model_key]:
            raise RuntimeError(f"Insufficient eligible edits for {model_key}: {len(candidates)} < {MODEL_MINIMUMS[model_key]}")
        model_selected: List[Dict[str, Any]] = []

        # First cover operations and behaviors when possible.
        required_groups = []
        for field in ["operation", "behavior", "error_category"]:
            values = sorted({row[field] for row in candidates if row.get(field)})
            required_groups.extend((field, value) for value in values)
        for field, value in required_groups:
            if len(model_selected) >= target:
                break
            if any(row[field] == value for row in model_selected):
                continue
            pool = [row for row in candidates if row[field] == value and row["edit_key"] not in selected_keys]
            if pool:
                choice = pool[0]
                model_selected.append(choice)
                selected_keys.add(choice["edit_key"])

        # Then fill with deterministic shuffled candidates to avoid selecting only early corpus rows.
        remaining = [row for row in candidates if row["edit_key"] not in selected_keys]
        rng.shuffle(remaining)
        remaining = sorted(remaining, key=lambda row: (len([r for r in model_selected if r["source_key"] == row["source_key"]]), stable_hash(row["edit_id"])))
        for row in remaining:
            if len(model_selected) >= target:
                break
            model_selected.append(row)
            selected_keys.add(row["edit_key"])
        selected.extend(model_selected)

    # If a model target was unavailable or filtering changed, fill to target_total with best remaining eligible edits.
    if len(selected) < target_total:
        remaining = [row for row in eligible if row["edit_key"] not in selected_keys]
        rng.shuffle(remaining)
        for row in remaining:
            if len(selected) >= target_total:
                break
            selected.append(row)
            selected_keys.add(row["edit_key"])

    selected = selected[:target_total]
    selected_ids = {row["edit_key"] for row in selected}
    excluded = [row for row in rows if row["edit_key"] not in selected_ids]
    return selected, excluded


def assign_splits(rows: List[Dict[str, Any]]) -> Dict[str, str]:
    source_keys = sorted({row["source_key"] for row in rows}, key=stable_hash)
    n = len(source_keys)
    train_cut = int(round(n * 0.70))
    dev_cut = int(round(n * 0.85))
    mapping = {}
    for idx, source_key in enumerate(source_keys):
        if idx < train_cut:
            split = "train"
        elif idx < dev_cut:
            split = "dev"
        else:
            split = "test"
        mapping[source_key] = split
    return mapping


def near_duplicate_pairs(rows: List[Dict[str, Any]], threshold: float = 0.92, limit: int = 50) -> List[Dict[str, Any]]:
    unique_sources = {}
    for row in rows:
        unique_sources.setdefault(row["source_key"], row["source"])
    items = list(unique_sources.items())
    pairs = []
    for i, (key_a, src_a) in enumerate(items):
        for key_b, src_b in items[i + 1 :]:
            if key_a == key_b:
                continue
            ratio = difflib.SequenceMatcher(None, normalize_for_duplicate(src_a), normalize_for_duplicate(src_b)).ratio()
            if ratio >= threshold:
                pairs.append({"source_a": key_a, "source_b": key_b, "similarity": round(ratio, 4)})
                if len(pairs) >= limit:
                    return pairs
    return pairs


def counter_by(rows: List[Dict[str, Any]], field: str) -> Dict[str, int]:
    return dict(sorted(Counter(str(row.get(field, "")) for row in rows).items()))


def write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build(args: argparse.Namespace) -> None:
    input_paths = [ROOT / path for path in args.inputs]
    all_rows = load_records(input_paths)
    selected, excluded = select_rows(all_rows, args.seed, args.target_total)
    split_map = assign_splits(selected)
    for idx, row in enumerate(selected):
        row["rulefaith_pool_id"] = f"rf-edit-{idx:04d}"
        row["rulefaith_split"] = split_map[row["source_key"]]
        row["selected_for"] = "rulefaith_natural_teacher_generation"

    split_rows = {split: [row for row in selected if row["rulefaith_split"] == split] for split in ["train", "dev", "test"]}
    target_to_splits = defaultdict(set)
    for row in selected:
        if row["target_key"]:
            target_to_splits[row["target_key"]].add(row["rulefaith_split"])
    target_cross_split = {target: sorted(splits) for target, splits in target_to_splits.items() if len(splits) > 1}
    source_cross_split = {
        source: sorted({row["rulefaith_split"] for row in selected if row["source_key"] == source})
        for source in {row["source_key"] for row in selected}
    }
    source_cross_split = {source: splits for source, splits in source_cross_split.items() if len(splits) > 1}
    near_dupes = near_duplicate_pairs(selected)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.results_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "edit_pool.jsonl", selected)
    for split, rows in split_rows.items():
        write_jsonl(args.out_dir / f"{split}_edits.jsonl", rows)

    stats = {
        "input_records": len(all_rows),
        "selected_records": len(selected),
        "excluded_records": len(excluded),
        "detokenization_artifacts_excluded": sum(1 for row in all_rows if row["detokenization_artifact"]),
        "counts": {
            "dataset": counter_by(selected, "dataset"),
            "model_key": counter_by(selected, "model_key"),
            "model_family": counter_by(selected, "model_family"),
            "behavior": counter_by(selected, "behavior"),
            "operation": counter_by(selected, "operation"),
            "error_type": counter_by(selected, "error_type"),
            "error_category": counter_by(selected, "error_category"),
            "split": counter_by(selected, "rulefaith_split"),
        },
        "audits": {
            "source_cross_split_count": len(source_cross_split),
            "target_cross_split_count": len(target_cross_split),
            "target_cross_split_examples": dict(list(target_cross_split.items())[:50]),
            "near_duplicate_pair_count_at_0_92": len(near_dupes),
            "near_duplicate_examples": near_dupes[:20],
        },
        "minimums": {
            "model_minimums": MODEL_MINIMUMS,
            "model_targets": MODEL_TARGETS,
        },
    }
    write_json(args.results_dir / "edit_pool_stats.json", stats)

    audit_lines = [
        "# RuleFaith Edit Pool Audit",
        "",
        f"Selected edits: {len(selected)}",
        f"Excluded detokenization/format artifacts: {stats['detokenization_artifacts_excluded']}",
        "",
        "## Counts",
        "",
    ]
    for name, counts in stats["counts"].items():
        audit_lines.append(f"### {name}")
        audit_lines.append("")
        for key, value in counts.items():
            audit_lines.append(f"- `{key}`: {value}")
        audit_lines.append("")
    audit_lines.extend(
        [
            "## Split Audits",
            "",
            f"- Source keys crossing splits: {len(source_cross_split)}",
            f"- Target strings crossing splits: {len(target_cross_split)}",
            f"- Near-duplicate source pairs at >=0.92 similarity: {len(near_dupes)}",
            "",
            "Target strings crossing splits are recorded as an audit signal, not silently removed. Later target-masked experiments must report robustness to these repeats.",
            "",
            "## Multi-Reference Handling",
            "",
            "JFLEG examples retain the existing benchmark limitation: primary ERRANT extraction uses the selected reference stored in the record, while source/sample ids allow later accept-if-any-reference alignment. This pool does not claim final multi-reference equivalence.",
            "",
            "## Scientific Boundary",
            "",
            "The pool is selected for natural teacher generation and method development. It is not a new human-gold label set.",
        ]
    )
    (args.results_dir / "edit_pool_audit.md").write_text("\n".join(audit_lines) + "\n", encoding="utf-8")

    card = [
        "# RuleFaith Edit Pool Card",
        "",
        "Created: 2026-07-19",
        "",
        "## Purpose",
        "",
        "This pool selects substantive model-produced edits for natural teacher explanation generation and RuleFaith-GEC method development.",
        "",
        "## Sources",
        "",
    ]
    for path in input_paths:
        if path.exists():
            card.append(f"- `{path.relative_to(ROOT)}`")
    card.extend(
        [
            "",
            "## Selection Rules",
            "",
            "- Exclude obvious detokenization, punctuation-spacing, and case/whitespace-only artifacts.",
            "- Preserve all three model families with minimum quotas.",
            "- Preserve EXPECT and JFLEG coverage.",
            "- Preserve correct, wrong, and overcorrection behaviors.",
            "- Preserve replace, insert, and delete operations.",
            "- Retain ORTH/PUNCT only when not an obvious formatting artifact.",
            "- Use source-level splits so the same source sentence does not cross train/dev/test.",
            "",
            "## Key Statistics",
            "",
            f"- Selected edits: {len(selected)}",
            f"- Train/dev/test: {stats['counts']['split']}",
            f"- By model: {stats['counts']['model_key']}",
            f"- By dataset: {stats['counts']['dataset']}",
            f"- By behavior: {stats['counts']['behavior']}",
            f"- By operation: {stats['counts']['operation']}",
            "",
            "## Known Risks",
            "",
            f"- Target strings crossing splits: {len(target_cross_split)}.",
            f"- Near-duplicate source pairs at >=0.92 similarity: {len(near_dupes)}.",
            "- CoEdIT remains smaller than GECToR/T5 because the existing CoEdIT pilot is smaller.",
            "- JFLEG multi-reference equivalence is not fully solved in this pool.",
        ]
    )
    DOCS_CARD.write_text("\n".join(card) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputs",
        nargs="+",
        default=[
            "data/faithfulness_benchmark/edit_records.jsonl",
        ],
    )
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--results-dir", type=Path, default=RESULTS_DIR)
    parser.add_argument("--target-total", type=int, default=300)
    parser.add_argument("--seed", type=int, default=20260719)
    args = parser.parse_args()
    build(args)


if __name__ == "__main__":
    main()

