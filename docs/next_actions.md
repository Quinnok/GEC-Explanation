# Next Actions

Last updated: 2026-07-21

## Next Highest-Priority Loop

Use the Codex-assisted Qwen3 audit prelabels for internal verifier/refiner debugging, while keeping the real-human audit as the next paper-quality evidence gate.

## Required Work

1. Treat `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_codex_prelabeled.csv` as AI-assisted pseudo-labels only.
2. Use `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_codex_prelabeled_merged_with_key.csv` and `results/rulefaith/qwen3_codex_prelabeled_breakdown.md` to identify which Qwen3 failure modes the next verifier/refiner revision should target first.
3. Do not promote any candidate to SFT positive data from Codex prelabels alone.
4. Send only `annotation/rulefaith_qwen3_audit_canonicalized/qwen3_canonicalized_human_audit_package.zip` to a real human auditor when paper-quality evidence is needed.
5. Keep `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_key.csv` hidden until after real human annotation.
6. Save the completed human form as `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed.csv`.
7. Run `python3 experiments/rulefaith/validate_qwen3_human_audit.py --form annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed.csv --key annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_key.csv --merged-output annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_merged_with_key.csv --summary-output results/rulefaith/qwen3_human_audit_validation_summary.json --report-output results/rulefaith/qwen3_human_audit_validation_report.md --overwrite`.
8. Use validated human audit outcomes to update the evidence verifier and decide whether any canonicalized Qwen3 candidates can become positives.

## Do Not Do Yet

- Do not train SFT or preference models on Qwen3 positives.
- Do not treat Qwen3 accepted candidates as human-gold explanations.
- Do not treat Codex prelabels as human audit results.
- Do not expand the benchmark or counterfactual set before closing this quality gate.
- Do not describe model-only evidence refinement as successful: both smoke and 20-edit probe fixed wrong-evidence flags mostly by clearing evidence spans.
