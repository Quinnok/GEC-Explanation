# Round 10 Annotation Guidelines

## Task A: Edit Explanation Faithfulness

Judge whether the explanation faithfully describes why the model made the shown edit. The question is about the model edit, not whether the edit is grammatically ideal.

Labels:

- `faithful`: the explanation identifies the correct edit target/direction and gives a rule or evidence compatible with the model edit.
- `partially_faithful`: the explanation is related but misses an important span, target, direction, rule, or evidence detail.
- `unfaithful`: the explanation points to the wrong edit, wrong rule, wrong evidence, wrong direction, or is generic.
- `uncertain`: the case is ambiguous, impossible to judge, or depends on an acceptable alternative correction.

## Task B: Counterfactual Edit Simulatability

Given the original edit, explanation, and counterfactual source, predict what should happen to the original edit if the explanation is faithful.

Labels:

- `preserve`: the same edit should still be made.
- `cancel`: the original edit should disappear.
- `change_target`: the edit should remain at the same target but change correction text.
- `change_span`: the correction should move to a different span.
- `change_operation`: the operation should change.
- `competing_edit`: other edits dominate and the original edit behavior cannot be cleanly isolated.
- `uncertain`: the counterfactual is invalid or ambiguous.

## Protocol

Use two independent annotators per item. Do not show annotators `annotation_metadata_with_auto_labels.jsonl`. Resolve disagreements in `adjudication_template.csv`. These files contain no human gold labels until real annotators fill them.
