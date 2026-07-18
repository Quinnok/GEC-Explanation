# Open Issues

Last updated: 2026-07-18

## P0

| Issue | Impact | Required Evidence | Proposed Resolution | Status |
|---|---|---|---|---|
| Novelty against reverse reconstruction, simulatability, and rationale faithfulness is only partially verified. | The paper may overclaim contribution. | Focused literature review plus final related-work pass before submission. | Round 05 built a 50-paper literature package and identified P0 threats from GEE, Prompt Insertion, EXCGEC, CLEME2.0, COCOGEC, Hase and Bansal, Jacovi and Goldberg, Lyu et al., and Parcalabescu and Frank; do not use "first" or "novel" yet. | Open |
| Reconstruction may copy explicit edit text. | Core method could be invalid. | Leakage-control ablations on model-produced edits and natural-language explanations. | Round 02 showed explicit/raw templates are leakage upper controls; Round 03 moved to model-produced edits. | Open |
| No real model-produced edit pilot exists locally. | No empirical claim can be made about model behavior. | Real GEC predictions, source-prediction edits, and behavior labels. | Built 600 predictions and 1707 model-produced edits from two public GEC models. | Closed for pilot |
| Human agreement is unavailable. | Automatic metric may not be credible. | Human-labeled faithfulness sample. | Design annotation protocol and request user decision before manual annotation. | Open |
| No verified human natural-language explanation source is available for EXPECT model-produced edits. | Main experiment cannot claim human gold explanation faithfulness. | License-clear explanation dataset, annotation protocol, or stronger open-source generation plus filtering. | EXPECT audit found evidence indices/error types but no free-text explanations; FLAN candidates are not gold. | Open |
| Counterfactual validity is unproven. | The new main method could measure perturbation noise or model instability rather than explanation faithfulness. | Counterfactual audit, rerun labels from original GEC models, invalid-variant filtering, and simulator confusion analysis. | Round 06 selected Counterfactual Edit Simulatability; implementation and audits are pending Round 08/09. | Open |
| Round 07 benchmark labels are automatic and template-heavy. | Reviewers may reject claims that conflate automatic construction with human faithfulness judgments. | Human annotation packet, inter-annotator agreement, and metrics reported separately by explanation type. | Round 07 generated 700 edits and 12,754 explanation/control instances with `human_gold_count=0`; data card explicitly forbids human-gold claims. | Open |

## P1

| Issue | Impact | Required Evidence | Proposed Resolution | Status |
|---|---|---|---|---|
| Edit extraction currently uses a simple token diff, not ERRANT. | Error types and edit boundaries may be weak. | Comparison to ERRANT. | ERRANT integrated; token diff comparison stored in `results/edit_extraction/token_diff_vs_errant.json`. | Closed for pilot |
| Literature matrix is incomplete. | Related work may miss closest baselines. | Verified entries for faithfulness/simulatability and GEC explanation work. | Round 05 generated 50 cards plus CSV/Markdown/XLSX matrices and novelty-threat docs. Final PDF-level citation pass still needed before submission. | Closed for research planning |
| Local TeX compiler is unavailable. | Cannot verify final AAAI PDF rendering locally. | Installed `pdflatex`, `latexmk`, or `tectonic`. | Installed local TinyTeX and compiled `paper/main.tex`. | Closed |
| T5 predictions create many ERRANT `R:ORTH` overcorrections from spacing and punctuation normalization. | Behavior statistics may overstate substantive overcorrection. | Detokenization normalization ablation and manual review. | Round 04 normalization ablation complete; raw and normalized/substantive views must both be reported. | Closed for pilot |
| ERRANT alignment has ambiguous cases. | Some wrong/over/missed labels may be noisy. | Alignment failure report and targeted manual review. | Round 04 stable alignment audit complete; exact-only comparison shows 90 non-exact related edits recovered as wrong corrections. | Open |
| Paper framing still contains old Round 02/Round 03 result tables. | Reviewers may misunderstand leakage-control results as the main experiment. | Main text must clearly mark these as leakage controls and replace or supplement with model-edit benchmark results. | Round 06 revised title/method and softened results wording; full Results rewrite awaits Round 09 experiments. | Open |
| JFLEG multi-reference equivalence is only partially used. | ERRANT labels may mark a valid alternative correction as overcorrection/wrong because Round 07 uses `ref0` for primary extraction. | Multi-reference ERRANT alignment or accept-if-any-reference matching. | All four JFLEG references are retained in `data/processed/jfleg_v1_samples.jsonl`; Round 08/09 should extend alignment. | Open |
| Predicted target strings repeat across splits. | Reconstructors and classifiers could learn common lexical shortcuts, especially punctuation/articles. | Target-masked evaluation, lexical-ablation splits, and grouped reporting by operation/error type. | `data/faithfulness_benchmark/leakage_audit.json` found 32 target strings crossing train/dev/test splits. | Open |
| CoEdIT is only a small instruction-following pilot. | Third model-family evidence is less stable than GECToR/T5 evidence. | Larger CoEdIT run or smaller instruction-following substitute, if CPU budget permits. | Round 07 ran 20 EXPECT sources, yielding 122 predicted edits and 8 missed edits. | Open |
