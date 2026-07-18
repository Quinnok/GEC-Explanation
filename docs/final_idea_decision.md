# Round 06 Final Idea Decision

Date: 2026-07-18

## Main Line

Counterfactual Edit Simulatability for faithful explanations of model-produced GEC edits.

The paper should ask whether an explanation predicts the actual edit behavior of a GEC model under controlled counterfactual changes. Error-irrelevant variants should preserve the model edit if the model is stable; rule-relevant variants may cancel, retarget, or change the edit. The key label is not a grammar-theory expectation but the rerun behavior of the same GEC model.

## Backup Line

Rule-grounded Faithfulness.

If counterfactual generation or rerun labels prove too noisy, the backup paper should evaluate whether explanations state grammar rules that are consistent with the model-produced edit, the ERRANT/EXPECT error type, the source evidence, and the edit direction. Evidence-grounded Faithfulness remains a supporting L3 component rather than a separate main line.

## Demoted or Reframed Ideas

- Reverse Edit Reconstruction: demoted to L1 edit correspondence and leakage diagnosis.
- Leakage-adjusted Edit Simulatability: required control, not standalone contribution.
- Evidence-grounded Faithfulness: supporting L3 signal.
- Faithfulness-calibrated Explanation Reranking: downstream application after benchmark validation.

## Updated Working Title

Counterfactual Edit Simulatability for Faithful Explanations of Grammatical Error Correction Edits

## Updated Core Question

Do natural-language explanations identify the rule and evidence that make a GEC model produce a particular edit, strongly enough to predict whether the edit is preserved, changed, or canceled under controlled counterfactual variants?

## Updated Contributions to Test

1. A model-produced English GEC edit benchmark with correction behavior labels, explanation candidates, and hard negatives.
2. A three-layer evaluation suite: L1 edit correspondence/leakage controls, L2 counterfactual edit simulatability, and L3 rule/evidence grounding.
3. A counterfactual protocol that reruns the original GEC model and uses actual model behavior as labels.
4. A behavior-stratified analysis across correct corrections, wrong corrections, overcorrections, missed-correction diagnoses, edit operations, and error types.
5. A human annotation package separating edit correspondence, behavioral faithfulness, grammatical validity, and helpfulness.

## Decision Evidence

- Round 02 proved explicit template reconstruction is an answer-leakage upper control.
- Round 03/04 established 1707 model-produced edits and behavior labels from two real public GEC models.
- Round 04 showed detokenization/ORTH/PUNCT effects can distort behavior counts unless raw and normalized views are separated.
- Round 05 found strong prior work that already covers GEC explanation generation, edit-wise explainable GEC benchmarks, behavior-decomposed GEC metrics, simulatability, and GEC counterfactual robustness.
- The surviving space is narrower: explanation-to-model-edit behavior under controlled GEC counterfactuals.

## Immediate Experimental Plan

1. Build `data/faithfulness_benchmark/` from the existing model-produced edit dataset, targeting at least 500 actual predicted edits and at least 100 missed-edit diagnoses.
2. Generate multi-source explanations and hard negatives for each predicted edit, explicitly labeling templates as leakage controls and generated text as non-gold candidates.
3. Implement L1 metrics first: random, majority, surface, structured extraction, reverse reconstruction, masked-target reconstruction, and leakage-adjusted deltas.
4. Implement L2 counterfactual pilot for high-precision edit types first: subject-verb agreement, articles/determiners, noun number, verb tense, prepositions, and pronouns.
5. Implement L3 rule/evidence verifier using ERRANT/EXPECT labels and evidence spans.
6. Prepare human annotation package before any claim that automatic faithfulness labels match human judgments.

## Claims Still Forbidden

- Do not claim the work is the first edit-wise GEC explanation benchmark.
- Do not claim reverse reconstruction measures internal model faithfulness.
- Do not call generated explanations human gold.
- Do not report counterfactual faithfulness results until GEC models have been rerun on the counterfactual variants.
