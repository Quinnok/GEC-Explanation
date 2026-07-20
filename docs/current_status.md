# Current Status

Last updated: 2026-07-20

## Current Branch

`main`

## Current Commit

Loop D evidence-refinement probe commit; use `git log --oneline -1` as the authoritative hash. The loop started from `841317b`.

## Current Method Version

RuleFaith-GEC method line, Qwen3-8B local open-teacher pilot, after deterministic evidence-span canonicalization and a 20-edit canonicalization-plus-refinement probe.

## Completed Loops

- Round 15 human-grounded metric stress test is merged into `main`.
- Round 16--20 method scaffolding, edit pool, verifier calibration, Qwen2.5/Qwen3 teacher pilots are merged into `main`.
- Loop A / Qwen3-8B candidate audit generated an automatic audit package over all 160 Qwen3 candidates and selected 80 stratified rows for manual review.
- Loop B / evidence gate repair tightened evidence-span validation, updated the Qwen3 prompt constraints, and generated a blind 80-row human audit package.
- Loop C / targeted evidence refinement showed that model-only evidence repair is JSON-stable but mostly clears evidence instead of adding contextual evidence; deterministic span canonicalization improves smoke10 and full-pool evidence scores.
- Loop D / 20-edit evidence refinement probe confirmed that targeted Qwen3 evidence repair after canonicalization is not ready to scale: 20/20 parsed, but contextual source evidence dropped from 7/20 to 2/20.

## Running Loops

- No long-running command is active. The next loop is human audit handoff for the canonicalized Qwen3 blind audit package.

## Blocked Loops

- GPT-5.5 teacher generation is blocked until API credentials and budget are available.
- Natural explanation human evaluation is blocked until a new blinded package is prepared and real annotators are available.
- Student training is blocked until teacher candidates pass the stricter evidence gate, manual audit, and refinement.
- Full `pytest` verification is blocked because `pytest` is not installed in the current shell; `python3 -m unittest discover -s experiments/tests` passes.

## Best Verified Result

The Qwen3-8B pilot produced 160 parsed teacher candidates with no generator-input leakage detected by the audit. Source edit spans and target presence in predictions passed for all 160 candidates. Prompt-v2 smoke10 generated 10/10 parsed candidates with 0/10 prediction-only evidence, but only 3/10 contextual source evidence. Deterministic evidence-span canonicalization on smoke10 improved contextual source evidence from 3/10 to 8/10 and reduced wrong-evidence automatic flags from 6/10 to 0/10. Full-pool canonicalization improved all-spans source-index match from 20/160 to 155/160, contextual source evidence from 24/160 to 82/160, and wrong-evidence flags from 141/160 to 29/160. Canonicalized prefilter buckets are accepted 34, refine 67, rejected 59. A canonicalized blind 80-row audit package exists under `annotation/rulefaith_qwen3_audit_canonicalized/`. The Loop D 20-edit probe parsed 20/20 Qwen3 refined outputs, but contextual source evidence dropped from 7/20 to 2/20 and missing evidence rose from 13/20 to 18/20, so this refinement prompt is rejected for scaling.

## Largest Scientific Risk

Evidence grounding remains incomplete after canonicalization: 78/160 candidates still lack contextual source evidence, 29/160 retain prediction-only/wrong-evidence risk, and model-only Qwen3 repair can remove evidence rather than ground it. Canonicalization does not prove linguistic rule correctness.

## Next Highest-Value Action

Hand off `annotation/rulefaith_qwen3_audit_canonicalized/manual_audit_form.csv` and `annotation/rulefaith_qwen3_audit_canonicalized/guidelines.md` to a real human auditor. Do not use Qwen3 candidates as positives until the audit passes and the evidence verifier/refinement strategy is revised.
