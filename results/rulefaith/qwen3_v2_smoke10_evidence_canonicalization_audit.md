# Evidence Span Canonicalization Audit

This deterministic pass repairs evidence span offsets when the cited text can be located in SOURCE. It does not judge whether the rule is linguistically correct.

## Summary

- `generated_at`: `2026-07-20T12:38:08+00:00`
- `git_commit`: `4831728`
- `input_count`: `10`
- `canonicalized_count`: `10`
- `action_counts`: `{'corrected_ambiguous_indices': 1, 'dropped_unlocatable_span': 1, 'corrected_indices': 7}`
- `before`: `{'contextual_source_evidence': 3, 'missing_evidence': 7, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 6}`
- `after`: `{'contextual_source_evidence': 8, 'missing_evidence': 2, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 0}`
- `improvement_counts`: `{'evidence_contextual_improved': 5, 'wrong_evidence_fixed': 6, 'prediction_only_evidence_regressed': 0}`
- `decision`: `keep_canonicalizer_as_span_normalization_step_before_model_refinement`
- `input_file`: `/Users/bytedance/Documents/GEC可解释性/results/rulefaith/qwen3_v2_smoke10_candidates.jsonl`
- `output_file`: `/Users/bytedance/Documents/GEC可解释性/results/rulefaith/qwen3_v2_smoke10_evidence_canonicalized_candidates.jsonl`

## Changed Cases

### rf-edit-0276::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0276::qwen3_8b::natural`
- actions: `{'corrected_ambiguous_indices': 1, 'dropped_unlocatable_span': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 9, "role": "article", "start": 8, "text": "the"}]`

### rf-edit-0277::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0277::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 12, "role": "noun", "start": 11, "text": "streets"}]`

### rf-edit-0074::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0074::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 38, "role": "subject_verb_phrase", "start": 34, "text": "many automobile companies launcing"}]`

### rf-edit-0016::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0016::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 17, "role": "article", "start": 16, "text": "an"}, {"end": 18, "role": "noun", "start": 17, "text": "experts"}]`

### rf-edit-0167::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0167::qwen3_8b::natural`
- actions: `{'corrected_indices': 1}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 2, "role": "introductory_phrase", "start": 0, "text": "For example"}]`

### rf-edit-0231::qwen3_8b::natural::evidence_canonicalized

- original: `rf-edit-0231::qwen3_8b::natural`
- actions: `{'corrected_indices': 3}`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 3, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch;invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 3, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 3, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- evidence: `[{"end": 1, "role": "subject", "start": 0, "text": "Everyone"}, {"end": 3, "role": "verb", "start": 2, "text": "develop"}, {"end": 8, "role": "object", "start": 3, "text": "their awareness of public manner"}]`
