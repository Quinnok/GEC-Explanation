# Qwen3 Evidence Refinement Probe20 Comparison

This report compares the same 20 canonicalized evidence-failure candidates before refinement, after Qwen3 targeted refinement, and after re-canonicalizing refined outputs.

## Summary

- aligned triples: `20/20`
- canonicalized only: `{'contextual_source_evidence': 7, 'missing_evidence': 13, 'prediction_only_evidence': 20, 'wrong_evidence_auto': 20, 'all_spans_source_index_match': 20}`
- Qwen3 refined: `{'contextual_source_evidence': 2, 'missing_evidence': 18, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 0, 'all_spans_source_index_match': 2}`
- Qwen3 refined then canonicalized: `{'contextual_source_evidence': 2, 'missing_evidence': 18, 'prediction_only_evidence': 0, 'wrong_evidence_auto': 0, 'all_spans_source_index_match': 2}`
- transition counts: `{'ctx:0->0->0;wrong:1->0->0': 13, 'ctx:1->0->0;wrong:1->0->0': 5, 'ctx:1->1->1;wrong:1->0->0': 2}`

## Decision

Do not scale this refinement prompt yet; it does not improve strict contextual evidence over canonicalized-only outputs.

## Cases

### rf-edit-0277::qwen3_8b::rule_grounded::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: Nouns that refer to specific or general things should be preceded by articles like 'the' or 'a'.
- refined evidence: `[]`

### rf-edit-0191::qwen3_8b::natural::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: Articles like 'a' or 'an' may be omitted when the noun they precede is clearly defined or when the context makes the noun's presence clear.
- refined evidence: `[]`

### rf-edit-0051::qwen3_8b::rule_grounded::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: The preposition 'for' is used to indicate purpose or relation to something, whereas 'of' indicates possession or composition.
- refined evidence: `[]`

### rf-edit-0163::qwen3_8b::natural::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: Use 'for' to indicate the purpose or reason of an action, while 'on' typically indicates a topic or subject.
- refined evidence: `[]`

### rf-edit-0114::qwen3_8b::rule_grounded::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: Use noun forms in parallel structures for consistency and grammatical correctness.
- refined evidence: `[]`

### rf-edit-0267::qwen3_8b::rule_grounded::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: Nouns that are countable and not previously mentioned in the sentence should be preceded by an article (a/an).
- refined evidence: `[]`

### rf-edit-0127::qwen3_8b::natural::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: The preposition 'for' is used to indicate purpose or relation to something, whereas 'of' indicates possession or composition.
- refined evidence: `[]`

### rf-edit-0074::qwen3_8b::rule_grounded::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: A subject must agree with its verb in number (singular/plural).
- refined evidence: `[]`

### rf-edit-0125::qwen3_8b::rule_grounded::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: When comparing two items in a list, the conjunction 'either' is often redundant if the list is already clear without it.
- refined evidence: `[]`

### rf-edit-0248::qwen3_8b::natural::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: Use a pronoun reference that clearly refers to the previously mentioned noun.
- refined evidence: `[]`

### rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: Use an apostrophe to indicate possession in plural nouns.
- refined evidence: `[]`

### rf-edit-0165::qwen3_8b::rule_grounded::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: Use of indefinite articles ('a', 'an') before singular countable nouns.
- refined evidence: `[]`

### rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: Use of definite or indefinite articles for noun phrases
- refined evidence: `[]`

### rf-edit-0250::qwen3_8b::natural::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: Use a comma to separate independent clauses when they are joined by a coordinating conjunction.
- refined evidence: `[]`

### rf-edit-0217::qwen3_8b::natural::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- refined rule: Correct spelling of words with common misspellings.
- refined evidence: `[{"end": 14, "role": "error", "start": 13, "text": "ablished"}]`

### rf-edit-0268::qwen3_8b::natural::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: A comma should be used to separate items in a list when the list contains three or more items.
- refined evidence: `[]`

### rf-edit-0257::qwen3_8b::natural::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: A comma should follow 'example' when it is used as a standalone sentence or introductory phrase.
- refined evidence: `[]`

### rf-edit-0251::qwen3_8b::natural::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: A comma should be used to separate independent clauses or items in a list when clarity is needed.
- refined evidence: `[]`

### rf-edit-0284::qwen3_8b::rule_grounded::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': False, 'evidence_all_spans_source_index_match': False, 'evidence_text_found_in_source': False, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': False, 'evidence_valid_source_span_count': 0, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 0, 'evidence_error_types': 'missing_evidence', 'missing_evidence': True, 'wrong_evidence_auto': False}`
- refined rule: Use semicolons to separate independent clauses when the second clause is a result or explanation of the first.
- refined evidence: `[]`

### rf-edit-0242::qwen3_8b::rule_grounded::evidence_canonicalized

- baseline checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- refined checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- refined+canonicalized checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': False, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': '', 'missing_evidence': False, 'wrong_evidence_auto': False}`
- refined rule: Correct misspelled words to their standard form.
- refined evidence: `[{"end": 5, "role": "error", "start": 4, "text": "partyies"}]`
