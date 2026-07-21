# RuleFaith Qwen3 Ready-Candidate Blind Validation Guidelines

This package is for validating candidate GEC edit explanations that passed automatic RuleFaith filters.

Important boundaries:

- The candidates are automatically filtered teacher outputs, not human gold.
- The validator should not know the teacher model, automatic decision, dataset, or previous filter score.
- Judge only the displayed source sentence, model prediction, atomic edit, and explanation fields.
- Do not infer hidden model reasoning.

Fill only:

- `validator_edit_alignment`
- `validator_edit_validity`
- `validator_rule_plausibility`
- `validator_evidence_sufficiency`
- `validator_overall_decision`
- `validator_notes`

Allowed values:

- `validator_edit_alignment`: `pass`, `partial`, `fail`, `uncertain`
- `validator_edit_validity`: `valid`, `acceptable_alternative`, `invalid`, `stylistic`, `uncertain`
- `validator_rule_plausibility`: `plausible`, `weak`, `implausible`, `uncertain`
- `validator_evidence_sufficiency`: `sufficient`, `partial`, `insufficient`, `uncertain`
- `validator_overall_decision`: `accept`, `refine`, `reject`, `uncertain`

Decision rule:

- Use `accept` only when alignment passes, edit validity is understood, the rule is plausible, and evidence is sufficient.
- Use `refine` when the explanation is mostly correct but needs clearer evidence, weaker confidence, or less edit-copy wording.
- Use `reject` when the rule is implausible, evidence is insufficient, or the explanation describes the wrong edit.
- Use `uncertain` only when the item cannot be judged from the displayed information.

Notes should be short and factual.
