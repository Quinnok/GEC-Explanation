# Evidence Span Canonicalization Audit

This deterministic pass repairs evidence span offsets when the cited text can be located in SOURCE. It does not judge whether the rule is linguistically correct.

## Summary

- `generated_at`: `2026-07-20T12:41:18+00:00`
- `git_commit`: `4831728`
- `input_count`: `56`
- `canonicalized_count`: `56`
- `action_counts`: `{'corrected_indices': 34, 'dropped_prediction_only_span': 11, 'corrected_ambiguous_indices': 4, 'kept_unverified_span': 11}`
- `before`: `{'contextual_source_evidence': 14, 'missing_evidence': 42, 'prediction_only_evidence': 19, 'wrong_evidence_auto': 50}`
- `after`: `{'contextual_source_evidence': 48, 'missing_evidence': 8, 'prediction_only_evidence': 8, 'wrong_evidence_auto': 8}`
- `improvement_counts`: `{'evidence_contextual_improved': 34, 'wrong_evidence_fixed': 42, 'prediction_only_evidence_regressed': 0}`
- `decision`: `keep_canonicalizer_as_span_normalization_step_before_model_refinement`
- `input_file`: `/Users/bytedance/Documents/GEC可解释性/data/rulefaith/filtering/qwen3_8b_rejected.jsonl`
- `output_file`: `/Users/bytedance/Documents/GEC可解释性/data/rulefaith/filtering/qwen3_8b_rejected_canonicalized.jsonl`

## Changed Cases

### rf-edit-0009::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0009::qwen3_8b::natural`
- actions: `{'corrected_indices': 2}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 3, "role": "subject", "start": 2, "text": "school"}, {"end": 4, "role": "verb", "start": 3, "text": "try"}]`

### rf-edit-0009::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0009::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 2}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 3, "role": "subject", "start": 2, "text": "school"}, {"end": 4, "role": "verb", "start": 3, "text": "try"}]`

### rf-edit-0025::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0025::qwen3_8b::natural`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[]`

### rf-edit-0025::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0025::qwen3_8b::rule_grounded`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[]`

### rf-edit-0033::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0033::qwen3_8b::rule_grounded`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[]`

### rf-edit-0039::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0039::qwen3_8b::natural`
- actions: `{'corrected_ambiguous_indices': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 16, "role": "redundant_conjunction", "start": 15, "text": "and"}]`

### rf-edit-0039::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0039::qwen3_8b::rule_grounded`
- actions: `{'corrected_ambiguous_indices': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 16, "role": "redundant_conjunction", "start": 15, "text": "and"}]`

### rf-edit-0056::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0056::qwen3_8b::natural`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 16, "role": "error", "start": 15, "text": "cigarrets"}]`

### rf-edit-0056::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0056::qwen3_8b::rule_grounded`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 16, "role": "error", "start": 15, "text": "cigarrets"}]`

### rf-edit-0125::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0125::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 30, "role": "edit_target", "start": 19, "text": "compared either to our parents ' or our grandparents ' lives"}]`

### rf-edit-0125::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0125::qwen3_8b::rule_grounded`
- actions: `{'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 25, "role": "target", "start": 20, "text": "either to our parents '"}]`

### rf-edit-0137::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0137::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 1, "role": "modified_text", "start": 0, "text": "Thus"}]`

### rf-edit-0137::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0137::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 1, "role": "modified_text", "start": 0, "text": "Thus"}]`

### rf-edit-0147::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0147::qwen3_8b::natural`
- actions: `{'corrected_indices': 2}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch;invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 20, "role": "dependent_clause", "start": 13, "text": "which is characterized by diversity and innovation"}, {"end": 13, "role": "main_clause", "start": 0, "text": "Specializing in one particular subject does not suit our life in this era"}]`

### rf-edit-0147::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0147::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 20, "role": "relative_clause", "start": 13, "text": "which is characterized by diversity and innovation"}]`

### rf-edit-0150::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0150::qwen3_8b::natural`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "error", "start": 10, "text": "scientifc"}]`

### rf-edit-0150::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0150::qwen3_8b::rule_grounded`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "error", "start": 10, "text": "scientifc"}]`

### rf-edit-0158::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0158::qwen3_8b::natural`
- actions: `{'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 18, "role": "introductory_phrase", "start": 0, "text": "Thus in concordance with the above I agree whole heartedly that in twenty years there will be fewer"}]`

### rf-edit-0158::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0158::qwen3_8b::rule_grounded`
- actions: `{'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 19, "role": "context", "start": 0, "text": "Thus in concordance with the above I agree whole heartedly that in twenty years there will be fewer cars"}]`

### rf-edit-0167::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0167::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 2, "role": "introductory_phrase", "start": 0, "text": "For example"}]`

### rf-edit-0167::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0167::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 2, "role": "introductory_phrase", "start": 0, "text": "For example"}]`

### rf-edit-0178::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0178::qwen3_8b::natural`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 9, "role": "error", "start": 7, "text": "manner ."}]`

### rf-edit-0178::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0178::qwen3_8b::rule_grounded`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 9, "role": "error", "start": 7, "text": "manner ."}]`

### rf-edit-0183::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0183::qwen3_8b::natural`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 44, "role": "original", "start": 42, "text": "material ."}]`

### rf-edit-0183::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0183::qwen3_8b::rule_grounded`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 44, "role": "original", "start": 42, "text": "material ."}]`

### rf-edit-0217::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0217::qwen3_8b::natural`
- actions: `{'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role;text_not_in_source', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 14, "role": "error", "start": 13, "text": "ablished"}, {"end": 14, "role": "correction", "start": 13, "text": "ablished"}]`

### rf-edit-0217::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0217::qwen3_8b::rule_grounded`
- actions: `{'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;text_not_in_source', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 14, "role": "error", "start": 13, "text": "ablished"}, {"end": 14, "role": "correct", "start": 13, "text": "ablished"}]`

### rf-edit-0242::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0242::qwen3_8b::natural`
- actions: `{'corrected_indices': 2}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 5, "role": "error", "start": 4, "text": "partyies"}, {"end": 14, "role": "correct", "start": 13, "text": "parties"}]`

### rf-edit-0242::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0242::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 2}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 5, "role": "error", "start": 4, "text": "partyies"}, {"end": 14, "role": "corrected", "start": 13, "text": "parties"}]`

### rf-edit-0250::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0250::qwen3_8b::natural`
- actions: `{'corrected_ambiguous_indices': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 35, "role": "target", "start": 34, "text": "village"}]`

### rf-edit-0250::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0250::qwen3_8b::rule_grounded`
- actions: `{'corrected_ambiguous_indices': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 35, "role": "target", "start": 34, "text": "village"}]`

### rf-edit-0251::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0251::qwen3_8b::natural`
- actions: `{'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 12, "role": "modified", "start": 11, "text": "streets"}]`

### rf-edit-0251::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0251::qwen3_8b::rule_grounded`
- actions: `{'kept_unverified_span': 2}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 12, "role": "target", "start": 11, "text": "streets"}, {"end": 12, "role": "source", "start": 11, "text": "streets"}]`

### rf-edit-0253::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0253::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 4, "role": "modified_text", "start": 3, "text": "family"}]`

### rf-edit-0253::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0253::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 4, "role": "clause", "start": 0, "text": "i love my family"}]`

### rf-edit-0262::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0262::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 23, "role": "modified_text", "start": 22, "text": "unfortunately"}]`

### rf-edit-0262::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0262::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 23, "role": "modified_text", "start": 22, "text": "unfortunately"}]`

### rf-edit-0268::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0268::qwen3_8b::natural`
- actions: `{'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 70, "role": "target", "start": 69, "text": "computer"}]`

### rf-edit-0273::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0273::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 3, "role": "introductory_phrase", "start": 0, "text": "In the end"}]`

### rf-edit-0273::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0273::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 3, "role": "clause", "start": 0, "text": "In the end"}]`

### rf-edit-0279::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0279::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 7, "role": "subordinating_conjunction", "start": 6, "text": "because"}]`

### rf-edit-0279::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0279::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 7, "role": "subordinating_conjunction", "start": 6, "text": "because"}]`

### rf-edit-0283::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0283::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 2, "role": "introductory_clause", "start": 0, "text": "Until dawn"}]`

### rf-edit-0283::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0283::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 2, "role": "introductory_clause", "start": 0, "text": "Until dawn"}]`

### rf-edit-0287::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0287::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 6, "role": "introduced_phrase", "start": 5, "text": "future"}]`

### rf-edit-0287::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0287::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 6, "role": "introduced_phrase", "start": 5, "text": "future"}]`

### rf-edit-0289::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0289::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "modified_text", "start": 10, "text": "finally"}]`

### rf-edit-0289::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0289::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "modified_text", "start": 10, "text": "finally"}]`

### rf-edit-0290::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0290::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 19, "role": "modified_text", "start": 18, "text": "normally"}]`

### rf-edit-0290::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0290::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 19, "role": "modified_text", "start": 18, "text": "normally"}]`

### rf-edit-0291::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0291::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 49, "role": "error", "start": 48, "text": "susage"}, {"end": 52, "role": "correct", "start": 48, "text": "susage and in order"}]`

### rf-edit-0291::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0291::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 49, "role": "error", "start": 48, "text": "susage"}, {"end": 52, "role": "correct", "start": 48, "text": "susage and in order"}]`
