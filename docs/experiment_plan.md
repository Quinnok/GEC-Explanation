# Experiment Plan

Last updated: 2026-07-18

## Current Objective

Build a model-produced edit benchmark for evaluating GEC explanation faithfulness with three layers: L1 edit correspondence and leakage controls, L2 Counterfactual Edit Simulatability, and L3 rule/evidence grounding.

## Current Data Status

Available local research data:

- EXPECT pilot sample: 300 real English GEC source/reference pairs in `data/processed/expect_v1_samples.jsonl`.
- Reference edit extraction: 320 ERRANT source-reference edits in `results/edit_extraction/expect_v1_errant_edits.jsonl`.
- Model predictions: 600 predictions in `results/model_predictions/expect_v1_model_predictions.jsonl`.
- Model-produced edit dataset: 1707 source-prediction ERRANT edits in `results/model_edits/model_edit_dataset.jsonl`.
- Missing-edit diagnosis: 319 unmatched reference edits in `results/model_edits/missing_edit_diagnosis.jsonl`.
- Open-source explanation candidates: 300 FLAN-T5-base candidates in `data/processed/model_edit_explanation_candidates.jsonl`.

## Completed Round 03 Pilot

- Two public GEC model families ran on CPU: GECToR as sequence-to-edit and T5 grammar correction as sequence-to-sequence.
- ERRANT extracts both source-reference and source-prediction edits.
- Behavior labels are generated for all predicted edits, not only the first edit per sentence.
- A 30-case balanced model alignment inspection report is available.
- EXPECT field audit confirms evidence and type labels, but no natural-language explanation field.
- Explicit templates are retained only as leakage upper controls.

## Next Experiments

1. Build `data/faithfulness_benchmark/` from model-produced edits, targeting at least 500 predicted edits and at least 100 missed-edit diagnoses.
2. Add a third no-paid model family when feasible, preferably an instruction-following/open text-editing model; if blocked, document the blocker and substitute another public GEC model.
3. Generate explanation candidates and hard negatives for each edit: explicit template, masked target, rule-only, FLAN, another open model, shuffled, wrong span, wrong target, wrong operation, wrong direction, wrong type, wrong rule, wrong evidence, generic, and counterfactually inconsistent.
4. Implement L1 baselines: random, majority, surface, embedding similarity, structured extraction, reverse reconstruction, masked-target reconstruction, and leakage-adjusted reconstruction.
5. Implement L2 Counterfactual Edit Simulatability by creating error-irrelevant and rule-relevant variants, rerunning the original GEC models, and scoring explanation predictions against actual rerun behavior.
6. Implement L3 rule/evidence verifier using ERRANT types and EXPECT evidence where available.
7. Prepare a human annotation package before claiming that automatic faithfulness labels match human judgments.

## Metrics To Keep

- Full Edit Exact Match.
- Span F1.
- Target Match.
- Operation Accuracy.
- Error Type Accuracy.
- Faithfulness Macro-F1.
- Counterfactual behavior accuracy.
- Preserve/change/cancel/retarget macro-F1.
- Rule consistency.
- Evidence span F1.
- Negative rejection rate by negative type.
- Behavior-conditioned scores: correct correction, wrong correction, overcorrection, and missed correction diagnosis.
- Grouped bootstrap confidence intervals by source sentence.

## Blocking Items

- Need a credible human or license-clear natural-language explanation source for final paper claims.
- Need human inspection protocol for explanation faithfulness.
- Need counterfactual validity audit before reporting L2 as behavioral faithfulness evidence.
