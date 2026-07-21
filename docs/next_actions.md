# Next Actions

Last updated: 2026-07-21

## Next Highest-Priority Loop

Send the natural explanation blind validation package to two independent annotators and collect completed forms. The package is ready at `annotation/rulefaith_natural/rulefaith_natural_validation_handoff.zip`.

## Required Work

1. Send only `annotation/rulefaith_natural/rulefaith_natural_validation_handoff.zip` to annotators.
2. Do not send `annotation/rulefaith_natural/hidden_system_key.csv`.
3. After receiving completed A/B forms, validate that item IDs are unchanged, labels are legal, and no metadata columns changed.
4. Compute agreement for edit alignment, edit validity, rule correctness, evidence correctness, overall faithfulness, learner helpfulness, fluency, and preference.
5. Create an adjudication file for disagreements and preserve raw A/B labels.
6. Do not report Codex pseudo-labels as human labels.
7. Treat `results/rulefaith/rulefaith_teacher_baselines.csv` as the current answer to the baseline question: FLAN-T5-base, Qwen2.5-0.5B, Qwen2.5-1.5B probe, and Qwen3-8B direct teacher baselines were all evaluated in the same candidate-generation setting.
8. Treat `results/rulefaith/rulefaith_ready_selector_metrics.json` as a revision signal: the deployable scorer beats first/highest-confidence selectors but remains below the rule-grounded simple selector.

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
- Do not tune the deployable scorer thresholds on Codex pseudo-labels; use a blinded natural-explanation package or preregistered dev split before revising thresholds.
