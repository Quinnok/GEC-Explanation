# Qwen3 Target-Masked RuleFaith Validation

This validation hides the target edit from rule/rationale/applicability-condition text and checks whether grammar and evidence signals survive without relying on direct target copying. It is an automatic diagnostic, not human evaluation.

## Summary

- Input candidates: 16
- Field-aware input buckets: `{'accepted': 8, 'refine': 8}`
- Target-masked buckets: `{'validated': 16}`
- Target-masked rates: `{'validated': 1.0}`
- Score mean/min/max: `1.0` / `1.0` / `1.0`

## Failure Counts


## Warning Counts


## Breakdown By Previous Bucket

- `accepted`: `{'validated': 8}`
- `refine`: `{'validated': 8}`

## Validated Examples

### rf-edit-0058::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- score: `1.0`
- source: Variety of buses are provided by the government in order to meet people 's financial means .
- edit: `replace` `Variety` -> `A variety`
- rule: Use of definite or indefinite articles for noun phrases
- rationale: The edit adds the indefinite article 'a' before 'variety', which is stylistically preferred when referring to a general category rather than a specific instance. While the original sentence is grammatically correct without the article, adding 'a' makes the sen
- evidence: `[{"end": 1, "role": "source", "source": "kept_existing", "start": 0, "text": "Variety"}, {"end": 3, "role": "head_noun", "source": "structured_heuristic", "start": 2, "text": "buses"}]`

### rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- score: `1.0`
- source: Variety of buses are provided by the government in order to meet people 's financial means .
- edit: `replace` `Variety` -> `A variety`
- rule: Use of definite or indefinite articles for noun phrases
- rationale: The original sentence begins with 'Variety', which is a non-count noun and does not require an article. Adding 'A' before 'variety' makes the noun phrase grammatically complete and more natural in standard English usage. The cited source evidence is "buses" as
- evidence: `[{"end": 3, "role": "head_noun", "source": "structured_heuristic", "start": 2, "text": "buses"}]`

### rf-edit-0138::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- score: `1.0`
- source: But such a high level of development of Egyptian civilization has a negative side as well as positive .
- edit: `replace` `civilization` -> `civilization,`
- rule: A comma should be used after introductory phrases or clauses to separate them from the main clause.
- rationale: The addition of a comma after 'civilization' separates the introductory phrase from the main clause, improving clarity and adhering to standard punctuation rules. However, this edit is considered stylistic rather than grammatically necessary, as the sentence r
- evidence: `[{"end": 10, "role": "modified_text", "source": "kept_existing", "start": 9, "text": "civilization"}, {"end": 10, "role": "modified_token", "source": "structured_heuristic", "start": 9, "text": "civilization"}, {"end": 9, "role": "noun_number_context", "source": "structured_heuristic", "start": 8, "text": "Egyptian"}, {"end": 11, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 10, "text": "has"}]`

### rf-edit-0138::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- score: `1.0`
- source: But such a high level of development of Egyptian civilization has a negative side as well as positive .
- edit: `replace` `civilization` -> `civilization,`
- rule: A comma should be used after introductory elements to separate clauses.
- rationale: The edit adds a comma after 'civilization' to separate the introductory phrase from the main clause, which is a stylistic choice to improve readability and clarity. However, this comma is not strictly necessary for grammatical correctness, making the edit opti
- evidence: `[{"end": 10, "role": "modified_text", "source": "kept_existing", "start": 9, "text": "civilization"}, {"end": 10, "role": "modified_token", "source": "structured_heuristic", "start": 9, "text": "civilization"}, {"end": 9, "role": "noun_number_context", "source": "structured_heuristic", "start": 8, "text": "Egyptian"}, {"end": 11, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 10, "text": "has"}]`

### rf-edit-0255::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- score: `1.0`
- source: i love my family especially my little sister , she has sixteen years old , i consider her my best friend because i usually tell her everything about my life .
- edit: `replace` `sister` -> `sister.`
- rule: A period should follow a complete sentence.
- rationale: The word 'sister' at the end of the first sentence is followed by a comma, which indicates the sentence is not yet complete. Adding a period after 'sister' would properly terminate the sentence, making it grammatically correct and stylistically appropriate. Th
- evidence: `[{"end": 8, "role": "token", "source": "kept_existing", "start": 7, "text": "sister"}, {"end": 8, "role": "modified_token", "source": "structured_heuristic", "start": 7, "text": "sister"}, {"end": 7, "role": "noun_number_context", "source": "structured_heuristic", "start": 6, "text": "little"}, {"end": 10, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 9, "text": "she"}]`

### rf-edit-0255::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- score: `1.0`
- source: i love my family especially my little sister , she has sixteen years old , i consider her my best friend because i usually tell her everything about my life .
- edit: `replace` `sister` -> `sister.`
- rule: A period should follow a complete sentence.
- rationale: The word 'sister' at the end of the first sentence is followed by a comma, which is incorrect because the sentence is complete. Adding a period after 'sister' would properly terminate the sentence. The cited source evidence is "sister" as modified token; "litt
- evidence: `[{"end": 8, "role": "token", "source": "kept_existing", "start": 7, "text": "sister"}, {"end": 8, "role": "modified_token", "source": "structured_heuristic", "start": 7, "text": "sister"}, {"end": 7, "role": "noun_number_context", "source": "structured_heuristic", "start": 6, "text": "little"}, {"end": 10, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 9, "text": "she"}]`

### rf-edit-0276::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- score: `1.0`
- source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- edit: `delete` `the` -> ``
- rule: Articles like 'the' may be omitted when the noun phrase is clearly defined or when the context makes the reference unambiguous.
- rationale: The article 'the' before 'latter half of the 20th century' is stylistically optional because the time period is clearly defined and widely understood in the context. Removing it results in a more concise and natural phrasing. The cited source evidence is "peop
- evidence: `[{"end": 9, "role": "deleted", "source": "kept_existing", "start": 8, "text": "the"}, {"end": 10, "role": "head_noun", "source": "structured_heuristic", "start": 9, "text": "people"}]`

### rf-edit-0276::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- score: `1.0`
- source: Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .
- edit: `delete` `the` -> ``
- rule: Articles like 'the' may be omitted when referring to general time periods or categories.
- rationale: The article 'the' is stylistically unnecessary before 'latter half of the 20th century' because it refers to a general time period rather than a specific instance. Removing 'the' makes the sentence more concise and natural in standard English usage. The cited 
- evidence: `[{"end": 9, "role": "deleted", "source": "kept_existing", "start": 8, "text": "the"}, {"end": 10, "role": "head_noun", "source": "structured_heuristic", "start": 9, "text": "people"}]`

### rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- score: `1.0`
- source: A worldwide war is the only case in which we would see a dramatic change in peoples lives in the time length of 50 years from now .
- edit: `insert` `` -> `'`
- rule: Use an apostrophe to indicate possession in plural nouns.
- rationale: The cited source evidence is "peoples" as noun number context; "lives" as noun phrase context. This evidence supports the rule that Use an apostrophe to indicate possession in plural nouns.
- evidence: `[{"end": 17, "role": "noun_number_context", "source": "structured_heuristic", "start": 16, "text": "peoples"}, {"end": 18, "role": "noun_phrase_context", "source": "structured_heuristic", "start": 17, "text": "lives"}]`

### rf-edit-0165::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- score: `1.0`
- source: But such a high level of development of Egyptian civilization has a negative side as well as positive .
- edit: `insert` `` -> `a`
- rule: Articles should be used to specify definiteness or indefiniteness in nouns.
- rationale: The cited source evidence is "positive" as head noun. This evidence supports the rule that Articles should be used to specify definiteness or indefiniteness in nouns.
- evidence: `[{"end": 18, "role": "affected", "source": "kept_existing", "start": 14, "text": "as well as positive"}, {"end": 18, "role": "head_noun", "source": "structured_heuristic", "start": 17, "text": "positive"}]`

Additional validated candidates are available in the JSONL bucket.

## Target-Dependence Examples


## Limitations

- This diagnostic checks target-copy dependence heuristically; it does not prove human rule correctness.
- Validated candidates remain automatic pseudo-labels and must not be used as final SFT positives without stronger validation.
- Empty-target delete edits are not target-mask stress tests because there is no target string to hide.
