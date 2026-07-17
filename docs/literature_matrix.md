# Literature Matrix

Last updated: 2026-07-18

| Paper | Venue | Year | Task | Method | Evaluation | Limitation | Difference |
|---|---:|---:|---|---|---|---|---|
| Enhancing Grammatical Error Correction Systems with Explanations | ACL | 2023 | Explainable GEC | EXPECT dataset with evidence words and error types for explanations | Baselines and human evaluation for learner usefulness | Does not directly test whether a free-form explanation reconstructs the exact model-produced edit | Our target is edit-faithfulness evaluation through reconstruction, not explanation generation alone |
| GEE! Grammar Error Explanation with Large Language Models | Findings of NAACL | 2024 | Grammar error explanation | Atomic edit extraction followed by LLM explanation | Multilingual edit extraction metrics and human evaluation | Focuses on generating/explaining gold correction pairs; faithfulness to model edits is not framed as reverse reconstruction | Our method treats reconstruction as an evaluation signal for explanation-edit consistency |
| Controlled Generation with Prompt Insertion for Natural Language Explanations in Grammatical Error Correction | LREC-COLING | 2024 | Natural-language GEC explanation generation | Prompt Insertion guides LLMs to cover extracted correction points | Dataset creation and controlled generation comparison | Controls coverage of correction points but does not evaluate explanations by recovering structured edits | Our method checks whether explanations imply the same edit fields |
| EXCGEC: A Benchmark for Edit-Wise Explainable Chinese Grammatical Error Correction | AAAI | 2025 | Edit-wise explainable Chinese GEC | Benchmark with hybrid edit-wise explanations | Automatic metrics and human evaluation | Chinese benchmark; evaluates explanation quality but not reverse reconstruction as the main diagnostic | Our target is English GEC and reconstruction-based edit faithfulness |
| CLEME2.0: Towards Interpretable Evaluation by Disentangling Edits for Grammatical Error Correction | ACL | 2025 | Interpretable GEC evaluation | Disentangles hit-correction, wrong-correction, under-correction, over-correction | Human consistency and reference-based metric comparisons | Evaluates correction behavior, not natural-language explanation faithfulness | Our method evaluates whether explanations correspond to produced edits |
| Explanation based In-Context Demonstrations Retrieval for Multilingual Grammatical Error Correction | NAACL | 2025 | GEC in-context example retrieval | Retrieves examples by matching grammar error explanations | Multilingual few-shot GEC performance | Uses explanations as retrieval signals, not as objects of faithfulness evaluation | Our method evaluates explanations themselves |

## Verification Notes

The entries above were checked against ACL Anthology or AAAI pages during iteration 1. The next pass must add BibTeX, closer faithfulness/simulatability work, and any papers named in the opening report that are not yet verified.

