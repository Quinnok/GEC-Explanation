# Decision Log

Last updated: 2026-07-18

| Date | Decision | Rationale | Risk |
|---|---|---|---|
| 2026-07-18 | Use AAAI 2027 template in `paper/`. | Official author kit is present locally. | Must re-check final AAAI instructions before submission. |
| 2026-07-18 | Treat toy pilot as code sanity check only. | No real dataset or model output is locally available. | Cannot support paper claims. |
| 2026-07-18 | Implement simple token-diff edit extraction first. | Provides executable scaffold while ERRANT integration is pending. | Not sufficient for final experiments. |
| 2026-07-18 | Use EXPECT as the real pilot data source. | Public upstream repository states MIT License and contains source/reference GEC pairs plus explanation-oriented labels. | Round 02 templates were automatic; Round 03 model-edit labels are automatic ERRANT alignments. |
| 2026-07-18 | Use ERRANT rather than token diff for real edit fields. | Token diff exact sample match with ERRANT is 94.7% before type labels. | ERRANT boundary ambiguity remains. |
| 2026-07-18 | Treat Round 02 generated explanation labels as automatic leakage controls only. | The construction is templated from ERRANT fields and produced 99.7%-100.0% full edit exact for explicit/raw controls. | It must not be interpreted as evidence that reverse reconstruction works on natural-language explanations. |
| 2026-07-18 | Upgrade Round 03 to model-produced edits. | The user explicitly rejected source-reference template pilot as the main experiment. | Model output creates detokenization and overcorrection boundary effects that must be analyzed rather than hidden. |
| 2026-07-18 | Use GECToR RoBERTa base 5k as the sequence-to-edit model. | It is a public local Hugging Face model for the GECToR tagger family and ran on CPU over 300 EXPECT sources. | Model card limits use to non-commercial purposes. |
| 2026-07-18 | Use `vennify/t5-base-grammar-correction` as the sequence-to-sequence model. | It is a public local Hugging Face seq2seq grammar-correction model and ran on CPU over 300 EXPECT sources. | License is CC-BY-NC-SA-4.0; outputs show many orthographic/detokenization edits under ERRANT. |
| 2026-07-18 | Define behavior labels by aligning source-reference ERRANT edits with source-prediction ERRANT edits. | This produces correct correction, wrong correction, overcorrection, and missed correction labels without using only the first edit. | Alignment failures and valid alternative corrections remain possible. |
| 2026-07-18 | Treat EXPECT fields as labels/evidence, not natural-language explanations. | Local README and JSONL fields show evidence indices and error types but no free-text explanation field. | A paper-grade natural-language explanation source still needs validation or annotation. |
| 2026-07-18 | Use FLAN-T5-base only as an open-source explanation-candidate generator. | It runs locally without paid APIs and uses source, model prediction, and predicted edit span rather than reference/gold edits. | Candidate quality is weak; outputs are not human gold and need stronger generation or filtering before main claims. |
