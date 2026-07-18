# Enhancing Grammatical Error Correction Systems with Explanations

## Title
Enhancing Grammatical Error Correction Systems with Explanations

## Authors
Yuejiao Fei, Leyang Cui, Sen Yang, Wai Lam, Zhenzhong Lan, Shuming Shi

## Year
2023

## Venue
ACL 2023

## Formal publication status
Formal ACL Anthology publication

## Official link
https://aclanthology.org/2023.acl-long.413/

## Code and data links
https://github.com/lorafei/Explainable_GEC

## Research background
Learners need evidence words and error types to understand corrections.

## Paper entry point
Create EXPECT with evidence-word and error-type annotations.

## Research question
Explanation-adjacent GEC labels

## Core hypothesis
Augment GEC pairs with evidence indices and error-type labels.

## Core idea
Augment GEC pairs with evidence indices and error-type labels.

## Innovation
Large explanation-oriented GEC dataset without free-text explanations.

## Detailed method
Annotates source/reference pairs with correction index, evidence index, and error type.

## Model input/output
Input: source and target corrections; output: evidence/error-type labels.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
EXPECT, derived from English learner correction data.

## Baselines
Dataset baselines for evidence/error type prediction.

## Metrics
Classification and extraction metrics.

## Main experiments
Baselines and analyses for the explanation-enhanced task.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
EXPECT is ideal for pilot data but not a human free-text explanation source.

## Human evaluation
None recorded in this pass.

## How experiments support claims
Official abstract describes EXPECT as evidence words plus grammatical error types.

## Main results
EXPECT is ideal for pilot data but not a human free-text explanation source.

## Limitations
No natural-language explanation field in the local data we audited.

## Unsolved problems
Natural-language, model-edit-level faithfulness remains unsolved.

## Relation to current research
Current pilot data source and label seed.

## Threat to current novelty
Medium: evidence/type labels already exist.

## Reusable modules
Evidence indices, error types, license-clear pilot data.

## Extensible research gap
Natural-language, model-edit-level faithfulness remains unsolved.

## Reading priority
P0

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
