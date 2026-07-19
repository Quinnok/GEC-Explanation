# RuleFaith-GEC Method Loop State

Last updated: 2026-07-19

## Current Branch

`method/rulefaith-gec`

## Frozen Baseline

Stress-test paper frozen at commit `4519543060cbaff49806fd9963412f4ca4ab83c0`.

## Current Round

Round 19: verifier calibration conditionally passed on the Round 15 human-adjudicated pressure-test set; Round 18 GPT-5.5 teacher generation remains blocked by missing API credentials.

## Highest-Priority Problem

Move from human-grounded metric stress testing to a method that produces and selectively abstains from edit-level GEC explanations.

## Current Known Blockers

- `OPENAI_API_KEY` is not visible in the current environment, so GPT-5.5 teacher generation cannot run yet.
- `openai` Python SDK is not visible in the current environment; installation attempts were interrupted by very slow package download, so the GPT branch remains optional-import guarded.
- Student model training may require GPU/model downloads and later user confirmation if a model exceeds 10GB.
- New natural explanation human evaluation will require real annotators later.

## Latest Completed Work

- Round 16 method branch and preregistration.
- Round 17 substantive edit pool: 300 selected edits, source-level train/dev/test split, model-family coverage, dataset coverage, and leakage audits.
- Round 18 teacher-generation scaffolding and open-teacher pilot: 160 FLAN-T5-base candidates for 80 edits, with quality audit showing a 61.25% low-quality rate; GPT-5.5 branch blocked by missing `OPENAI_API_KEY`.
- Round 19 verifier calibration: Rule/Evidence verifier conditionally passes Gate A on stress-test labels, with rule/evidence AUROC above reverse reconstruction.

## Next Internal Action

Provide GPT-5.5 API credentials and budget/model confirmation to run the 80-edit GPT teacher pilot; without that, proceed only with verifier/refinement scaffolding and do not enter preference-data construction.
