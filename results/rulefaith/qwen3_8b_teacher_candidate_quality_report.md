# Teacher Candidate Quality Report

Input: `data/rulefaith/teacher_candidates_qwen3_8b_pilot.jsonl`

## Summary

- `candidate_count`: 160
- `provider_counts`: {'qwen3_8b': 160}
- `teacher_model_counts`: {'Qwen/Qwen3-8B': 160}
- `candidate_type_counts`: {'natural': 80, 'rule_grounded': 80}
- `parse_status_counts`: {'parsed_json': 159, 'wrapped_non_json_response': 1}
- `generic_count`: 3
- `prompt_contamination_count`: 0
- `source_copy_like_count`: 0
- `too_short_count`: 0
- `low_quality_count`: 3
- `low_quality_rate`: 0.0187

## Highest-Risk Examples

- `rf-edit-0225::qwen3_8b::natural`: {
  "edit_description": "Replace 'the' with 'they' at the beginning of the sentence.",
  "edit_validity": "invalid",
  "rule_id": "subject_verb_agreement",
  "rule_text": "The subject and verb in a sentence must agree in number (singular/pl
- `rf-edit-0207::qwen3_8b::rule_grounded`: {
  "edit_description": "Replace 'do' with 'they' to correct the subject-verb agreement and make the sentence grammatically correct.",
  "edit_validity": "valid",
  "rule_id": "subject_verb_agreement",
  "rule_text": "A subject and its corr
- `rf-edit-0207::qwen3_8b::natural`: {
  "edit_description": "Replace 'do' with 'they' to correct the subject-verb agreement and make the sentence grammatically correct.",
  "edit_validity": "valid",
  "rule_id": "svo_agreement",
  "rule_text": "Subject-verb agreement requires
- `rf-edit-0035::qwen3_8b::natural`: {
  "edit_description": "Insert an apostrophe after 'peoples'",
  "edit_validity": "stylistic",
  "rule_id": "punctuation_apostrophe",
  "rule_text": "An apostrophe is used to indicate possession or contraction.",
  "evidence_spans": [
    
- `rf-edit-0052::qwen3_8b::rule_grounded`: {
  "edit_description": "Replace 'unmeaningful' with 'on important'",
  "edit_validity": "invalid",
  "rule_id": "grammar_subject_complement",
  "rule_text": "A subject complement should follow a linking verb and provide information about t
- `rf-edit-0052::qwen3_8b::natural`: {
  "edit_description": "Replace 'unmeaningful' with 'on important'",
  "edit_validity": "invalid",
  "rule_id": "grammar_and_syntax",
  "rule_text": "A preposition must follow a verb when indicating direction or relation.",
  "evidence_spa
- `rf-edit-0236::qwen3_8b::rule_grounded`: {
  "edit_description": "Replace 'latter 1/2' with 'beginning' to indicate the time period being referenced.",
  "edit_validity": "invalid",
  "rule_id": "semantic_inconsistency",
  "rule_text": "Replacements must maintain semantic coherenc
- `rf-edit-0240::qwen3_8b::natural`: {
  "edit_description": "Deleting the text from 'going there that would drive me nuts' to 'prices are not expensive.'",
  "edit_validity": "invalid",
  "rule_id": "sentence_continuation",
  "rule_text": "A sentence should not abruptly end m
- `rf-edit-0225::qwen3_8b::rule_grounded`: {
  "edit_description": "Replace 'the' with 'they' at the beginning of the sentence.",
  "edit_validity": "invalid",
  "rule_id": "subject_verb_agreement",
  "rule_text": "The subject and verb in a sentence must agree in number (singular/pl
- `rf-edit-0118::qwen3_8b::rule_grounded`: {
  "edit_description": "Replace 'that' with 'when' to connect the clauses",
  "edit_validity": "acceptable_alternative",
  "rule_id": "subordinating_conjunction_usage",
  "rule_text": "Use 'when' to introduce a time clause, and 'that' to i
- `rf-edit-0098::qwen3_8b::rule_grounded`: {
  "edit_description": "Insert '5' at position [9,9)",
  "edit_validity": "invalid",
  "rule_id": "number_formatting",
  "rule_text": "Numbers representing time should be written with proper formatting, including decimal points where neces
- `rf-edit-0163::qwen3_8b::rule_grounded`: {
  "edit_description": "Replace 'on' with 'for' in the phrase 'have had a most significant impact on the people'",
  "edit_validity": "acceptable_alternative",
  "rule_id": "preposition_usage",
  "rule_text": "Use 'for' to indicate the pur
- `rf-edit-0118::qwen3_8b::natural`: {
  "edit_description": "Replace 'that' with 'when' to introduce a subordinate clause.",
  "edit_validity": "acceptable_alternative",
  "rule_id": "subordinating_conjunction_usage",
  "rule_text": "Subordinating conjunctions like 'when' are
- `rf-edit-0114::qwen3_8b::natural`: {
  "edit_description": "Replace 'understand' with 'ing' form 'understanding'",
  "edit_validity": "stylistic",
  "rule_id": "noun_phrase_consistency",
  "rule_text": "Use noun forms in parallel structures for consistency and grammatical co
- `rf-edit-0034::qwen3_8b::natural`: {
  "edit_description": "Replace 'pot' with 'potting' to correct the verb form.",
  "edit_validity": "valid",
  "rule_id": "grammar-verb-form",
  "rule_text": "Use the correct verb form based on context and grammatical structure.",
  "evide
- `rf-edit-0231::qwen3_8b::rule_grounded`: {
  "edit_description": "Replace 'should' with 'is to' to rephrase the sentence's purpose.",
  "edit_validity": "acceptable_alternative",
  "rule_id": "grammar_rephrasing",
  "rule_text": "Use 'is to' to express purpose or intention in form
- `rf-edit-0284::qwen3_8b::natural`: {
  "edit_description": "Replace 'city' with 'city;'",
  "edit_validity": "stylistic",
  "rule_id": "punctuation_usage",
  "rule_text": "Use semicolons to separate independent clauses when the clauses are closely related.",
  "evidence_span
- `rf-edit-0058::qwen3_8b::natural`: {
  "edit_description": "Replace 'Variety' with 'A variety'",
  "edit_validity": "stylistic",
  "rule_id": "article_usage",
  "rule_text": "Use of definite or indefinite articles for noun phrases",
  "evidence_spans": [
    {
      "text": 
- `rf-edit-0170::qwen3_8b::natural`: {
  "edit_description": "Inserting 'the' before 'museum' to specify which museum is being referred to.",
  "edit_validity": "valid",
  "rule_id": "article_usage",
  "rule_text": "Definite articles ('the') should be used when referring to sp
- `rf-edit-0236::qwen3_8b::natural`: {
  "edit_description": "Replace 'latter 1/2' with 'beginning'",
  "edit_validity": "invalid",
  "rule_id": "semantic_coherence",
  "rule_text": "Replacements should maintain semantic coherence and logical consistency within the context.",


## Interpretation

These teacher candidates are model-generated explanations for verifier filtering and failure analysis. They are not human gold and should not be used as positives without RuleFaith validation.
