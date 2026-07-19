# Annotation Final Gold V2 Data Card

Created: `2026-07-19T11:34:28+00:00`

## Scope

- Includes 160 `edit_explanation_faithfulness` items.
- Excludes 80 counterfactual items because their explanation fields were incomplete in Round 10.
- Combines double annotations from two independent human annotators with third-party human adjudication.

## Provenance

A/B annotations were completed by two independent human annotators and disagreements were resolved by a human third-party adjudicator, as confirmed by the user on 2026-07-19.

- Annotators: two independent human annotators, confirmed by the user on 2026-07-19.
- Adjudicator: human third-party adjudicator, confirmed by the user on 2026-07-19.

## Counts

- Adjudicated disagreements: 100
- Agreement-inherited items: 60
- Missing instance ids: 0

## Final Label Distribution

### final_edit_alignment

- `correct`: 18
- `incorrect`: 96
- `partially_correct`: 46

### final_edit_validity

- `acceptable_alternative`: 3
- `invalid`: 7
- `stylistic`: 13
- `uncertain`: 3
- `valid`: 134

### final_rule_correctness

- `correct`: 4
- `incorrect`: 39
- `not_applicable`: 99
- `partially_correct`: 18

### final_evidence

- `correct`: 1
- `incorrect`: 19
- `not_provided`: 125
- `partially_correct`: 15

### final_faithfulness

- `faithful`: 1
- `partially_faithful`: 57
- `unfaithful`: 102

## Important Limitations

- The benchmark is a stress-test sample, not a natural random sample of all GEC explanations.
- Only one item is labeled fully `faithful`; report binary and ordinal tasks carefully.
- Agreement-inherited items were not independently blind-audited in this automated run.
- Because the set is intentionally adversarial and template-heavy, do not use its label prevalence as an estimate of natural GEC explanation quality.
