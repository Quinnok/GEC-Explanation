# Current Status

Last updated: 2026-07-20

## Current Branch

`main`

## Current Commit

`9fd12b9` before Loop A changes.

## Current Method Version

RuleFaith-GEC method line, Qwen3-8B local open-teacher pilot, before targeted refinement.

## Completed Loops

- Round 15 human-grounded metric stress test is merged into `main`.
- Round 16--20 method scaffolding, edit pool, verifier calibration, Qwen2.5/Qwen3 teacher pilots are merged into `main`.
- Loop A / Qwen3-8B candidate audit generated an automatic audit package over all 160 Qwen3 candidates and selected 80 stratified rows for manual review.

## Running Loops

- Evidence verifier/prompt repair is the next loop; no long-running command is active.

## Blocked Loops

- GPT-5.5 teacher generation is blocked until API credentials and budget are available.
- Natural explanation human evaluation is blocked until a new blinded package is prepared and real annotators are available.
- Student training is blocked until teacher candidates pass manual audit and refinement.
- Full `pytest` verification is blocked because `pytest` is not installed in the current shell; `python3 -m unittest discover -s experiments/tests` passes.

## Best Verified Result

The Qwen3-8B pilot produced 160 parsed teacher candidates with no generator-input leakage detected by the audit. Source edit spans and target presence in predictions passed for all 160 candidates.

## Largest Scientific Risk

Evidence grounding remains weak: only 48/160 candidates have evidence spans whose token indices exactly match the source, and 109/160 are missing contextual evidence under the automatic audit.

## Next Highest-Value Action

Fix the evidence-span verifier and teacher/refinement prompt before using Qwen3 accepted/refine candidates as positive SFT or preference data.
