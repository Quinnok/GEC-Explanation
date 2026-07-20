# Research Decisions

Last updated: 2026-07-20

| Date | Decision | Evidence | Consequence |
|---|---|---|---|
| 2026-07-20 | Treat Qwen3-8B as a usable local open-teacher candidate source, but not as clean positive training data yet. | `results/rulefaith/qwen3_manual_audit_summary.json` covers all 160 candidates: no input leakage, 41 accepted by the previous prefilter, 63 refine, 56 rejected. | Continue with manual audit and targeted refinement rather than direct SFT. |
| 2026-07-20 | Do not enter targeted refinement until evidence-span validation is tightened. | Automatic audit found evidence span index matches for only 48/160 candidates and contextual evidence for 51/160. | Next loop should improve evidence verifier/prompt, then rerun the Qwen3 audit. |
| 2026-07-20 | Keep false-rationalization as a P0 risk for Qwen3 candidates. | 19 candidates were automatically flagged as possible false rationalizations and 28 as validity-error risks. | Edit-validity gate must be used before choosing positives for wrong/overcorrection edits. |
| 2026-07-20 | Use Qwen3 prompt-v2 and blind audit before any positive-data construction. | Loop B strict audit found only 24/160 contextual source-evidence candidates and 87/160 prediction-only evidence cases in prompt-v1 outputs. A 1-candidate prompt-v2 smoke test produced parsed JSON with source-index-matched evidence and no prediction-only evidence. | Existing Qwen3 v1 candidates remain useful for audit/refinement, not direct SFT positives. |
| 2026-07-20 | Do not scale prompt-v2 generation directly before targeted evidence refinement. | Prompt-v2 smoke10 produced 10/10 parsed candidates and 0/10 prediction-only evidence, but only 3/10 contextual source-evidence candidates and 6/10 wrong-evidence flags. | Next loop should target missing/wrong evidence spans rather than only increasing generation volume. |
