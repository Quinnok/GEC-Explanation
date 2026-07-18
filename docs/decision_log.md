# Decision Log

Last updated: 2026-07-18

| Date | Decision | Rationale | Risk |
|---|---|---|---|
| 2026-07-18 | Use AAAI 2027 template in `paper/`. | Official author kit is present locally. | Must re-check final AAAI instructions before submission. |
| 2026-07-18 | Treat toy pilot as code sanity check only. | No real dataset or model output is locally available. | Cannot support paper claims. |
| 2026-07-18 | Implement simple token-diff edit extraction first. | Provides executable scaffold while ERRANT integration is pending. | Not sufficient for final experiments. |


| 2026-07-18 | Use EXPECT as the real pilot data source. | Public upstream repository states MIT License and contains source/reference GEC pairs plus explanation-oriented labels. | Pilot is limited to automatic constructions and first ERRANT edit per sentence. |
| 2026-07-18 | Use ERRANT rather than token diff for real edit fields. | Token diff exact sample match with ERRANT is 94.7% before type labels. | ERRANT boundary ambiguity remains. |
| 2026-07-18 | Treat generated explanation labels as automatic pilot labels only. | The construction is templated from ERRANT fields. | Human gold faithfulness validation remains open. |

| 2026-07-18 | Use EXPECT as the real pilot data source. | Public upstream repository states MIT License and contains source/reference GEC pairs plus explanation-oriented labels. | Pilot is limited to automatic constructions and first ERRANT edit per sentence. |
| 2026-07-18 | Use ERRANT rather than token diff for real edit fields. | Token diff exact sample match with ERRANT is 94.7% before type labels. | ERRANT boundary ambiguity remains. |
| 2026-07-18 | Treat generated explanation labels as automatic pilot labels only. | The construction is templated from ERRANT fields. | Human gold faithfulness validation remains open. |
