# RuleFaith-GEC Method Loop State

Last updated: 2026-07-20

## Current Branch

`method/rulefaith-gec`

## Frozen Baseline

Stress-test paper frozen at commit `4519543060cbaff49806fd9963412f4ca4ab83c0`.

## Current Round

Round 20 open-teacher prefilter: verifier calibration conditionally passed on the Round 15 human-adjudicated pressure-test set. FLAN-T5 and Qwen2.5 open-teacher pilots were too weak for positive distillation data, but the Qwen3-8B no-thinking pilot produced the first non-trivial local open-teacher candidate pool.

## Highest-Priority Problem

Move from human-grounded metric stress testing to a method that produces and selectively abstains from edit-level GEC explanations.

## Current Known Blockers

- `OPENAI_API_KEY` is not visible in the current environment, so GPT-5.5 teacher generation cannot run yet.
- `openai` Python SDK is not visible in the current environment; installation attempts were interrupted by very slow package download, so the GPT branch remains optional-import guarded.
- Qwen3-8B accepted 41/160 candidates under the conservative RuleFaith prefilter, but these need manual spot-checking and/or refinement before SFT/preference construction.
- Student model training may require GPU/model downloads and later user confirmation if a model exceeds 10GB.
- New natural explanation human evaluation will require real annotators later.

## Latest Completed Work

- Round 16 method branch and preregistration.
- Round 17 substantive edit pool: 300 selected edits, source-level train/dev/test split, model-family coverage, dataset coverage, and leakage audits.
- Round 18 teacher-generation scaffolding and open-teacher pilot: 160 FLAN-T5-base candidates for 80 edits, with quality audit showing a 61.25% low-quality rate; GPT-5.5 branch blocked by missing `OPENAI_API_KEY`.
- Round 19 verifier calibration: Rule/Evidence verifier conditionally passes Gate A on stress-test labels, with rule/evidence AUROC above reverse reconstruction.
- Qwen small teacher addendum: implemented `qwen_small` provider, config, raw-response logging, parse-failure logging, and parallel shard runner.
- Round 20 open-teacher prefilter: Qwen2.5-0.5B generated 160 candidates; parse JSON rate 0.975, alignment proxy pass 0.769, rule edit-copy rate 0.887, contextual evidence rate 0.037, accepted 1/160. FLAN-T5 accepted 0/160. Qwen2.5-1.5B non-punctuation probe accepted 0/20 because all candidates lacked explicit rule text. Qwen3-8B generated 160 candidates with thinking disabled; parse JSON rate 0.994, rule edit-copy rate 0.006, contextual evidence rate 0.388, and conservative prefilter accepted 41/160 with 63 candidates marked for refinement.

## Next Internal Action

Run RuleFaith refinement and manual spot-checking for Qwen3-8B accepted/refine candidates. Do not enter SFT/preference training until accepted/refined Qwen3 candidates pass this quality gate, or GPT-5.5 credentials become available.
