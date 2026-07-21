# Next Actions

Last updated: 2026-07-21

## Next Highest-Priority Loop

Implement targeted repair for the 16 Qwen3 candidates in the ready-validation package.

## Required Work

1. Use `annotation/rulefaith_qwen3_ready_validation/repair_instructions.csv`.
2. Generate revised explanations that explicitly integrate evidence, remove rationale edit-copy, and reduce unsupported high confidence.
3. Re-run target-masked validation and rule/evidence audit on repaired candidates.
4. Merge successful repairs into a separate validation candidate pool.
5. Do not promote any candidate to SFT positive data until human/stronger validation support it.

## Do Not Do Yet

- Do not train SFT or preference models on Qwen3 positives.
- Do not treat Qwen3 accepted candidates as human-gold explanations.
- Do not treat Codex labels as human audit results.
- Do not expand the benchmark or counterfactual set before closing this quality gate.
- Do not describe model-only evidence refinement as successful: both smoke and 20-edit probe fixed wrong-evidence flags mostly by clearing evidence spans.
- Do not treat `evidence_contextual=160/160` as proof of final evidence correctness; use the stricter specific-source-evidence and RuleFaith selection results.
- Do not treat field-aware `accepted=45` as final positives; it is only a target-masked validation pool.
- Do not treat target-masked `validated=47` as final positives; it is still an automatic heuristic pool.
- Do not treat rule-plausibility `ready_for_human_spotcheck=25` as final positives; it is only ready for blind validation.
- Do not expose `ready_validation_key.csv` to blind validators.
