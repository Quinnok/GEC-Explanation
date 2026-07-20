# Qwen3 Prompt-v2 Smoke10 Audit

## Summary

- `candidate_count`: 10
- `parse_status_counts`: {'parsed_json': 10}
- `dataset_counts`: {'EXPECT': 6, 'JFLEG': 4}
- `model_key_counts`: {'coedit_large': 4, 'gector_roberta_base': 3, 't5_base_grammar': 3}
- `operation_counts`: {'replace': 5, 'delete': 2, 'insert': 3}
- `source_span_match_count`: 10
- `target_present_in_prediction_count`: 10
- `evidence_span_index_match_count`: 6
- `evidence_all_spans_source_index_match_count`: 4
- `contextual_source_evidence_count`: 3
- `missing_evidence_count`: 7
- `prediction_only_evidence_count`: 0
- `wrong_evidence_auto_count`: 6
- `evidence_error_type_counts`: {'invalid_indices': 3, 'index_text_mismatch': 4}
- `interpretation`: Prompt-v2 smoke10 improves source-only behavior relative to prompt-v1, but contextual evidence remains weak and sample size is too small for method claims.

## Cases

### rf-edit-0251::qwen3_8b::natural

- parse: `parsed_json`; model: `coedit_large`; op: `replace`
- evidence: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- rule: Commas are used to separate independent clauses or items in a list.
- rationale: The addition of a comma after 'streets' serves to improve readability by separating the independent clause 'maybe cars will fly above the streets' from the following clause 'and computers will have totally changed'. While not strictly grammatically required, it is a stylistic choice that enhances clarity in complex sentences.

### rf-edit-0276::qwen3_8b::natural

- parse: `parsed_json`; model: `coedit_large`; op: `delete`
- evidence: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Articles like 'the' may be omitted when referring to general time periods or categories.
- rationale: The article 'the' before 'latter half of the 20th century' is stylistically optional when referring to a general time period. Removing it results in a more concise and natural phrasing.

### rf-edit-0277::qwen3_8b::natural

- parse: `parsed_json`; model: `coedit_large`; op: `insert`
- evidence: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Nouns requiring articles (the, a, an) should be preceded by them when referring to specific or general concepts.
- rationale: The noun 'streets' in the original sentence lacks an article, making the phrase less grammatically complete. While the sentence is understandable without 'the', adding 'the' improves clarity and adheres to standard article usage conventions. This is considered a stylistic enhancement rather than a grammatical necessity.

### rf-edit-0074::qwen3_8b::natural

- parse: `parsed_json`; model: `gector_roberta_base`; op: `insert`
- evidence: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Subject-verb agreement requires the auxiliary verb 'are' to be used with the present participle 'launcing' when the subject is plural.
- rationale: The sentence contains a plural subject 'many automobile companies' followed by the present participle 'launcing', which requires the auxiliary verb 'are' to form the correct present continuous tense. The absence of 'are' makes the sentence grammatically incorrect.

### rf-edit-0016::qwen3_8b::natural

- parse: `parsed_json`; model: `gector_roberta_base`; op: `delete`
- evidence: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Articles 'a' and 'an' should agree with the following noun in terms of count and sound.
- rationale: The article 'an' is incorrectly used before the plural noun 'experts'. 'An' is used before singular nouns that begin with a vowel sound, while 'experts' is plural and does not require an article. The correct article would be 'the' if referring to specific experts, or the article could be omitted if the sentence is general.

### rf-edit-0098::qwen3_8b::natural

- parse: `parsed_json`; model: `gector_roberta_base`; op: `insert`
- evidence: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 0, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- rule: Numbers in time expressions should be fully formed and consistent.
- rationale: The original text contains '5 5 seconds', which is an incomplete time expression. Inserting '5' at the specified position attempts to form '5 5 5 seconds', but this is not a standard way to express time. The edit may be intended to correct a formatting issue, but without additional context, it's unclear if this is a valid or stylistic choice.

### rf-edit-0167::qwen3_8b::natural

- parse: `parsed_json`; model: `t5_base_grammar`; op: `replace`
- evidence: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 1, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: A comma should follow an introductory phrase or clause when it is followed by a main clause.
- rationale: The phrase 'For example' is an introductory phrase that precedes a main clause. Adding a comma after it improves readability and adheres to standard punctuation conventions for such constructions.

### rf-edit-0231::qwen3_8b::natural

- parse: `parsed_json`; model: `t5_base_grammar`; op: `replace`
- evidence: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 3, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'index_text_mismatch;invalid_indices', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Use 'is to' to introduce a purpose or goal clause following a noun phrase.
- rationale: The original sentence uses 'should' to express a recommendation, but the model edit changes it to 'is to', which introduces a goal clause. This edit transforms the sentence into a declarative statement about the intended purpose rather than a suggestion. While this is a valid alternative phrasing, it changes the tone and intent of the original sentence.

### rf-edit-0150::qwen3_8b::natural

- parse: `parsed_json`; model: `t5_base_grammar`; op: `replace`
- evidence: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- rule: Ensure correct spelling of words, particularly academic and technical terms.
- rationale: The word 'scientifc' is misspelled. The correct spelling is 'scientific', which is commonly used in academic and technical contexts to refer to subjects related to science. This correction ensures clarity and correctness in the sentence.

### rf-edit-0248::qwen3_8b::natural

- parse: `parsed_json`; model: `coedit_large`; op: `replace`
- evidence: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Pronouns should clearly refer to their antecedents and maintain grammatical consistency.
- rationale: The phrase 'its name' introduces a new clause that should logically begin with a subject pronoun ('It') to maintain clarity and grammatical flow. While 'its name' is not grammatically incorrect, using 'It' provides a more direct and stylistically preferable reference to the restaurant, enhancing readability.
