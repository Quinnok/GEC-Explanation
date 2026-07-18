# Round 06: Idea Restructuring

Date: 2026-07-18

## Objective

Use the Round 05 literature package to redesign the paper idea instead of preserving Reverse Edit Reconstruction by inertia.

## Outputs

- `docs/idea_candidates.md`
- `docs/idea_score_matrix.csv`
- `docs/idea_review_panel.md`
- `docs/final_idea_decision.md`

## Decision

The main line is Counterfactual Edit Simulatability for model-produced GEC edit explanations. The backup line is Rule-grounded Faithfulness. Reverse Edit Reconstruction is now an L1 diagnostic and leakage-control condition.

## Rationale

The literature makes pure reconstruction too weak as a contribution. Strong precedents already exist for simulatability, self-consistency critiques, edit-wise GEC explanations, behavior-decomposed GEC evaluation, and counterfactual GEC robustness. The defensible space is to evaluate whether an explanation predicts how the same GEC model's produced edit behaves when the input is counterfactually changed.

## Required Next Round

Round 07 must build `data/faithfulness_benchmark/` from model-produced edits, not reference-edit templates, and must create multi-source explanation candidates plus hard negatives.
