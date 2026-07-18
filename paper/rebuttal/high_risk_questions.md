# High-Risk Questions

## Why is reconstruction not faithfulness?

Reconstruction only tests whether the explanation contains enough information to recover the observed edit fields. It can be solved by copying the target edit, so the paper treats it as L1 edit correspondence and leakage diagnosis, not internal causal faithfulness.

## Why is counterfactual simulatability GEC-specific?

The counterfactuals are defined over grammar-edit opportunities: prepositions, determiners, agreement, tense, punctuation, and other ERRANT-typed edit conditions. Labels are derived by rerunning the same GEC model and comparing edit behavior, not by generic sentence classification.

## How is simulator ability controlled?

The paper reports random, variant-family, source-edit availability, explanation-leakage, explanation-type, and trained explanation-type prior baselines. The current best L2 result is weak, so the paper does not claim a strong simulator.

## How is counterfactual validity checked?

Validity is checked automatically by rerunning the original model and separating preserve, cancel, change-span, change-target, and competing-edit outcomes. Invalid or competing cases are saved in Round 09 error-analysis packets. Human validity annotation remains future work.

## How is model instability handled?

Competing edits are not collapsed into cancellations. Model instability cases are stored separately under `results/round09/error_analysis/model_instability_cases_20.jsonl`.

## How are multiple references handled?

JFLEG retains all four references, but the current ERRANT extraction uses reference 0 for the primary pilot. Multi-reference accept-if-any alignment is a P1 future ablation and is listed as a limitation.

## Why not use a simple LLM judge?

Round 11 includes a local open-source FLAN-T5 judge baseline over all 880 reranking candidates. It scores 0.455 automatic pairwise accuracy, below random 0.509, so a simple LLM judge is not sufficient here.

## Is human annotation enough?

No human annotation has been completed. The project provides a 240-item annotation package and agreement script, but human-faithfulness claims remain blocked until real double annotation is collected.

## Is the data LLM-generated?

The source/reference GEC data come from public GEC datasets. Some explanation candidates and hard negatives are automatically generated from edit fields or local open-source models, and are marked as automatic. They are not human gold.

## How is this different from GEE, EXCGEC, and general faithfulness work?

GEE and Prompt Insertion focus on generating explanations; EXCGEC provides edit-wise explainable Chinese GEC data; general faithfulness work studies broader explanation evaluation and simulatability. This project evaluates whether explanations of model-produced English GEC edits predict the same model's edit behavior under controlled GEC-specific counterfactuals.
