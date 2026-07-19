# RuleFaith-GEC Go / No-Go Gates

Created: 2026-07-19

## Gate A: Verifier Pilot

Go only if:

- Edit Alignment AUROC >= 0.75.
- Rule AUROC >= 0.65.
- Evidence AUROC >= 0.65.
- Wrong-rule and wrong-evidence negatives are identified better than reconstruction.
- Target-masked performance does not collapse to chance.

No-Go action:

- Revise verifier features, prompts, or calibration split.
- Do not generate large preference data until Gate A passes.

## Gate B: Method Pilot

Go only if:

- RuleFaith improves Rule Correctness or Evidence Correctness over Direct/Vanilla.
- False rationalization decreases.
- Trend holds for at least two corrector families.
- Coverage remains acceptable and edit-copy rate decreases.

No-Go action:

- Diagnose verifier, refinement, and scoring failures before scaling.

## Gate C: Student Training

Go only if:

- Filtered SFT outperforms Vanilla SFT on dev.
- Preference student does not reduce edit alignment.
- Gains are not explained only by longer explanations.

No-Go action:

- Rebuild data, adjust preference pairs, or reduce model scope.

## Gate D: Human Evaluation

Go only if:

- RuleFaith is significantly better than Vanilla in at least two of Overall Faithfulness, Rule Correctness, or Evidence Correctness.
- Inter-annotator agreement is acceptable.
- Results are not driven by one error type or one corrector family.

No-Go action:

- Reframe as diagnostic/evaluation paper or repair method.

## Gate E: Submission

Go only if:

- Every main contribution has real experimental support.
- No P0 issues remain.
- Major P1 issues are resolved or explicitly bounded.
- Paper compiles cleanly.
- Figures and tables trace to result files.
- Reproducibility and rebuttal materials are current.

