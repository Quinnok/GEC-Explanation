# Next Actions

Last updated: 2026-07-21

## Next Highest-Priority Loop

Use the Codex-completed Qwen3 audit forms to implement the next verifier/refiner revision. Real-human evidence remains unavailable, but the immediate blank-form bottleneck is closed for internal work.

## Required Work

1. Use `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_completed_by_codex_merged_with_key.csv` as the main internal triage input.
2. Use `annotation/rulefaith_qwen3_audit/manual_audit_completed_by_codex_merged_with_key.csv` only for pre-canonicalization comparison.
3. Prioritize fixes for missing evidence, edit-copy, unsupported confidence, wrong-rule, and false-rationalization risks.
4. Do not promote any candidate to SFT positive data from Codex labels alone.
5. If paper-quality human evidence is required later, still use the original blind handoff zip and keep hidden keys hidden until real annotation returns.

## Do Not Do Yet

- Do not train SFT or preference models on Qwen3 positives.
- Do not treat Qwen3 accepted candidates as human-gold explanations.
- Do not treat Codex labels as human audit results.
- Do not expand the benchmark or counterfactual set before closing this quality gate.
- Do not describe model-only evidence refinement as successful: both smoke and 20-edit probe fixed wrong-evidence flags mostly by clearing evidence spans.
