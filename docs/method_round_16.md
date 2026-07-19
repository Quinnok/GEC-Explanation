# Method Round 16

## Status

Round 16 method branch and preregistration.

## Main Objective

Freeze the Round 15 stress-test paper state and initialize the RuleFaith-GEC method branch.

## Highest Risk

The project could overclaim a method before natural teacher candidates, verifier calibration, and student training exist.

## Git Commit

`3d9598e`

## Data Version

Frozen stress-test base commit: `4519543060cbaff49806fd9963412f4ca4ab83c0`.

## Model Version

No new model calls in Round 16.

## Work Completed

- Created `method/rulefaith-gec` branch.
- Created method directory structure.
- Recorded Round 15 stress-test snapshot and key file hashes.
- Wrote method paper brief.
- Pre-registered H1--H6 and secondary hypotheses.
- Wrote claim-evidence matrix and Go/No-Go gates.
- Added frozen metric mapping config.
- Initialized method loop, experiment, decision, and open-issue logs.

## Files Created or Modified

- `docs/method_snapshots/round15_stress_test_snapshot.md`
- `docs/method_paper_brief.md`
- `docs/method_hypotheses.md`
- `docs/method_claim_evidence_matrix.md`
- `docs/method_go_no_go.md`
- `configs/rulefaith/preregistered_metrics.yaml`
- `docs/method_loop_state.md`
- `docs/method_experiment_log.md`
- `docs/method_decision_log.md`
- `docs/method_open_issues.md`

## Commands Executed

- `git status -sb`
- `git branch --show-current`
- `git log --oneline -n 20`
- `git remote -v`
- `git checkout -b method/rulefaith-gec`
- `shasum -a 256 ...`

## Verified Results

Round 16 is a preregistration/setup round; no method result is claimed.

## Failed Runs

Branch creation triggered a Git LFS hook warning when `git-lfs` was not on PATH, but the branch was created and subsequent Git operations use the local `git-lfs` path.

## Scientific Interpretation

The method branch is now separated from the stress-test paper line. Future claims must be backed by natural teacher candidates, verifier calibration, method pilots, student models, and human evaluation.

## Claim-Evidence Updates

All method claims are currently unverified except the diagnostic motivation inherited from Round 15.

## Open Issues

- GPT-5.5 API key not visible.
- Verifier Gate A not yet run.
- Natural explanation data not yet generated.
- Student model not selected.

## Next Internal Action

Round 17: construct a substantive edit pool from existing model-produced edits.
