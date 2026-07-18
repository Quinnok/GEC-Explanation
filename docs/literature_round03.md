# Round 03 Focused Literature Pass

Last updated: 2026-07-18

## Scope

This pass checked the nearest work around reverse reconstruction, explanation simulatability, rationale faithfulness, explanation-to-prediction consistency, and edit-wise GEC explanation evaluation. Sources checked include ACL Anthology, AAAI proceedings, Hugging Face model cards, and public GitHub repositories.

## Closest Work 1: GEE! Grammar Error Explanation with Large Language Models

- Source: https://aclanthology.org/2024.findings-naacl.49/
- Input: a pair of erroneous and corrected sentences.
- Output: one-sentence explanations for grammatical errors.
- Uses reverse reconstruction? No verified use of a reverse edit reconstruction metric. The paper frames generation through structured atomic edit extraction followed by LLM explanation.
- Evaluates GEC edit-level explanations? Yes, it is directly about grammar error explanations for errors/edits, with multilingual evaluation and human correctness judgments.
- Difference from this project: GEE primarily generates explanations for correction pairs. Round 03 targets explanations for edits actually produced by GEC models and evaluates whether the explanation is consistent with the produced edit under leakage controls.

## Closest Work 2: Controlled Generation with Prompt Insertion for Natural-Language Explanations in GEC

- Source: https://aclanthology.org/2024.lrec-main.350/
- Input: GEC input text and correction points extracted after correction.
- Output: natural-language explanations controlled by Prompt Insertion.
- Uses reverse reconstruction? No verified reverse reconstruction evaluation. It inserts extracted correction points to guide explanation generation.
- Evaluates GEC edit-level explanations? Yes, at the level of correction points and generated reasons, but not as reconstruction of a structured model-produced edit.
- Difference from this project: Prompt Insertion is a generation-control method. This project treats explicit edit strings as leakage controls and asks whether generated/free-form explanations imply the same structured edit.

## Closest Work 3: EXCGEC

- Source: https://ojs.aaai.org/index.php/AAAI/article/view/34759
- Input: Chinese GEC examples with edits.
- Output: correction plus hybrid edit-wise explanations.
- Uses reverse reconstruction? No verified reverse reconstruction metric.
- Evaluates GEC edit-level explanations? Yes, it is an edit-wise explainable Chinese GEC benchmark with automatic metrics and human evaluation.
- Difference from this project: EXCGEC is a Chinese benchmark for joint correction/explanation. Round 03 is English, model-prediction-centered, and focused on explanation-to-produced-edit consistency rather than benchmark construction alone.

## Additional Related Work

- EXPECT: https://aclanthology.org/2023.acl-long.413/ and https://github.com/lorafei/Explainable_GEC. It provides evidence words and grammatical error types for GEC explanations, but the inspected JSONL files do not contain free-text explanations.
- Hase and Bansal 2020 simulatability: https://aclanthology.org/2020.acl-main.491/. Simulatability asks whether people can predict model behavior with explanations. This is conceptually close, but it is not an edit-wise GEC reverse reconstruction protocol.
- Lyu et al. 2024 faithfulness survey: https://aclanthology.org/2024.cl-2.6/. It defines faithfulness broadly as accurately representing model reasoning and surveys NLP methods, but it does not provide a GEC edit reconstruction benchmark.
- Parcalabescu and Frank 2024: https://aclanthology.org/2024.acl-long.329/. It cautions that many natural-language explanation faithfulness tests measure output-level self-consistency rather than internal reasoning faithfulness. This warning applies directly to the current project: reverse edit reconstruction should be framed as explanation-edit consistency, not as proof of internal model reasoning.

## Current Novelty Assessment

The current contribution still appears plausible as an English GEC edit-level diagnostic for whether a natural-language explanation is consistent with a model-produced edit. However, the evidence does not justify using "first" or "novel" yet. A final systematic search is still required before submission, especially for adjacent terms such as inverse prediction, self-rationalization consistency, recourse reconstruction, and post-hoc explanation consistency.

## Claim Constraint

Use this wording direction for now: "We study reconstruction as a leakage-aware diagnostic for explanation-to-edit consistency in model-produced GEC edits." Do not claim that the method measures internal model reasoning, and do not interpret Round 02 explicit-template reconstruction as method effectiveness.
