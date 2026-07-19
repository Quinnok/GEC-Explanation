# RuleFaith-GEC Method Loop State

Last updated: 2026-07-20

## Current Branch

`method/rulefaith-gec`

## Frozen Baseline

Stress-test paper frozen at commit `4519543060cbaff49806fd9963412f4ca4ab83c0`.

## Current Round

Round 20 open-teacher prefilter: verifier calibration conditionally passed on the Round 15 human-adjudicated pressure-test set; Qwen small and FLAN-T5 open-teacher pilots have run, but neither provides enough accepted positive candidates for distillation. GPT-5.5 teacher generation remains blocked by missing API credentials.

## Highest-Priority Problem

Move from human-grounded metric stress testing to a method that produces and selectively abstains from edit-level GEC explanations.

## Current Known Blockers

- `OPENAI_API_KEY` is not visible in the current environment, so GPT-5.5 teacher generation cannot run yet.
- `openai` Python SDK is not visible in the current environment; installation attempts were interrupted by very slow package download, so the GPT branch remains optional-import guarded.
- Available local open teachers are insufficient for positive teacher data: Qwen2.5-0.5B produced only 1 accepted candidate out of 160, and Qwen2.5-1.5B probe produced 0 accepted candidates out of 20 under the current RuleFaith prefilter.
- Student model training may require GPU/model downloads and later user confirmation if a model exceeds 10GB.
- New natural explanation human evaluation will require real annotators later.

## Latest Completed Work

- Round 16 method branch and preregistration.
- Round 17 substantive edit pool: 300 selected edits, source-level train/dev/test split, model-family coverage, dataset coverage, and leakage audits.
- Round 18 teacher-generation scaffolding and open-teacher pilot: 160 FLAN-T5-base candidates for 80 edits, with quality audit showing a 61.25% low-quality rate; GPT-5.5 branch blocked by missing `OPENAI_API_KEY`.
- Round 19 verifier calibration: Rule/Evidence verifier conditionally passes Gate A on stress-test labels, with rule/evidence AUROC above reverse reconstruction.
- Qwen small teacher addendum: implemented `qwen_small` provider, config, raw-response logging, parse-failure logging, and parallel shard runner.
- Round 20 open-teacher prefilter: Qwen2.5-0.5B generated 160 candidates; parse JSON rate 0.975, alignment proxy pass 0.769, rule edit-copy rate 0.887, contextual evidence rate 0.037, accepted 1/160. FLAN-T5 accepted 0/160. Qwen2.5-1.5B non-punctuation probe accepted 0/20 because all candidates lacked explicit rule text.

## Next Internal Action

Provide GPT-5.5 API credentials and budget/model confirmation, or approve a stronger local teacher/prompting strategy. Do not enter SFT/preference training with the current FLAN/Qwen small outputs as positives.
