# RuleFaith-GEC Method Loop State

Last updated: 2026-07-19

## Current Branch

`method/rulefaith-gec`

## Frozen Baseline

Stress-test paper frozen at commit `4519543060cbaff49806fd9963412f4ca4ab83c0`.

## Current Round

Round 17: substantive edit pool complete; Round 18 teacher candidate generation is next.

## Highest-Priority Problem

Move from human-grounded metric stress testing to a method that produces and selectively abstains from edit-level GEC explanations.

## Current Known Blockers

- `OPENAI_API_KEY` is not visible in the current environment, so GPT-5.5 teacher generation cannot run yet.
- Student model training may require GPU/model downloads and later user confirmation if a model exceeds 10GB.
- New natural explanation human evaluation will require real annotators later.

## Latest Completed Work

- Round 16 method branch and preregistration.
- Round 17 substantive edit pool: 300 selected edits, source-level train/dev/test split, model-family coverage, dataset coverage, and leakage audits.

## Next Internal Action

Design teacher-generation prompts and scripts, then run the 80-edit teacher pilot if GPT-5.5 credentials are available.
