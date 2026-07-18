# Evaluating Models' Local Decision Boundaries via Contrast Sets

## Title
Evaluating Models' Local Decision Boundaries via Contrast Sets

## Authors
See official paper page

## Year
2020

## Venue
Findings of EMNLP 2020

## Formal publication status
Formal ACL Anthology publication

## Official link
https://aclanthology.org/2020.findings-emnlp.117/

## Code and data links
Not recorded in this pass

## Research background
Standard i.i.d. tests may not probe local decision boundaries.

## Paper entry point
Create small perturbations that change gold labels.

## Research question
Contrast-set evaluation

## Core hypothesis
Contrast sets evaluate whether models handle minimal meaningful changes.

## Core idea
Contrast sets evaluate whether models handle minimal meaningful changes.

## Innovation
Manual contrastive evaluation of local behavior.

## Detailed method
Authors perturb examples to produce label-changing contrast sets and compare model performance.

## Model input/output
Input: original examples; output: contrast examples and labels.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
Several NLP tasks.

## Baselines
Task models.

## Metrics
Accuracy on original/contrast examples.

## Main experiments
Contrast evaluation across tasks.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Rule-relevant counterfactuals for GEC are analogous to contrast sets.

## Human evaluation
Human-created contrast examples.

## How experiments support claims
Canonical contrast-set paper.

## Main results
Rule-relevant counterfactuals for GEC are analogous to contrast sets.

## Limitations
Human construction is costly.

## Unsolved problems
Model-output labels for edit-level GEC counterfactuals.

## Relation to current research
Supports the distinction between error-irrelevant and rule-relevant variants.

## Threat to current novelty
Medium.

## Reusable modules
Local decision-boundary framing.

## Extensible research gap
Model-output labels for edit-level GEC counterfactuals.

## Reading priority
P1

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
