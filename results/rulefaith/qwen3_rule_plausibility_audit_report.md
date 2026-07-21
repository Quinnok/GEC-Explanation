# Qwen3 Rule Plausibility and Evidence Sufficiency Audit

This automatic audit runs after target-masked validation. It checks whether the rule type is plausible for the edit category and whether evidence spans are sufficient for that rule type. It is not human evaluation.

## Summary

- Candidate count: 47
- Decision counts: `{'needs_refinement': 16, 'ready_for_human_spotcheck': 25, 'reject': 6}`
- Decision rates: `{'needs_refinement': 0.3404, 'ready_for_human_spotcheck': 0.5319, 'reject': 0.1277}`
- Rule plausibility: `{'plausible': 47}`
- Evidence sufficiency: `{'insufficient': 6, 'sufficient': 41}`

## Reason Counts

- `evidence_not_mentioned_in_rule_or_rationale`: 14
- `missing_required_evidence:noun_number_context`: 1
- `missing_required_evidence:specific_source_evidence`: 5
- `rationale_edit_copy`: 8
- `unsupported_high_confidence`: 6

## Ready Examples

### rf-edit-0016::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: Students can focus on only a few subjects they are intwerested in and they will become an experts in those areas . 
- edit: `delete` `an` -> ``
- rule: Articles like 'a' or 'an' may be omitted when the noun is clearly defined or when the context makes the number clear.
- evidence: `[{"end": 21, "role": "original", "source": "kept_existing", "start": 12, "text": "and they will become an experts in those areas"}, {"end": 18, "role": "head_noun", "source": "structured_heuristic", "start": 17, "text": "experts"}]`

### rf-edit-0016::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: Students can focus on only a few subjects they are intwerested in and they will become an experts in those areas . 
- edit: `delete` `an` -> ``
- rule: Avoid unnecessary articles when the noun is clearly defined or when the context makes the article redundant.
- evidence: `[{"end": 21, "role": "original", "source": "kept_existing", "start": 13, "text": "they will become an experts in those areas"}, {"end": 18, "role": "head_noun", "source": "structured_heuristic", "start": 17, "text": "experts"}]`

### rf-edit-0023::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: Beacuse all those broad knowledge help they to understand their major in university as well as help they to make a correct choice in specializing study . 
- edit: `replace` `in specializing` -> `specializing in`
- rule: The preposition 'in' typically follows the verb 'specializing' when indicating the field of study, making 'specializing in' the preferred phrasing.
- evidence: `[{"end": 25, "role": "source", "source": "kept_existing", "start": 23, "text": "in specializing"}, {"end": 26, "role": "head_noun", "source": "structured_heuristic", "start": 25, "text": "study"}]`

### rf-edit-0023::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: Beacuse all those broad knowledge help they to understand their major in university as well as help they to make a correct choice in specializing study . 
- edit: `replace` `in specializing` -> `specializing in`
- rule: The preposition 'in' should typically follow the verb 'specializing' when indicating the field of study, resulting in the phrase 'specializing in'.
- evidence: `[{"end": 25, "role": "source", "source": "kept_existing", "start": 23, "text": "in specializing"}, {"end": 26, "role": "head_noun", "source": "structured_heuristic", "start": 25, "text": "study"}]`

### rf-edit-0033::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: I think about transport that the government should help the public transport , for example buses , train , the metro and more , for a single reason : the quality of life against the pollution .
- edit: `delete` `the` -> ``
- rule: Articles like 'the' may be omitted when they are redundant or when the noun phrase is clearly understood without them.
- evidence: `[{"end": 36, "role": "head_noun", "source": "structured_heuristic", "start": 35, "text": "pollution"}]`

### rf-edit-0051::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- edit: `replace` `of` -> `for`
- rule: The preposition 'for' is used to indicate purpose or relation to something, while 'of' indicates possession or composition.
- evidence: `[{"end": 25, "role": "preposition_governor", "source": "structured_heuristic", "start": 24, "text": "Caring"}, {"end": 28, "role": "preposition_complement", "source": "structured_heuristic", "start": 27, "text": "environment"}]`

### rf-edit-0051::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- edit: `replace` `of` -> `for`
- rule: The preposition 'for' is used to indicate purpose or relation to something, whereas 'of' indicates possession or composition.
- evidence: `[{"end": 25, "role": "preposition_governor", "source": "structured_heuristic", "start": 24, "text": "Caring"}, {"end": 28, "role": "preposition_complement", "source": "structured_heuristic", "start": 27, "text": "environment"}]`

### rf-edit-0062::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: We have to know this problem it 's serious but almost people doens't know about this . 
- edit: `replace` `this` -> `it`
- rule: Use appropriate pronouns to refer back to previously mentioned nouns.
- evidence: `[{"end": 16, "role": "antecedent", "source": "kept_existing", "start": 15, "text": "this"}, {"end": 6, "role": "antecedent", "source": "kept_existing", "start": 5, "text": "problem"}, {"end": 15, "role": "pronoun_antecedent_context", "source": "structured_heuristic", "start": 14, "text": "about"}]`

### rf-edit-0062::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: We have to know this problem it 's serious but almost people doens't know about this . 
- edit: `replace` `this` -> `it`
- rule: Use a pronoun to refer back to a previously mentioned noun to avoid repetition.
- evidence: `[{"end": 6, "role": "antecedent", "source": "kept_existing", "start": 5, "text": "problem"}, {"end": 16, "role": "repetition", "source": "kept_existing", "start": 15, "text": "this"}, {"end": 15, "role": "pronoun_antecedent_context", "source": "structured_heuristic", "start": 14, "text": "about"}]`

### rf-edit-0127::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- edit: `replace` `of` -> `for`
- rule: The preposition 'for' is used to indicate purpose or relation to something, whereas 'of' indicates possession or composition.
- evidence: `[{"end": 25, "role": "preposition_governor", "source": "structured_heuristic", "start": 24, "text": "Caring"}, {"end": 28, "role": "preposition_complement", "source": "structured_heuristic", "start": 27, "text": "environment"}]`

### rf-edit-0127::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- edit: `replace` `of` -> `for`
- rule: The preposition 'for' is used to indicate purpose or benefit, while 'of' indicates possession or association.
- evidence: `[{"end": 25, "role": "preposition_governor", "source": "structured_heuristic", "start": 24, "text": "Caring"}, {"end": 28, "role": "preposition_complement", "source": "structured_heuristic", "start": 27, "text": "environment"}]`

### rf-edit-0163::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- edit: `replace` `on` -> `for`
- rule: Use 'for' to indicate the purpose or reason of an action, while 'on' is used for topics or subjects.
- evidence: `[{"end": 10, "role": "original", "source": "kept_existing", "start": 1, "text": "have had a most significant impact on the people"}, {"end": 7, "role": "preposition_governor", "source": "structured_heuristic", "start": 6, "text": "impact"}, {"end": 10, "role": "preposition_complement", "source": "structured_heuristic", "start": 9, "text": "people"}]`

Additional ready candidates are available in the JSONL bucket.

## Refinement / Reject Examples

- `rf-edit-0058::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`evidence_not_mentioned_in_rule_or_rationale`
  - rule: Use of definite or indefinite articles for noun phrases
- `rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`evidence_not_mentioned_in_rule_or_rationale`
  - rule: Use of definite or indefinite articles for noun phrases
- `rf-edit-0126::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` decision=`reject` reasons=`missing_required_evidence:noun_number_context;evidence_not_mentioned_in_rule_or_rationale;unsupported_high_confidence`
  - rule: Avoid unnecessary periods following a sentence-ending word unless it is part of a list or a specific stylistic choice.
- `rf-edit-0138::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`evidence_not_mentioned_in_rule_or_rationale`
  - rule: A comma should be used after introductory phrases or clauses to separate them from the main clause.
- `rf-edit-0138::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`evidence_not_mentioned_in_rule_or_rationale`
  - rule: A comma should be used after introductory elements to separate clauses.
- `rf-edit-0255::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`evidence_not_mentioned_in_rule_or_rationale`
  - rule: A period should follow a complete sentence.
- `rf-edit-0255::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`evidence_not_mentioned_in_rule_or_rationale`
  - rule: A period should follow a complete sentence.
- `rf-edit-0257::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` decision=`reject` reasons=`missing_required_evidence:specific_source_evidence;evidence_not_mentioned_in_rule_or_rationale;unsupported_high_confidence`
  - rule: A comma should follow 'example' when it is used as a standalone sentence or introductory phrase.
- `rf-edit-0257::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` decision=`reject` reasons=`missing_required_evidence:specific_source_evidence;evidence_not_mentioned_in_rule_or_rationale;unsupported_high_confidence`
  - rule: When using 'example' as a standalone word in a sentence, a comma should follow it if it is followed by additional explanatory content.
- `rf-edit-0276::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`evidence_not_mentioned_in_rule_or_rationale`
  - rule: Articles like 'the' may be omitted when the noun phrase is clearly defined or when the context makes the reference unambiguous.
- `rf-edit-0276::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`evidence_not_mentioned_in_rule_or_rationale`
  - rule: Articles like 'the' may be omitted when referring to general time periods or categories.
- `rf-edit-0293::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` decision=`reject` reasons=`missing_required_evidence:specific_source_evidence;evidence_not_mentioned_in_rule_or_rationale;unsupported_high_confidence`
  - rule: A period should follow a sentence if it ends with a declarative statement.
- `rf-edit-0293::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` decision=`reject` reasons=`missing_required_evidence:specific_source_evidence;evidence_not_mentioned_in_rule_or_rationale;unsupported_high_confidence`
  - rule: Add a period after a sentence-ending word if it is followed by a new sentence.
- `rf-edit-0294::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` decision=`reject` reasons=`missing_required_evidence:specific_source_evidence;evidence_not_mentioned_in_rule_or_rationale;unsupported_high_confidence`
  - rule: A period should be used to end a sentence.
- `rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`rationale_edit_copy`
  - rule: Use an apostrophe to indicate possession in plural nouns.
- `rf-edit-0165::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`rationale_edit_copy`
  - rule: Articles should be used to specify definiteness or indefiniteness in nouns.
- `rf-edit-0165::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`rationale_edit_copy`
  - rule: Use of indefinite articles ('a', 'an') before singular countable nouns.
- `rf-edit-0265::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`rationale_edit_copy`
  - rule: In the structure 'how different our lives are', the verb 'are' should be used instead of 'is' to maintain subject-verb agreement.
- `rf-edit-0267::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`rationale_edit_copy`
  - rule: Use of articles (a/an) before singular countable nouns.
- `rf-edit-0277::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` decision=`needs_refinement` reasons=`rationale_edit_copy`
  - rule: Nouns that refer to specific or general things should be preceded by articles like 'the' or 'a' when necessary.

## Limitations

- This audit uses deterministic heuristics and ERRANT-style category assumptions.
- It can catch obvious category/evidence issues but may miss subtle grammatical invalidity.
- Ready candidates are only ready for human or stronger validation, not final positive training data.
