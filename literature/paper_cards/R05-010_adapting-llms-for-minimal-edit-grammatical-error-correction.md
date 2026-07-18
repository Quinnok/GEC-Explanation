# Adapting LLMs for Minimal-edit Grammatical Error Correction

## Title
Adapting LLMs for Minimal-edit Grammatical Error Correction

## Authors
Ryszard Staruch, Filip Gralinski, Daniel Dzienisiewicz

## Year
2025

## Venue
BEA 2025

## Formal publication status
Formal ACL Anthology workshop publication

## Official link
https://aclanthology.org/2025.bea-1.9/

## Code and data links
Not recorded in this pass

## Research background
Decoder-only LLMs may be fluent but over-edit in GEC.

## Paper entry point
Fine-tune LLMs toward minimal edits and tune error rates.

## Research question
Minimal-edit LLM GEC

## Core hypothesis
A practical adaptation schedule for minimal-edit correction.

## Core idea
A practical adaptation schedule for minimal-edit correction.

## Innovation
Recent open reference for LLM-based GEC under minimal-edit goals.

## Detailed method
Fine-tune LLMs on detokenized GEC data and control precision-recall behavior.

## Model input/output
Input: sentence; output: minimally edited correction.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
Common English GEC datasets in detokenized form.

## Baselines
Prior T5 and GEC systems.

## Metrics
Precision, recall, F0.5 on CoNLL/BEA.

## Main experiments
Minimal-edit adaptation across training schedules/model choices.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Detokenization and minimal edit choices are central confounds for our T5 behavior.

## Human evaluation
None recorded in this pass.

## How experiments support claims
Official abstract reports state-of-the-art single-model BEA result and detokenization study.

## Main results
Detokenization and minimal edit choices are central confounds for our T5 behavior.

## Limitations
No explanation evaluation.

## Unsolved problems
Need edit explanation faithfulness under minimal-edit constraints.

## Relation to current research
Guides model-output normalization and instruction-following baseline selection.

## Threat to current novelty
Low for faithfulness, medium for correction behavior analysis.

## Reusable modules
Minimal-edit prompt/training framing.

## Extensible research gap
Need edit explanation faithfulness under minimal-edit constraints.

## Reading priority
P1

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
