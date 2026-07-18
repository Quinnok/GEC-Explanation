# Round 06 Idea Candidates

Date: 2026-07-18

All ideas are evaluated after the Round 05 literature package. Scores and judgments are planning evidence, not experimental results.

## 1. Reverse Edit Reconstruction

- One-sentence problem: Can a source sentence plus explanation recover the structured edit?
- Motivation: A faithful edit explanation should specify enough about location, operation, target, and type to identify the edit.
- Closest work: Hase and Bansal on simulatability, M2/ERRANT edit matching, GEE and Prompt Insertion on edit explanations, Parcalabescu and Frank on self-consistency.
- Real technical difference: Applies reconstruction to GEC edit structures, but this is mostly a mechanized correspondence test.
- GEC specificity: Medium; spans, operation, target, and ERRANT type are GEC-specific, but reconstruction itself is general.
- Method structure: Extract model edits, generate explanations, reconstruct edit fields, compare to predicted edit.
- Needed data: Model-produced edits and explanation candidates.
- Needed models: Structured parser, optional small seq2seq reconstructor.
- Main experiment: Leakage-controlled reconstruction across explanation conditions.
- Ablation: Source-only, explanation-only, explicit template, masked target, raw edit string.
- Human evaluation: Needed only to validate that reconstruction correlates with perceived faithfulness.
- Innovation strength: Low after Round 05.
- Implementation cost: Low.
- Compute cost: Low.
- Data risk: Medium because explicit explanations leak answers.
- Reviewer risk: Very high; reviewers can say this measures output self-consistency or string leakage.
- Likely rejection reason: "This is just extracting an edit from an explanation, not faithfulness."
- Success contribution: Useful L1 diagnostic and leakage detector.
- Failure pivot: Keep as a control, not the main method.

## 2. Leakage-adjusted Edit Simulatability

- One-sentence problem: Can we measure explanation-to-edit predictiveness after removing target-copying shortcuts?
- Motivation: Round 02 shows explicit templates can make reconstruction trivial.
- Closest work: Hase and Bansal simulatability, Parcalabescu and Frank self-consistency, GEE/Prompt Insertion.
- Real technical difference: Explicitly estimates and subtracts reconstruction gains attributable to target/source leakage.
- GEC specificity: Medium-high because leakage is structured by edit target, operation, and ERRANT type.
- Method structure: Run reconstruction under raw, masked-target, shuffled, source-only, and explanation-only conditions; report leakage-adjusted deltas.
- Needed data: Model-produced edits, explanation variants, hard negatives.
- Needed models: Structured extractor, optional embedding or open LLM reconstructor.
- Main experiment: Compare raw reconstruction score against masked and shuffled controls.
- Ablation: No target, no operation, no type, no source, no behavior stratification.
- Human evaluation: Correlate leakage-adjusted score with human faithfulness labels if available.
- Innovation strength: Medium.
- Implementation cost: Low-medium.
- Compute cost: Low.
- Data risk: Medium; needs enough non-template explanations.
- Reviewer risk: Medium; may still look like a diagnostic rather than a full benchmark.
- Likely rejection reason: "Good control, but not a new faithfulness concept."
- Success contribution: Necessary control layer for any reconstruction claims.
- Failure pivot: Retain as L1 diagnostic supporting L2 counterfactual method.

## 3. Counterfactual Edit Simulatability

- One-sentence problem: Does an explanation predict how the GEC model's edit changes under controlled counterfactual variants?
- Motivation: Faithful explanations should identify rule-relevant conditions, not only restate the observed edit.
- Closest work: Hase and Bansal simulatability, CheckList, contrast sets, Polyjuice, COCOGEC, CLEME2.0 behavior decomposition.
- Real technical difference: Labels come from rerunning the original GEC model on counterfactual inputs and comparing model-produced edits, while explanations are evaluated for predicting preserve/change/cancel/retarget behavior.
- GEC specificity: Very high; perturbations target grammatical conditions such as number, tense, article licensing, preposition government, pronoun agreement, and edit spans.
- Method structure: Build error-irrelevant and rule-relevant counterfactuals, rerun GEC models, align resulting edits, evaluate whether explanation-derived predictions match actual edit behavior.
- Needed data: Model-produced edits, counterfactual source variants, rerun model predictions, explanations and negatives.
- Needed models: Original GEC models, counterfactual generator/filter, simulator/verifier.
- Main experiment: Compare counterfactual score with L1 reconstruction and rule/evidence baselines across models, behaviors, and error types.
- Ablation: Only irrelevant counterfactuals, only rule-relevant counterfactuals, no rerun labels, no normalization, no behavior strata.
- Human evaluation: Humans judge whether explanation should imply edit preservation or change and compare to model behavior.
- Innovation strength: High, if clearly separated from COCOGEC robustness.
- Implementation cost: Medium-high.
- Compute cost: Medium; rerunning lightweight GEC models is feasible on CPU for pilot scale.
- Data risk: Medium; counterfactual validity needs filtering and audit.
- Reviewer risk: Medium-high; COCOGEC is close, and simulator validity can be challenged.
- Likely rejection reason: "Counterfactual generation may test model robustness rather than explanation faithfulness."
- Success contribution: A GEC-specific behavioral faithfulness metric beyond leakage-prone reconstruction.
- Failure pivot: If counterfactuals are too noisy, fall back to Rule-grounded Faithfulness with a smaller audited counterfactual analysis.

## 4. Rule-grounded Faithfulness

- One-sentence problem: Does the explanation state a grammar rule consistent with the edit type, evidence, and direction?
- Motivation: Learner-facing GEC explanations should be grammatically meaningful and specific.
- Closest work: EXPECT, GEE, EXCGEC, pedagogically relevant grammatical error characterization, ERASER rationale evaluation.
- Real technical difference: Evaluates rule/edit/evidence consistency for model-produced edits rather than generation quality alone.
- GEC specificity: Very high; rule categories map directly to grammar error types.
- Method structure: Extract rule claim from explanation, classify rule family, verify compatibility with ERRANT type, source evidence, target edit, and behavior.
- Needed data: Edits with ERRANT/EXPECT labels, explanation candidates, rule schema.
- Needed models: Rule classifier, evidence span extractor, contradiction checks.
- Main experiment: Rule consistency and contradiction detection across positive/negative explanations.
- Ablation: No error type, no evidence, no target, no source context.
- Human evaluation: Human ratings for rule correctness, evidence correctness, specificity, and faithfulness.
- Innovation strength: Medium-high.
- Implementation cost: Medium.
- Compute cost: Low-medium.
- Data risk: Medium; rule schema must be reliable and not overfit to ERRANT labels.
- Reviewer risk: Medium; could be seen as linguistic validity rather than model faithfulness.
- Likely rejection reason: "Rule correctness is not model faithfulness."
- Success contribution: Strong L3 signal and backup paper direction if counterfactuals fail.
- Failure pivot: Use as human-eval dimension and reranking feature.

## 5. Evidence-grounded Faithfulness

- One-sentence problem: Does the explanation cite evidence spans that actually support the produced edit?
- Motivation: EXPECT supplies evidence indices; evidence is a bridge between explanation text and correction behavior.
- Closest work: EXPECT, ERASER, rationale extraction, GEE.
- Real technical difference: Tests whether evidence spans align with model-produced edits, not only reference edits.
- GEC specificity: High; evidence is tied to error causes and source spans.
- Method structure: Extract evidence spans from explanation, compare with EXPECT evidence and predicted edit span, then run evidence deletion/substitution tests.
- Needed data: EXPECT evidence labels plus model edits.
- Needed models: Span extractor, evidence perturbation generator.
- Main experiment: Evidence-span precision/recall and edit-behavior sensitivity to evidence perturbation.
- Ablation: Remove evidence text, substitute evidence, swap evidence across samples.
- Human evaluation: Human evidence correctness and specificity labels.
- Innovation strength: Medium.
- Implementation cost: Medium.
- Compute cost: Low.
- Data risk: Medium; EXPECT evidence labels are reference-oriented, not necessarily model-oriented.
- Reviewer risk: Medium; evidence overlap can become another surface metric.
- Likely rejection reason: "Evidence labels do not prove model behavior."
- Success contribution: Useful grounding layer and annotation target.
- Failure pivot: Combine with Rule-grounded Faithfulness rather than stand alone.

## 6. Faithfulness-calibrated Explanation Reranking

- One-sentence problem: Can faithfulness metrics select better explanations among multiple candidates for the same edit?
- Motivation: A benchmark should be useful beyond scoring; reranking demonstrates practical value.
- Closest work: Explanation-based retrieval for GEC, GEE generation, LLM judges, reranking/selection work in GEC.
- Real technical difference: Uses L1/L2/L3 faithfulness features to rank explanations rather than generate corrections.
- GEC specificity: Medium-high when features use edit behavior, ERRANT type, and counterfactual reruns.
- Method structure: Generate multiple explanation candidates, score with baselines and proposed metrics, evaluate top-1 against human or proxy labels.
- Needed data: Multiple explanation candidates per edit and preference/faithfulness labels.
- Needed models: Candidate generators, reranker, optional LLM judge.
- Main experiment: Ranking accuracy, MRR, faithfulness, grammatical validity, helpfulness, and reward-hacking checks.
- Ablation: Remove counterfactual score, remove rule/evidence score, length-only, surface-only.
- Human evaluation: Needed for final preference claims.
- Innovation strength: Medium.
- Implementation cost: Medium-high.
- Compute cost: Medium.
- Data risk: High without human preferences.
- Reviewer risk: High if automatic labels drive the ranking.
- Likely rejection reason: "The application is built on unvalidated metrics."
- Success contribution: Strong Round 11 application after benchmark is credible.
- Failure pivot: Keep as future work until human labels exist.
