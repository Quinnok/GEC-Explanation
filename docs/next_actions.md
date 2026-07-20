# Next Actions

Last updated: 2026-07-20

## Next Highest-Priority Loop

Hand off the canonicalized Qwen3 blind audit package to a real human auditor, then use those labels to revise the evidence verifier and refinement strategy.

## Required Work

1. Send `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_form.csv` and `annotation/rulefaith_qwen3_audit_canonicalized/guidelines.md` to a real human auditor.
2. Keep `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_key.csv` hidden until after annotation.
3. Collect all human issue flags, notes, and `human_decision`.
4. Merge the completed audit with `manual_audit_key.csv`.
5. Use human audit outcomes to update the evidence verifier and decide whether any canonicalized Qwen3 candidates can become positives.
6. If evidence quality remains weak, redesign the refiner prompt or move to a stronger teacher before preference construction.

## Do Not Do Yet

- Do not train SFT or preference models on Qwen3 positives.
- Do not treat Qwen3 accepted candidates as human-gold explanations.
- Do not expand the benchmark or counterfactual set before closing this quality gate.
- Do not describe model-only evidence refinement as successful: both smoke and 20-edit probe fixed wrong-evidence flags mostly by clearing evidence spans.
