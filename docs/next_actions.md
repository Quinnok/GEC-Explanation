# Next Actions

Last updated: 2026-07-21

## Next Highest-Priority Loop

Use the 58 strict RuleFaith `refine` candidates from structured evidence repair to implement an alignment/leakage-aware refinement loop.

## Required Work

1. Use `data/rulefaith/filtering/qwen3_structured_rulefaith_refine.jsonl` as the next repair input.
2. Add an alignment verifier/refiner that fixes candidates whose diagnostic text does not match the atomic edit.
3. Add a leakage-aware target-masked check before accepting any candidate.
4. Keep structured evidence repair as preprocessing, not final scoring.
5. Do not promote any candidate to SFT positive data until strict RuleFaith gates and human/stronger validation support it.

## Do Not Do Yet

- Do not train SFT or preference models on Qwen3 positives.
- Do not treat Qwen3 accepted candidates as human-gold explanations.
- Do not treat Codex labels as human audit results.
- Do not expand the benchmark or counterfactual set before closing this quality gate.
- Do not describe model-only evidence refinement as successful: both smoke and 20-edit probe fixed wrong-evidence flags mostly by clearing evidence spans.
- Do not treat `evidence_contextual=160/160` as proof of final evidence correctness; use the stricter specific-source-evidence and RuleFaith selection results.
