# Round 05 Literature Overview

This folder is a working literature package for an English edit-level GEC explanation faithfulness paper. It separates bibliographic evidence from local research decisions.

## Counts

- Total papers: 50
- 2026 papers: 5
- 2025 papers: 12
- 2023-2024 papers: 15
- Earlier foundations: 18
- P0 closest/threat papers: 13

## Status Mix

- Formal AAAI proceedings publication: 1
- Formal ACL Anthology publication: 29
- Formal ACL Anthology workshop publication: 17
- Formal OpenReview conference publication: 1
- Formal journal publication: 2

## Category Mix

- counterfactual: 5
- faithfulness: 7
- gec_evaluation: 15
- gec_explanation: 7
- gec_robustness: 14
- rule_grounding: 1
- simulatability: 1

## Closest Papers

| ID | Paper | Why It Is Close |
|---|---|---|
| R05-001 | [COCOGEC: Counterfactual Generation for Robust Grammatical Error Correction](https://aclanthology.org/2026.findings-acl.195/) | Closest work for L2 counterfactual simulation; our distinction must be explanation-to-edit behavior, not only robust correction. |
| R05-004 | [Edit-level Majority Voting Mitigates Over-Correction in LLM-based Grammatical Error Correction](https://aclanthology.org/2026.bea-1.60/) | Supports behavior-stratified benchmark design and overcorrection negative cases. |
| R05-006 | [EXCGEC: A Benchmark for Edit-Wise Explainable Chinese Grammatical Error Correction](https://ojs.aaai.org/index.php/AAAI/article/view/34759) | Closest benchmark work; our English model-produced edit faithfulness must be clearly separated. |
| R05-008 | [CLEME2.0: Towards Interpretable Evaluation by Disentangling Edits for Grammatical Error Correction](https://aclanthology.org/2025.acl-long.10/) | Provides behavior vocabulary and a nearest metric baseline. |
| R05-018 | [GEE! Grammar Error Explanation with Large Language Models](https://aclanthology.org/2024.findings-naacl.49/) | Closest explanation generation work; our benchmark should evaluate explanation candidates rather than claim generation novelty. |
| R05-019 | [Controlled Generation with Prompt Insertion for Natural Language Explanations in Grammatical Error Correction](https://aclanthology.org/2024.lrec-main.350/) | Supports keeping explicit templates as leakage controls. |
| R05-020 | [Enhancing Grammatical Error Correction Systems with Explanations](https://aclanthology.org/2023.acl-long.413/) | Current pilot data source and label seed. |
| R05-031 | [Automatic Annotation and Evaluation of Error Types for Grammatical Error Correction](https://aclanthology.org/P17-1074/) | Core extraction layer; our labels inherit its noise. |
| R05-034 | [The BEA-2019 Shared Task on Grammatical Error Correction](https://aclanthology.org/W19-4406/) | Priority data-source expansion after EXPECT. |
| R05-039 | [Which Algorithmic Explanations Help Users Predict Model Behavior?](https://aclanthology.org/2020.acl-main.491/) | Nearest conceptual ancestor for counterfactual edit simulatability. |
| R05-040 | [Towards Faithfully Interpretable NLP Systems: How Should We Define and Evaluate Faithfulness?](https://aclanthology.org/2020.acl-main.386/) | Constrains claims and terminology. |
| R05-041 | [Towards Faithful Model Explanation in NLP: A Survey](https://aclanthology.org/2024.cl-2.6/) | Defines method families and evaluation threats. |
| R05-042 | [On Measuring Faithfulness or Self-consistency of Natural Language Explanations](https://aclanthology.org/2024.acl-long.329/) | Central caution for paper claims. |

## Working Interpretation

The literature makes one point sharp: reverse edit reconstruction alone is not enough. It is best treated as an L1 edit-correspondence or leakage diagnostic. A defensible main line should instead evaluate whether an explanation predicts the model's edit behavior under controlled GEC-specific perturbations, while reporting rule/evidence grounding as a separate L3 signal.
