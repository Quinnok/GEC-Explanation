# Round 07 Benchmark Card

Generated: `2026-07-18T05:42:47+00:00`

This benchmark is an automatic, model-edit-level pilot for GEC explanation faithfulness. Each edit record corresponds to an edit actually produced by a public GEC model, not to a reference edit used as a prediction.

## Scope

- Edit records: 700
- Explanation instances: 12754
- Missing-edit diagnoses: 160
- Human gold labels: 0
- Dataset counts: `{"EXPECT": 420, "JFLEG": 280}`
- Model counts: `{"coedit_large": 122, "gector_roberta_base": 298, "t5_base_grammar": 280}`
- Model-family counts: `{"instruction-following text editor": 122, "sequence-to-edit": 298, "sequence-to-sequence": 280}`
- Behavior counts: `{"correct_correction": 136, "overcorrection": 438, "wrong_correction": 126}`
- Operation counts: `{"delete": 58, "insert": 115, "replace": 527}`
- ERRANT error-type count: 41
- Split counts: `{"dev": 80, "test": 134, "train": 486}`

## Explanation Sources

- `explicit_template`: automatic leakage upper control copied from structured edit fields.
- `masked_target_template`: automatic target-masked leakage control.
- `rule_only`, `gee_style_automatic`, `rule_grounded_automatic`: automatic rule templates from ERRANT type/source span.
- `flan_t5_candidate`: open-source generated candidate, not gold.
- Negative controls: wrong span/source token/target/operation/direction/error type/rule/evidence, cross-sentence swaps, generic, partial, and pending counterfactual inconsistency seeds.
- `faithful_wrong_model_edit`: positive for model-behavior faithfulness only; it says the explanation matches what the model did, not that the edit is grammatically correct.

## Explanation Type Counts

| Item | Count |
|---|---:|
| `counterfactually_inconsistent_seed` | 700 |
| `explicit_template` | 700 |
| `faithful_wrong_model_edit` | 564 |
| `flan_t5_candidate` | 290 |
| `gee_style_automatic` | 700 |
| `generic` | 700 |
| `masked_target_template` | 700 |
| `partially_correct` | 700 |
| `rule_grounded_automatic` | 700 |
| `rule_only` | 700 |
| `swapped_across_sentence` | 700 |
| `wrong_direction` | 700 |
| `wrong_error_type` | 700 |
| `wrong_evidence` | 700 |
| `wrong_operation` | 700 |
| `wrong_rule` | 700 |
| `wrong_source_token` | 700 |
| `wrong_span` | 700 |
| `wrong_target` | 700 |

## Negative Type Counts

| Item | Count |
|---|---:|
| `counterfactual_inconsistent_pending` | 700 |
| `generic` | 700 |
| `partially_correct` | 700 |
| `swapped_across_sentence` | 700 |
| `wrong_direction` | 700 |
| `wrong_error_type` | 700 |
| `wrong_evidence` | 700 |
| `wrong_operation` | 700 |
| `wrong_rule` | 700 |
| `wrong_source_token` | 700 |
| `wrong_span` | 700 |
| `wrong_target` | 700 |

## Leakage Controls

- Source cross-split duplicates: 0
- Repeated predicted targets across splits: 32
- Template near-duplicate risk is expected for automatic controls and is recorded in `data/faithfulness_benchmark/leakage_audit.json`.
- Primary claims must be stratified by explanation type; explicit templates and raw edit strings cannot dominate aggregate results.
- Counterfactual inconsistency seeds are placeholders until Round 08 reruns the original GEC models on counterfactual sources.

## Behavior Summaries

- EXPECT GECToR/T5 behavior: `{"gector_roberta_base": {"correct_correction": 142, "missed_correction": 141, "overcorrection": 493, "wrong_correction": 37}, "t5_base_grammar": {"correct_correction": 71, "missed_correction": 178, "overcorrection": 893, "wrong_correction": 71}}`
- JFLEG GECToR/T5 behavior: `{"gector_roberta_base": {"correct_correction": 104, "missed_correction": 177, "overcorrection": 51, "wrong_correction": 85}, "t5_base_grammar": {"correct_correction": 76, "missed_correction": 201, "overcorrection": 135, "wrong_correction": 89}}`
- EXPECT CoEdIT behavior: `{"coedit_large": {"correct_correction": 10, "missed_correction": 8, "overcorrection": 108, "wrong_correction": 4}}`

## Files

- `data/faithfulness_benchmark/edit_records.jsonl`
- `data/faithfulness_benchmark/explanation_instances.jsonl`
- `data/faithfulness_benchmark/missing_edit_diagnosis.jsonl`
- `data/faithfulness_benchmark/benchmark_stats.json`
- `data/faithfulness_benchmark/leakage_audit.json`
