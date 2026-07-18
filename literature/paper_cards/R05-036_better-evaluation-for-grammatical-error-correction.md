# Better Evaluation for Grammatical Error Correction

## Title
Better Evaluation for Grammatical Error Correction

## Authors
Daniel Dahlmeier, Hwee Tou Ng

## Year
2012

## Venue
NAACL-HLT 2012

## Formal publication status
Formal ACL Anthology publication

## Official link
https://aclanthology.org/N12-1067/

## Code and data links
Not recorded in this pass

## Research background
GEC needed edit-based evaluation rather than plain string overlap.

## Paper entry point
Compare edits between system and references.

## Research question
GEC evaluation metric

## Core hypothesis
M2 scorer for MaxMatch edit-based evaluation.

## Core idea
M2 scorer for MaxMatch edit-based evaluation.

## Innovation
Foundational edit-based scorer.

## Detailed method
Align system/reference edits and maximize matches under an F-score objective.

## Model input/output
Input: source, system correction, reference edits; output: precision/recall/F-score.

## Mathematical objective
Maximize matched edits and compute F-measure variants.

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
GEC shared-task style data.

## Baselines
Prior scoring methods.

## Metrics
M2 precision, recall, F-score.

## Main experiments
Metric comparison and evaluation analysis.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Edit matching precedes our reconstruction idea by many years.

## Human evaluation
None recorded in this pass.

## How experiments support claims
Canonical scorer cited across GEC work.

## Main results
Edit matching precedes our reconstruction idea by many years.

## Limitations
Metric for corrections, not explanations.

## Unsolved problems
Explanation behavior is outside M2.

## Relation to current research
Clarifies that edit matching is infrastructure, not novelty.

## Threat to current novelty
High for naive edit-correspondence claims.

## Reusable modules
Edit matching/scoring logic.

## Extensible research gap
Explanation behavior is outside M2.

## Reading priority
P1

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
