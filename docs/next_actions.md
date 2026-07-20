# Next Actions

Last updated: 2026-07-20

## Next Highest-Priority Loop

Send the prepared canonicalized Qwen3 blind audit package to a real human auditor, then validate and merge the completed labels.

## Required Work

1. Send only `annotation/rulefaith_qwen3_audit_canonicalized/qwen3_canonicalized_human_audit_package.zip` to a real human auditor.
2. Keep `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_key.csv` hidden until after annotation.
3. Save the completed form as `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed.csv`.
4. Run `python3 experiments/rulefaith/validate_qwen3_human_audit.py --form annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed.csv --key annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_key.csv --merged-output annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_merged_with_key.csv --summary-output results/rulefaith/qwen3_human_audit_validation_summary.json --report-output results/rulefaith/qwen3_human_audit_validation_report.md --overwrite`.
5. Use validated human audit outcomes to update the evidence verifier and decide whether any canonicalized Qwen3 candidates can become positives.
6. If evidence quality remains weak, redesign the refiner prompt or move to a stronger teacher before preference construction.

## Do Not Do Yet

- Do not train SFT or preference models on Qwen3 positives.
- Do not treat Qwen3 accepted candidates as human-gold explanations.
- Do not expand the benchmark or counterfactual set before closing this quality gate.
- Do not describe model-only evidence refinement as successful: both smoke and 20-edit probe fixed wrong-evidence flags mostly by clearing evidence spans.
