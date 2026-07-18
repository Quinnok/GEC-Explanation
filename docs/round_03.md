# Round 03: Model-Predicted Edit Pilot

Last updated: 2026-07-18

## Starting Point

Round 03 starts after the Round 02 bootstrap and real EXPECT source-reference pilot. Round 02 is committed as `1bb4c57 Round 02 real EXPECT ERRANT pilot`. The Round 02 explicit-template result is treated only as an answer-leakage upper control, not as evidence that Reverse Edit Reconstruction works for natural-language explanations.

## Engineering Cleanup

- Removed duplicate Round 02 status entries from `docs/experiment_log.md`.
- Deleted untracked smoke prediction files and untracked install/shutdown-warning logs.
- Updated `.gitignore` for Round 03 install logs and smoke outputs.
- Added `experiments/run_model_pilot.sh`.
- Updated `experiments/run_all.sh` to run tests, build the real EXPECT sample, run the model pilot, and compile the paper.
- Updated `paper/sections/experimental_setup.tex` to distinguish leakage-control templates from the model-predicted edit pilot.
- Added a Results caveat that current tables are Round 02 leakage-control sanity checks only.

## Real GEC Model Outputs

Command:

```bash
.venv311/bin/python experiments/src/run_model_predictions.py \
  --sample-size 300 \
  --overwrite \
  --output results/model_predictions/expect_v1_model_predictions.jsonl \
  --metadata results/model_predictions/runtime_metadata.json
```

Outputs:

- `results/model_predictions/expect_v1_model_predictions.jsonl`: 600 rows.
- `results/model_predictions/runtime_metadata.json`: model versions, decoding, and CPU runtime metadata.

Models:

| Model key | Family | Model ID | Revision | License note | Changed / 300 | Reference copy / 300 | CPU time |
|---|---|---|---|---|---:|---:|---:|
| `gector_roberta_base` | sequence-to-edit | `gotutiyan/gector-roberta-base-5k` | `adaac6fb919431fb5a038b1e449055ae638613a4` | non-commercial only | 247 | 39 | 13.511s |
| `t5_base_grammar` | sequence-to-sequence | `vennify/t5-base-grammar-correction` | `9e4a09d21dca1072a69302df9261289d03c3ed78` | CC-BY-NC-SA-4.0 | 295 | 0 | 157.650s |

References were never copied as predictions; model predictions are generated from source sentences.

## Model Prediction Edit Extraction and Behavior Classification

Command:

```bash
.venv311/bin/python experiments/src/analyze_model_edits.py \
  --predictions results/model_predictions/expect_v1_model_predictions.jsonl \
  --out-dir results/model_edits \
  --check-size 30
```

Outputs:

- `results/model_edits/model_edit_dataset.jsonl`: 1707 model-produced predicted edits.
- `results/model_edits/missing_edit_diagnosis.jsonl`: 319 missed reference edits.
- `results/model_edits/per_sentence_alignment.jsonl`: 600 source/reference/prediction alignment summaries.
- `results/model_edits/behavior_summary.json`: model and error-type behavior distributions.
- `results/model_edits/model_edit_alignment_check_30.md`: 30 readable checks, balanced across the two models.
- `results/model_edits/alignment_failures.jsonl`: 6 ambiguous alignment cases.

Behavior distribution:

| Model | Correct Correction | Wrong Correction | Overcorrection | Missed Correction |
|---|---:|---:|---:|---:|
| `gector_roberta_base` | 142 | 37 | 493 | 141 |
| `t5_base_grammar` | 71 | 71 | 893 | 178 |

Important caveat: T5 has many `R:ORTH` overcorrections from punctuation and spacing normalization. This is retained as a real raw-output issue and should get a normalization ablation rather than being silently removed.

## Model Edit-Level Dataset Schema

`results/model_edits/model_edit_dataset.jsonl` stores one row per actual predicted edit:

```json
{
  "sample_id": "...",
  "source": "...",
  "reference": "...",
  "prediction": "...",
  "model": "...",
  "predicted_edit": {"start": 0, "end": 1, "source_text": "...", "target_text": "...", "operation": "...", "error_type": "..."},
  "aligned_reference_edit": null,
  "behavior": "correct_correction | wrong_correction | overcorrection",
  "error_type": "..."
}
```

Missed corrections are stored separately in `results/model_edits/missing_edit_diagnosis.jsonl`.

## Explanation Source Audit

EXPECT field audit is stored in `docs/expect_field_audit.md`.

Conclusion:

- EXPECT contains source, target, correction index, evidence index, error type, predicted parsing order, and origin fields.
- `evidence_index` and `error_type` are real explanation-adjacent labels.
- EXPECT does not contain direct free-text natural-language explanations in the inspected JSONL files.
- `predicted_parsing_order` is not a human natural-language explanation.
- Round 02 templates remain leakage controls only.

Open-source candidate generation command:

```bash
.venv311/bin/python experiments/src/generate_model_edit_explanations.py \
  --limit 300 \
  --batch-size 8 \
  --output data/processed/model_edit_explanation_candidates.jsonl \
  --stats data/processed/model_edit_explanation_candidate_stats.json
```

Outputs:

- `data/processed/model_edit_explanation_candidates.jsonl`: 300 FLAN-T5-base explanation candidates, balanced 150 per GEC model.
- `data/processed/model_edit_explanation_candidate_stats.json`: generator revision `7bcac572ce56db69c1ea7c8af255c5d7c9672fc2`, Apache 2.0 model card, 109.459s CPU runtime.
- `results/model_explanations/explanation_candidate_check_30.md`: candidate quality inspection.
- `results/model_explanations/explanation_candidate_quality_flags.json`: rough automatic quality flags.

Quality conclusion: FLAN candidates are a runnable open-source explanation source, but the first audit shows generic and few-shot-copy-like outputs. They are candidates, not gold, and should not become the final main explanation source without filtering or replacement.

## Focused Literature Pass

Stored in `docs/literature_round03.md` and summarized in `docs/literature_matrix.md`.

Closest checked works:

1. GEE! Grammar Error Explanation with Large Language Models.
2. Controlled Generation with Prompt Insertion for Natural Language Explanations in GEC.
3. EXCGEC: edit-wise explainable Chinese GEC.

Current conclusion: a leakage-aware edit reconstruction diagnostic for model-produced English GEC edits remains a plausible contribution, but the manuscript must not use "first" or "novel" until a final systematic related-work pass is complete. Also, reconstruction should be framed as explanation-to-edit consistency, not proof of internal model reasoning.

## Next Single Action

Run the reconstruction and leakage-control baselines on `results/model_edits/model_edit_dataset.jsonl` using FLAN candidates, shuffled candidates, raw edit strings, and explicit-template upper controls; report them separately from Round 02 template results.
