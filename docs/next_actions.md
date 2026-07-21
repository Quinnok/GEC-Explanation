# Next Actions

Last updated: 2026-07-21

## Next Highest-Priority Loop

Use the 17 Codex-pseudo-accepted Qwen3 candidates for a minimal internal RuleFaith smoke test and prepare a real-human natural explanation validation package for paper-quality evidence. The same-setting teacher and selection baselines have been filled in under `results/rulefaith/` and `results/paper_assets/`.

## Required Work

1. Use `annotation/rulefaith_qwen3_ready_validation_v2/ready_validation_completed_by_codex.csv` only as internal pseudo-validation.
2. Use `annotation/rulefaith_qwen3_ready_validation_v2/ready_validation_completed_by_codex_merged_with_key.csv` to trace provisional accepts/refines/rejects back to candidate IDs.
3. Build a small RuleFaith smoke set from the 17 pseudo-accepted candidates plus matched refine/reject contrasts.
4. Do not report Codex pseudo-labels as human labels.
5. Prepare a blinded natural-explanation validation package before making final method-paper claims.
6. Treat `results/rulefaith/rulefaith_teacher_baselines.csv` as the current answer to the baseline question: FLAN-T5-base, Qwen2.5-0.5B, Qwen2.5-1.5B probe, and Qwen3-8B direct teacher baselines were all evaluated in the same candidate-generation setting.
7. Treat `results/rulefaith/rulefaith_selection_baselines.csv` as a small internal selection diagnostic only; it uses Codex/AI pseudo-validation, not human labels.

## Do Not Do Yet

- Do not train SFT or preference models on Qwen3 positives.
- Do not treat Qwen3 accepted or Codex-pseudo-accepted candidates as human-gold explanations.
- Do not treat Codex labels as human audit results.
- Do not expand the benchmark or counterfactual set before closing this quality gate.
- Do not describe model-only evidence refinement as successful: both smoke and 20-edit probe fixed wrong-evidence flags mostly by clearing evidence spans.
- Do not treat `evidence_contextual=160/160` as proof of final evidence correctness; use the stricter specific-source-evidence and RuleFaith selection results.
- Do not treat field-aware `accepted=45` as final positives; it is only a target-masked validation pool.
- Do not treat target-masked `validated=47` as final positives; it is still an automatic heuristic pool.
- Do not treat rule-plausibility `ready_for_human_spotcheck=25` as final positives; it is only ready for blind validation.
- Do not expose `ready_validation_key.csv` to blind validators.
- Do not call Codex-filled validation human labels.
- Do not hide the 11 rejects from the method narrative; they show why automatic gates are insufficient.
