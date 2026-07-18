# GECToR - Grammatical Error Correction: Tag, Not Rewrite

## Title
GECToR - Grammatical Error Correction: Tag, Not Rewrite

## Authors
Kostiantyn Omelianchuk, Vitaliy Atrasevych, Artem Chernodub, Oleksandr Skurzhanskyi

## Year
2020

## Venue
BEA 2020

## Formal publication status
Formal ACL Anthology workshop publication

## Official link
https://aclanthology.org/2020.bea-1.16/

## Code and data links
Not recorded in this pass

## Research background
Seq2seq rewriting can be slower and less controllable than edit tagging.

## Paper entry point
Frame GEC as token-level edit tagging.

## Research question
Sequence-to-edit GEC

## Core hypothesis
Predict edit tags instead of generating a full rewritten sentence.

## Core idea
Predict edit tags instead of generating a full rewritten sentence.

## Innovation
Fast strong edit-based GEC architecture.

## Detailed method
Use a transformer encoder to assign keep/delete/replace/append-style edit tags and iteratively
apply corrections.

## Model input/output
Input: erroneous sentence; output: edit tags and corrected sentence.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
Standard English GEC datasets.

## Baselines
Seq2seq and prior GEC systems.

## Metrics
F0.5 and runtime.

## Main experiments
Compare tagger-based GEC to rewrite systems.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Good model family for actual predicted edit benchmark.

## Human evaluation
None recorded in this pass.

## How experiments support claims
Official paper page and model family underpin our sequence-to-edit pilot.

## Main results
Good model family for actual predicted edit benchmark.

## Limitations
Edit tags are not explanations.

## Unsolved problems
Need natural-language explanation evaluation for tagger edits.

## Relation to current research
Round 03 sequence-to-edit model family.

## Threat to current novelty
Low for explanation metric; high if we claim edit-tagging contribution.

## Reusable modules
Sequence-to-edit model outputs.

## Extensible research gap
Need natural-language explanation evaluation for tagger edits.

## Reading priority
P1

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
