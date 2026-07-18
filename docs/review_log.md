# Review Log

Last updated: 2026-07-18

## Round 13 Simulated AAAI Reviews

Three simulated review rounds were completed with nine roles each: GEC expert, explainability expert, faithfulness expert, evaluation expert, counterfactual learning expert, educational NLP expert, reproducibility reviewer, skeptical reviewer 2, and area chair.

| Review Round | Main Critique | Actions Taken | Residual Risk |
|---|---|---|---|
| 01 | Draft overclaims by title/framing; close-work boundary needs sharpening. | Title changed to evaluation framing; Introduction states this is not a new explanation generator; Related Work clarifies boundary with EXCGEC, GEE, Prompt Insertion, and COCOGEC. | Human labels unavailable. |
| 02 | Counterfactual validity, metric mixing, and artifact packaging remain P1 risks. | Supplementary appendix adds counterfactual validity and close-work scope; Results clarifies L1/L2 scores are not one leaderboard. | Multi-reference JFLEG and stronger L2 simulator remain future work. |
| 03 | No automatic P0 remains, but double-human annotation is still a hard external blocker for human-faithfulness claims. | Open issues updated: automatic P0s closed for draft, human annotation marked blocked, artifact/rebuttal tasks deferred to Round 14. | AAAI acceptance remains risky without real human validation. |

Detailed review tables:

- `docs/reviews/round13_review_round_01.md`
- `docs/reviews/round13_review_round_02.md`
- `docs/reviews/round13_review_round_03.md`
