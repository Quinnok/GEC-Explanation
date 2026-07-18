# License Summary

This summary is for research planning and does not replace legal review.

| Artifact | License/Restriction | Evidence Location | Project Handling |
|---|---|---|---|
| EXPECT data | MIT License according to upstream repository. | `docs/data_statement.md`, `docs/license_report.md`. | Used for public research pilot. |
| JFLEG data | CC BY-NC-SA 4.0 according to upstream README. | `docs/data_statement.md`, `docs/license_report.md`. | Used for non-commercial research pilot; all references retained. |
| GECToR checkpoint | Public Hugging Face model with non-commercial restriction noted in runtime metadata. | `results/model_predictions/runtime_metadata.json`. | Used locally for CPU pilot; note restriction in paper/artifact. |
| T5 grammar checkpoint | Public Hugging Face model with CC-BY-NC-SA-4.0 noted in runtime metadata. | `results/model_predictions/runtime_metadata.json`. | Used locally for CPU pilot; note non-commercial/share-alike constraint. |
| CoEdIT-large checkpoint | Public Hugging Face model with CC-BY-NC-4.0 noted in runtime metadata. | `results/model_predictions/expect_v1_coedit_runtime_metadata.json`. | Small CPU branch only; note non-commercial constraint. |
| FLAN-T5-base | Public open-source Hugging Face model. | `results/round11/local_llm_judge_metadata.json`. | Used as no-paid-API automatic judge baseline. |
| AAAI-27 author kit | Official AAAI author kit. | `AuthorKit27/`, `paper/aaai2027.sty`, `paper/aaai2027.bst`. | Used for manuscript formatting. |

Human annotation files in `annotation/round10/` contain no completed human labels. Do not describe hidden automatic metadata as human gold.
