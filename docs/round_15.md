# Round 15: Human-Grounded Metric Evaluation

Date: 2026-07-19

## Inputs

- Full V2 A/B comparison imported from `annotation/round15/source/annotation_v2_agreement_analysis.xlsx`.
- Completed adjudication imported from `annotation/round15/source/annotation_v2_adjudication_completed.csv`.
- Hidden metadata mapping from `annotation/round10/annotation_metadata_with_auto_labels.jsonl`.
- Automatic method outputs from `results/round08/` and `results/round11/`.

## Work Completed

Created reproducible scripts:

- `experiments/src/finalize_annotation_gold.py`
- `experiments/src/evaluate_human_gold_metrics.py`
- `experiments/run_round15.sh`

Generated final adjudicated labels:

- `annotation/round15/annotation_final_gold_v2.csv`
- `annotation/round15/annotation_final_gold_v2.jsonl`
- `annotation/round15/annotation_final_gold_v2_stats.json`
- `annotation/round15/annotation_v2_data_card.md`

Generated human-gold evaluation outputs:

- `results/human_gold/main_metric_table.csv`
- `results/human_gold/main_metric_table_selected.csv`
- `results/human_gold/main_metric_table.tex`
- `results/human_gold/correlation_table.csv`
- `results/human_gold/correlation_table.tex`
- `results/human_gold/stress_test_breakdown.csv`
- `results/human_gold/error_cases.md`
- `results/human_gold/bootstrap_results.json`
- `results/human_gold/coverage_report.json`
- `results/human_gold/human_gold_metric_summary.json`

Copied paper-ready assets:

- `results/paper_assets/human_gold_metric_table.tex`
- `results/paper_assets/human_gold_correlation_table.tex`

## Label Status

The final file contains 160 edit-explanation items:

- 100 adjudicated disagreement items.
- 60 double-annotator agreement items inherited without an additional blind audit.
- 0 counterfactual items.

The five missing adjudication notes in the supplied adjudication file were filled by deterministic protocol-based notes.

Important provenance limitation:

> A/B annotations and adjudication were supplied by the user. Confirm whether the annotators and adjudicator are human before describing these labels as human gold in the paper.

## Main Findings

The final stress-test label distribution is highly skewed:

- `faithful=1`, `partially_faithful=57`, `unfaithful=102`.
- `correct` or `partially_correct` edit alignment: 64/160.
- `correct` or `partially_correct` rule correctness: 22/160.
- `correct` or `partially_correct` evidence correctness: 16/160.

Full-coverage automatic metrics against binary overall faithfulness:

| Method | Macro-F1 | AUROC |
|---|---:|---:|
| surface leakage score | 0.800 | 0.820 |
| reverse reconstruction | 0.789 | 0.772 |
| target-masked score | 0.789 | 0.773 |
| combined proxy | 0.713 | 0.880 |
| rule/evidence verifier | 0.695 | 0.720 |
| leakage-adjusted reconstruction | 0.408 | 0.509 |

For rule correctness, the rule/evidence verifier is the best full-coverage method but still weak:

- Rule Macro-F1: 0.558.
- Evidence Macro-F1: 0.470.

## Interpretation

The current result does **not** support claiming that RuleFaith has solved GEC explanation faithfulness.

It does support a more conservative and stronger paper direction:

> Edit reconstruction and leakage-heavy metrics can align with coarse faithfulness labels in a stress-test set, but they remain poor tests of rule and evidence quality. GEC explanation evaluation should be decomposed into edit alignment, edit validity, rule correctness, evidence correctness, and overall faithfulness.

## Updated Research Decision

Main line:

> Human-adjudicated stress testing of GEC explanation metrics.

Downgraded:

- Reverse reconstruction: L1 edit-alignment diagnostic.
- Counterfactual simulatability: future behavioral layer; current simulator remains weak.
- RuleFaith: promising next method line, not established by current verifier.

See `docs/post_human_eval_idea_decision.md`.

## Remaining Issues

- Confirm annotator/adjudicator identity before using `human gold` terminology.
- Agreement-inherited 60 items were not independently blind-audited in this automated run.
- The set is intentionally adversarial and template-heavy; do not report faithful-label prevalence as natural explanation quality.
- Natural GPT-5.5/open-model explanations still need a balanced validation subset.
- Round 10 counterfactual annotation rows remain excluded because their explanation field is incomplete.
