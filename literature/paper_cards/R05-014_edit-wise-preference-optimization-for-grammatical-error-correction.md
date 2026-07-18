# Edit-Wise Preference Optimization for Grammatical Error Correction

## Title
Edit-Wise Preference Optimization for Grammatical Error Correction

## Authors
See official paper page

## Year
2025

## Venue
COLING 2025

## Formal publication status
Formal ACL Anthology publication

## Official link
https://aclanthology.org/2025.coling-main.229/

## Code and data links
Not recorded in this pass

## Research background
Whole-sentence preference objectives may hide edit-level quality.

## Paper entry point
Optimize correction choices at edit granularity.

## Research question
Preference optimization for GEC edits

## Core hypothesis
Use edit-wise preference signals to train/rank GEC outputs.

## Core idea
Use edit-wise preference signals to train/rank GEC outputs.

## Innovation
Preference optimization targets individual edit decisions.

## Detailed method
Derives preference examples around edits and optimizes correction behavior.

## Model input/output
Input: source and candidate corrections/edits; output: preferred correction/edit selection.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
GEC datasets with candidate edits; verify exact construction in PDF.

## Baselines
Seq2Edit and Seq2Seq systems, preference baselines.

## Metrics
F0.5 and edit-level preference/evaluation metrics.

## Main experiments
Preference optimization comparison on GEC benchmarks.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Edit-level objectives are active in current GEC research.

## Human evaluation
None recorded in this pass.

## How experiments support claims
Official PDF foregrounds edit-wise optimization for GEC.

## Main results
Edit-level objectives are active in current GEC research.

## Limitations
Preference for correction quality is not explanation faithfulness.

## Unsolved problems
Need explanation-based faithful reranking, not only correction preference.

## Relation to current research
Potential downstream application for explanation reranking.

## Threat to current novelty
Medium if we claim edit-wise optimization novelty.

## Reusable modules
Edit candidate preference setup.

## Extensible research gap
Need explanation-based faithful reranking, not only correction preference.

## Reading priority
P1

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
