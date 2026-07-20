# RuleFaith-GEC Method Paper Brief

Created: 2026-07-19

## Working Title

RuleFaith-GEC: Verifier-Guided Selective Distillation for Faithful Edit-Level Grammatical Error Explanations

## Goal

Turn the existing GEC explanation stress-test project into a method paper that generates more faithful edit-level grammar explanations, rather than only diagnosing metric failure.

## Central Research Question

How can an explanation model generate edit-level GEC explanations that align with the model-produced edit, state correct grammar rules, cite relevant evidence, identify invalid edits without false rationalization, and abstain under uncertainty?

## Core Hypothesis

Verifier-guided filtering, refinement, preference construction, and selective calibration can improve rule correctness, evidence correctness, and false-rationalization behavior relative to direct prompting and vanilla teacher distillation.

## Method Structure

1. Teacher candidate generation
   - GPT-5.5 teacher candidates.
   - At least one open instruction-model teacher.
   - No reference correction, human final label, or behavior label is provided to the teacher.

2. Edit validity gate
   - Classifies model edit validity independently of explanation quality.
   - Allows honest explanation of invalid edits.

3. Edit alignment verifier
   - Uses reconstruction, target-masked reconstruction, leakage-adjusted reconstruction, lexical checks, and structured extraction.
   - Treated as edit correspondence, not complete faithfulness.

4. Rule and evidence verifier
   - Checks whether the rule is correct and applicable.
   - Checks whether contextual evidence is present and correct.

5. Counterfactual consistency verifier
   - Uses model reruns as diagnostic signals.
   - Does not fabricate behavior labels from grammar expectations.

6. Selective refinement and distillation
   - Accept, refine, reject, or abstain based on verifier scores.
   - Construct SFT and preference data.
   - Train Direct, Vanilla SFT, Filtered SFT, Preference, and RuleFaith-GEC variants.

## Three Main Contributions

1. Verifier-guided explanation generation for edit-level GEC.
2. Faithfulness-guided distillation with hard negative preference pairs and abstention.
3. Human-validated empirical evidence that the method improves rule/evidence faithfulness and reduces false rationalization.

## What Is No Longer a Main Contribution

- Benchmark construction alone.
- Reverse reconstruction alone.
- Counterfactual simulator as the central method.
- The 12,754 automatic instances as the primary claim.

## Current Hard Risks

- GPT-5.5 API key is not currently visible in the environment.
- Student training may require GPU or model downloads over the user-confirmation threshold.
- The current 160 human labels are stress-test labels, not natural explanation labels.
- The current rule/evidence verifier is too weak for a solved RuleFaith claim.

