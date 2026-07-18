# GEE! Grammar Error Explanation with Large Language Models

## Title
GEE! Grammar Error Explanation with Large Language Models

## Authors
Yixiao Song, Kalpesh Krishna, Rajesh Bhatt, Kevin Gimpel, Mohit Iyyer

## Year
2024

## Venue
Findings of NAACL 2024

## Formal publication status
Formal ACL Anthology publication

## Official link
https://aclanthology.org/2024.findings-naacl.49/

## Code and data links
Not recorded in this pass

## Research background
GEC tools usually correct errors without explaining them in language learners can use.

## Paper entry point
Explain each grammatical error in an erroneous/corrected pair.

## Research question
Natural-language grammar error explanation

## Core hypothesis
Two-step pipeline: structured atomic edit extraction followed by GPT-4 explanation generation.

## Core idea
Two-step pipeline: structured atomic edit extraction followed by GPT-4 explanation generation.

## Innovation
Defines GEE and releases multilingual explanation data/code.

## Detailed method
Extract atomic edits from erroneous/corrected sentence pairs, then prompt a large model to
explain each edit.

## Model input/output
Input: erroneous and corrected sentences; output: one-sentence explanations per edit.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
German, Chinese, and English GEC data.

## Baselines
One-shot prompting and pipeline variants.

## Metrics
Edit extraction F1 and human evaluation of detected/explained errors.

## Main experiments
Multilingual edit extraction and explanation generation evaluation.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
The strongest English-adjacent natural-language GEE precedent.

## Human evaluation
Yes, reports human evaluation of generated explanations.

## How experiments support claims
Official abstract reports extraction F1 and human evaluation percentages.

## Main results
The strongest English-adjacent natural-language GEE precedent.

## Limitations
Uses corrected pairs and strong/proprietary generation; does not directly test faithfulness to
model-produced edits.

## Unsolved problems
Behavioral faithfulness and leakage-controlled simulatability for model edits.

## Relation to current research
Closest explanation generation work; our benchmark should evaluate explanation candidates rather
than claim generation novelty.

## Threat to current novelty
Very high if we claim GEE generation novelty.

## Reusable modules
Atomic edit extraction and explanation schema.

## Extensible research gap
Behavioral faithfulness and leakage-controlled simulatability for model edits.

## Reading priority
P0

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
