# Method Round 19

## Status

Verifier calibration complete with a conditional Gate A pass.

## Main Objective

Calibrate the RuleFaith verifier stack against existing human-adjudicated stress-test labels.

## Highest Risk

The calibration set is adversarial and template-heavy, so verifier success here may not transfer to natural teacher outputs.

## Git Commit

Recorded in Git history as `Round 19 verifier calibration`.

## Data Version

- Human gold stress labels: `annotation/round15/annotation_final_gold_v2.csv`
- Metric source: `results/human_gold/main_metric_table.csv`

## Model Version

No new model calls.

## Work Completed

- Created verifier calibration config.
- Added verifier directory documentation.
- Implemented `experiments/rulefaith/calibrate_verifiers.py`.
- Generated RuleFaith verifier metric JSON, calibration CSV, and verifier error cases.
- Created `docs/rulefaith_verifier_design.md`.

## Files Created or Modified

- `configs/rulefaith/verifier_calibration.yaml`
- `experiments/rulefaith/verifiers/README.md`
- `experiments/rulefaith/calibrate_verifiers.py`
- `results/rulefaith/verifier_metrics.json`
- `results/rulefaith/verifier_calibration.csv`
- `results/rulefaith/verifier_error_cases.md`
- `docs/rulefaith_verifier_design.md`

## Commands Executed

- `.venv311/bin/python -m py_compile experiments/rulefaith/calibrate_verifiers.py`
- `.venv311/bin/python experiments/rulefaith/calibrate_verifiers.py`

## Verified Results

- Gate A status: `conditional_pass`.
- Edit Alignment AUROC: 0.75.
- Rule Correctness AUROC: 0.7562582345191041.
- Evidence Correctness AUROC: 0.6666666666666666.
- Target-masked edit-alignment AUROC: 0.7582194010416666.
- Rule AUROC delta over reverse reconstruction: +0.3280632411067194.
- Evidence AUROC delta over reverse reconstruction: +0.2530381944444444.

## Failed Runs

- `cd paper && ../.local-tools/tectonic --keep-logs --keep-intermediates main.tex` failed because `aaai2027.sty` requires pdfTeX and the current shell cannot find `pdflatex` or `latexmk`.
- This round did not modify paper sources; existing `paper/main.pdf` remains from the previous successful compile.

## Scientific Interpretation

Rule/Evidence verifier signals are strong enough to justify method-pilot filtering, and they address the documented weakness of reverse reconstruction on rule/evidence failures. This remains calibration evidence, not a final natural-generation result.

## Claim-Evidence Updates

- M-C10 is conditionally supported.
- M-C1 through M-C8 remain unverified because no student training or natural explanation human evaluation has run.

## Open Issues

- Restore `pdflatex` or `latexmk` in PATH before the next paper rewrite/compile gate.
- Re-run calibration after GPT/open natural candidates exist.
- Build an explicit edit-validity gate before false-rationalization claims.
- Do not enter preference-data construction until strong teacher candidates exist.

## Next Internal Action

Run GPT-5.5 teacher generation once `OPENAI_API_KEY`, model availability, and budget are confirmed.
