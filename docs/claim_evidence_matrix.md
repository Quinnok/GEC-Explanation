# Claim-Evidence Matrix

Last updated: 2026-07-18

| Claim ID | Claim | Required Evidence | Current Evidence | Experiment | Status | Risk |
|---|---|---|---|---|---|---|
| C1 | Existing GEC explanations contain edit-level inconsistencies. | Human-audited examples across real GEC model outputs and explanations. | Opening report motivates the issue; no local empirical evidence yet. | Build and annotate pilot explanations. | P0 Unverified | The problem may be less frequent than expected. |
| C2 | Text similarity is insufficient for detecting fine-grained explanation-edit mismatch. | Comparison against surface and embedding baselines on hard negatives. | No local evidence yet. | Run baselines on labeled hard-negative data. | P1 Unverified | Strong LLM or structured baselines may close the gap. |
| C3 | Reverse edit reconstruction measures edit faithfulness. | Correlation with human edit-faithfulness labels. | Conceptual definition only. | Human evaluation plus reconstruction metrics. | P0 Unverified | Reconstruction may measure information sufficiency, not faithfulness. |
| C4 | Structured reconstruction distinguishes location, target, operation, direction, and type errors. | Field-level metrics on controlled negative types. | Metric code implemented; no real data. | Negative-type pilot. | P1 Partially implemented | Edit boundaries can be ambiguous. |
| C5 | The method remains useful under implicit or masked explanations. | Ablation over explicit, implicit, masked-target, rule-only, and raw-edit conditions. | No evidence yet. | Leakage-control experiment. | P0 Unverified | Method may collapse without explicit edit leakage. |
| C6 | Reconstruction scores improve explanation candidate reranking. | Ranking metrics against human preferences. | No evidence yet. | Multi-candidate reranking experiment. | P2 Unverified | Candidate quality may dominate ranking. |
| C7 | Automatic reconstruction scores agree with human judgments. | Cohen's kappa or correlation on human-labeled samples. | No evidence yet. | Human annotation study. | P0 Unverified | Human labels may have low agreement. |

