# Large Language Models Are State-of-the-Art Evaluator for Grammatical Error Correction

## Title
Large Language Models Are State-of-the-Art Evaluator for Grammatical Error Correction

## Authors
See official paper page

## Year
2024

## Venue
BEA 2024

## Formal publication status
Formal ACL Anthology workshop publication

## Official link
https://aclanthology.org/2024.bea-1.6/

## Code and data links
Not recorded in this pass

## Research background
Reference-based metrics may not align with human judgments under fluent LLM outputs.

## Paper entry point
Prompt LLMs with evaluation criteria for GEC.

## Research question
LLM-based GEC evaluation

## Core hypothesis
Use LLMs as evaluators of GEC system outputs.

## Core idea
Use LLMs as evaluators of GEC system outputs.

## Innovation
Applies LLM-as-judge to GEC evaluation.

## Detailed method
Design prompts inspired by evaluation criteria and compare with existing metrics/human
judgments.

## Model input/output
Input: source, correction, possibly reference; output: evaluation score/judgment.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
GEC system outputs and human evaluation data.

## Baselines
Existing automatic metrics.

## Metrics
Correlation/consistency with human judgments.

## Main experiments
LLM evaluator comparisons for GEC.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
LLM judge is a necessary baseline but risky.

## Human evaluation
None recorded in this pass.

## How experiments support claims
Official abstract identifies lack of research on LLMs as GEC evaluators and investigates prompt
criteria.

## Main results
LLM judge is a necessary baseline but risky.

## Limitations
Paid/proprietary models may be involved; evaluator faithfulness is not guaranteed.

## Unsolved problems
Need no-paid, edit-wise, leakage-controlled faithfulness metrics.

## Relation to current research
Baseline and review-risk source.

## Threat to current novelty
Medium if our method is only LLM judging.

## Reusable modules
Evaluation prompt dimensions.

## Extensible research gap
Need no-paid, edit-wise, leakage-controlled faithfulness metrics.

## Reading priority
P1

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
