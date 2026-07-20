# Qwen3 Evidence Refinement Smoke Audit

## Loop

- Loop ID: Loop C / targeted evidence refinement smoke.
- Bottleneck: Qwen3 prompt-v2 reduces prediction-only evidence but still misses contextual source evidence.
- Hypothesis: an evidence-only repair prompt can improve contextual SOURCE evidence without adding target/prediction leakage.
- Success criterion: selected refined outputs increase contextual evidence and do not increase prediction-only evidence.

## Summary

- `generated_at`: 2026-07-20T12:36:47+00:00
- `git_commit`: 4831728
- `prompt_version`: rulefaith_qwen3_evidence_refine_v2_compact_source_only_json
- `input_count`: 10
- `selected_for_refinement_count`: 7
- `refined_count`: 7
- `parse_status_counts`: `{'parsed_json': 7}`
- `original_full`: `{'contextual_source_evidence': 3, 'missing_evidence': 7, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 6}`
- `selected_before`: `{'contextual_source_evidence': 0, 'missing_evidence': 7, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 6}`
- `selected_after`: `{'contextual_source_evidence': 0, 'missing_evidence': 7, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 0}`
- `full_after_replacing_selected`: `{'contextual_source_evidence': 3, 'missing_evidence': 7, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 0}`
- `improvement_counts`: `{'evidence_contextual_improved': 0, 'wrong_evidence_fixed': 6, 'prediction_only_evidence_regressed': 0}`
- `decision`: revise_refinement_prompt_before_scaling
- `input_file`: /Users/bytedance/Documents/GEC可解释性/results/rulefaith/qwen3_v2_smoke10_candidates.jsonl
- `output_file`: /Users/bytedance/Documents/GEC可解释性/results/rulefaith/qwen3_v2_smoke10_evidence_refined_candidates.jsonl
- `dry_run`: False
- `selected_original_candidate_ids`: ['rf-edit-0276::qwen3_8b::natural', 'rf-edit-0277::qwen3_8b::natural', 'rf-edit-0074::qwen3_8b::natural', 'rf-edit-0016::qwen3_8b::natural', 'rf-edit-0167::qwen3_8b::natural', 'rf-edit-0231::qwen3_8b::natural', 'rf-edit-0248::qwen3_8b::natural']

## Refined Cases

### rf-edit-0276::qwen3_8b::natural::evidence_refined

- original: `rf-edit-0276::qwen3_8b::natural`; parse: `parsed_json`; latency: `22.4038`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Articles like 'the' may be omitted when referring to general time periods or categories.
- evidence: `[]`
- rationale: The article 'the' before 'latter half of the 20th century' is stylistically optional when referring to a general time period. Removing it results in a more concise and natural phrasing.

### rf-edit-0277::qwen3_8b::natural::evidence_refined

- original: `rf-edit-0277::qwen3_8b::natural`; parse: `parsed_json`; latency: `21.2785`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Nouns requiring articles (the, a, an) should be preceded by them when referring to specific or general concepts.
- evidence: `[]`
- rationale: The noun 'streets' in the original sentence lacks an article, making the phrase less grammatically complete. While the sentence is understandable without 'the', adding 'the' improves clarity and adheres to standard article usage conventions. This is considered a stylistic enhancement rather than a grammatical necessity.

### rf-edit-0074::qwen3_8b::natural::evidence_refined

- original: `rf-edit-0074::qwen3_8b::natural`; parse: `parsed_json`; latency: `25.7156`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Subject-verb agreement requires the auxiliary verb 'are' to be used with the present participle 'launcing' when the subject is plural.
- evidence: `[]`
- rationale: The sentence contains a plural subject 'many automobile companies' followed by the present participle 'launcing', which requires the auxiliary verb 'are' to form the correct present continuous tense. The absence of 'are' makes the sentence grammatically incorrect.

### rf-edit-0016::qwen3_8b::natural::evidence_refined

- original: `rf-edit-0016::qwen3_8b::natural`; parse: `parsed_json`; latency: `19.9787`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Articles 'a' and 'an' should agree with the following noun in terms of count and sound.
- evidence: `[]`
- rationale: The article 'an' is incorrectly used before the plural noun 'experts'. 'An' is used before singular nouns that begin with a vowel sound, while 'experts' is plural and does not require an article. The correct article would be 'the' if referring to specific experts, or the article could be omitted if the sentence is general.

### rf-edit-0167::qwen3_8b::natural::evidence_refined

- original: `rf-edit-0167::qwen3_8b::natural`; parse: `parsed_json`; latency: `17.324`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: A comma should follow an introductory phrase or clause when it is followed by a main clause.
- evidence: `[]`
- rationale: The phrase 'For example' is an introductory phrase that precedes a main clause. Adding a comma after it improves readability and adheres to standard punctuation conventions for such constructions.

### rf-edit-0231::qwen3_8b::natural::evidence_refined

- original: `rf-edit-0231::qwen3_8b::natural`; parse: `parsed_json`; latency: `20.098`
- before: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 3, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch;invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Use 'is to' to introduce a purpose or goal clause following a noun phrase.
- evidence: `[]`
- rationale: The original sentence uses 'should' to express a recommendation, but the model edit changes it to 'is to', which introduces a goal clause. However, the evidence provided in the original JSON does not correctly reference SOURCE tokens and contains index_text_mismatch and invalid_indices errors. Therefore, the evidence is unreliable and cannot support the edit.

### rf-edit-0248::qwen3_8b::natural::evidence_refined

- original: `rf-edit-0248::qwen3_8b::natural`; parse: `parsed_json`; latency: `24.0842`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Pronouns should clearly refer to their antecedents and maintain grammatical consistency.
- evidence: `[]`
- rationale:
