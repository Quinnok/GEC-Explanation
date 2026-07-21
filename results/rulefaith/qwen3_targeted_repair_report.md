# Qwen3 Targeted Repair

This deterministic repair pass uses Loop K audit reasons to connect cited source evidence back into the rationale and remove rationale-level edit-copy wording. It is not a model-generated or human-authored revision.

## Summary

- Candidate count: 16
- Rationale edit-copy before/after: 8 -> 0
- Evidence mentioned in rule/rationale before/after: 8 -> 16
- Action counts: `{'appended_source_evidence_to_rationale': 8, 'capped_confidence_at_0.8': 14, 'replaced_rationale_edit_copy': 8}`

## Examples

### rf-edit-0058::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- actions: `appended_source_evidence_to_rationale;capped_confidence_at_0.8`
- rationale: The edit adds the indefinite article 'a' before 'variety', which is stylistically preferred when referring to a general category rather than a specific instance. While the original sentence is grammatically correct without the article, adding 'a' makes the sentence more natural and idiomatic in standard English usage. 

### rf-edit-0058::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- actions: `appended_source_evidence_to_rationale;capped_confidence_at_0.8`
- rationale: The original sentence begins with 'Variety', which is a non-count noun and does not require an article. Adding 'A' before 'variety' makes the noun phrase grammatically complete and more natural in standard English usage. The cited source evidence is "buses" as head noun.

### rf-edit-0138::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- actions: `appended_source_evidence_to_rationale;capped_confidence_at_0.8`
- rationale: The addition of a comma after 'civilization' separates the introductory phrase from the main clause, improving clarity and adhering to standard punctuation rules. However, this edit is considered stylistic rather than grammatically necessary, as the sentence remains understandable without the comma. The cited source ev

### rf-edit-0138::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- actions: `appended_source_evidence_to_rationale`
- rationale: The edit adds a comma after 'civilization' to separate the introductory phrase from the main clause, which is a stylistic choice to improve readability and clarity. However, this comma is not strictly necessary for grammatical correctness, making the edit optional rather than mandatory. The cited source evidence is "ci

### rf-edit-0255::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- actions: `appended_source_evidence_to_rationale;capped_confidence_at_0.8`
- rationale: The word 'sister' at the end of the first sentence is followed by a comma, which indicates the sentence is not yet complete. Adding a period after 'sister' would properly terminate the sentence, making it grammatically correct and stylistically appropriate. The cited source evidence is "sister" as modified token; "litt

### rf-edit-0255::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- actions: `appended_source_evidence_to_rationale;capped_confidence_at_0.8`
- rationale: The word 'sister' at the end of the first sentence is followed by a comma, which is incorrect because the sentence is complete. Adding a period after 'sister' would properly terminate the sentence. The cited source evidence is "sister" as modified token; "little" as noun number context; "she" as noun phrase context.

### rf-edit-0276::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- actions: `appended_source_evidence_to_rationale;capped_confidence_at_0.8`
- rationale: The article 'the' before 'latter half of the 20th century' is stylistically optional because the time period is clearly defined and widely understood in the context. Removing it results in a more concise and natural phrasing. The cited source evidence is "people" as head noun.

### rf-edit-0276::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- actions: `appended_source_evidence_to_rationale;capped_confidence_at_0.8`
- rationale: The article 'the' is stylistically unnecessary before 'latter half of the 20th century' because it refers to a general time period rather than a specific instance. Removing 'the' makes the sentence more concise and natural in standard English usage. The cited source evidence is "people" as head noun.

### rf-edit-0035::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- actions: `replaced_rationale_edit_copy;capped_confidence_at_0.8`
- rationale: The cited source evidence is "peoples" as noun number context; "lives" as noun phrase context. This evidence supports the rule that Use an apostrophe to indicate possession in plural nouns.

### rf-edit-0165::qwen3_8b::natural::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- actions: `replaced_rationale_edit_copy;capped_confidence_at_0.8`
- rationale: The cited source evidence is "positive" as head noun. This evidence supports the rule that Articles should be used to specify definiteness or indefiniteness in nouns.

### rf-edit-0165::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- actions: `replaced_rationale_edit_copy;capped_confidence_at_0.8`
- rationale: The cited source evidence is "positive" as head noun. This evidence supports the rule that Use of indefinite articles ('a', 'an') before singular countable nouns.

### rf-edit-0265::qwen3_8b::rule_grounded::evidence_canonicalized::structured_evidence_repaired::targeted_repaired

- actions: `replaced_rationale_edit_copy;capped_confidence_at_0.8`
- rationale: The cited source evidence is "our" as verb complement or time context. This evidence supports the rule that In the structure 'how different our lives are', the verb 'are' should be used instead of 'is' to maintain subject-verb agreement.

## Limitations

- This repair improves structural evidence integration, but it does not prove grammatical correctness.
- Repaired candidates must pass the target-masked and rule/evidence gates again.
- Repaired candidates remain automatic pseudo-label artifacts, not human gold.
