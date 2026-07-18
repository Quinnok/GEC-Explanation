# Explanation based In-Context Demonstrations Retrieval for Multilingual Grammatical Error Correction

## Title
Explanation based In-Context Demonstrations Retrieval for Multilingual Grammatical Error
Correction

## Authors
See official paper page

## Year
2025

## Venue
NAACL 2025

## Formal publication status
Formal ACL Anthology publication

## Official link
https://aclanthology.org/2025.naacl-long.251/

## Code and data links
Not recorded in this pass

## Research background
Input similarity need not match error-pattern similarity.

## Paper entry point
Use grammatical error explanations for retrieving demonstrations.

## Research question
Few-shot GEC demonstration retrieval

## Core hypothesis
Retrieve in-context examples using explanation/error-pattern information.

## Core idea
Retrieve in-context examples using explanation/error-pattern information.

## Innovation
Treats explanations as a retrieval signal for GEC.

## Detailed method
Builds explanation-informed retrieval features, then prompts/few-shot correctors with selected
demonstrations.

## Model input/output
Input: source sentence and candidate examples; output: selected demonstrations and correction.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
Multilingual GEC data; verify exact set in PDF.

## Baselines
Similarity-based and retrieval baselines.

## Metrics
GEC benchmark scores.

## Main experiments
Compare explanation-based retrieval against standard ICL selection.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Explanations can guide correction, but this is not explanation faithfulness evaluation.

## Human evaluation
None recorded in this pass.

## How experiments support claims
Official abstract states explanation-based retrieval for multilingual GEC.

## Main results
Explanations can guide correction, but this is not explanation faithfulness evaluation.

## Limitations
Does not isolate edit-level explanation validity.

## Unsolved problems
Need leakage-controlled edit-level explanation metrics.

## Relation to current research
Close on explanation usage; our benchmark evaluates whether explanations predict model edits.

## Threat to current novelty
Medium.

## Reusable modules
Explanation-derived retrieval features.

## Extensible research gap
Need leakage-controlled edit-level explanation metrics.

## Reading priority
P1

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
