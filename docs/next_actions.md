# Next Actions

Last updated: 2026-07-21

## Next Highest-Priority Loop

Run target-masked validation over the 45 field-aware accepted candidates and 13 field-aware refine candidates from repaired Qwen3 outputs.

## Required Work

1. Use `data/rulefaith/filtering/qwen3_field_aware_rulefaith_accepted.jsonl` and `data/rulefaith/filtering/qwen3_field_aware_rulefaith_refine.jsonl` as the next validation inputs.
2. Add a target-masked verifier that hides the target edit from rule/rationale scoring.
3. Compare target-visible and target-masked scores for alignment, rule, evidence, leakage, and genericness.
4. Keep structured evidence repair and field-aware selection as preprocessing, not final scoring.
5. Do not promote any candidate to SFT positive data until target-masked and human/stronger validation support it.

## Do Not Do Yet

- Do not train SFT or preference models on Qwen3 positives.
- Do not treat Qwen3 accepted candidates as human-gold explanations.
- Do not treat Codex labels as human audit results.
- Do not expand the benchmark or counterfactual set before closing this quality gate.
- Do not describe model-only evidence refinement as successful: both smoke and 20-edit probe fixed wrong-evidence flags mostly by clearing evidence spans.
- Do not treat `evidence_contextual=160/160` as proof of final evidence correctness; use the stricter specific-source-evidence and RuleFaith selection results.
- Do not treat field-aware `accepted=45` as final positives; it is only a target-masked validation pool.
