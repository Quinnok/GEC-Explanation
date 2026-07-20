# Evidence Span Canonicalization Audit

This deterministic pass repairs evidence span offsets when the cited text can be located in SOURCE. It does not judge whether the rule is linguistically correct.

## Summary

- `generated_at`: `2026-07-20T12:41:18+00:00`
- `git_commit`: `4831728`
- `input_count`: `63`
- `canonicalized_count`: `63`
- `action_counts`: `{'dropped_prediction_only_span': 33, 'corrected_indices': 36, 'corrected_ambiguous_indices': 8, 'kept_unverified_span': 4}`
- `before`: `{'contextual_source_evidence': 10, 'missing_evidence': 53, 'prediction_only_evidence': 46, 'wrong_evidence_auto': 52}`
- `after`: `{'contextual_source_evidence': 19, 'missing_evidence': 44, 'prediction_only_evidence': 16, 'wrong_evidence_auto': 16}`
- `improvement_counts`: `{'evidence_contextual_improved': 9, 'wrong_evidence_fixed': 36, 'prediction_only_evidence_regressed': 0}`
- `decision`: `keep_canonicalizer_as_span_normalization_step_before_model_refinement`
- `input_file`: `/Users/bytedance/Documents/GEC可解释性/data/rulefaith/filtering/qwen3_8b_refine.jsonl`
- `output_file`: `/Users/bytedance/Documents/GEC可解释性/data/rulefaith/filtering/qwen3_8b_refine_canonicalized.jsonl`

## Changed Cases

### rf-edit-0023::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0023::qwen3_8b::natural`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 25, "role": "source", "start": 23, "text": "in specializing"}]`

### rf-edit-0023::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0023::qwen3_8b::rule_grounded`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 25, "role": "source", "start": 23, "text": "in specializing"}]`

### rf-edit-0024::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0024::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 26, "role": "source", "start": 0, "text": "Thus in concordance with the above I agree whole heartedly that in twenty years there will be fewer cars in use than there are today ."}]`

### rf-edit-0024::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0024::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 26, "role": "source", "start": 0, "text": "Thus in concordance with the above I agree whole heartedly that in twenty years there will be fewer cars in use than there are today ."}]`

### rf-edit-0034::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0034::qwen3_8b::natural`
- actions: `{'corrected_ambiguous_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 15, "role": "error", "start": 14, "text": "pot"}]`

### rf-edit-0034::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0034::qwen3_8b::rule_grounded`
- actions: `{'corrected_ambiguous_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 15, "role": "error", "start": 14, "text": "pot"}]`

### rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0035::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 17, "role": "target", "start": 16, "text": "peoples"}]`

### rf-edit-0051::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0051::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 28, "role": "target", "start": 24, "text": "Caring of the environment"}]`

### rf-edit-0051::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0051::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 28, "role": "target", "start": 24, "text": "Caring of the environment"}]`

### rf-edit-0052::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0052::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'invalid_indices;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 5, "role": "source", "start": 4, "text": "unmeaningful"}]`

### rf-edit-0058::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0058::qwen3_8b::natural`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 1, "role": "source", "start": 0, "text": "Variety"}]`

### rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0058::qwen3_8b::rule_grounded`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 1, "role": "modified", "start": 0, "text": "Variety"}]`

### rf-edit-0068::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0068::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "original", "start": 10, "text": "almost"}]`

### rf-edit-0074::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0074::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 38, "role": "source", "start": 34, "text": "many automobile companies launcing"}]`

### rf-edit-0074::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0074::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 38, "role": "target", "start": 34, "text": "many automobile companies launcing"}]`

### rf-edit-0081::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0081::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;invalid_indices;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 6, "role": "source", "start": 0, "text": "He has ever been with me"}]`

### rf-edit-0107::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0107::qwen3_8b::natural`
- actions: `{'corrected_ambiguous_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 33, "role": "error", "start": 32, "text": "pot"}]`

### rf-edit-0107::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0107::qwen3_8b::rule_grounded`
- actions: `{'corrected_ambiguous_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 33, "role": "error", "start": 32, "text": "pot"}]`

### rf-edit-0111::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0111::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'invalid_indices;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 8, "role": "error", "start": 7, "text": "champion"}]`

### rf-edit-0111::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0111::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'invalid_indices;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 8, "role": "error", "start": 7, "text": "champion"}]`

### rf-edit-0114::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0114::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 8, "role": "source", "start": 7, "text": "understand"}]`

### rf-edit-0123::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0123::qwen3_8b::natural`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 7, "role": "source", "start": 5, "text": "subjects ."}]`

### rf-edit-0123::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0123::qwen3_8b::rule_grounded`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 7, "role": "original", "start": 5, "text": "subjects ."}]`

### rf-edit-0126::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0126::qwen3_8b::natural`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 33, "role": "source", "start": 31, "text": "jobs ."}]`

### rf-edit-0126::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0126::qwen3_8b::rule_grounded`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 33, "role": "original", "start": 31, "text": "jobs ."}]`

### rf-edit-0127::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0127::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 28, "role": "target", "start": 24, "text": "Caring of the environment"}]`

### rf-edit-0127::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0127::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 28, "role": "target", "start": 24, "text": "Caring of the environment"}]`

### rf-edit-0138::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0138::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 10, "role": "modified_text", "start": 9, "text": "civilization"}]`

### rf-edit-0138::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0138::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 10, "role": "modified_text", "start": 9, "text": "civilization"}]`

### rf-edit-0141::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0141::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 6, "role": "error", "start": 5, "text": "nocive"}]`

### rf-edit-0141::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0141::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 6, "role": "original", "start": 5, "text": "nocive"}]`

### rf-edit-0163::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0163::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;prediction_or_target_role;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 8, "role": "target", "start": 7, "text": "on"}]`

### rf-edit-0165::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0165::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 18, "role": "target", "start": 14, "text": "as well as positive"}]`

### rf-edit-0207::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0207::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 17, "role": "source", "start": 0, "text": "One person if do n't have good health that means so many things they could lost ."}]`

### rf-edit-0207::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0207::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 17, "role": "source", "start": 0, "text": "One person if do n't have good health that means so many things they could lost ."}]`

### rf-edit-0225::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0225::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 24, "role": "source", "start": 0, "text": "Third the butt it in hte front of the door of store to make the poeple see it even if it is not good"}]`

### rf-edit-0234::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0234::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 9, "role": "error", "start": 8, "text": "agricultures"}]`

### rf-edit-0234::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0234::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 9, "role": "error", "start": 8, "text": "agricultures"}]`

### rf-edit-0236::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0236::qwen3_8b::natural`
- actions: `{'kept_unverified_span': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 14, "role": "source", "start": 12, "text": "latter 1/2"}]`

### rf-edit-0236::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0236::qwen3_8b::rule_grounded`
- actions: `{'kept_unverified_span': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 14, "role": "source", "start": 12, "text": "latter 1/2"}]`

### rf-edit-0248::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0248::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 16, "role": "source", "start": 0, "text": "I 'd like to tell you about my favorite restaurant its name is \" Lemon \""}, {"end": 6, "role": "target", "start": 0, "text": "I 'd like to tell you"}]`

### rf-edit-0255::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0255::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 8, "role": "token", "start": 7, "text": "sister"}]`

### rf-edit-0255::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0255::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 8, "role": "token", "start": 7, "text": "sister"}]`

### rf-edit-0257::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0257::qwen3_8b::natural`
- actions: `{'corrected_indices': 2}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 33, "role": "source", "start": 32, "text": "example"}, {"end": 33, "role": "target", "start": 32, "text": "example"}]`

### rf-edit-0257::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0257::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 33, "role": "target", "start": 32, "text": "example"}]`

### rf-edit-0261::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0261::qwen3_8b::natural`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 14, "role": "source", "start": 13, "text": "1/2"}]`

### rf-edit-0261::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0261::qwen3_8b::rule_grounded`
- actions: `{'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 14, "role": "replaced_text", "start": 13, "text": "1/2"}]`

### rf-edit-0267::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0267::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 18, "role": "target", "start": 17, "text": "positive"}]`

### rf-edit-0268::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0268::qwen3_8b::rule_grounded`
- actions: `{'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 75, "role": "target", "start": 69, "text": "computer ed finally the internet.our grandparents"}]`

### rf-edit-0277::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0277::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 12, "role": "target", "start": 11, "text": "streets"}]`

### rf-edit-0284::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0284::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 8, "role": "source", "start": 7, "text": "city"}]`

### rf-edit-0284::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0284::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 8, "role": "modified", "start": 7, "text": "city"}]`

### rf-edit-0292::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0292::qwen3_8b::natural`
- actions: `{'corrected_ambiguous_indices': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 64, "role": "token", "start": 63, "text": "sauce"}]`

### rf-edit-0292::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0292::qwen3_8b::rule_grounded`
- actions: `{'corrected_ambiguous_indices': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 64, "role": "token", "start": 63, "text": "sauce"}]`

### rf-edit-0294::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0294::qwen3_8b::natural`
- actions: `{'corrected_ambiguous_indices': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 72, "role": "token", "start": 71, "text": "there"}]`

### rf-edit-0294::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0294::qwen3_8b::rule_grounded`
- actions: `{'corrected_ambiguous_indices': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 72, "role": "token", "start": 71, "text": "there"}]`
