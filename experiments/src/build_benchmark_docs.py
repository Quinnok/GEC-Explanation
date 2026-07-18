from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BENCHMARK_DIR = ROOT / "data" / "faithfulness_benchmark"
DEFAULT_DOCS_DIR = ROOT / "docs"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def md_count_table(title: str, counts: Dict[str, Any]) -> str:
    rows = [f"## {title}", "", "| Item | Count |", "|---|---:|"]
    for key, value in counts.items():
        rows.append(f"| `{key}` | {value} |")
    return "\n".join(rows)


def short_json(data: Any) -> str:
    return "`" + json.dumps(data, sort_keys=True) + "`"


def load_model_metadata(paths: Iterable[Path]) -> Dict[str, Dict[str, Any]]:
    models: Dict[str, Dict[str, Any]] = {}
    for path in paths:
        if not path.exists():
            continue
        payload = read_json(path)
        for key, value in payload.get("models", {}).items():
            models[key] = value
    return models


def source_split_audit(edit_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    source_to_splits: Dict[str, set[str]] = defaultdict(set)
    source_to_ids: Dict[str, set[str]] = defaultdict(set)
    target_to_splits: Dict[str, set[str]] = defaultdict(set)
    for row in edit_rows:
        source_hash = hashlib.sha1(row["source"].encode("utf-8")).hexdigest()
        source_to_splits[source_hash].add(row["split"])
        source_to_ids[source_hash].add(row["sample_id"])
        target = row.get("predicted_edit", {}).get("target_text", "")
        if target:
            target_to_splits[target.lower()].add(row["split"])
    cross_split_sources = {
        key: sorted(value)
        for key, value in source_to_splits.items()
        if len(value) > 1
    }
    repeated_targets = {
        key: sorted(value)
        for key, value in target_to_splits.items()
        if len(value) > 1
    }
    return {
        "source_count": len(source_to_splits),
        "source_cross_split_duplicate_count": len(cross_split_sources),
        "source_cross_split_duplicate_examples": dict(list(cross_split_sources.items())[:10]),
        "source_id_duplicate_count": sum(1 for value in source_to_ids.values() if len(value) > 1),
        "predicted_target_cross_split_overlap_count": len(repeated_targets),
        "predicted_target_cross_split_overlap_examples": dict(list(repeated_targets.items())[:20]),
    }


def build(args: argparse.Namespace) -> None:
    benchmark_dir = args.benchmark_dir
    docs_dir = args.docs_dir
    stats = read_json(benchmark_dir / "benchmark_stats.json")
    edit_rows = read_jsonl(benchmark_dir / "edit_records.jsonl")
    explanation_rows = read_jsonl(benchmark_dir / "explanation_instances.jsonl")
    expect_stats = read_json(args.expect_stats) if args.expect_stats.exists() else {}
    jfleg_stats = read_json(args.jfleg_stats) if args.jfleg_stats.exists() else {}
    metadata = load_model_metadata(args.model_metadata)
    expect_behavior = read_json(args.expect_behavior) if args.expect_behavior.exists() else {}
    jfleg_behavior = read_json(args.jfleg_behavior) if args.jfleg_behavior.exists() else {}
    coedit_behavior = read_json(args.coedit_behavior) if args.coedit_behavior.exists() else {}

    leakage = source_split_audit(edit_rows)
    leakage.update(
        {
            "created_at": utc_now(),
            "explicit_template_count": stats.get("explanation_type_counts", {}).get("explicit_template", 0),
            "masked_target_template_count": stats.get("explanation_type_counts", {}).get("masked_target_template", 0),
            "automatic_label_note": stats.get("important_note"),
            "template_near_duplicate_risk": (
                "High for explicit, masked-target, rule-only, and synthetic negative templates; "
                "these must be stratified by explanation_type and excluded from primary natural-language claims."
            ),
            "generator_evaluator_overlap_policy": (
                "FLAN-T5-base explanation candidates are not evaluated with the same generator in Round 07. "
                "Future LLM judges must be model-disjoint from explanation generators."
            ),
        }
    )
    write_json(benchmark_dir / "leakage_audit.json", leakage)

    model_lines = []
    for key, item in metadata.items():
        config = item.get("config", {})
        runtime = item.get("runtime", {})
        model_lines.extend(
            [
                f"### {key}",
                "",
                f"- Model: `{config.get('model_id', 'unknown')}`",
                f"- Family: `{config.get('model_family', 'unknown')}`",
                f"- Revision: `{config.get('model_revision', 'unknown')}`",
                f"- License note: {config.get('license', 'unknown')}",
                f"- Decoding: {short_json(config.get('decoding', {}))}",
                f"- Runtime: {runtime.get('sample_count', 0)} samples, {runtime.get('changed_count', 0)} changed, "
                f"{runtime.get('reference_copy_count', 0)} copied reference, {runtime.get('duration_seconds', 0)} CPU seconds.",
                "",
            ]
        )

    benchmark_card = "\n".join(
        [
            "# Round 07 Benchmark Card",
            "",
            f"Generated: `{utc_now()}`",
            "",
            "This benchmark is an automatic, model-edit-level pilot for GEC explanation faithfulness. "
            "Each edit record corresponds to an edit actually produced by a public GEC model, not to a reference edit used as a prediction.",
            "",
            "## Scope",
            "",
            f"- Edit records: {stats['edit_count']}",
            f"- Explanation instances: {stats['explanation_instance_count']}",
            f"- Missing-edit diagnoses: {stats['missing_edit_count']}",
            f"- Human gold labels: {stats['human_gold_count']}",
            f"- Dataset counts: {short_json(stats['dataset_counts'])}",
            f"- Model counts: {short_json(stats['model_counts'])}",
            f"- Model-family counts: {short_json(stats['model_family_counts'])}",
            f"- Behavior counts: {short_json(stats['behavior_counts'])}",
            f"- Operation counts: {short_json(stats['operation_counts'])}",
            f"- ERRANT error-type count: {stats['error_type_count']}",
            f"- Split counts: {short_json(stats['split_counts'])}",
            "",
            "## Explanation Sources",
            "",
            "- `explicit_template`: automatic leakage upper control copied from structured edit fields.",
            "- `masked_target_template`: automatic target-masked leakage control.",
            "- `rule_only`, `gee_style_automatic`, `rule_grounded_automatic`: automatic rule templates from ERRANT type/source span.",
            "- `flan_t5_candidate`: open-source generated candidate, not gold.",
            "- Negative controls: wrong span/source token/target/operation/direction/error type/rule/evidence, cross-sentence swaps, generic, partial, and pending counterfactual inconsistency seeds.",
            "- `faithful_wrong_model_edit`: positive for model-behavior faithfulness only; it says the explanation matches what the model did, not that the edit is grammatically correct.",
            "",
            md_count_table("Explanation Type Counts", stats["explanation_type_counts"]),
            "",
            md_count_table("Negative Type Counts", stats["negative_type_counts"]),
            "",
            "## Leakage Controls",
            "",
            f"- Source cross-split duplicates: {leakage['source_cross_split_duplicate_count']}",
            f"- Repeated predicted targets across splits: {leakage['predicted_target_cross_split_overlap_count']}",
            "- Template near-duplicate risk is expected for automatic controls and is recorded in `data/faithfulness_benchmark/leakage_audit.json`.",
            "- Primary claims must be stratified by explanation type; explicit templates and raw edit strings cannot dominate aggregate results.",
            "- Counterfactual inconsistency seeds are placeholders until Round 08 reruns the original GEC models on counterfactual sources.",
            "",
            "## Behavior Summaries",
            "",
            f"- EXPECT GECToR/T5 behavior: {short_json(expect_behavior.get('model_behavior_distribution', {}))}",
            f"- JFLEG GECToR/T5 behavior: {short_json(jfleg_behavior.get('model_behavior_distribution', {}))}",
            f"- EXPECT CoEdIT behavior: {short_json(coedit_behavior.get('model_behavior_distribution', {}))}",
            "",
            "## Files",
            "",
            "- `data/faithfulness_benchmark/edit_records.jsonl`",
            "- `data/faithfulness_benchmark/explanation_instances.jsonl`",
            "- `data/faithfulness_benchmark/missing_edit_diagnosis.jsonl`",
            "- `data/faithfulness_benchmark/benchmark_stats.json`",
            "- `data/faithfulness_benchmark/leakage_audit.json`",
        ]
    )

    data_statement = "\n".join(
        [
            "# Data Statement",
            "",
            f"Generated: `{utc_now()}`",
            "",
            "## EXPECT",
            "",
            f"- Source: `{expect_stats.get('source_repo', 'https://github.com/lorafei/Explainable_GEC')}`",
            f"- Commit: `{expect_stats.get('source_commit', 'unknown')}`",
            f"- License: `{expect_stats.get('license', 'unknown')}`",
            f"- Processed sample count: {expect_stats.get('sample_count', 0)}",
            f"- Source-reference ERRANT edit count: {expect_stats.get('edit_count', 0)}",
            f"- Split counts: {short_json(expect_stats.get('split_counts', {}))}",
            "",
            "EXPECT provides source/reference sentence pairs plus explanation-adjacent labels such as evidence indices and error types. "
            "The local audit found no natural-language explanation field for model-produced edits.",
            "",
            "## JFLEG",
            "",
            f"- Source: `{jfleg_stats.get('source', 'https://github.com/keisks/jfleg')}`",
            f"- Commit: `{jfleg_stats.get('commit', 'unknown')}`",
            f"- License: `{jfleg_stats.get('license', 'unknown')}`",
            f"- Processed sample count: {jfleg_stats.get('sample_count', 0)}",
            f"- Split counts: {short_json(jfleg_stats.get('split_counts', {}))}",
            f"- Reference policy: {jfleg_stats.get('reference_policy', 'unknown')}",
            "",
            "## Benchmark Construction",
            "",
            "The benchmark aligns source-reference ERRANT edits with source-prediction ERRANT edits. "
            "Predicted edits are labeled as correct, wrong, or overcorrection by automatic alignment; unmatched reference edits are stored as missed-correction diagnoses. "
            "Labels are automatic and are not human adjudications.",
            "",
            "## Splitting",
            "",
            "Train/dev/test splits are deterministic hashes of dataset, sample id, and source text. "
            f"The leakage audit found {leakage['source_cross_split_duplicate_count']} source texts crossing splits. "
            "Template families are repeated across splits by design, so aggregate metrics must be reported by explanation type.",
            "",
            "## Annotation Status",
            "",
            "No double-human annotation has been collected. Round 10 must prepare annotation packets and adjudication guidelines before any human-gold claim.",
        ]
    )

    license_lines = [
        "# License Report",
        "",
        f"Generated: `{utc_now()}`",
        "",
        "| Resource | Local Role | Source | Version | License Note |",
        "|---|---|---|---|---|",
        f"| EXPECT | Source/reference data and labels | `{expect_stats.get('source_repo', 'https://github.com/lorafei/Explainable_GEC')}` | `{expect_stats.get('source_commit', 'unknown')}` | `{expect_stats.get('license', 'unknown')}` |",
        f"| JFLEG | Second source/reference data source | `{jfleg_stats.get('source', 'https://github.com/keisks/jfleg')}` | `{jfleg_stats.get('commit', 'unknown')}` | `{jfleg_stats.get('license', 'unknown')}` |",
    ]
    for key, item in metadata.items():
        config = item.get("config", {})
        license_lines.append(
            f"| {key} | GEC model predictions | `{config.get('model_id', 'unknown')}` | `{config.get('model_revision', 'unknown')}` | {config.get('license', 'unknown')} |"
        )
    license_lines.extend(
        [
            "| FLAN-T5-base | Explanation candidate generator | `google/flan-t5-base` | `7bcac572ce56db69c1ea7c8af255c5d7c9672fc2` | Apache-2.0 model card |",
            "",
            "License-sensitive note: several data/model resources are non-commercial or share-alike. This repository stores pilot outputs for research planning; final release must re-check redistribution terms and avoid bundling restricted raw corpora if required.",
        ]
    )

    round_07 = "\n".join(
        [
            "# Round 07: GEC Explanation Faithfulness Benchmark",
            "",
            "## Completed",
            "",
            "- Added JFLEG as a second license-clear GEC data source and retained all four references per row.",
            "- Ran GECToR and T5 over 80 JFLEG samples each, producing 540 JFLEG model edits and 378 missed-edit diagnoses.",
            "- Ran CoEdIT-large over 20 EXPECT samples as an instruction-following open generation/editor branch, producing 122 predicted edits and 8 missed-edit diagnoses.",
            "- Built a 700-edit benchmark with 12,754 explanation/control instances and 160 missing-edit diagnoses.",
            "- Included three model families in the selected benchmark: sequence-to-edit, sequence-to-sequence, and instruction-following text editor.",
            "- Generated benchmark card, data statement, license report, and leakage audit from JSON outputs.",
            "",
            "## Key Stats",
            "",
            f"- Dataset counts: {short_json(stats['dataset_counts'])}",
            f"- Model counts: {short_json(stats['model_counts'])}",
            f"- Behavior counts: {short_json(stats['behavior_counts'])}",
            f"- Operation counts: {short_json(stats['operation_counts'])}",
            f"- Error types: {stats['error_type_count']}",
            f"- Human gold labels: {stats['human_gold_count']}",
            "",
            "## Caveats",
            "",
            "- CoEdIT is a small 20-sentence CPU pilot because the model is 770M parameters / about 3.13GB of weights.",
            "- Automatic explanations and negatives are not human gold.",
            "- Explicit templates remain leakage upper controls only.",
            "- Counterfactual labels are pending Round 08 reruns of the original GEC models.",
        ]
    )

    write_text(docs_dir / "benchmark_card.md", benchmark_card)
    write_text(docs_dir / "data_statement.md", data_statement)
    write_text(docs_dir / "license_report.md", "\n".join(license_lines))
    write_text(docs_dir / "round_07.md", round_07)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Round 07 benchmark documentation from JSON outputs.")
    parser.add_argument("--benchmark-dir", type=Path, default=DEFAULT_BENCHMARK_DIR)
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    parser.add_argument("--expect-stats", type=Path, default=ROOT / "data" / "processed" / "expect_v1_sample_stats.json")
    parser.add_argument("--jfleg-stats", type=Path, default=ROOT / "data" / "processed" / "jfleg_v1_sample_stats.json")
    parser.add_argument(
        "--model-metadata",
        type=Path,
        nargs="+",
        default=[
            ROOT / "results" / "model_predictions" / "runtime_metadata.json",
            ROOT / "results" / "model_predictions" / "jfleg_v1_runtime_metadata.json",
            ROOT / "results" / "model_predictions" / "expect_v1_coedit_runtime_metadata.json",
        ],
    )
    parser.add_argument("--expect-behavior", type=Path, default=ROOT / "results" / "model_edits" / "behavior_summary.json")
    parser.add_argument("--jfleg-behavior", type=Path, default=ROOT / "results" / "model_edits_jfleg" / "behavior_summary.json")
    parser.add_argument("--coedit-behavior", type=Path, default=ROOT / "results" / "model_edits_coedit_expect" / "behavior_summary.json")
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
