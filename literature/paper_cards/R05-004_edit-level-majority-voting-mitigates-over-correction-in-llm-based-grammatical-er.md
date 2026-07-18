# Edit-level Majority Voting Mitigates Over-Correction in LLM-based Grammatical Error Correction

## Title
Edit-level Majority Voting Mitigates Over-Correction in LLM-based Grammatical Error Correction

## Authors
Takumi Goto, Yusuke Sakai, Taro Watanabe

## Year
2026

## Venue
BEA 2026

## Formal publication status
Formal ACL Anthology workshop publication

## Official link
https://aclanthology.org/2026.bea-1.60/

## Code and data links
Not recorded in this pass

## Research background
LLM-based GEC often over-edits beyond minimal correction.

## Paper entry point
Operate at edit level rather than whole-sentence voting.

## Research question
Overcorrection mitigation

## Core hypothesis
Use training-free edit-level majority voting over multiple candidates.

## Core idea
Use training-free edit-level majority voting over multiple candidates.

## Innovation
Shows edit-level aggregation can directly target overcorrection.

## Detailed method
Generate multiple correction candidates, extract edits, and keep edits supported by a majority.

## Model input/output
Input: source sentence and multiple LLM correction candidates; output: voted correction/edit
set.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
Nine benchmarks covering several languages as reported by the official abstract.

## Baselines
Greedy decoding and MBR decoding.

## Metrics
GEC benchmark scores and overcorrection behavior.

## Main experiments
Cross-benchmark comparison of edit-level voting against decoding baselines.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Overcorrection is a central behavior stratum for explanation evaluation.

## Human evaluation
None recorded in this pass.

## How experiments support claims
Official abstract states training-free edit-level majority voting and improvements over
greedy/MBR in most cases.

## Main results
Overcorrection is a central behavior stratum for explanation evaluation.

## Limitations
Aims to improve correction, not assess explanation faithfulness.

## Unsolved problems
Explanations for retained versus rejected edits remain unevaluated.

## Relation to current research
Supports behavior-stratified benchmark design and overcorrection negative cases.

## Threat to current novelty
Medium: if we frame only edit-level overcorrection analysis, novelty is weak.

## Reusable modules
Edit-level candidate aggregation idea.

## Extensible research gap
Explanations for retained versus rejected edits remain unevaluated.

## Reading priority
P0

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
