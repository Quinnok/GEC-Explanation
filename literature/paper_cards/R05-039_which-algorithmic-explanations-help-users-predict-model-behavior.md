# Which Algorithmic Explanations Help Users Predict Model Behavior?

## Title
Which Algorithmic Explanations Help Users Predict Model Behavior?

## Authors
Peter Hase, Mohit Bansal

## Year
2020

## Venue
ACL 2020

## Formal publication status
Formal ACL Anthology publication

## Official link
https://aclanthology.org/2020.acl-main.491/

## Code and data links
Not recorded in this pass

## Research background
Interpretability should help users predict model behavior, not only look plausible.

## Paper entry point
Human subject tests for model behavior prediction.

## Research question
Explanation simulatability

## Core hypothesis
Evaluate explanations by whether humans can simulate model outputs on new inputs.

## Core idea
Evaluate explanations by whether humans can simulate model outputs on new inputs.

## Innovation
Strong precedent for simulatability and counterfactual simulation tests.

## Detailed method
Compare LIME, Anchors, decision boundaries, prototypes, and composites in human simulation
tasks.

## Model input/output
Input: model examples/explanations; output: user prediction of model behavior.

## Mathematical objective
Measure prediction accuracy of human/model-behavior simulation.

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
Text and tabular datasets.

## Baselines
Five explanation methods.

## Metrics
Human prediction accuracy and subjective ratings.

## Main experiments
Human simulatability tests.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Directly motivates explanation-to-behavior evaluation.

## Human evaluation
Yes, human subject experiments.

## How experiments support claims
Official abstract defines simulatability and reports limited evidence of explanation
effectiveness.

## Main results
Directly motivates explanation-to-behavior evaluation.

## Limitations
General ML/NLP; not edit-wise GEC.

## Unsolved problems
No GEC-specific edit operation/target/type prediction.

## Relation to current research
Nearest conceptual ancestor for counterfactual edit simulatability.

## Threat to current novelty
High for simulatability claims.

## Reusable modules
Simulation task and subjective-vs-objective distinction.

## Extensible research gap
No GEC-specific edit operation/target/type prediction.

## Reading priority
P0

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
