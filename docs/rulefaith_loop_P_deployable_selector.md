# RuleFaith Loop P: Deployable Ready-Pool Selector

## Status

- Loop ID: P
- Current bottleneck: previous selection result included a pseudo-validator upper bound but no deployable selector.
- Hypothesis: a fixed RuleFaith feature scorer using edit alignment, rule signal, source evidence, leakage, specificity, and validity-risk features can improve over first-candidate and confidence heuristics without reading pseudo labels.
- Required evidence: candidate-level scores, group-level top-1 selection, selective abstention, and pairwise ranking diagnostics against Codex/AI pseudo-validation for internal triage.
- Success criterion: scorer is reproducible, does not use `validator_*` fields for scoring, and improves over first/highest-confidence baselines without hiding pseudo-label limitations.

## Results

- score bucket counts: `{'accept': 28, 'refine': 9, 'reject': 4}`
- top-1 selection: `{'strategy': 'RuleFaith deployable score top-1', 'edit_groups': 23, 'covered_groups': 23, 'coverage': 1.0, 'accept_selected': 9, 'refine_selected': 8, 'reject_selected': 6, 'accept_rate': 0.3913, 'non_reject_rate': 0.7391, 'mean_utility': 0.5652}`
- selective selection: `{'strategy': 'RuleFaith deployable score selective', 'edit_groups': 23, 'covered_groups': 18, 'coverage': 0.7826, 'accept_selected': 7, 'refine_selected': 7, 'reject_selected': 4, 'accept_rate': 0.3889, 'non_reject_rate': 0.7778, 'mean_utility': 0.5833}`
- pairwise accuracy: `0.5` over `4` comparable pairs
- hypothesis status: `partially_supported_for_first_and_confidence_baselines_but_not_ready`
- comparison boundary: top-1 improves over first/highest-confidence selectors from Loop O, but remains below the rule-grounded simple selector and should be revised before paper-quality claims.

## Interpretation

The deployable scorer is a method-pilot diagnostic. It can rank and abstain without reading pseudo labels, but the evaluation labels are still Codex/AI pseudo-validation. The current scorer is not strong enough to serve as a final selector: it beats first-candidate and highest-confidence heuristics but does not beat the rule-grounded candidate baseline, and its selective mode mostly improves non-reject rate rather than accept rate. This result is useful for engineering the RuleFaith selector and deciding which candidates require real-human validation; it is not final human evidence.

## Artifacts

- `results/rulefaith/rulefaith_ready_candidate_scores.csv`
- `results/rulefaith/rulefaith_ready_selector_metrics.json`
- `results/rulefaith/rulefaith_ready_selector_metrics.csv`
- `results/rulefaith/rulefaith_ready_selector_cases.md`
- `results/paper_assets/rulefaith_ready_selector_metrics.tex`

## Provenance

- generated at: `2026-07-21T11:31:09.587993+00:00`
- git commit at generation time: `a2c0301`

## Next Highest-Priority Loop

Use this scorer to construct a blinded natural-explanation comparison package; do not tune thresholds on the pseudo-validation labels.
