# Failed Experiments

Last updated: 2026-07-20

No Loop A experiment is marked as failed. The Qwen3-8B audit result is `revise`: the candidate pool is useful, but evidence grounding and false-rationalization risks must be fixed before training or preference construction.

| Date | Hypothesis | Implementation | Result | Decision |
|---|---|---|---|---|
| 2026-07-20 | Qwen3-8B accepted/refine candidates may be ready for targeted refinement after automatic audit. | Audited all 160 Qwen3 candidates with leakage, span, rule, evidence, genericness, edit-copy, target-copy, and false-rationalization checks. | No input leakage and all edit spans passed, but evidence grounding was weak and false-rationalization risks remained. | Revise evidence verifier/prompt before targeted refinement. |
