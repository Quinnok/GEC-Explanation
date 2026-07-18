# Controlled Generation with Prompt Insertion for Natural Language Explanations in Grammatical Error Correction

## Title
Controlled Generation with Prompt Insertion for Natural Language Explanations in Grammatical
Error Correction

## Authors
Masahiro Kaneko, Naoaki Okazaki

## Year
2024

## Venue
LREC-COLING 2024

## Formal publication status
Formal ACL Anthology publication

## Official link
https://aclanthology.org/2024.lrec-main.350/

## Code and data links
Not recorded in this pass

## Research background
Prompting directly for corrections plus explanations is format-fragile.

## Paper entry point
Control generation by inserting prompts around correction positions.

## Research question
Controlled natural-language explanations for GEC

## Core hypothesis
Prompt Insertion helps generate consistent natural-language explanations for GEC corrections.

## Core idea
Prompt Insertion helps generate consistent natural-language explanations for GEC corrections.

## Innovation
A control mechanism for explanation generation.

## Detailed method
Align input/output tokens, identify correction points, and condition generation through inserted
prompts.

## Model input/output
Input: source/correction pair with prompt insertions; output: natural-language reason.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
GEC correction examples; verify exact dataset in PDF.

## Baselines
Prompting methods without insertion.

## Metrics
Generation quality and consistency metrics.

## Main experiments
Controlled generation compared with prompt baselines.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Template/control choices can cause leakage and format artifacts.

## Human evaluation
None recorded in this pass.

## How experiments support claims
Official abstract describes prompt insertion for GEC explanation generation.

## Main results
Template/control choices can cause leakage and format artifacts.

## Limitations
Focuses on generation control, not evaluator faithfulness.

## Unsolved problems
Need evaluate if explanation preserves target under counterfactual behavior.

## Relation to current research
Supports keeping explicit templates as leakage controls.

## Threat to current novelty
High for generation method claims.

## Reusable modules
Prompt insertion idea.

## Extensible research gap
Need evaluate if explanation preserves target under counterfactual behavior.

## Reading priority
P0

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
