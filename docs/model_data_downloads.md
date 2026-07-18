# Model and Data Download Notes

## Datasets

| Resource | Source | Local Use | License/Restriction |
|---|---|---|---|
| EXPECT | `https://github.com/lorafei/Explainable_GEC` | English source/reference pairs plus evidence/error-type fields. | Upstream repository states MIT License. |
| JFLEG | `https://github.com/keisks/jfleg` | English GEC source sentences with four references; current ERRANT pilot uses reference 0 while retaining all references. | Upstream README states CC BY-NC-SA 4.0. |

Downloads are stored under `data/downloads/`, which is intentionally ignored by Git.

## Models

| Model Key | Hugging Face ID | Role | Local Status |
|---|---|---|---|
| `gector_roberta_base` | `gotutiyan/gector-roberta-base-5k` | Sequence-to-edit GEC model. | Ran locally on CPU. |
| `t5_base_grammar` | `vennify/t5-base-grammar-correction` | Sequence-to-sequence GEC model. | Ran locally on CPU. |
| `coedit_large` | `grammarly/coedit-large` | Instruction-following text editor pilot. | Ran locally on CPU for a small 20-source branch. |
| `flan_t5_base` | `google/flan-t5-base` | Open-source explanation candidate/judge baseline. | Ran locally on CPU; no paid API. |

Downloaded model weights are stored by Hugging Face cache or `models/`; large local caches are not committed.

## No Paid APIs

No paid API or private-key service is used. The LLM judge in Round 11 is a local open-source FLAN-T5 baseline and is not human evaluation.
