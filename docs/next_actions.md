# Next Actions

Last updated: 2026-07-20

## Next Highest-Priority Loop

Implement targeted evidence refinement for Qwen3 prompt-v2 outputs.

## Required Work

1. Add a targeted evidence-refinement prompt that asks Qwen3 to repair only missing/wrong evidence spans.
2. Run it on the 10 prompt-v2 smoke candidates with missing evidence.
3. Re-audit refined outputs with the strict evidence gate.
4. If contextual source evidence improves without adding prediction-only evidence, scale to the 80-row audit subset.
4. Send `annotation/rulefaith_qwen3_audit/manual_audit_form.csv` and `annotation/rulefaith_qwen3_audit/guidelines.md` to a human auditor.
5. Only then use accepted/refine candidates for targeted refinement or preference construction.

## Do Not Do Yet

- Do not train SFT or preference models on Qwen3 positives.
- Do not treat Qwen3 accepted candidates as human-gold explanations.
- Do not expand the benchmark or counterfactual set before closing this quality gate.
