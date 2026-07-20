# Next Actions

Last updated: 2026-07-20

## Next Highest-Priority Loop

Run a 20-edit canonicalization-plus-refinement probe on remaining missing-evidence cases, then hand off the canonicalized blind audit package.

## Required Work

1. Build a 20-edit probe from candidates that still lack contextual evidence after canonicalization.
2. Apply targeted Qwen3 model refinement only to those remaining failures.
3. Compare canonicalized-only vs canonicalized+refined outputs with the strict evidence gate.
4. Send either the original blind audit package or `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_form.csv` plus guidelines to a human auditor.
5. Only then use accepted/refine candidates for preference construction.

## Do Not Do Yet

- Do not train SFT or preference models on Qwen3 positives.
- Do not treat Qwen3 accepted candidates as human-gold explanations.
- Do not expand the benchmark or counterfactual set before closing this quality gate.
- Do not describe model-only evidence refinement as successful: the smoke run fixed wrong-evidence flags mostly by clearing evidence spans.
