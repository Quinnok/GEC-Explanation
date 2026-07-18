# Rebuttal Draft: Reviewer 1

## Likely Concern

The work may conflate reconstruction with faithfulness, and automatic labels may not validate human-perceived explanation quality.

## Response

We agree and have revised the framing accordingly. The paper separates edit correspondence, behavioral simulatability, grammatical validity, and helpfulness. Reverse reconstruction is explicitly reported as an L1 edit-correspondence/leakage diagnostic, not as evidence of internal causal faithfulness. Human faithfulness is not claimed: the benchmark has `human_gold_count=0`, and the Human Evaluation section reports that double annotation is blocked until real annotators complete the package.

## Evidence

- `paper/sections/problem_formulation.tex`
- `paper/sections/results.tex`
- `paper/sections/human_evaluation.tex`
- `results/round10/human_annotation_status.json`
- `results/round09/statistical_analysis.json`

## Planned Revision If Space Allows

Move additional explanation of the distinction between correspondence and faithfulness to the supplementary appendix rather than expanding the main paper.

