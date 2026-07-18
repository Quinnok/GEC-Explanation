# Chronological Lineage

## 2012

- R05-036: [Better Evaluation for Grammatical Error Correction](https://aclanthology.org/N12-1067/) - Edit matching precedes our reconstruction idea by many years.

## 2014

- R05-035: [The CoNLL-2014 Shared Task on Grammatical Error Correction](https://aclanthology.org/W14-1701/) - Useful standard test but not necessarily license-simple for redistribution.

## 2015

- R05-037: [Ground Truth for Grammatical Error Correction Metrics](https://aclanthology.org/P15-2097/) - Human-grounded validation is a long-standing demand.

## 2016

- R05-044: [Rationalizing Neural Predictions](https://aclanthology.org/D16-1011/) - Evidence spans are not automatically explanations unless tied to behavior.

## 2017

- R05-031: [Automatic Annotation and Evaluation of Error Types for Grammatical Error Correction](https://aclanthology.org/P17-1074/) - Foundational dependency for this project.
- R05-038: [JFLEG: A Fluency Corpus and Benchmark for Grammatical Error Correction](https://aclanthology.org/E17-2037/) - Our benchmark must mark minimal-edit vs fluency-edit behavior.

## 2019

- R05-033: [Parallel Iterative Edit Models for Local Sequence Transduction](https://aclanthology.org/D19-1435/) - Edit-based correction is a mature modeling direction.
- R05-034: [The BEA-2019 Shared Task on Grammatical Error Correction](https://aclanthology.org/W19-4406/) - Candidate second English data source, but license/access must be checked.
- R05-045: [Attention is not Explanation](https://aclanthology.org/N19-1357/) - Surface/attention-style baselines should be treated skeptically.
- R05-046: [Attention is not not Explanation](https://aclanthology.org/D19-1002/) - Our paper should distinguish what each metric can and cannot prove.

## 2020

- R05-032: [GECToR - Grammatical Error Correction: Tag, Not Rewrite](https://aclanthology.org/2020.bea-1.16/) - Good model family for actual predicted edit benchmark.
- R05-039: [Which Algorithmic Explanations Help Users Predict Model Behavior?](https://aclanthology.org/2020.acl-main.491/) - Directly motivates explanation-to-behavior evaluation.
- R05-040: [Towards Faithfully Interpretable NLP Systems: How Should We Define and Evaluate Faithfulness?](https://aclanthology.org/2020.acl-main.386/) - We must not equate output reconstruction with internal faithfulness.
- R05-043: [ERASER: A Benchmark to Evaluate Rationalized NLP Models](https://aclanthology.org/2020.acl-main.408/) - Rationale faithfulness metrics need human/evidence labels.
- R05-047: [Beyond Accuracy: Behavioral Testing of NLP Models with CheckList](https://aclanthology.org/2020.acl-main.442/) - Counterfactual edit simulatability can be cast as behavior testing.
- R05-048: [Evaluating Models' Local Decision Boundaries via Contrast Sets](https://aclanthology.org/2020.findings-emnlp.117/) - Rule-relevant counterfactuals for GEC are analogous to contrast sets.
- R05-050: [Learning The Difference That Makes A Difference With Counterfactually-Augmented Data](https://openreview.net/forum?id=Sklgs0NFvr) - Human counterfactuals are strong but costly; we must not fake them.

## 2021

- R05-049: [Polyjuice: Generating Counterfactuals for Explaining, Evaluating, and Improving Models](https://aclanthology.org/2021.acl-long.523/) - Useful generator baseline but not GEC-specific.

## 2023

- R05-020: [Enhancing Grammatical Error Correction Systems with Explanations](https://aclanthology.org/2023.acl-long.413/) - EXPECT is ideal for pilot data but not a human free-text explanation source.
- R05-021: [Grammatical Error Correction: A Survey of the State of the Art](https://aclanthology.org/2023.cl-3.4/) - Evaluation reliability and human judgment concerns are central.
- R05-028: [Exploring Effectiveness of GPT-3 in Grammatical Error Correction: A Study on Performance and Controllability in Prompt-Based Methods](https://aclanthology.org/2023.bea-1.18/) - Prompt controls must be logged for model predictions and explanation generation.
- R05-029: [A Closer Look at k-Nearest Neighbors Grammatical Error Correction](https://aclanthology.org/2023.bea-1.19/) - Example evidence is another explanation-like artifact.
- R05-030: [CoEdIT: Text Editing by Task-Specific Instruction Tuning](https://aclanthology.org/2023.findings-emnlp.350/) - Candidate lightweight open generator/corrector.

## 2024

- R05-018: [GEE! Grammar Error Explanation with Large Language Models](https://aclanthology.org/2024.findings-naacl.49/) - The strongest English-adjacent natural-language GEE precedent.
- R05-019: [Controlled Generation with Prompt Insertion for Natural Language Explanations in Grammatical Error Correction](https://aclanthology.org/2024.lrec-main.350/) - Template/control choices can cause leakage and format artifacts.
- R05-022: [Pillars of Grammatical Error Correction: Comprehensive Inspection Of Contemporary Approaches In The Era of Large Language Models](https://aclanthology.org/2024.bea-1.3/) - Strong models and outputs can be reused for benchmark expansion.
- R05-023: [No Error Left Behind: Multilingual Grammatical Error Correction with Pre-trained Translation Models](https://aclanthology.org/2024.eacl-long.73/) - Seq2seq/translation framing remains a core model family.
- R05-024: [To Err Is Human, but Llamas Can Learn It Too](https://aclanthology.org/2024.findings-emnlp.727/) - Synthetic data must be clearly separated from gold labels.
- R05-025: [Large Language Models Are State-of-the-Art Evaluator for Grammatical Error Correction](https://aclanthology.org/2024.bea-1.6/) - LLM judge is a necessary baseline but risky.
- R05-026: [Evaluating Prompting Strategies for Grammatical Error Correction Based on Language Proficiency](https://aclanthology.org/2024.lrec-main.569/) - Instruction prompts are a confound in third-model benchmark design.
- R05-027: [Evaluation of Really Good Grammatical Error Correction](https://aclanthology.org/2024.lrec-main.584/) - Supports our move away from single aggregate scores.
- R05-041: [Towards Faithful Model Explanation in NLP: A Survey](https://aclanthology.org/2024.cl-2.6/) - Our method should be framed as behavioral faithfulness/self-consistency unless human/internal evidence exists.
- R05-042: [On Measuring Faithfulness or Self-consistency of Natural Language Explanations](https://aclanthology.org/2024.acl-long.329/) - Our reverse reconstruction must be named self-consistency/correspondence, not faithfulness.

## 2025

- R05-006: [EXCGEC: A Benchmark for Edit-Wise Explainable Chinese Grammatical Error Correction](https://ojs.aaai.org/index.php/AAAI/article/view/34759) - This is the strongest edit-wise explainable GEC benchmark precedent.
- R05-007: [Explanation based In-Context Demonstrations Retrieval for Multilingual Grammatical Error Correction](https://aclanthology.org/2025.naacl-long.251/) - Explanations can guide correction, but this is not explanation faithfulness evaluation.
- R05-008: [CLEME2.0: Towards Interpretable Evaluation by Disentangling Edits for Grammatical Error Correction](https://aclanthology.org/2025.acl-long.10/) - Our behavior labels align with an emerging metric direction.
- R05-009: [Improving Explainability of Sentence-level Metrics via Edit-level Attribution for Grammatical Error Correction](https://aclanthology.org/2025.acl-srw.77/) - Edit-level explanation is now applied even to evaluation metrics.
- R05-010: [Adapting LLMs for Minimal-edit Grammatical Error Correction](https://aclanthology.org/2025.bea-1.9/) - Detokenization and minimal edit choices are central confounds for our T5 behavior.
- R05-011: [gec-metrics: A Unified Library for Grammatical Error Correction Evaluation](https://aclanthology.org/2025.acl-demo.50/) - Our artifact should mirror this reproducibility discipline.
- R05-012: [LLM-based post-editing as reference-free GEC evaluation](https://aclanthology.org/2025.bea-1.16/) - LLM judges/post-editors are plausible but must be controlled.
- R05-013: [LLMs in alliance with Edit-based models: advancing In-Context Learning for Grammatical Error Correction by Specific Example Selection](https://aclanthology.org/2025.bea-1.38/) - Edit types can guide LLM behavior.
- R05-014: [Edit-Wise Preference Optimization for Grammatical Error Correction](https://aclanthology.org/2025.coling-main.229/) - Edit-level objectives are active in current GEC research.
- R05-015: [Paragraph-level Error Correction and Explanation Generation](https://aclanthology.org/2025.bea-1.72/) - Contextual explanations are relevant but increase annotation burden.
- R05-016: [A Silver Multilingual Dataset for Grammatical Error Correction](https://aclanthology.org/2025.unlp-1.17/) - Silver data needs license and quality controls.
- R05-017: [Minimal-Edit Instruction Tuning for Low-Resource Indic GEC](https://aclanthology.org/2025.bhasha-1.17/) - Minimal-edit framing supports our separation of valid correction from overcorrection.

## 2026

- R05-001: [COCOGEC: Counterfactual Generation for Robust Grammatical Error Correction](https://aclanthology.org/2026.findings-acl.195/) - Counterfactuals are a strong and very close precedent for any GEC counterfactual method.
- R05-002: [LLM-Powered but Rule-Grounded: Pedagogically Relevant Grammatical Error Characterization for Learner Model Construction](https://aclanthology.org/2026.bea-1.58/) - Rule and pedagogy dimensions are useful grounding targets for explanations.
- R05-003: [Instruction-Following LLMs for Grammatical Error Correction: Analyzing Neutral-Anchored Instructional Sensitivity Across Editing Modes](https://aclanthology.org/2026.bea-1.17/) - Useful for selecting a third model family in our benchmark.
- R05-004: [Edit-level Majority Voting Mitigates Over-Correction in LLM-based Grammatical Error Correction](https://aclanthology.org/2026.bea-1.60/) - Overcorrection is a central behavior stratum for explanation evaluation.
- R05-005: [FinnGEC: Benchmarking Grammatical Error Correction for Finnish](https://aclanthology.org/2026.bea-1.33/) - Data-source generality matters but is outside the immediate English AAAI target.
