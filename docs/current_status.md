# Current Status

Last updated: 2026-07-20

## Current Branch

`main`

## Current Commit

Loop B evidence-gate commit; use `git log --oneline -1` as the authoritative hash. The loop started from `a8549e5`.

## Current Method Version

RuleFaith-GEC method line, Qwen3-8B local open-teacher pilot, before targeted refinement.

## Completed Loops

- Round 15 human-grounded metric stress test is merged into `main`.
- Round 16--20 method scaffolding, edit pool, verifier calibration, Qwen2.5/Qwen3 teacher pilots are merged into `main`.
- Loop A / Qwen3-8B candidate audit generated an automatic audit package over all 160 Qwen3 candidates and selected 80 stratified rows for manual review.
- Loop B / evidence gate repair tightened evidence-span validation, updated the Qwen3 prompt constraints, and generated a blind 80-row human audit package.

## Running Loops

- No long-running command is active. The next loop is Qwen3 prompt-v2 regeneration or targeted refinement smoke testing.

## Blocked Loops

- GPT-5.5 teacher generation is blocked until API credentials and budget are available.
- Natural explanation human evaluation is blocked until a new blinded package is prepared and real annotators are available.
- Student training is blocked until teacher candidates pass the stricter evidence gate, manual audit, and refinement.
- Full `pytest` verification is blocked because `pytest` is not installed in the current shell; `python3 -m unittest discover -s experiments/tests` passes.

## Best Verified Result

The Qwen3-8B pilot produced 160 parsed teacher candidates with no generator-input leakage detected by the audit. Source edit spans and target presence in predictions passed for all 160 candidates. A blind 80-row audit package now exists under `annotation/rulefaith_qwen3_audit/`. Prompt-v2 smoke10 generated 10/10 parsed candidates with 0/10 prediction-only evidence, but only 3/10 contextual source evidence.

## Largest Scientific Risk

Evidence grounding remains weak under the stricter gate: only 20/160 candidates have all evidence spans source-index matched, only 24/160 have contextual source evidence, and 87/160 include prediction-only evidence.

## Next Highest-Value Action

Implement targeted evidence refinement or strengthen the evidence prompt, then rerun a 10--20 edit audit. Do not use Qwen3 v1 candidates as positives yet.
