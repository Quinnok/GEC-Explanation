# Qwen3 Rule Plausibility and Evidence Sufficiency Audit

This automatic audit runs after target-masked validation. It checks whether the rule type is plausible for the edit category and whether evidence spans are sufficient for that rule type. It is not human evaluation.

## Summary

- Candidate count: 16
- Decision counts: `{'ready_for_human_spotcheck': 16}`
- Decision rates: `{'ready_for_human_spotcheck': 1.0}`
- Rule plausibility: `{'plausible': 16}`
- Evidence sufficiency: `{'sufficient': 16}`

## Reason Counts


## Ready Examples

### rf-edit-0058::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- source: Variety of buses are provided by the government in order to meet people 's financial means .
- edit: `replace` `Variety` -> `A variety`
- rule: Use of definite or indefinite articles for noun phrases
- evidence: `[{"end": 1, "role": "source", "source": "kept_existing", "start": 0, "text": "Variety"}, {"end": 3, "role": "head_noun", "source": "structured_heuristic", "start": 2, "text": "buses"}]`

### rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- source: Variety of buses are provided by the government in order to meet people 's financial means .
- edit: `replace` `Variety` -> `A variety`
- rule: Use of definite or indefinite articles for noun phrases
- evidence: `[{"end": 3, "role": "head_noun", "source": "structured_heuristic", "start": 2, "text": "buses"}]`

### rf-edit-0138::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- source: But such a high level of development of Egyptian civilization has a negative side as well as positive .
- edit: `replace` `civilization` -> `civilization,`
- rule: A comma should be used after introductory phrases or clauses to separate them from the main clause.
- evidence: `[{"end": 10, "role": "modified_text", "source": "kept_existing", "start": 9, "text": "civilization"}, {"end": 10, "role": "modified_token", "source": "structured_heuristic", "start": 9, "text": "civilization"}, {"end": 9, "role": "noun_number_context", "source": "structured_heuristic", "start": 8, "text": "Egyptian"}, {"end": 11, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 10, "text": "has"}]`

### rf-edit-0138::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- source: But such a high level of development of Egyptian civilization has a negative side as well as positive .
- edit: `replace` `civilization` -> `civilization,`
- rule: A comma should be used after introductory elements to separate clauses.
- evidence: `[{"end": 10, "role": "modified_text", "source": "kept_existing", "start": 9, "text": "civilization"}, {"end": 10, "role": "modified_token", "source": "structured_heuristic", "start": 9, "text": "civilization"}, {"end": 9, "role": "noun_number_context", "source": "structured_heuristic", "start": 8, "text": "Egyptian"}, {"end": 11, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 10, "text": "has"}]`

### rf-edit-0255::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- source: i love my family especially my little sister , she has sixteen years old , i consider her my best friend because i usually tell her everything about my life .
- edit: `replace` `sister` -> `sister.`
- rule: A period should follow a complete sentence.
- evidence: `[{"end": 8, "role": "token", "source": "kept_existing", "start": 7, "text": "sister"}, {"end": 8, "role": "modified_token", "source": "structured_heuristic", "start": 7, "text": "sister"}, {"end": 7, "role": "noun_number_context", "source": "structured_heuristic", "start": 6, "text": "little"}, {"end": 10, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 9, "text": "she"}]`

### rf-edit-0255::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- source: i love my family especially my little sister , she has sixteen years old , i consider her my best friend because i usually tell her everything about my life .
- edit: `replace` `sister` -> `sister.`
- rule: A period should follow a complete sentence.
- evidence: `[{"end": 8, "role": "token", "source": "kept_existing", "start": 7, "text": "sister"}, {"end": 8, "role": "modified_token", "source": "structured_heuristic", "start": 7, "text": "sister"}, {"end": 7, "role": "noun_number_context", "source": "structured_heuristic", "start": 6, "text": "little"}, {"end": 10, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 9, "text": "she"}]`

### rf-edit-0276::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- edit: `delete` `the` -> ``
- rule: Articles like 'the' may be omitted when the noun phrase is clearly defined or when the context makes the reference unambiguous.
- evidence: `[{"end": 9, "role": "deleted", "source": "kept_existing", "start": 8, "text": "the"}, {"end": 10, "role": "head_noun", "source": "structured_heuristic", "start": 9, "text": "people"}]`

### rf-edit-0276::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- edit: `delete` `the` -> ``
- rule: Articles like 'the' may be omitted when referring to general time periods or categories.
- evidence: `[{"end": 9, "role": "deleted", "source": "kept_existing", "start": 8, "text": "the"}, {"end": 10, "role": "head_noun", "source": "structured_heuristic", "start": 9, "text": "people"}]`

### rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- source: A worldwide war is the only case in which we would see a dramatic change in peoples lives in the time length of 50 years from now .
- edit: `insert` `` -> `'`
- rule: Use an apostrophe to indicate possession in plural nouns.
- evidence: `[{"end": 17, "role": "noun_number_context", "source": "structured_heuristic", "start": 16, "text": "peoples"}, {"end": 18, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 17, "text": "lives"}]`

### rf-edit-0165::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- source: But such a high level of development of Egyptian civilization has a negative side as well as positive .
- edit: `insert` `` -> `a`
- rule: Articles should be used to specify definiteness or indefiniteness in nouns.
- evidence: `[{"end": 18, "role": "affected", "source": "kept_existing", "start": 14, "text": "as well as positive"}, {"end": 18, "role": "head_noun", "source": "structured_heuristic", "start": 17, "text": "positive"}]`

### rf-edit-0165::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- source: But such a high level of development of Egyptian civilization has a negative side as well as positive .
- edit: `insert` `` -> `a`
- rule: Use of indefinite articles ('a', 'an') before singular countable nouns.
- evidence: `[{"end": 18, "role": "head_noun", "source": "structured_heuristic", "start": 17, "text": "positive"}]`

### rf-edit-0265::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- source: Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .
- edit: `delete` `is` -> ``
- rule: In the structure 'how different our lives are', the verb 'are' should be used instead of 'is' to maintain subject-verb agreement.
- evidence: `[{"end": 17, "role": "error", "source": "kept_existing", "start": 16, "text": "is"}, {"end": 16, "role": "verb_context", "source": "structured_heuristic", "start": 15, "text": "different"}, {"end": 18, "role": "verb_complement_or_time_context", "source": "structured_heuristic", "start": 17, "text": "our"}]`

Additional ready candidates are available in the JSONL bucket.

## Refinement / Reject Examples


## Limitations

- This audit uses deterministic heuristics and ERRANT-style category assumptions.
- It can catch obvious category/evidence issues but may miss subtle grammatical invalidity.
- Ready candidates are only ready for human or stronger validation, not final positive training data.
