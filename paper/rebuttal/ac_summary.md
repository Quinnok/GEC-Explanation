# Area Chair Summary Preparation

## One-Sentence Contribution

The paper introduces an executable pilot benchmark and diagnostic suite for evaluating whether explanations of model-produced GEC edits correspond to the edit, predict the same model's counterfactual edit behavior, and state rule/evidence claims consistent with the edit.

## What the Paper Does Not Claim

- It does not claim reverse reconstruction proves internal causal faithfulness.
- It does not claim automatic labels are human gold.
- It does not claim current counterfactual simulators are strong.
- It does not claim selected explanations are human-preferred or learner-helpful.

## Main Evidence

- 700 model-produced edits from EXPECT and JFLEG.
- 12,754 automatic explanation/control instances.
- 120 counterfactual variants labeled by actual GEC model reruns.
- L1 leakage controls: reverse reconstruction 0.640 Macro-F1, target-masked 0.439, leakage-adjusted 0.496.
- L2 negative result: best current simulator 0.297 Macro-F1.
- Reranking reward-hacking result: combined reranker 0.935 automatic pairwise accuracy but 100.0% top-1 edit-copy/template selection.

## Remaining Risk

The strongest unresolved weakness is the absence of real double-human annotation. The project provides a complete annotation package, but labels cannot be fabricated.

