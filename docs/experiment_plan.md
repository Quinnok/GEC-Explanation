# Experiment Plan

Last updated: 2026-07-18

## Current Objective

Move from a source-reference template sanity check to an edit-level pilot over corrections actually produced by public GEC models. The immediate question is whether explanation-to-edit consistency can be evaluated without letting explicit templates leak the full answer.

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

1. Add a normalization ablation for seq2seq detokenization effects, especially T5 `R:ORTH` overcorrections.
2. Improve open-source explanation generation or retrieve from a license-clear explanation dataset; do not use direct predicted-edit templates as the main explanation source.
3. Build leakage-aware reconstruction baselines on model-produced edits: source only, explanation only, source plus generated explanation, shuffled explanation, raw edit string, and explicit template upper control.
4. Add manual adjudication protocol for a small sample before making faithfulness claims.
5. Expand literature verification before using any "first" or "novel" language.

## Metrics To Keep

- Full Edit Exact Match.
- Span F1.
- Target Match.
- Operation Accuracy.
- Error Type Accuracy.
- Faithfulness Macro-F1.
- Negative rejection rate by negative type.
- Behavior-conditioned scores: correct correction, wrong correction, overcorrection, and missed correction diagnosis.

## Blocking Items

- Need a credible human or license-clear natural-language explanation source for final paper claims.
- Need human inspection protocol for explanation faithfulness.
- Need final related-work sweep for reverse reconstruction and simulatability before contribution language is frozen.
