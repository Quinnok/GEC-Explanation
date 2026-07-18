# Automatic Annotation and Evaluation of Error Types for Grammatical Error Correction

## Title
Automatic Annotation and Evaluation of Error Types for Grammatical Error Correction

## Authors
Christopher Bryant, Mariano Felice, Ted Briscoe

## Year
2017

## Venue
ACL 2017

## Formal publication status
Formal ACL Anthology publication

## Official link
https://aclanthology.org/P17-1074/

## Code and data links
https://github.com/chrisjbryant/errant

## Research background
GEC system outputs lacked automatic error-type annotations.

## Paper entry point
Extract edits from original/corrected pairs and classify them.

## Research question
Automatic edit extraction and error typing

## Core hypothesis
ERRANT standardizes edit extraction and type classification.

## Core idea
ERRANT standardizes edit extraction and type classification.

## Innovation
Dataset-agnostic rule-based framework for error type evaluation.

## Detailed method
Align parallel sentences, extract edits, classify using linguistic rules, and support M2
evaluation.

## Model input/output
Input: source/corrected sentence pair; output: typed edits and evaluation.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
Parallel GEC datasets and system outputs.

## Baselines
Existing annotation/evaluation methods.

## Metrics
Error-type evaluation and human ratings of extracted edits.

## Main experiments
Apply ERRANT to system outputs and evaluate annotation quality.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Foundational dependency for this project.

## Human evaluation
Yes, human experts rated automatic edits in the paper.

## How experiments support claims
Official abstract states ERRANT extracts and classifies edits using a new rule-based framework.

## Main results
Foundational dependency for this project.

## Limitations
Automatic boundaries and types can be ambiguous.

## Unsolved problems
Need explanation faithfulness beyond typed edits.

## Relation to current research
Core extraction layer; our labels inherit its noise.

## Threat to current novelty
High if we claim edit extraction novelty.

## Reusable modules
ERRANT edit schema and type labels.

## Extensible research gap
Need explanation faithfulness beyond typed edits.

## Reading priority
P0

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
