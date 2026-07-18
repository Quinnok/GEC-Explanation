# To Err Is Human, but Llamas Can Learn It Too

## Title
To Err Is Human, but Llamas Can Learn It Too

## Authors
Agnes Luhtaru, Taido Purason, Martin Vainikko, Maksym Del, Mark Fishel

## Year
2024

## Venue
Findings of EMNLP 2024

## Formal publication status
Formal ACL Anthology publication

## Official link
https://aclanthology.org/2024.findings-emnlp.727/

## Code and data links
Not recorded in this pass

## Research background
GEC training data can be expanded through artificial error generation.

## Paper entry point
Fine-tune Llama-style LMs to generate realistic learner errors.

## Research question
Artificial error generation and GEC training

## Core hypothesis
Synthetic errors from LMs improve downstream GEC.

## Core idea
Synthetic errors from LMs improve downstream GEC.

## Innovation
Uses LLM-based error generation across languages.

## Detailed method
Generate artificial errors, train GEC models, evaluate across German/Ukrainian/Estonian.

## Model input/output
Input: correct text; output: artificial erroneous text and trained GEC model outputs.

## Mathematical objective
Not central or not specified in this working card

## Data construction
Use the paper card for project-level implications; verify exact details in the PDF before final
citation.

## Datasets
Multilingual GEC data plus generated errors.

## Baselines
Existing error-generation and GEC models.

## Metrics
F0.5 gains as reported in abstract.

## Main experiments
Train GEC models with generated errors and compare benchmark scores.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
Synthetic data must be clearly separated from gold labels.

## Human evaluation
None recorded in this pass.

## How experiments support claims
Official abstract reports 0.8 to 6 F0.5 gains across tested languages.

## Main results
Synthetic data must be clearly separated from gold labels.

## Limitations
Error generation is not explanation faithfulness.

## Unsolved problems
No explanation evaluation tied to model behavior.

## Relation to current research
Warning for generated negative/explanation data labels.

## Threat to current novelty
Low.

## Reusable modules
Synthetic-error generation caution.

## Extensible research gap
No explanation evaluation tied to model behavior.

## Reading priority
P1

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
