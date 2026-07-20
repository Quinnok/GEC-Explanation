# Qwen3 Evidence Refinement Smoke Audit

## Loop

- Loop ID: Loop C / targeted evidence refinement smoke.
- Bottleneck: Qwen3 prompt-v2 reduces prediction-only evidence but still misses contextual source evidence.
- Hypothesis: an evidence-only repair prompt can improve contextual SOURCE evidence without adding target/prediction leakage.
- Success criterion: selected refined outputs increase contextual evidence and do not increase prediction-only evidence.

## Summary

- `generated_at`: 2026-07-20T13:10:29+00:00
- `git_commit`: 841317b
- `prompt_version`: rulefaith_qwen3_evidence_refine_v2_compact_source_only_json
- `input_count`: 20
- `selected_for_refinement_count`: 20
- `refined_count`: 20
- `parse_status_counts`: `{'parsed_json': 20}`
- `original_full`: `{'contextual_source_evidence': 7, 'missing_evidence': 13, 'prediction_only_evidence': 20, 'wrong_evidence_auto': 20}`
- `selected_before`: `{'contextual_source_evidence': 7, 'missing_evidence': 13, 'prediction_only_evidence': 20, 'wrong_evidence_auto': 20}`
- `selected_after`: `{'contextual_source_evidence': 2, 'missing_evidence': 18, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 0}`
- `full_after_replacing_selected`: `{'contextual_source_evidence': 2, 'missing_evidence': 18, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 0}`
- `improvement_counts`: `{'evidence_contextual_improved': 0, 'wrong_evidence_fixed': 20, 'prediction_only_evidence_regressed': 0}`
- `decision`: revise_refinement_prompt_before_scaling
- `input_file`: /Users/bytedance/Documents/GEC可解释性/data/rulefaith/qwen3_evidence_refinement_probe20.jsonl
- `output_file`: /Users/bytedance/Documents/GEC可解释性/results/rulefaith/qwen3_evidence_refinement_probe20_refined_candidates.jsonl
- `dry_run`: False
- `selected_original_candidate_ids`: ['rf-edit-0277::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0191::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0051::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0163::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0114::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0267::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0127::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0074::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0125::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0248::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0165::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0250::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0217::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0268::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0257::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0251::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0284::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0242::qwen3_8b::rule_grounded::evidence_canonicalized']

## Refined Cases

### rf-edit-0277::qwen3_8b::rule_grounded::evidence_canonicalized::evidence_refined

- original: `rf-edit-0277::qwen3_8b::rule_grounded::evidence_canonicalized`; parse: `parsed_json`; latency: `18.813`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Nouns that refer to specific or general things should be preceded by articles like 'the' or 'a'.
- evidence: `[]`
- rationale: The insertion of 'the' before 'streets' is a stylistic choice to make the sentence more precise and natural, as 'streets' without an article can sound vague or incomplete in this context.

### rf-edit-0191::qwen3_8b::natural::evidence_canonicalized::evidence_refined

- original: `rf-edit-0191::qwen3_8b::natural::evidence_canonicalized`; parse: `parsed_json`; latency: `17.1764`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Articles like 'a' or 'an' may be omitted when the noun they precede is clearly defined or when the context makes the noun's presence clear.
- evidence: `[]`
- rationale: The article 'an' is unnecessary before the plural noun 'experts' because the subject 'students' and the verb 'become' make it clear that the noun is plural. Removing 'an' results in more concise and natural phrasing.

### rf-edit-0051::qwen3_8b::rule_grounded::evidence_canonicalized::evidence_refined

- original: `rf-edit-0051::qwen3_8b::rule_grounded::evidence_canonicalized`; parse: `parsed_json`; latency: `22.6621`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: The preposition 'for' is used to indicate purpose or relation to something, whereas 'of' indicates possession or composition.
- evidence: `[]`
- rationale: The phrase 'Caring of the environment' is grammatically incorrect because 'of' does not convey the intended relationship between the action (caring) and its target (the environment). The correct preposition to use here is 'for', which indicates purpose or relation. However, the evidence provided refers to text that is not present in the source, making the edit invalid.

### rf-edit-0163::qwen3_8b::natural::evidence_canonicalized::evidence_refined

- original: `rf-edit-0163::qwen3_8b::natural::evidence_canonicalized`; parse: `parsed_json`; latency: `20.1395`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Use 'for' to indicate the purpose or reason of an action, while 'on' typically indicates a topic or subject.
- evidence: `[]`
- rationale: The original sentence uses 'on' which implies a surface-level interaction, but the intended meaning is about the impact being directed towards the people. Replacing 'on' with 'for' better conveys that the impact was experienced by the people, aligning with the intended meaning.

### rf-edit-0114::qwen3_8b::rule_grounded::evidence_canonicalized::evidence_refined

- original: `rf-edit-0114::qwen3_8b::rule_grounded::evidence_canonicalized`; parse: `parsed_json`; latency: `17.283`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Use noun forms in parallel structures for consistency and grammatical correctness.
- evidence: `[]`
- rationale: The verb 'understand' is replaced with its noun form 'understanding' to maintain parallelism with 'learning', which is already in the noun form. This creates a more consistent and grammatically balanced structure in the sentence.

### rf-edit-0267::qwen3_8b::rule_grounded::evidence_canonicalized::evidence_refined

- original: `rf-edit-0267::qwen3_8b::rule_grounded::evidence_canonicalized`; parse: `parsed_json`; latency: `16.4987`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Nouns that are countable and not previously mentioned in the sentence should be preceded by an article (a/an).
- evidence: `[]`
- rationale: The noun 'side' is countable and refers to a specific concept ('positive side') that has not been introduced earlier in the sentence. Therefore, it should be preceded by the indefinite article 'a' to make the sentence grammatically correct and natural.

### rf-edit-0127::qwen3_8b::natural::evidence_canonicalized::evidence_refined

- original: `rf-edit-0127::qwen3_8b::natural::evidence_canonicalized`; parse: `parsed_json`; latency: `20.7822`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: The preposition 'for' is used to indicate purpose or relation to something, whereas 'of' indicates possession or composition.
- evidence: `[]`
- rationale: The phrase 'Caring of the environment' is grammatically incorrect because 'of' does not convey the intended relationship between the action (caring) and its object (the environment). However, the evidence provided refers to text that is not present in the source, making it invalid.

### rf-edit-0074::qwen3_8b::rule_grounded::evidence_canonicalized::evidence_refined

- original: `rf-edit-0074::qwen3_8b::rule_grounded::evidence_canonicalized`; parse: `parsed_json`; latency: `20.344`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: A subject must agree with its verb in number (singular/plural).
- evidence: `[]`
- rationale: The subject 'many automobile companies' is plural, so the verb should be 'are launcing' instead of just 'launcing' to maintain subject-verb agreement. This ensures grammatical correctness in the sentence structure.

### rf-edit-0125::qwen3_8b::rule_grounded::evidence_canonicalized::evidence_refined

- original: `rf-edit-0125::qwen3_8b::rule_grounded::evidence_canonicalized`; parse: `parsed_json`; latency: `22.2859`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: When comparing two items in a list, the conjunction 'either' is often redundant if the list is already clear without it.
- evidence: `[]`
- rationale: The word 'either' is redundant in this context because the sentence already uses 'or' to introduce the two options. Removing 'either' makes the sentence more concise and natural.

### rf-edit-0248::qwen3_8b::natural::evidence_canonicalized::evidence_refined

- original: `rf-edit-0248::qwen3_8b::natural::evidence_canonicalized`; parse: `parsed_json`; latency: `16.769`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Use a pronoun reference that clearly refers to the previously mentioned noun.
- evidence: `[]`
- rationale: 

### rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized::evidence_refined

- original: `rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized`; parse: `parsed_json`; latency: `18.9213`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Use an apostrophe to indicate possession in plural nouns.
- evidence: `[]`
- rationale: The word 'peoples' is a plural noun and requires an apostrophe to indicate possession. However, the apostrophe should be placed after the plural noun to form the possessive, which is not present in the original source text.

### rf-edit-0165::qwen3_8b::rule_grounded::evidence_canonicalized::evidence_refined

- original: `rf-edit-0165::qwen3_8b::rule_grounded::evidence_canonicalized`; parse: `parsed_json`; latency: `18.3743`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Use of indefinite articles ('a', 'an') before singular countable nouns.
- evidence: `[]`
- rationale: The original sentence lacks an article before 'positive', which is a singular countable noun. Inserting 'a' makes the sentence grammatically complete and stylistically correct by adhering to standard article usage rules.

### rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized::evidence_refined

- original: `rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized`; parse: `parsed_json`; latency: `20.484`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Use of definite or indefinite articles for noun phrases
- evidence: `[]`
- rationale: The original sentence begins with 'Variety', which is a non-count noun and does not require an article. Adding 'A' before 'variety' makes the noun phrase grammatically complete and more natural in standard English usage.

### rf-edit-0250::qwen3_8b::natural::evidence_canonicalized::evidence_refined

- original: `rf-edit-0250::qwen3_8b::natural::evidence_canonicalized`; parse: `parsed_json`; latency: `24.2396`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Use a comma to separate independent clauses when they are joined by a coordinating conjunction.
- evidence: `[]`
- rationale: The edit adds a comma after 'village' to improve clarity and proper punctuation between two independent clauses. While the original sentence is grammatically correct without the comma, adding it enhances readability and adheres to standard punctuation conventions.

### rf-edit-0217::qwen3_8b::natural::evidence_canonicalized::evidence_refined

- original: `rf-edit-0217::qwen3_8b::natural::evidence_canonicalized`; parse: `parsed_json`; latency: `24.1122`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- rule: Correct spelling of words with common misspellings.
- evidence: `[{"end": 14, "role": "error", "start": 13, "text": "ablished"}]`
- rationale: The word 'ablished' is a common misspelling of 'established'. Correcting it ensures clarity and proper communication of the intended meaning.

### rf-edit-0268::qwen3_8b::natural::evidence_canonicalized::evidence_refined

- original: `rf-edit-0268::qwen3_8b::natural::evidence_canonicalized`; parse: `parsed_json`; latency: `20.4433`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: A comma should be used to separate items in a list when the list contains three or more items.
- evidence: `[]`
- rationale: The edit adds a comma after 'computer' to properly separate items in the list. While the original sentence may still be understandable, the addition of the comma improves clarity and adheres to standard punctuation rules for lists.

### rf-edit-0257::qwen3_8b::natural::evidence_canonicalized::evidence_refined

- original: `rf-edit-0257::qwen3_8b::natural::evidence_canonicalized`; parse: `parsed_json`; latency: `23.8577`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: A comma should follow 'example' when it is used as a standalone sentence or introductory phrase.
- evidence: `[]`
- rationale: The edit adds a comma after 'example' to improve clarity and punctuation consistency, which is a stylistic choice rather than a grammatical necessity. This is common in writing to separate examples from the main clause.

### rf-edit-0251::qwen3_8b::natural::evidence_canonicalized::evidence_refined

- original: `rf-edit-0251::qwen3_8b::natural::evidence_canonicalized`; parse: `parsed_json`; latency: `19.6949`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: A comma should be used to separate independent clauses or items in a list when clarity is needed.
- evidence: `[]`
- rationale: The addition of a comma after 'streets' serves to separate the clause 'cars will fly above the streets' from the following clause 'computers will have totally changed', improving readability and adhering to standard punctuation rules for compound sentences.

### rf-edit-0284::qwen3_8b::rule_grounded::evidence_canonicalized::evidence_refined

- original: `rf-edit-0284::qwen3_8b::rule_grounded::evidence_canonicalized`; parse: `parsed_json`; latency: `21.8845`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- rule: Use semicolons to separate independent clauses when the second clause is a result or explanation of the first.
- evidence: `[]`
- rationale: The edit attempts to replace 'city' with 'city;' to introduce a semicolon. However, this is not valid because the semicolon should follow the full clause, not just the word 'city'. The semicolon should be placed after the entire first clause, not mid-sentence. Additionally, the evidence provided does not match the source text exactly, making the edit invalid.

### rf-edit-0242::qwen3_8b::rule_grounded::evidence_canonicalized::evidence_refined

- original: `rf-edit-0242::qwen3_8b::rule_grounded::evidence_canonicalized`; parse: `parsed_json`; latency: `22.0866`
- before: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- after: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- rule: Correct misspelled words to their standard form.
- evidence: `[{"end": 5, "role": "error", "start": 4, "text": "partyies"}]`
- rationale: The word 'partyies' contains an incorrect double 'i', which is a common spelling mistake. The correct spelling is 'parties', which is a standard English word referring to social gatherings. However, the evidence spans provided incorrectly reference text from the model prediction rather than the source text.
