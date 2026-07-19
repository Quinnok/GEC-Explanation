from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ALL_SAMPLES = ROOT / "annotation" / "round15" / "source" / "annotation_v2_all_samples.csv"
DEFAULT_ADJUDICATION = ROOT / "annotation" / "round15" / "source" / "annotation_v2_adjudication_completed.csv"
DEFAULT_METADATA = ROOT / "annotation" / "round10" / "annotation_metadata_with_auto_labels.jsonl"
DEFAULT_OUT_DIR = ROOT / "annotation" / "round15"
DEFAULT_RESULTS_DIR = ROOT / "results" / "human_gold"

DIMENSIONS = [
    ("edit_alignment", "final_edit_alignment"),
    ("edit_validity", "final_edit_validity"),
    ("rule_correctness", "final_rule_correctness"),
    ("evidence", "final_evidence"),
    ("faithfulness", "final_faithfulness"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def note_for(row: Dict[str, str]) -> str:
    alignment = row.get("final_edit_alignment", "")
    validity = row.get("final_edit_validity", "")
    rule = row.get("final_rule_correctness", "")
    evidence = row.get("final_evidence", "")
    faith = row.get("final_faithfulness", "")
    if faith == "faithful":
        return "Edit alignment, rule, and evidence are judged correct for this model edit."
    if alignment == "incorrect":
        return "Explanation does not align with the displayed atomic model edit."
    if rule == "incorrect":
        return "Explanation aligns with the edit only partly or fully, but states an incorrect rule."
    if evidence == "incorrect":
        return "Explanation cites incorrect contextual evidence for the edit."
    if rule == "not_applicable" and evidence == "not_provided":
        return "Explanation identifies or references the edit but gives no rule or contextual evidence."
    if validity == "invalid":
        return "The model edit itself is judged invalid; faithfulness is based on the explanation separately."
    if validity == "stylistic":
        return "The model edit is primarily stylistic or optional."
    return "Adjudicated by protocol rules."


def build_gold(args: argparse.Namespace) -> None:
    all_rows = read_csv(args.all_samples)
    adjudication_rows = read_csv(args.adjudication)
    metadata = {row["item_id"]: row for row in read_jsonl(args.metadata)}
    adjudicated = {row["item_id"]: row for row in adjudication_rows}

    eligible = [row for row in all_rows if row["item_id"].startswith("r10-faith-")]
    final_rows: List[Dict[str, Any]] = []
    completed_adjudication_rows: List[Dict[str, str]] = []

    for row in eligible:
        item_id = row["item_id"]
        meta = metadata.get(item_id, {})
        if item_id in adjudicated:
            adj = dict(adjudicated[item_id])
            if not adj.get("adjudication_notes", "").strip():
                adj["adjudication_notes"] = note_for(adj)
            completed_adjudication_rows.append(adj)
            source_row = adj
            gold_source = "adjudicated_disagreement"
            gold_status = "adjudicated"
        else:
            source_row = row
            gold_source = "double_annotator_agreement"
            gold_status = "accepted_by_agreement_not_blind_audited"

        final: Dict[str, Any] = {
            "item_id": item_id,
            "task_type": "edit_explanation_faithfulness",
            "dataset": row.get("dataset", ""),
            "model_key": row.get("model_key", ""),
            "model_family": row.get("model_family", ""),
            "model_behavior": row.get("model_behavior", ""),
            "error_type": row.get("error_type", ""),
            "explanation_type": row.get("explanation_type", ""),
            "source": row.get("source", ""),
            "model_prediction": row.get("model_prediction", ""),
            "model_edit": row.get("model_edit", ""),
            "explanation": row.get("explanation", ""),
            "instance_id": meta.get("instance_id", ""),
            "edit_id": meta.get("edit_id", ""),
            "automatic_label": meta.get("automatic_label", ""),
            "automatic_negative_type": meta.get("automatic_negative_type", ""),
            "gold_source": gold_source,
            "gold_status": gold_status,
            "adjudication_notes": source_row.get("adjudication_notes", ""),
            "A_notes": row.get("A_notes", ""),
            "B_notes": row.get("B_notes", ""),
        }
        for dim, final_key in DIMENSIONS:
            a_key = f"A_{dim}"
            b_key = f"B_{dim}"
            final[f"annotator_a_{dim}"] = row.get(a_key, "")
            final[f"annotator_b_{dim}"] = row.get(b_key, "")
            if item_id in adjudicated:
                final[f"final_{dim}"] = source_row.get(final_key, "")
            else:
                final[f"final_{dim}"] = row.get(a_key, "")
        final_rows.append(final)

    label_counts = {
        f"final_{dim}": dict(Counter(row[f"final_{dim}"] for row in final_rows))
        for dim, _ in DIMENSIONS
    }
    agreement_rows = [row for row in final_rows if row["gold_source"] == "double_annotator_agreement"]
    adjudicated_rows = [row for row in final_rows if row["gold_source"] == "adjudicated_disagreement"]
    missing_notes = [row["item_id"] for row in completed_adjudication_rows if not row.get("adjudication_notes", "").strip()]

    fieldnames = [
        "item_id",
        "task_type",
        "dataset",
        "model_key",
        "model_family",
        "model_behavior",
        "error_type",
        "explanation_type",
        "source",
        "model_prediction",
        "model_edit",
        "explanation",
        "instance_id",
        "edit_id",
        "automatic_label",
        "automatic_negative_type",
        "annotator_a_edit_alignment",
        "annotator_b_edit_alignment",
        "final_edit_alignment",
        "annotator_a_edit_validity",
        "annotator_b_edit_validity",
        "final_edit_validity",
        "annotator_a_rule_correctness",
        "annotator_b_rule_correctness",
        "final_rule_correctness",
        "annotator_a_evidence",
        "annotator_b_evidence",
        "final_evidence",
        "annotator_a_faithfulness",
        "annotator_b_faithfulness",
        "final_faithfulness",
        "A_notes",
        "B_notes",
        "adjudication_notes",
        "gold_source",
        "gold_status",
    ]
    write_csv(args.out_dir / "annotation_final_gold_v2.csv", final_rows, fieldnames)
    write_jsonl(args.out_dir / "annotation_final_gold_v2.jsonl", final_rows)
    write_csv(
        args.out_dir / "annotation_v2_adjudication_completed_notes_filled.csv",
        completed_adjudication_rows,
        list(completed_adjudication_rows[0].keys()) if completed_adjudication_rows else None,
    )

    stats = {
        "created_at": utc_now(),
        "item_count": len(final_rows),
        "adjudicated_count": len(adjudicated_rows),
        "agreement_inherited_count": len(agreement_rows),
        "counterfactual_items_included": 0,
        "label_counts": label_counts,
        "missing_instance_id_count": sum(1 for row in final_rows if not row["instance_id"]),
        "missing_adjudication_note_count_after_fill": len(missing_notes),
        "blind_audit_status": "not_completed_in_this_automated_run",
        "annotator_provenance": "two independent human annotators, confirmed by the user on 2026-07-19",
        "adjudicator_provenance": "human third-party adjudicator, confirmed by the user on 2026-07-19",
        "provenance_note": (
            "A/B annotations were completed by two independent human annotators and disagreements were resolved "
            "by a human third-party adjudicator, as confirmed by the user on 2026-07-19."
        ),
    }
    write_json(args.out_dir / "annotation_final_gold_v2_stats.json", stats)
    write_json(args.results_dir / "annotation_final_gold_v2_stats.json", stats)

    data_card = [
        "# Annotation Final Gold V2 Data Card",
        "",
        f"Created: `{stats['created_at']}`",
        "",
        "## Scope",
        "",
        "- Includes 160 `edit_explanation_faithfulness` items.",
        "- Excludes 80 counterfactual items because their explanation fields were incomplete in Round 10.",
        "- Combines double annotations from two independent human annotators with third-party human adjudication.",
        "",
        "## Provenance",
        "",
        stats["provenance_note"],
        "",
        f"- Annotators: {stats['annotator_provenance']}.",
        f"- Adjudicator: {stats['adjudicator_provenance']}.",
        "",
        "## Counts",
        "",
        f"- Adjudicated disagreements: {stats['adjudicated_count']}",
        f"- Agreement-inherited items: {stats['agreement_inherited_count']}",
        f"- Missing instance ids: {stats['missing_instance_id_count']}",
        "",
        "## Final Label Distribution",
        "",
    ]
    for key, counts in label_counts.items():
        data_card.append(f"### {key}")
        data_card.append("")
        for label, count in sorted(counts.items()):
            data_card.append(f"- `{label}`: {count}")
        data_card.append("")
    data_card.extend(
        [
            "## Important Limitations",
            "",
            "- The benchmark is a stress-test sample, not a natural random sample of all GEC explanations.",
            "- Only one item is labeled fully `faithful`; report binary and ordinal tasks carefully.",
            "- Agreement-inherited items were not independently blind-audited in this automated run.",
            "- Because the set is intentionally adversarial and template-heavy, do not use its label prevalence as an estimate of natural GEC explanation quality.",
        ]
    )
    (args.out_dir / "annotation_v2_data_card.md").write_text("\n".join(data_card).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Finalize Round 15 adjudicated annotation gold labels.")
    parser.add_argument("--all-samples", type=Path, default=DEFAULT_ALL_SAMPLES)
    parser.add_argument("--adjudication", type=Path, default=DEFAULT_ADJUDICATION)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    return parser.parse_args()


if __name__ == "__main__":
    build_gold(parse_args())
