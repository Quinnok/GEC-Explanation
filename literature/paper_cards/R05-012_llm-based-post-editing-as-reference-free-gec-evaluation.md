# LLM-based post-editing as reference-free GEC evaluation

## Title
LLM-based post-editing as reference-free GEC evaluation

## Authors
See official paper page

## Year
2025

## Venue
BEA 2025

## Formal publication status
Formal ACL Anthology workshop publication

## Official link
https://aclanthology.org/2025.bea-1.16/

## Code and data links
Not recorded in this pass

## Research background
Human post-editing is expensive; automatic reference-free evaluation is attractive.

## Paper entry point
Use LLM post-editing as an evaluator of system outputs.

## Research question
Reference-free GEC evaluation

## Core hypothesis
Compare LLM post-editing against human post-editing/direct ratings.

## Core idea
Compare LLM post-editing against human post-editing/direct ratings.

## Innovation
Reference-free evaluation through post-editing behavior.

## Detailed method
Ask LLMs to post-edit GEC system outputs, then compare evaluation setups.

## Model input/output
Input: source/system output; output: post-edited text and evaluation signal.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
English and Swedish texts with recent GEC systems.

## Baselines
Reference-based metrics and human ratings/post-edits.

## Metrics
Agreement with human post-editing and direct ratings.

## Main experiments
Meta-analysis over evaluation setups.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
LLM judges/post-editors are plausible but must be controlled.

## Human evaluation
None recorded in this pass.

## How experiments support claims
Official abstract states agreement with human post-editing/direct ratings for studied languages.

## Main results
LLM judges/post-editors are plausible but must be controlled.

## Limitations
Can conflate evaluator ability with GEC quality.

## Unsolved problems
Need edit-wise and explanation-specific faithfulness labels.

## Relation to current research
Potential LLM-judge baseline and reviewer risk.

## Threat to current novelty
Medium if we rely only on LLM judging.

## Reusable modules
Post-editing as evaluation protocol.

## Extensible research gap
Need edit-wise and explanation-specific faithfulness labels.

## Reading priority
P1

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
