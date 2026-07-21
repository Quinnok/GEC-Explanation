# Qwen3 Field-Aware RuleFaith Selection

This gate separates required edit description from leakage in rule/rationale fields. It does not treat `edit_description` edit-copy as a direct failure, but it still rejects alignment, validity, false-rationalization, rule, and evidence hard failures.

## Bucket Counts

- current: `{'accepted': 45, 'refine': 13, 'rejected': 102}`
- previous strict: `{'accepted': 0, 'refine': 58, 'rejected': 102}`

## Field Leakage Counts

- `edit_description_edit_copy`: 108
- `edit_description_target_copy`: 100
- `rationale_edit_copy`: 26
- `rationale_target_copy`: 86
- `rule_text_target_copy`: 40

## Hard Failure Reasons

- `alignment_error`: 58
- `missing_rule`: 1
- `no_specific_source_evidence`: 36
- `parse_not_json`: 1
- `possible_false_rationalization`: 19
- `validity_error_auto`: 28

## Refine Reasons

Active refine bucket:

- `generic_explanation`: 1
- `rationale_edit_copy`: 13

All refine triggers before hard-reject override:

- `generic_explanation`: 1
- `rationale_edit_copy`: 26
- `unsupported_confidence`: 70

## Accepted Examples

### rf-edit-0016::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: Students can focus on only a few subjects they are intwerested in and they will become an experts in those areas . 
- edit: `delete` `an` -> ``
- rule: Articles like 'a' or 'an' may be omitted when the noun is clearly defined or when the context makes the number clear.
- rationale: The article 'an' is unnecessary before the plural noun 'experts' because the subject 'students' implies multiple individuals who can become experts. Removing 'an' improves clarity and grammatical correctness in this context.
- evidence: `[{"end": 21, "role": "original", "source": "kept_existing", "start": 12, "text": "and they will become an experts in those areas"}, {"end": 18, "role": "head_noun", "source": "structured_heuristic", "start": 17, "text": "experts"}]`

### rf-edit-0016::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: Students can focus on only a few subjects they are intwerested in and they will become an experts in those areas . 
- edit: `delete` `an` -> ``
- rule: Avoid unnecessary articles when the noun is clearly defined or when the context makes the article redundant.
- rationale: The article 'an' is unnecessary before the plural noun 'experts' because 'experts' is already plural and does not require an article. Removing 'an' improves clarity and conciseness without altering the meaning.
- evidence: `[{"end": 21, "role": "original", "source": "kept_existing", "start": 13, "text": "they will become an experts in those areas"}, {"end": 18, "role": "head_noun", "source": "structured_heuristic", "start": 17, "text": "experts"}]`

### rf-edit-0023::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: Beacuse all those broad knowledge help they to understand their major in university as well as help they to make a correct choice in specializing study . 
- edit: `replace` `in specializing` -> `specializing in`
- rule: The preposition 'in' typically follows the verb 'specializing' when indicating the field of study, making 'specializing in' the preferred phrasing.
- rationale: The phrase 'specializing in' is the standard and more natural construction when referring to a field of study. Reversing the order to 'in specializing' is non-standard and less idiomatic in English.
- evidence: `[{"end": 25, "role": "source", "source": "kept_existing", "start": 23, "text": "in specializing"}, {"end": 26, "role": "head_noun", "source": "structured_heuristic", "start": 25, "text": "study"}]`

### rf-edit-0023::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: Beacuse all those broad knowledge help they to understand their major in university as well as help they to make a correct choice in specializing study . 
- edit: `replace` `in specializing` -> `specializing in`
- rule: The preposition 'in' should typically follow the verb 'specializing' when indicating the field of study, resulting in the phrase 'specializing in'.
- rationale: The phrase 'specializing in' is the standard and more natural phrasing when referring to a field of study. Reversing the order to 'in specializing' is non-standard and less idiomatic in English.
- evidence: `[{"end": 25, "role": "source", "source": "kept_existing", "start": 23, "text": "in specializing"}, {"end": 26, "role": "head_noun", "source": "structured_heuristic", "start": 25, "text": "study"}]`

### rf-edit-0033::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: I think about transport that the government should help the public transport , for example buses , train , the metro and more , for a single reason : the quality of life against the pollution .
- edit: `delete` `the` -> ``
- rule: Articles like 'the' may be omitted when they are redundant or when the noun phrase is clearly understood without them.
- rationale: The article 'the' before 'pollution' is stylistically unnecessary because it is already clear from context that the comparison is between quality of life and pollution, without requiring a definite article. Removing 'the' makes the sentence
- evidence: `[{"end": 36, "role": "head_noun", "source": "structured_heuristic", "start": 35, "text": "pollution"}]`

### rf-edit-0051::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- edit: `replace` `of` -> `for`
- rule: The preposition 'for' is used to indicate purpose or relation to something, while 'of' indicates possession or composition.
- rationale: The phrase 'Caring of the environment' is grammatically incorrect because 'of' does not convey the intended relationship between the action (caring) and its object (the environment). The correct preposition to use here is 'for', which indic
- evidence: `[{"end": 25, "role": "preposition_governor", "source": "structured_heuristic", "start": 24, "text": "Caring"}, {"end": 28, "role": "preposition_complement", "source": "structured_heuristic", "start": 27, "text": "environment"}]`

### rf-edit-0051::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- edit: `replace` `of` -> `for`
- rule: The preposition 'for' is used to indicate purpose or relation to something, whereas 'of' indicates possession or composition.
- rationale: The phrase 'Caring of the environment' is grammatically incorrect because 'of' does not convey the intended relationship between the action (caring) and its target (the environment). The correct preposition to use here is 'for', which indic
- evidence: `[{"end": 25, "role": "preposition_governor", "source": "structured_heuristic", "start": 24, "text": "Caring"}, {"end": 28, "role": "preposition_complement", "source": "structured_heuristic", "start": 27, "text": "environment"}]`

### rf-edit-0058::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: Variety of buses are provided by the government in order to meet people 's financial means .
- edit: `replace` `Variety` -> `A variety`
- rule: Use of definite or indefinite articles for noun phrases
- rationale: The edit adds the indefinite article 'a' before 'variety', which is stylistically preferred when referring to a general category rather than a specific instance. While the original sentence is grammatically correct without the article, addi
- evidence: `[{"end": 1, "role": "source", "source": "kept_existing", "start": 0, "text": "Variety"}, {"end": 3, "role": "head_noun", "source": "structured_heuristic", "start": 2, "text": "buses"}]`

### rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: Variety of buses are provided by the government in order to meet people 's financial means .
- edit: `replace` `Variety` -> `A variety`
- rule: Use of definite or indefinite articles for noun phrases
- rationale: The original sentence begins with 'Variety', which is a non-count noun and does not require an article. Adding 'A' before 'variety' makes the noun phrase grammatically complete and more natural in standard English usage.
- evidence: `[{"end": 3, "role": "head_noun", "source": "structured_heuristic", "start": 2, "text": "buses"}]`

### rf-edit-0062::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: We have to know this problem it 's serious but almost people doens't know about this . 
- edit: `replace` `this` -> `it`
- rule: Use appropriate pronouns to refer back to previously mentioned nouns.
- rationale: The pronoun 'this' is used to refer to the problem, which is a singular noun. However, 'this' typically refers to a concrete object or situation, while 'it' is more appropriate for abstract concepts like a problem. Replacing 'this' with 'it
- evidence: `[{"end": 16, "role": "antecedent", "source": "kept_existing", "start": 15, "text": "this"}, {"end": 6, "role": "antecedent", "source": "kept_existing", "start": 5, "text": "problem"}, {"end": 15, "role": "pronoun_antecedent_context", "source": "structured_heuristic", "start": 14, "text": "about"}]`

### rf-edit-0062::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- source: We have to know this problem it 's serious but almost people doens't know about this . 
- edit: `replace` `this` -> `it`
- rule: Use a pronoun to refer back to a previously mentioned noun to avoid repetition.
- rationale: The word 'this' is used to refer to the problem mentioned earlier, but 'it' is more appropriate as a pronoun to avoid repetition and improve clarity.
- evidence: `[{"end": 6, "role": "antecedent", "source": "kept_existing", "start": 5, "text": "problem"}, {"end": 16, "role": "repetition", "source": "kept_existing", "start": 15, "text": "this"}, {"end": 15, "role": "pronoun_antecedent_context", "source": "structured_heuristic", "start": 14, "text": "about"}]`

### rf-edit-0077::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- source: Additionally , our city government has prohibited smoking in public area and under 18 years old and provides a free session of talks or presentations to increase the awareness of clean , safe , fresh environment to the city .
- edit: `replace` `area` -> `areas`
- rule: Subjects and verbs must agree in number (singular/plural).
- rationale: The original sentence uses 'public area' which is singular, but the verb 'has prohibited' is plural, creating a subject-verb agreement error. Changing 'area' to 'areas' makes the subject plural and aligns it with the verb 'has prohibited'.
- evidence: `[{"end": 11, "role": "subject", "source": "kept_existing", "start": 9, "text": "public area"}, {"end": 10, "role": "noun_number_context", "source": "structured_heuristic", "start": 9, "text": "public"}, {"end": 13, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 12, "text": "under"}]`

Additional accepted candidates are available in the JSONL bucket.

## Limitations

- Accepted means suitable for target-masked validation, not ready for SFT positive construction.
- These are automatic pseudo-label decisions, not human evaluation.
- Rule correctness still requires human or stronger verifier confirmation.
