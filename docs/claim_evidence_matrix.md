# Claim-Evidence Matrix

Last updated: 2026-07-18

| Claim | Current Evidence | Status | Risk |
|---|---|---|---|
| The project can run on real English GEC data. | EXPECT MIT-licensed sample: 300 source/reference pairs and 320 ERRANT edits in `data/processed/expect_v1_samples.jsonl`. | Supported for pilot | Full benchmark coverage still pending. |
| ERRANT is preferable to token diff for typed edit extraction. | Token diff matches ERRANT exactly on 94.7% of sampled sentences before type labels. | Supported for pilot | ERRANT itself can have boundary ambiguity. |
| Explicit explanations can leak the answer to a structured reconstructor. | Structured baseline explicit Full Edit Exact: 99.7%; raw edit string Full Edit Exact: 100.0%. | Supported for pilot | Template explanations make this an upper-control result. |
| Masking the target reduces target reconstruction. | Structured baseline masked-target Target Match: 11.7%. | Supported for pilot | Masked templates are automatic, not human explanations. |
| The current labels are not human gold. | Explanation pilot stats record `label_source=automatic_template`; 3000 explanation records generated automatically. | Explicitly constrained | Human validation is still required for final claims. |
