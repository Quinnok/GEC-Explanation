# Qwen3 Target-Masked RuleFaith Validation

This validation hides the target edit from rule/rationale/applicability-condition text and checks whether grammar and evidence signals survive without relying on direct target copying. It is an automatic diagnostic, not human evaluation.

## Summary

- Input candidates: 58
- Field-aware input buckets: `{'accepted': 45, 'refine': 13}`
- Target-masked buckets: `{'refine': 8, 'rejected': 3, 'validated': 47}`
- Target-masked rates: `{'refine': 0.1379, 'rejected': 0.0517, 'validated': 0.8103}`
- Score mean/min/max: `0.8543` / `0.0` / `1.0`

## Failure Counts

- `generic_after_target_mask`: 1
- `masked_rule_lacks_grammar_signal`: 2
- `rule_category_mismatch:noun_number_explained_as_subject_verb_agreement`: 2
- `rule_category_mismatch:orthography_rule_lacks_spelling_signal`: 2
- `rule_category_mismatch:pronoun_rule_lacks_pronoun_signal`: 1
- `rule_category_mismatch:verb_rule_lacks_verb_signal`: 1
- `target_dependent_quality_text`: 7

## Warning Counts

- `rationale_edit_copy`: 13
- `specific_evidence_not_mentioned_in_rule_or_rationale`: 21

## Breakdown By Previous Bucket

- `accepted`: `{'refine': 5, 'rejected': 1, 'validated': 39}`
- `refine`: `{'refine': 3, 'rejected': 2, 'validated': 8}`

## Validated Examples

### rf-edit-0016::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- score: `1.0`
- source: Students can focus on only a few subjects they are intwerested in and they will become an experts in those areas . 
- edit: `delete` `an` -> ``
- rule: Articles like 'a' or 'an' may be omitted when the noun is clearly defined or when the context makes the number clear.
- rationale: The article 'an' is unnecessary before the plural noun 'experts' because the subject 'students' implies multiple individuals who can become experts. Removing 'an' improves clarity and grammatical correctness in this context.
- evidence: `[{"end": 21, "role": "original", "source": "kept_existing", "start": 12, "text": "and they will become an experts in those areas"}, {"end": 18, "role": "head_noun", "source": "structured_heuristic", "start": 17, "text": "experts"}]`

### rf-edit-0016::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- score: `1.0`
- source: Students can focus on only a few subjects they are intwerested in and they will become an experts in those areas . 
- edit: `delete` `an` -> ``
- rule: Avoid unnecessary articles when the noun is clearly defined or when the context makes the article redundant.
- rationale: The article 'an' is unnecessary before the plural noun 'experts' because 'experts' is already plural and does not require an article. Removing 'an' improves clarity and conciseness without altering the meaning.
- evidence: `[{"end": 21, "role": "original", "source": "kept_existing", "start": 13, "text": "they will become an experts in those areas"}, {"end": 18, "role": "head_noun", "source": "structured_heuristic", "start": 17, "text": "experts"}]`

### rf-edit-0023::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- score: `1.0`
- source: Beacuse all those broad knowledge help they to understand their major in university as well as help they to make a correct choice in specializing study . 
- edit: `replace` `in specializing` -> `specializing in`
- rule: The preposition 'in' typically follows the verb 'specializing' when indicating the field of study, making 'specializing in' the preferred phrasing.
- rationale: The phrase 'specializing in' is the standard and more natural construction when referring to a field of study. Reversing the order to 'in specializing' is non-standard and less idiomatic in English.
- evidence: `[{"end": 25, "role": "source", "source": "kept_existing", "start": 23, "text": "in specializing"}, {"end": 26, "role": "head_noun", "source": "structured_heuristic", "start": 25, "text": "study"}]`

### rf-edit-0023::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- score: `1.0`
- source: Beacuse all those broad knowledge help they to understand their major in university as well as help they to make a correct choice in specializing study . 
- edit: `replace` `in specializing` -> `specializing in`
- rule: The preposition 'in' should typically follow the verb 'specializing' when indicating the field of study, resulting in the phrase 'specializing in'.
- rationale: The phrase 'specializing in' is the standard and more natural phrasing when referring to a field of study. Reversing the order to 'in specializing' is non-standard and less idiomatic in English.
- evidence: `[{"end": 25, "role": "source", "source": "kept_existing", "start": 23, "text": "in specializing"}, {"end": 26, "role": "head_noun", "source": "structured_heuristic", "start": 25, "text": "study"}]`

### rf-edit-0033::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- score: `1.0`
- source: I think about transport that the government should help the public transport , for example buses , train , the metro and more , for a single reason : the quality of life against the pollution .
- edit: `delete` `the` -> ``
- rule: Articles like 'the' may be omitted when they are redundant or when the noun phrase is clearly understood without them.
- rationale: The article 'the' before 'pollution' is stylistically unnecessary because it is already clear from context that the comparison is between quality of life and pollution, without requiring a definite article. Removing 'the' makes the sentence more concise and na
- evidence: `[{"end": 36, "role": "head_noun", "source": "structured_heuristic", "start": 35, "text": "pollution"}]`

### rf-edit-0051::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- score: `1.0`
- source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- edit: `replace` `of` -> `for`
- rule: The preposition 'for' is used to indicate purpose or relation to something, while 'of' indicates possession or composition.
- rationale: The phrase 'Caring of the environment' is grammatically incorrect because 'of' does not convey the intended relationship between the action (caring) and its object (the environment). The correct preposition to use here is 'for', which indicates purpose or rela
- evidence: `[{"end": 25, "role": "preposition_governor", "source": "structured_heuristic", "start": 24, "text": "Caring"}, {"end": 28, "role": "preposition_complement", "source": "structured_heuristic", "start": 27, "text": "environment"}]`

### rf-edit-0051::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- score: `1.0`
- source: I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .
- edit: `replace` `of` -> `for`
- rule: The preposition 'for' is used to indicate purpose or relation to something, whereas 'of' indicates possession or composition.
- rationale: The phrase 'Caring of the environment' is grammatically incorrect because 'of' does not convey the intended relationship between the action (caring) and its target (the environment). The correct preposition to use here is 'for', which indicates purpose or rela
- evidence: `[{"end": 25, "role": "preposition_governor", "source": "structured_heuristic", "start": 24, "text": "Caring"}, {"end": 28, "role": "preposition_complement", "source": "structured_heuristic", "start": 27, "text": "environment"}]`

### rf-edit-0058::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- score: `0.9`
- source: Variety of buses are provided by the government in order to meet people 's financial means .
- edit: `replace` `Variety` -> `A variety`
- rule: Use of definite or indefinite articles for noun phrases
- rationale: The edit adds the indefinite article 'a' before 'variety', which is stylistically preferred when referring to a general category rather than a specific instance. While the original sentence is grammatically correct without the article, adding 'a' makes the sen
- evidence: `[{"end": 1, "role": "source", "source": "kept_existing", "start": 0, "text": "Variety"}, {"end": 3, "role": "head_noun", "source": "structured_heuristic", "start": 2, "text": "buses"}]`

### rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired

- score: `0.9`
- source: Variety of buses are provided by the government in order to meet people 's financial means .
- edit: `replace` `Variety` -> `A variety`
- rule: Use of definite or indefinite articles for noun phrases
- rationale: The original sentence begins with 'Variety', which is a non-count noun and does not require an article. Adding 'A' before 'variety' makes the noun phrase grammatically complete and more natural in standard English usage.
- evidence: `[{"end": 3, "role": "head_noun", "source": "structured_heuristic", "start": 2, "text": "buses"}]`

### rf-edit-0062::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired

- score: `1.0`
- source: We have to know this problem it 's serious but almost people doens't know about this . 
- edit: `replace` `this` -> `it`
- rule: Use appropriate pronouns to refer back to previously mentioned nouns.
- rationale: The pronoun 'this' is used to refer to the problem, which is a singular noun. However, 'this' typically refers to a concrete object or situation, while 'it' is more appropriate for abstract concepts like a problem. Replacing 'this' with 'it' improves clarity a
- evidence: `[{"end": 16, "role": "antecedent", "source": "kept_existing", "start": 15, "text": "this"}, {"end": 6, "role": "antecedent", "source": "kept_existing", "start": 5, "text": "problem"}, {"end": 15, "role": "pronoun_antecedent_context", "source": "structured_heuristic", "start": 14, "text": "about"}]`

Additional validated candidates are available in the JSONL bucket.

## Target-Dependence Examples

- `rf-edit-0114::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` score=`0.7` failures=`target_dependent_quality_text`
  - target: `understanding`
  - masked quality text: Use noun forms in parallel structures for consistency and grammatical correctness. The original sentence uses 'think to learn' and 'understand' in parallel, but 'understand' is a verb while 'learn' is a verb as well. To maintain parallelism and grammatical con
- `rf-edit-0234::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` score=`0.4` failures=`rule_category_mismatch:orthography_rule_lacks_spelling_signal;target_dependent_quality_text`
  - target: `agriculture`
  - masked quality text: the word '[TARGET_MASK]' is uncountable and does not have a plural form The word 'agricultures' is incorrect because '[TARGET_MASK]' is an uncountable noun and does not have a plural form. The correct term should be '[TARGET_MASK]' when referring to agricultur
- `rf-edit-0294::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` score=`0.7` failures=`target_dependent_quality_text`
  - target: `there.`
  - masked quality text: A period should be used to end a sentence. The word 'there' is used as a standalone sentence in the original text, which requires a period to properly end the sentence. Replacing 'there' with '[TARGET_MASK]' adds the necessary punctuation to indicate the compl
- `rf-edit-0114::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=`0.5` failures=`target_dependent_quality_text`
  - target: `understanding`
  - masked quality text: Use noun forms in parallel structures for consistency and grammatical correctness. The verb 'understand' is replaced with its noun form '[TARGET_MASK]' to maintain parallelism with 'learning', which is already in the noun form. This creates a more consistent a
- `rf-edit-0231::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired` score=`0.5` failures=`target_dependent_quality_text`
  - target: `is to`
  - masked quality text: Use '[TARGET_MASK]' to express purpose or intention more clearly in certain contexts. Replacing 'should' with '[TARGET_MASK]' transforms the sentence from a statement of obligation to one that expresses a clear purpose. This change aligns with the structure of
- `rf-edit-0231::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=`0.0` failures=`masked_rule_lacks_grammar_signal;generic_after_target_mask;rule_category_mismatch:verb_rule_lacks_verb_signal;target_dependent_quality_text`
  - target: `is to`
  - masked quality text: Use '[TARGET_MASK]' to express purpose or intention in formal writing. Replacing 'should' with '[TARGET_MASK]' transforms the sentence from a suggestion into a statement of purpose, which may be more appropriate in certain contexts such as instructional or exp
- `rf-edit-0234::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired` score=`0.2` failures=`rule_category_mismatch:orthography_rule_lacks_spelling_signal;target_dependent_quality_text`
  - target: `agriculture`
  - masked quality text: the word '[TARGET_MASK]' is uncountable and does not have a plural form The word '[TARGET_MASK]' is an uncountable noun and does not have a plural form. Therefore, 'agricultures' is incorrect and should be replaced with '[TARGET_MASK]'. the context refers to [

## Limitations

- This diagnostic checks target-copy dependence heuristically; it does not prove human rule correctness.
- Validated candidates remain automatic pseudo-labels and must not be used as final SFT positives without stronger validation.
- Empty-target delete edits are not target-mask stress tests because there is no target string to hide.
