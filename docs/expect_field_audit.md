# EXPECT Field Audit

Last updated: 2026-07-18

## Source Checked

- Local repository: `data/downloads/Explainable_GEC`
- Upstream: https://github.com/lorafei/Explainable_GEC
- Recorded commit: `6e44b68f6e4c199dd3b235cacb604a856bd3d133`
- Files inspected: `data/json/train.json`, `data/json/dev.json`, `data/json/test.json`, `data/json/gector.json`, `data/json/t5.json`, and upstream `README.md`.

## Fields Present

Every inspected EXPECT JSONL record contains:

| Field | Meaning in upstream README | Usable as real annotation? | Round 03 treatment |
|---|---|---|---|
| `source` | Erroneous sentence tokens, with `[NONE]` placeholders for insertions/deletions. | Yes, as dataset-provided source text. | Used to build source sentences. |
| `target` | Corrected sentence tokens. | Yes, as dataset-provided reference correction. | Used as reference, never as model prediction. |
| `correction_index` | Indices of erroneous/corrected words in concatenated source-target sequence. | Yes, as explanation-adjacent supervision. | Audited, but not used as natural-language explanation. |
| `evidence_index` | Evidence-word indices in concatenated source-target sequence. | Yes, as evidence-word supervision. | Potential future rationale/evidence baseline. |
| `error_type` | Coarse grammatical error class. | Yes, as dataset-provided error type. | Used only for dataset statistics and potential future comparison. |
| `predicted_parsing_order` | Dependency-order features around corrections. | No human explanation; parser-derived/predicted feature. | Not treated as gold explanation. |
| `origin` | Learner CEFR proficiency for W&I+LOCNESS-derived splits. | Yes, metadata. | Stored when present. |

## Natural-Language Explanation Availability

EXPECT does not contain a free-text natural-language explanation field in the inspected JSONL data. It provides explanation-adjacent labels: evidence words and error types. Therefore:

- No EXPECT field can be used directly as a human-written edit-level natural-language explanation.
- Round 02 template explanations are automatic constructions and remain leakage controls only.
- Round 03 FLAN-T5-base explanations are open-source model candidates generated from source, model prediction, and predicted edit span; they are not human gold.

## Consequence

The paper may use EXPECT as real GEC data and may use its evidence/error-type labels as structured supervision or analysis metadata. It must not claim that EXPECT supplies human natural-language explanations for model-produced edits unless a separate, license-clear annotation source is added.
