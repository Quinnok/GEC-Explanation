# COCOGEC: Counterfactual Generation for Robust Grammatical Error Correction

## Title
COCOGEC: Counterfactual Generation for Robust Grammatical Error Correction

## Authors
Qianyu Wang, Xiaoman Wang, Yuanyuan Liang, Xinyuan Li, Yunshi Lan

## Year
2026

## Venue
Findings of ACL 2026

## Formal publication status
Formal ACL Anthology publication

## Official link
https://aclanthology.org/2026.findings-acl.195/

## Code and data links
Official page reports code release at https://github.com/Quinnok/CoCoGEC

## Research background
GEC systems can be brittle when context changes without intending to change the error pattern.

## Paper entry point
Generate context perturbations that should preserve or stress GEC labels.

## Research question
GEC robustness under counterfactual perturbations

## Core hypothesis
A GEC-specific counterfactual generation pipeline for intra-sentence and inter-sentence
variants.

## Core idea
A GEC-specific counterfactual generation pipeline for intra-sentence and inter-sentence
variants.

## Innovation
Moves counterfactual testing into GEC robustness rather than generic classification.

## Detailed method
Constructs counterfactual contexts, reruns GEC systems, and measures stability or label flipping
under controlled variants.

## Model input/output
Input: source sentence and context; output: perturbed GEC examples and model corrections.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
BEA-19*, CoNLL-14*, TEM-8* and generated perturbation sets as reported by the paper page.

## Baselines
Data augmentation and robustness baselines.

## Metrics
F0.5 and robustness/stability measurements.

## Main experiments
Counterfactually augmented training and evaluation on perturbed GEC benchmarks.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Counterfactuals are a strong and very close precedent for any GEC counterfactual method.

## Human evaluation
Not the center of the paper; verify exact validation procedure in PDF.

## How experiments support claims
Official abstract reports large F0.5 gains on perturbed GEC datasets.

## Main results
Counterfactuals are a strong and very close precedent for any GEC counterfactual method.

## Limitations
Targets correction robustness, not natural-language explanation faithfulness.

## Unsolved problems
Does not evaluate whether explanations predict or justify model-produced edits.

## Relation to current research
Closest work for L2 counterfactual simulation; our distinction must be explanation-to-edit
behavior, not only robust correction.

## Threat to current novelty
Very high: it already uses GEC-specific counterfactuals and model behavior.

## Reusable modules
Counterfactual perturbation taxonomy and stability measurement.

## Extensible research gap
Does not evaluate whether explanations predict or justify model-produced edits.

## Reading priority
P0

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
