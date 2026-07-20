# Evidence Span Canonicalization Audit

This deterministic pass repairs evidence span offsets when the cited text can be located in SOURCE. It does not judge whether the rule is linguistically correct.

## Summary

- `generated_at`: `2026-07-20T12:41:18+00:00`
- `git_commit`: `4831728`
- `input_count`: `41`
- `canonicalized_count`: `41`
- `action_counts`: `{'corrected_indices': 36, 'dropped_prediction_only_span': 19, 'corrected_ambiguous_indices': 4, 'kept_unverified_span': 6, 'dropped_unlocatable_span': 2}`
- `before`: `{'contextual_source_evidence': 0, 'missing_evidence': 41, 'prediction_only_evidence': 22, 'wrong_evidence_auto': 39}`
- `after`: `{'contextual_source_evidence': 15, 'missing_evidence': 26, 'prediction_only_evidence': 5, 'wrong_evidence_auto': 5}`
- `improvement_counts`: `{'evidence_contextual_improved': 15, 'wrong_evidence_fixed': 34, 'prediction_only_evidence_regressed': 0}`
- `decision`: `keep_canonicalizer_as_span_normalization_step_before_model_refinement`
- `input_file`: `/Users/bytedance/Documents/GEC可解释性/data/rulefaith/filtering/qwen3_8b_accepted.jsonl`
- `output_file`: `/Users/bytedance/Documents/GEC可解释性/data/rulefaith/filtering/qwen3_8b_accepted_canonicalized.jsonl`

## Changed Cases

### rf-edit-0016::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0016::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 21, "role": "original", "start": 12, "text": "and they will become an experts in those areas"}]`

### rf-edit-0016::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0016::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 21, "role": "original", "start": 13, "text": "they will become an experts in those areas"}]`

### rf-edit-0021::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0021::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'invalid_indices;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 25, "role": "error", "start": 23, "text": "or country"}]`

### rf-edit-0021::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0021::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'invalid_indices;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 25, "role": "error_span", "start": 22, "text": "in or country"}]`

### rf-edit-0026::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0026::qwen3_8b::natural`
- actions: `{'dropped_prediction_only_span': 1, 'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 29, "role": "pronoun", "start": 28, "text": "its"}]`

### rf-edit-0026::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0026::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 2}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 20, "role": "antecedent", "start": 18, "text": "international companies"}, {"end": 29, "role": "pronoun", "start": 28, "text": "its"}]`

### rf-edit-0033::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0033::qwen3_8b::natural`
- actions: `{'dropped_prediction_only_span': 2}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'invalid_indices;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[]`

### rf-edit-0052::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0052::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'invalid_indices;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 6, "role": "original", "start": 0, "text": "because they spent time unmeaningful subjects"}]`

### rf-edit-0062::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0062::qwen3_8b::natural`
- actions: `{'corrected_ambiguous_indices': 1, 'corrected_indices': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 16, "role": "antecedent", "start": 15, "text": "this"}, {"end": 6, "role": "antecedent", "start": 5, "text": "problem"}]`

### rf-edit-0062::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0062::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'corrected_ambiguous_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 6, "role": "antecedent", "start": 5, "text": "problem"}, {"end": 16, "role": "repetition", "start": 15, "text": "this"}]`

### rf-edit-0068::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0068::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 2}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "error", "start": 10, "text": "almost"}, {"end": 13, "role": "spelling", "start": 12, "text": "doens't"}]`

### rf-edit-0077::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0077::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "subject", "start": 9, "text": "public area"}]`

### rf-edit-0077::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0077::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "subject", "start": 9, "text": "public area"}]`

### rf-edit-0081::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0081::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;invalid_indices;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 6, "role": "error", "start": 0, "text": "He has ever been with me"}]`

### rf-edit-0092::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0092::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 28, "role": "error", "start": 21, "text": "it has different food to other restaurants"}]`

### rf-edit-0092::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0092::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 28, "role": "error", "start": 21, "text": "it has different food to other restaurants"}]`

### rf-edit-0114::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0114::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_only_text;prediction_or_target_role;text_not_in_source', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 8, "role": "target", "start": 7, "text": "understand"}]`

### rf-edit-0118::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0118::qwen3_8b::natural`
- actions: `{'corrected_indices': 2}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch;invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 14, "role": "original_clause", "start": 7, "text": "that we looked up through the trees"}, {"end": 22, "role": "dependent_clause", "start": 14, "text": "we saw how low the forest had swung"}]`

### rf-edit-0118::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0118::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 22, "role": "clause", "start": 6, "text": "except that we looked up through the trees we saw how low the forest had swung"}]`

### rf-edit-0151::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0151::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 17, "role": "affected_span", "start": 14, "text": "leads dark future"}]`

### rf-edit-0151::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0151::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 17, "role": "affected_span", "start": 14, "text": "leads dark future"}]`

### rf-edit-0163::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0163::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 10, "role": "original", "start": 1, "text": "have had a most significant impact on the people"}, {"end": 13, "role": "modified", "start": 7, "text": "on the people in the latter"}]`

### rf-edit-0165::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0165::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 18, "role": "affected", "start": 14, "text": "as well as positive"}]`

### rf-edit-0170::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0170::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "noun", "start": 10, "text": "Museum"}]`

### rf-edit-0170::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0170::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "noun", "start": 10, "text": "Museum"}]`

### rf-edit-0191::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0191::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 21, "role": "original", "start": 12, "text": "and they will become an experts in those areas"}, {"end": 18, "role": "modified", "start": 16, "text": "an experts"}]`

### rf-edit-0191::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0191::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 21, "role": "original", "start": 13, "text": "they will become an experts in those areas"}, {"end": 18, "role": "modified", "start": 16, "text": "an experts"}]`

### rf-edit-0199::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0199::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "error", "start": 7, "text": "interested at the environment"}]`

### rf-edit-0199::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0199::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "error_span", "start": 7, "text": "interested at the environment"}]`

### rf-edit-0225::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0225::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 24, "role": "original", "start": 0, "text": "Third the butt it in hte front of the door of store to make the poeple see it even if it is not good"}]`

### rf-edit-0248::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0248::qwen3_8b::natural`
- actions: `{'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- evidence: `[{"end": 16, "role": "original", "start": 10, "text": "its name is \" Lemon \""}, {"end": 16, "role": "modified", "start": 10, "text": "its name is \" Lemon \""}]`

### rf-edit-0264::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0264::qwen3_8b::natural`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "error", "start": 7, "text": "interested at the environment"}]`

### rf-edit-0264::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0264::qwen3_8b::rule_grounded`
- actions: `{'corrected_indices': 1, 'dropped_prediction_only_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 2, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'index_text_mismatch;prediction_only_text', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 11, "role": "error_span", "start": 7, "text": "interested at the environment"}]`

### rf-edit-0265::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0265::qwen3_8b::natural`
- actions: `{'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 17, "role": "deleted_text", "start": 16, "text": "is"}]`

### rf-edit-0265::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0265::qwen3_8b::rule_grounded`
- actions: `{'kept_unverified_span': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 17, "role": "error", "start": 16, "text": "is"}]`

### rf-edit-0267::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0267::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 18, "role": "affected_span", "start": 14, "text": "as well as positive"}]`

### rf-edit-0276::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0276::qwen3_8b::natural`
- actions: `{'corrected_ambiguous_indices': 1, 'dropped_unlocatable_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 9, "role": "deleted", "start": 8, "text": "the"}]`

### rf-edit-0276::qwen3_8b::rule_grounded::evidence_canonicalized

- original: `rf-edit-0276::qwen3_8b::rule_grounded`
- actions: `{'corrected_ambiguous_indices': 1, 'dropped_unlocatable_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 9, "role": "deleted", "start": 8, "text": "the"}]`

### rf-edit-0277::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0277::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 12, "role": "noun", "start": 11, "text": "streets"}]`
