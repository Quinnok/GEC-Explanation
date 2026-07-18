# Round 01: Startup Framing

Last updated: 2026-07-18

## Current Stage

Phase A preparation: formulate the research problem and identify what must be verified before claiming novelty.

## Highest-priority Question

Does the proposed reverse edit reconstruction framing define a distinct and testable research problem for edit-level faithfulness of GEC explanations?

## Evidence Collected

- Research seed defines a model-produced GEC edit `e`, an explanation `r`, and a reverse reconstructor `R(x, r)`.
- The current argument is conceptual only.
- No literature has been verified yet in this workspace.
- AAAI 2027 author kit is available locally at `/Users/bytedance/Documents/GEC可解释性/AuthorKit27`.

## Analysis

One-sentence research question: Can the faithfulness of a natural-language explanation for a GEC edit be evaluated by testing whether the edit can be reconstructed from the original sentence and the explanation?

Conditional assessment: this could become an independent AAAI paper only if the literature check shows a real gap, leakage controls are convincing, and human evaluation demonstrates that reconstruction-based scores correlate with edit-faithfulness judgments. Without those three pieces, the idea risks being seen as a useful diagnostic or workshop-level evaluation protocol rather than a full AAAI contribution.

Three possible paper positionings:

1. Evaluation task paper: define and benchmark edit-level faithfulness for GEC explanations.
2. Method paper: propose reverse edit reconstruction and reconstruction-based reranking.
3. Diagnostic analysis paper: characterize edit-level explanation failures in GEC models.

Five most severe risks:

1. Prior work may already cover the core idea under simulatability, rationale faithfulness, inverse reconstruction, or explanation evaluation.
2. The reconstructor may exploit explicit target-edit leakage instead of using genuine explanatory content.
3. Reconstruction may measure information sufficiency but not faithfulness, grammatical validity, or helpfulness.
4. Automatically extracted edits and automatically generated explanations may introduce enough noise to invalidate conclusions.
5. Strong baselines such as LLM-as-a-judge or structured extraction may match or outperform reconstruction.

## Proposed Decision

Proceed, but treat the project as an unverified hypothesis. The first paper framing should be evaluation/diagnostic rather than claiming a new explanation generation method.

## Risks

All novelty, effectiveness, and generality claims are currently unverified. Do not state "first", "novel", "outperforms", or "faithfully evaluates" until the literature and experiments support them.

## Updated Research Artifacts

- `docs/project_brief.md`
- `docs/claim_evidence_matrix.md`
- `docs/literature_matrix.md`
- `docs/experiment_plan.md`
- `docs/open_issues.md`

## Next Single Action

Run a focused literature verification pass on reverse reconstruction, simulatability, and edit-level explanation evaluation for GEC and closely related NLP tasks.
