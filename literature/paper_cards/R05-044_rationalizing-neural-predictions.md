# Rationalizing Neural Predictions

## Title
Rationalizing Neural Predictions

## Authors
See official paper page

## Year
2016

## Venue
EMNLP 2016

## Formal publication status
Formal ACL Anthology publication

## Official link
https://aclanthology.org/D16-1011/

## Code and data links
Not recorded in this pass

## Research background
Neural predictions can be accompanied by selected input rationales.

## Paper entry point
Jointly learn rationale selection and prediction.

## Research question
Rationale extraction

## Core hypothesis
Select concise text snippets that support model predictions.

## Core idea
Select concise text snippets that support model predictions.

## Innovation
Influential neural rationale model.

## Detailed method
Generator selects rationales; encoder predicts labels from selected rationales.

## Model input/output
Input: document/text; output: rationale tokens and prediction.

## Mathematical objective
Optimize prediction loss plus sparsity/continuity constraints.

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
Text classification datasets.

## Baselines
Neural classifiers and rationale variants.

## Metrics
Prediction accuracy and rationale quality.

## Main experiments
Evaluate rationales and predictions on text classification.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Evidence spans are not automatically explanations unless tied to behavior.

## Human evaluation
None recorded in this pass.

## How experiments support claims
Canonical paper for rationale extraction.

## Main results
Evidence spans are not automatically explanations unless tied to behavior.

## Limitations
Classification focus, no GEC correction operations.

## Unsolved problems
Rationales for edits and correction targets.

## Relation to current research
Basis for evidence span extraction/deletion tests.

## Threat to current novelty
Medium.

## Reusable modules
Sparsity/continuity rationale constraints.

## Extensible research gap
Rationales for edits and correction targets.

## Reading priority
P1

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
