# Qwen3-8B RuleFaith Manual Audit Guidelines

You are auditing model-generated explanation candidates for edit-level GEC explanations.

## Scope

- Audit rows: 80
- Each row evaluates one model-produced atomic edit and one Qwen3-8B explanation candidate.
- The file is blind: it does not show accepted/refine/rejected bucket labels or automatic risk flags.
- These explanations are teacher-generated candidates, not human gold.

## What To Check

Fill each issue column with `yes`, `no`, or `uncertain`.

- `human_alignment_error`: yes if the explanation describes a different edit, wrong operation, wrong source text, wrong target text, or wrong direction.
- `human_validity_error`: yes if the explanation says or implies the model edit is valid when the edit is invalid, unnecessary, or only stylistic.
- `human_wrong_rule`: yes if the stated linguistic rule is false.
- `human_inapplicable_rule`: yes if the rule is true in general but does not justify this edit in this sentence.
- `human_missing_evidence`: yes if no sentence-specific contextual evidence is provided.
- `human_wrong_evidence`: yes if the cited evidence span, token index, trigger, subject, antecedent, governor, or contextual relation is wrong.
- `human_generic_explanation`: yes if the explanation could apply to many unrelated sentences and does not identify this case's concrete trigger.
- `human_edit_copy`: yes if the explanation mainly copies the source-target edit without rule or evidence grounding.
- `human_semantic_distortion`: yes if the explanation changes the intended meaning or rationalizes a semantically wrong correction.
- `human_unsupported_confidence`: yes if the confidence is high despite missing evidence, weak rule support, invalid edit, or uncertainty.

## Evidence Rules

- Evidence spans must refer to text in the original SOURCE, not the model prediction.
- The `start` and `end` fields are whitespace-token offsets in SOURCE.
- A target phrase that only appears in MODEL_PREDICTION is not source evidence.
- The modified token alone is usually not enough evidence for grammar rules.
- For spelling, capitalization, and punctuation, the edited token itself may be sufficient only if the explanation explicitly concerns that orthographic property.
- Subject-verb agreement should cite the subject and verb.
- Article/determiner explanations should cite the head noun and definiteness/countability/number cue when available.
- Tense explanations should cite the time cue or relevant event context when available.
- Preposition explanations should cite the governing verb/adjective/noun or collocation when available.

## Decision

Use `human_decision`:

- `accept`: explanation is aligned and has no serious rule/evidence/validity issue.
- `refine`: explanation is useful but needs targeted repair.
- `reject`: explanation is misleading, wrong, too generic, or mostly edit-copy.
- `abstain`: there is not enough information to judge or the edit itself is too ambiguous.

Keep notes concise. Do not use automatic labels or previous audit outputs while filling the blind form.
