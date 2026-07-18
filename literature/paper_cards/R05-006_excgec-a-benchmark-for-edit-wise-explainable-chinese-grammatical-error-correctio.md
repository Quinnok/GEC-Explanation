# EXCGEC: A Benchmark for Edit-Wise Explainable Chinese Grammatical Error Correction

## Title
EXCGEC: A Benchmark for Edit-Wise Explainable Chinese Grammatical Error Correction

## Authors
Jingheng Ye et al.

## Year
2025

## Venue
AAAI 2025

## Formal publication status
Formal AAAI proceedings publication

## Official link
https://ojs.aaai.org/index.php/AAAI/article/view/34759

## Code and data links
https://github.com/THUKElab/EXCGEC

## Research background
Correction and explanation are often studied separately.

## Paper entry point
Jointly define correction and explanation for Chinese GEC.

## Research question
Edit-wise explainable GEC benchmark

## Core hypothesis
EXGEC task with explanation-augmented edit-wise samples.

## Core idea
EXGEC task with explanation-augmented edit-wise samples.

## Innovation
Benchmark and evaluation suite for correction-explanation interaction.

## Detailed method
Annotates edit-wise explanations and evaluates LLMs in post-explaining and pre-explaining
settings.

## Model input/output
Input: erroneous Chinese sentence; output: correction and free-text explanation.

## Mathematical objective
Multi-task correction/explanation evaluation; automatic metrics compared with human judgements.

## Data construction
8,216 explanation-augmented samples reported by official page.

## Datasets
Chinese EXCGEC benchmark.

## Baselines
Several LLM series in pipeline and multi-task settings.

## Metrics
Traditional free-text metrics such as METEOR/ROUGE plus human evaluation consistency.

## Main experiments
Benchmark LLMs for correction plus explanation tasks.

## Ablation experiments
Reported where available; not exhaustively transcribed in this pass.

## Analysis experiments
This is the strongest edit-wise explainable GEC benchmark precedent.

## Human evaluation
Yes, human evaluation of free-text explanations according to official abstract.

## How experiments support claims
AAAI page reports benchmark size, task definition, evaluation suite, and findings.

## Main results
This is the strongest edit-wise explainable GEC benchmark precedent.

## Limitations
Chinese focus; evaluates explanation text quality/consistency, not necessarily behavioral
faithfulness for model-produced English edits.

## Unsolved problems
Faithfulness to actual model edit behavior under counterfactual perturbations remains open.

## Relation to current research
Closest benchmark work; our English model-produced edit faithfulness must be clearly separated.

## Threat to current novelty
Very high if our claim is only edit-wise GEC explanations.

## Reusable modules
Benchmark framing, post/pre-explaining settings, explanation annotation dimensions.

## Extensible research gap
Faithfulness to actual model edit behavior under counterfactual perturbations remains open.

## Reading priority
P0

## Round 05 verification note
Metadata and abstracts were checked from official pages on 2026-07-18; detailed PDF-level claims
still need a final citation pass before submission.
