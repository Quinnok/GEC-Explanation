# Round 13: Simulated Review and P0/P1 Fixes

## Completed

- Ran three simulated AAAI review rounds with nine roles per round.
- Wrote detailed review tables under `docs/reviews/`.
- Fixed the highest-risk overclaim by changing the title to evaluation framing.
- Added Introduction language stating the paper is a benchmark/diagnostic suite, not a new explanation generator.
- Strengthened the close-work boundary with EXCGEC, GEE, Prompt Insertion, and COCOGEC.
- Added supplementary appendix notes on counterfactual validity, pilot scope, and close-work scope.
- Clarified in Results that L1/L3 Macro-F1 and L2 multiclass Macro-F1 are not one unified leaderboard.
- Updated `docs/open_issues.md` to close automatic P0s for draft and mark human double annotation as the remaining external blocker.

## Review Outcome

- Automatic P0s resolved for the draft: overclaiming, reconstruction-faithfulness conflation, and fabricated-human-label risk.
- Remaining hard blocker: no real double-human annotation, so no human-faithfulness or helpfulness correlation can be claimed.
- Main P1 risks: JFLEG multi-reference alignment, CoEdIT sample size, stronger L2 simulator, counterfactual validity annotation, visual polish, artifact packaging.

## Files

- `docs/reviews/round13_review_round_01.md`
- `docs/reviews/round13_review_round_02.md`
- `docs/reviews/round13_review_round_03.md`
- `docs/review_log.md`
- Updated `paper/main.tex`, `paper/sections/introduction.tex`, `paper/sections/related_work.tex`, `paper/sections/results.tex`, and `paper/supplementary/appendix.tex`.

## Verification

- `bash experiments/run_round12.sh` passed.
- Unit tests passed: `.venv311/bin/python -m unittest discover -s experiments/tests`.
- Python compile checks passed for updated scripts.
- Paper scan found no `RESULT-PENDING`, `first`, or `novel` wording in `paper/sections/` or `paper/main.tex`.
- `results/round12/paper_consistency_check.json` reports 8 total pages, bibliography starting on page 7, clean main/appendix LaTeX logs, 0 result-pending placeholders, and anonymous submission status true.
