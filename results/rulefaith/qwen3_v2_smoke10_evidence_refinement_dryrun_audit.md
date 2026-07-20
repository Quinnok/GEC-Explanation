# Qwen3 Evidence Refinement Smoke Audit

## Loop

- Loop ID: Loop C / targeted evidence refinement smoke.
- Bottleneck: Qwen3 prompt-v2 reduces prediction-only evidence but still misses contextual source evidence.
- Hypothesis: an evidence-only repair prompt can improve contextual SOURCE evidence without adding target/prediction leakage.
- Success criterion: selected refined outputs increase contextual evidence and do not increase prediction-only evidence.

## Summary

- `generated_at`: 2026-07-20T12:28:30+00:00
- `git_commit`: 4831728
- `prompt_version`: rulefaith_qwen3_evidence_refine_v1_source_only
- `input_count`: 10
- `selected_for_refinement_count`: 7
- `refined_count`: 0
- `parse_status_counts`: `{}`
- `original_full`: `{'contextual_source_evidence': 3, 'missing_evidence': 7, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 6}`
- `selected_before`: `{'contextual_source_evidence': 0, 'missing_evidence': 7, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 6}`
- `selected_after`: `{'contextual_source_evidence': 0, 'missing_evidence': 0, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 0}`
- `full_after_replacing_selected`: `{'contextual_source_evidence': 3, 'missing_evidence': 7, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 6}`
- `improvement_counts`: `{'evidence_contextual_improved': 0, 'wrong_evidence_fixed': 0, 'prediction_only_evidence_regressed': 0}`
- `decision`: revise_refinement_prompt_before_scaling
- `input_file`: /Users/bytedance/Documents/GEC可解释性/results/rulefaith/qwen3_v2_smoke10_candidates.jsonl
- `output_file`: /Users/bytedance/Documents/GEC可解释性/results/rulefaith/qwen3_v2_smoke10_evidence_refined_candidates.jsonl
- `dry_run`: True
- `selected_original_candidate_ids`: ['rf-edit-0276::qwen3_8b::natural', 'rf-edit-0277::qwen3_8b::natural', 'rf-edit-0074::qwen3_8b::natural', 'rf-edit-0016::qwen3_8b::natural', 'rf-edit-0167::qwen3_8b::natural', 'rf-edit-0231::qwen3_8b::natural', 'rf-edit-0248::qwen3_8b::natural']

## Refined Cases
