# RuleFaith Verifier Design

Created: 2026-07-19

## Role in RuleFaith-GEC

The verifier stack scores teacher and student explanations along separate dimensions: edit validity, edit alignment, rule correctness, evidence correctness, leakage, and genericness. Reverse reconstruction is retained only as an edit-alignment signal.

## Round 19 Calibration Source

- Human labels: `annotation/round15/annotation_final_gold_v2.csv`
- Metric table: `results/human_gold/main_metric_table.csv`
- Calibration output: `results/rulefaith/verifier_calibration.csv`
- Gate output: `results/rulefaith/verifier_metrics.json`

## Gate A Result

- Status: `conditional_pass`
- Edit Alignment AUROC: `0.75`
- Rule AUROC: `0.7562582345191041`
- Evidence AUROC: `0.6666666666666666`
- Target-masked alignment AUROC: `0.7582194010416666`

## Design Decision

Proceed to method-pilot filtering with the current verifier as a calibration baseline, but do not claim final generation quality until natural teacher candidates and human evaluation are available.

## Required Next Improvements

- Add an explicit edit-validity gate for invalid and stylistic edits.
- Add rule/evidence-specific failure mining for natural teacher outputs.
- Add leakage and genericness penalties before preference data construction.
- Avoid using the same LLM as both sole teacher and sole final judge.
