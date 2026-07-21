# RuleFaith Natural Explanation Annotation Guidelines

You are evaluating natural edit-level explanations for Grammatical Error Correction (GEC).

For each row, judge only the displayed source sentence, model prediction, atomic model edit, and explanation fields. Do not infer hidden model reasoning. Do not assume the edit is correct.

Fill these labels:

- `edit_alignment_label`: correct, partially_correct, incorrect, uncertain.
- `edit_validity_label`: valid, acceptable_alternative, invalid, stylistic, uncertain.
- `rule_correctness_label`: correct, partially_correct, incorrect, not_applicable, uncertain.
- `evidence_label`: correct, partially_correct, incorrect, not_provided, uncertain.
- `overall_faithfulness_label`: faithful, partially_faithful, unfaithful, uncertain.
- `learner_helpfulness_label`: helpful, partially_helpful, unhelpful, uncertain.
- `fluency_label`: fluent, mostly_fluent, disfluent, uncertain.
- `preference_label`: best_in_group, acceptable_not_best, not_preferred, uncertain.
- `notes`: concise explanation when needed.

Important rules:

1. Evaluate only the current atomic edit, not every edit in the full model prediction.
2. A wrong model edit can be faithfully described if the explanation honestly identifies the problem.
3. Pure edit-copy is at most partially faithful unless it also gives a correct rule and contextual evidence.
4. Evidence must be source-grounded. Mentioning only the changed token is not automatically contextual evidence.
5. Do not reward long explanations unless they are specific, correct, and evidence-grounded.
6. Do not use system identity. The rows are randomized and anonymized.
7. Rows sharing the same `edit_group_id` are alternative explanations for the same edit. Use `preference_label` relative to other rows in the same group after reviewing the group.
