# Next Actions

Last updated: 2026-07-20

## Next Highest-Priority Loop

Fix evidence grounding before targeted refinement.

## Required Work

1. Tighten evidence-span validation so source token indices, text, and contextual role are checked separately.
2. Update Qwen3/refinement prompt to require evidence spans from the original source only.
3. Re-run `experiments/rulefaith/build_qwen3_manual_audit.py`.
4. Manually review the 80 selected rows in `results/rulefaith/qwen3_manual_audit.csv`.
5. Only then use accepted/refine candidates for targeted refinement or preference construction.

## Do Not Do Yet

- Do not train SFT or preference models on Qwen3 positives.
- Do not treat Qwen3 accepted candidates as human-gold explanations.
- Do not expand the benchmark or counterfactual set before closing this quality gate.
