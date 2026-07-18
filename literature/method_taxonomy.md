# Method Taxonomy

| Layer | Method Family | Representative Work | Role in This Project |
|---|---|---|---|
| Correction model | Sequence-to-edit | PIE, GECToR, edit-level majority voting | Produces model edits with explicit operations. |
| Correction model | Sequence-to-sequence / instruction following | T5, CoEdIT, prompted LLM GEC, minimal-edit LLMs | Produces fluent corrections and overcorrection cases. |
| Edit extraction | Automatic typed edits | M2, ERRANT, CLEME2.0 | Defines spans, targets, operations, and error types. |
| Explanation generation | Free-text GEE | GEE, Prompt Insertion, EXCGEC | Provides close baselines and leakage risks. |
| Explanation labels | Evidence/rule labels | EXPECT, pedagogical characterization, ERASER | Grounds L3 rule/evidence checks. |
| L1 evaluation | Correspondence/reconstruction | M2-style matching, reverse reconstruction, structured extraction | Diagnostic only; vulnerable to explicit leakage. |
| L2 evaluation | Counterfactual simulatability | Hase and Bansal, CheckList, contrast sets, COCOGEC | Likely main contribution when tied to model-produced edit behavior. |
| L3 evaluation | Rule/evidence grounding | EXPECT, rationale work, pedagogical characterization | Secondary faithfulness/plausibility axis. |
