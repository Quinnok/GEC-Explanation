# Qwen3 Evidence Refinement Probe20 Card

## Loop

- Loop ID: Loop D / 20-edit canonicalization-plus-refinement probe.
- Bottleneck: 78/160 canonicalized Qwen3 candidates still lack contextual source evidence or retain evidence-risk flags.
- Hypothesis: targeted Qwen3 refinement may repair a stratified subset of remaining evidence failures beyond deterministic span canonicalization.
- Success criterion: refined+canonicalized outputs improve contextual source evidence without increasing prediction-only evidence or edit-copy-only behavior.
- Failure criterion: refinement clears evidence or changes wording without adding source-grounded contextual evidence.

## Summary

- `generated_at`: `2026-07-20T13:02:48+00:00`
- `git_commit`: `841317b`
- `seed`: `20260720`
- `limit`: `20`
- `input_file`: `/Users/bytedance/Documents/GEC可解释性/data/rulefaith/teacher_candidates_qwen3_8b_canonicalized.jsonl`
- `output_file`: `/Users/bytedance/Documents/GEC可解释性/data/rulefaith/qwen3_evidence_refinement_probe20.jsonl`
- `input_count`: `160`
- `eligible_candidate_count`: `89`
- `eligible_edit_group_count`: `49`
- `selected_candidate_count`: `20`
- `selected_edit_group_count`: `20`
- `input_evidence_flags`: `{'contextual_source_evidence': 82, 'missing_evidence': 78, 'prediction_only_evidence': 29, 'wrong_evidence_auto': 29}`
- `eligible_evidence_flags`: `{'contextual_source_evidence': 11, 'missing_evidence': 78, 'prediction_only_evidence': 29, 'wrong_evidence_auto': 29}`
- `selected_evidence_flags`: `{'contextual_source_evidence': 7, 'missing_evidence': 13, 'prediction_only_evidence': 20, 'wrong_evidence_auto': 20}`
- `selected_breakdown`: `{'dataset': {'EXPECT': 18, 'JFLEG': 2}, 'model_key': {'coedit_large': 9, 'gector_roberta_base': 5, 't5_base_grammar': 6}, 'model_family': {'instruction-following text editor': 9, 'sequence-to-edit': 5, 'sequence-to-sequence': 6}, 'operation': {'delete': 2, 'insert': 5, 'replace': 13}, 'original_candidate_type': {'natural': 9, 'rule_grounded': 11}, 'rulefaith_split': {'test': 5, 'train': 15}}`
- `selected_candidate_ids`: `['rf-edit-0277::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0191::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0051::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0163::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0114::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0267::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0127::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0074::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0125::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0248::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0165::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0250::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0217::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0268::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0257::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0251::qwen3_8b::natural::evidence_canonicalized', 'rf-edit-0284::qwen3_8b::rule_grounded::evidence_canonicalized', 'rf-edit-0242::qwen3_8b::rule_grounded::evidence_canonicalized']`
- `decision`: `run_targeted_qwen3_refinement_probe_before_scaling`

## Selected Rows

### rf-edit-0277::qwen3_8b::rule_grounded::evidence_canonicalized

- dataset/model: `EXPECT` / `coedit_large`
- split/type/op: `train` / `rule_grounded` / `insert`
- edit: `{'end': 11, 'error_type': 'M:DET', 'operation': 'insert', 'source_text': '', 'start': 11, 'target_text': 'the'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Nouns that refer to specific or general things should be preceded by articles like 'the' or 'a'.
- evidence: `[{"end": 12, "role": "target", "start": 11, "text": "streets"}]`

### rf-edit-0191::qwen3_8b::natural::evidence_canonicalized

- dataset/model: `JFLEG` / `t5_base_grammar`
- split/type/op: `train` / `natural` / `delete`
- edit: `{'end': 17, 'error_type': 'U:DET', 'operation': 'delete', 'source_text': 'an', 'start': 16, 'target_text': ''}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Articles like 'a' or 'an' may be omitted when the noun they precede is clearly defined or when the context makes the noun's presence clear.
- evidence: `[{"end": 21, "role": "original", "start": 12, "text": "and they will become an experts in those areas"}, {"end": 18, "role": "modified", "start": 16, "text": "an experts"}]`

### rf-edit-0051::qwen3_8b::rule_grounded::evidence_canonicalized

- dataset/model: `EXPECT` / `gector_roberta_base`
- split/type/op: `test` / `rule_grounded` / `replace`
- edit: `{'end': 26, 'error_type': 'R:PREP', 'operation': 'replace', 'source_text': 'of', 'start': 25, 'target_text': 'for'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: The preposition 'for' is used to indicate purpose or relation to something, whereas 'of' indicates possession or composition.
- evidence: `[{"end": 28, "role": "target", "start": 24, "text": "Caring of the environment"}]`

### rf-edit-0163::qwen3_8b::natural::evidence_canonicalized

- dataset/model: `EXPECT` / `t5_base_grammar`
- split/type/op: `test` / `natural` / `replace`
- edit: `{'end': 8, 'error_type': 'R:PREP', 'operation': 'replace', 'source_text': 'on', 'start': 7, 'target_text': 'for'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Use 'for' to indicate the purpose or reason of an action, while 'on' typically indicates a topic or subject.
- evidence: `[{"end": 8, "role": "target", "start": 7, "text": "on"}]`

### rf-edit-0114::qwen3_8b::rule_grounded::evidence_canonicalized

- dataset/model: `JFLEG` / `gector_roberta_base`
- split/type/op: `train` / `rule_grounded` / `replace`
- edit: `{'end': 8, 'error_type': 'R:VERB:FORM', 'operation': 'replace', 'source_text': 'understand', 'start': 7, 'target_text': 'understanding'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Use noun forms in parallel structures for consistency and grammatical correctness.
- evidence: `[{"end": 8, "role": "target", "start": 7, "text": "understand"}]`

### rf-edit-0267::qwen3_8b::rule_grounded::evidence_canonicalized

- dataset/model: `EXPECT` / `coedit_large`
- split/type/op: `train` / `rule_grounded` / `insert`
- edit: `{'end': 17, 'error_type': 'M:DET', 'operation': 'insert', 'source_text': '', 'start': 17, 'target_text': 'a'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Nouns that are countable and not previously mentioned in the sentence should be preceded by an article (a/an).
- evidence: `[{"end": 18, "role": "target", "start": 17, "text": "positive"}]`

### rf-edit-0127::qwen3_8b::natural::evidence_canonicalized

- dataset/model: `EXPECT` / `t5_base_grammar`
- split/type/op: `test` / `natural` / `replace`
- edit: `{'end': 26, 'error_type': 'R:PREP', 'operation': 'replace', 'source_text': 'of', 'start': 25, 'target_text': 'for'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: The preposition 'for' is used to indicate purpose or relation to something, whereas 'of' indicates possession or composition.
- evidence: `[{"end": 28, "role": "target", "start": 24, "text": "Caring of the environment"}]`

### rf-edit-0074::qwen3_8b::rule_grounded::evidence_canonicalized

- dataset/model: `EXPECT` / `gector_roberta_base`
- split/type/op: `train` / `rule_grounded` / `insert`
- edit: `{'end': 37, 'error_type': 'M:VERB:TENSE', 'operation': 'insert', 'source_text': '', 'start': 37, 'target_text': 'are'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: A subject must agree with its verb in number (singular/plural).
- evidence: `[{"end": 38, "role": "target", "start": 34, "text": "many automobile companies launcing"}]`

### rf-edit-0125::qwen3_8b::rule_grounded::evidence_canonicalized

- dataset/model: `EXPECT` / `t5_base_grammar`
- split/type/op: `train` / `rule_grounded` / `delete`
- edit: `{'end': 21, 'error_type': 'U:CONJ', 'operation': 'delete', 'source_text': 'either', 'start': 20, 'target_text': ''}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: When comparing two items in a list, the conjunction 'either' is often redundant if the list is already clear without it.
- evidence: `[{"end": 25, "role": "target", "start": 20, "text": "either to our parents '"}]`

### rf-edit-0248::qwen3_8b::natural::evidence_canonicalized

- dataset/model: `EXPECT` / `coedit_large`
- split/type/op: `train` / `natural` / `replace`
- edit: `{'end': 12, 'error_type': 'R:OTHER', 'operation': 'replace', 'source_text': 'its name', 'start': 10, 'target_text': 'It'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Use a pronoun reference that clearly refers to the previously mentioned noun.
- evidence: `[{"end": 16, "role": "original", "start": 10, "text": "its name is \" Lemon \""}, {"end": 16, "role": "modified", "start": 10, "text": "its name is \" Lemon \""}]`

### rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized

- dataset/model: `EXPECT` / `gector_roberta_base`
- split/type/op: `train` / `rule_grounded` / `insert`
- edit: `{'end': 17, 'error_type': 'M:NOUN:POSS', 'operation': 'insert', 'source_text': '', 'start': 17, 'target_text': "'"}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Use an apostrophe to indicate possession in plural nouns.
- evidence: `[{"end": 17, "role": "target", "start": 16, "text": "peoples"}]`

### rf-edit-0165::qwen3_8b::rule_grounded::evidence_canonicalized

- dataset/model: `EXPECT` / `t5_base_grammar`
- split/type/op: `train` / `rule_grounded` / `insert`
- edit: `{'end': 17, 'error_type': 'M:DET', 'operation': 'insert', 'source_text': '', 'start': 17, 'target_text': 'a'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Use of indefinite articles ('a', 'an') before singular countable nouns.
- evidence: `[{"end": 18, "role": "target", "start": 14, "text": "as well as positive"}]`

### rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized

- dataset/model: `EXPECT` / `gector_roberta_base`
- split/type/op: `train` / `rule_grounded` / `replace`
- edit: `{'end': 1, 'error_type': 'M:DET', 'operation': 'replace', 'source_text': 'Variety', 'start': 0, 'target_text': 'A variety'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': False, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 0, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': True, 'wrong_evidence_auto': True}`
- rule: Use of definite or indefinite articles for noun phrases
- evidence: `[{"end": 1, "role": "modified", "start": 0, "text": "Variety"}]`

### rf-edit-0250::qwen3_8b::natural::evidence_canonicalized

- dataset/model: `EXPECT` / `coedit_large`
- split/type/op: `test` / `natural` / `replace`
- edit: `{'end': 35, 'error_type': 'R:NOUN', 'operation': 'replace', 'source_text': 'village', 'start': 34, 'target_text': 'village,'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- rule: Use a comma to separate independent clauses when they are joined by a coordinating conjunction.
- evidence: `[{"end": 35, "role": "target", "start": 34, "text": "village"}]`

### rf-edit-0217::qwen3_8b::natural::evidence_canonicalized

- dataset/model: `EXPECT` / `t5_base_grammar`
- split/type/op: `test` / `natural` / `replace`
- edit: `{'end': 14, 'error_type': 'R:SPELL', 'operation': 'replace', 'source_text': 'ablished', 'start': 13, 'target_text': 'established,'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- rule: Correct spelling of words with common misspellings.
- evidence: `[{"end": 14, "role": "error", "start": 13, "text": "ablished"}, {"end": 14, "role": "correction", "start": 13, "text": "ablished"}]`

### rf-edit-0268::qwen3_8b::natural::evidence_canonicalized

- dataset/model: `EXPECT` / `coedit_large`
- split/type/op: `train` / `natural` / `replace`
- edit: `{'end': 70, 'error_type': 'R:NOUN', 'operation': 'replace', 'source_text': 'computer', 'start': 69, 'target_text': 'computer,'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- rule: A comma should be used to separate items in a list when the list contains three or more items.
- evidence: `[{"end": 70, "role": "target", "start": 69, "text": "computer"}]`

### rf-edit-0257::qwen3_8b::natural::evidence_canonicalized

- dataset/model: `EXPECT` / `coedit_large`
- split/type/op: `train` / `natural` / `replace`
- edit: `{'end': 33, 'error_type': 'R:OTHER', 'operation': 'replace', 'source_text': 'example', 'start': 32, 'target_text': 'example,'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- rule: A comma should follow 'example' when it is used as a standalone sentence or introductory phrase.
- evidence: `[{"end": 33, "role": "source", "start": 32, "text": "example"}, {"end": 33, "role": "target", "start": 32, "text": "example"}]`

### rf-edit-0251::qwen3_8b::natural::evidence_canonicalized

- dataset/model: `EXPECT` / `coedit_large`
- split/type/op: `train` / `natural` / `replace`
- edit: `{'end': 12, 'error_type': 'R:NOUN', 'operation': 'replace', 'source_text': 'streets', 'start': 11, 'target_text': 'streets,'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- rule: A comma should be used to separate independent clauses or items in a list when clarity is needed.
- evidence: `[{"end": 12, "role": "modified", "start": 11, "text": "streets"}]`

### rf-edit-0284::qwen3_8b::rule_grounded::evidence_canonicalized

- dataset/model: `EXPECT` / `coedit_large`
- split/type/op: `train` / `rule_grounded` / `replace`
- edit: `{'end': 8, 'error_type': 'R:NOUN', 'operation': 'replace', 'source_text': 'city', 'start': 7, 'target_text': 'city;'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 1, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 1, 'evidence_edit_token_only_count': 1, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- rule: Use semicolons to separate independent clauses when the second clause is a result or explanation of the first.
- evidence: `[{"end": 8, "role": "modified", "start": 7, "text": "city"}]`

### rf-edit-0242::qwen3_8b::rule_grounded::evidence_canonicalized

- dataset/model: `EXPECT` / `coedit_large`
- split/type/op: `train` / `rule_grounded` / `replace`
- edit: `{'end': 5, 'error_type': 'R:SPELL', 'operation': 'replace', 'source_text': 'partyies', 'start': 4, 'target_text': 'parties'}`
- checks: `{'evidence_span_index_match': True, 'evidence_all_spans_source_index_match': True, 'evidence_text_found_in_source': True, 'evidence_text_found_in_prediction_only': True, 'evidence_contextual': True, 'evidence_valid_source_span_count': 2, 'evidence_invalid_source_span_count': 0, 'evidence_contextual_source_count': 2, 'evidence_edit_token_only_count': 2, 'evidence_error_types': 'prediction_or_target_role', 'missing_evidence': False, 'wrong_evidence_auto': True}`
- rule: Correct misspelled words to their standard form.
- evidence: `[{"end": 5, "role": "error", "start": 4, "text": "partyies"}, {"end": 14, "role": "corrected", "start": 13, "text": "parties"}]`
