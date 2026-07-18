# Data Sources

Last updated: 2026-07-18

## EXPECT

- Source: https://github.com/lorafei/Explainable_GEC
- Paper: Enhancing Grammatical Error Correction Systems with Explanations, ACL 2023.
- License: MIT, as stated in the upstream repository README and LICENSE.
- Local download: `data/downloads/Explainable_GEC`.
- Download command: `git clone --depth 1 https://github.com/lorafei/Explainable_GEC.git data/downloads/Explainable_GEC`.
- Recorded commit: `6e44b68f6e4c199dd3b235cacb604a856bd3d133`.
- Pilot sample file: `data/processed/expect_v1_samples.jsonl`.
- Pilot sample count: 300.
- ERRANT edit count in pilot: 320.
- Split counts: `{"test": 300}`.
- Operation counts: `{"delete": 39, "insert": 51, "replace": 230}`.

The versioned pilot uses real source/reference sentence pairs from EXPECT. The generated explanations in this project are automatic template constructions for pilot diagnostics, not human gold explanations.

## Public GEC Models Used in Round 03

### GECToR RoBERTa base 5k

- Source: https://huggingface.co/gotutiyan/gector-roberta-base-5k
- Model family: sequence-to-edit GEC tagger.
- Local role: generated predictions for the 300 EXPECT source sentences.
- Recorded revision: `adaac6fb919431fb5a038b1e449055ae638613a4`.
- License note: upstream model card states "Only non-commercial purposes."
- Decoding: `keep_confidence=0.0`, `min_error_prob=0.0`, `n_iteration=5`, `batch_size=8`.
- Runtime metadata: `results/model_predictions/runtime_metadata.json`.

### T5 Base Grammar Correction

- Source: https://huggingface.co/vennify/t5-base-grammar-correction
- Model family: sequence-to-sequence text generation.
- Local role: generated predictions for the 300 EXPECT source sentences.
- Recorded revision: `9e4a09d21dca1072a69302df9261289d03c3ed78`.
- License note: upstream model card states `cc-by-nc-sa-4.0`.
- Decoding: prefix `grammar: `, `num_beams=5`, `max_input_length=256`, `max_new_tokens=128`, `batch_size=8`.
- Runtime metadata: `results/model_predictions/runtime_metadata.json`.

## Open-Source Explanation Candidate Generator

- Source: https://huggingface.co/google/flan-t5-base
- Local role: generated 300 explanation candidates for model-produced edits.
- Recorded revision: `7bcac572ce56db69c1ea7c8af255c5d7c9672fc2`.
- License note: upstream model card states Apache 2.0.
- Input fields: source sentence, model prediction, and predicted edit span.
- Output file: `data/processed/model_edit_explanation_candidates.jsonl`.
- Constraint: these are model-generated candidates, not human gold explanations. Explicit templates are kept only as leakage upper controls.
