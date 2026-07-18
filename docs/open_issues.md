# Open Issues

Last updated: 2026-07-18

## P0

| Issue | Impact | Required Evidence | Proposed Resolution | Status |
|---|---|---|---|---|
| Novelty against reverse reconstruction, simulatability, and rationale faithfulness is only partially verified. | The paper may overclaim contribution. | Focused literature review plus final related-work pass before submission. | Current pass found close GEC explanation and simulatability work; do not use "first" or "novel" yet. | Open |
| Reconstruction may copy explicit edit text. | Core method could be invalid. | Leakage-control ablations on model-produced edits and natural-language explanations. | Round 02 showed explicit/raw templates are leakage upper controls; Round 03 moved to model-produced edits. | Open |
| No real model-produced edit pilot exists locally. | No empirical claim can be made about model behavior. | Real GEC predictions, source-prediction edits, and behavior labels. | Built 600 predictions and 1707 model-produced edits from two public GEC models. | Closed for pilot |
| Human agreement is unavailable. | Automatic metric may not be credible. | Human-labeled faithfulness sample. | Design annotation protocol and request user decision before manual annotation. | Open |
| No verified human natural-language explanation source is available for EXPECT model-produced edits. | Main experiment cannot claim human gold explanation faithfulness. | License-clear explanation dataset, annotation protocol, or stronger open-source generation plus filtering. | EXPECT audit found evidence indices/error types but no free-text explanations; FLAN candidates are not gold. | Open |

## P1

| Issue | Impact | Required Evidence | Proposed Resolution | Status |
|---|---|---|---|---|
| Edit extraction currently uses a simple token diff, not ERRANT. | Error types and edit boundaries may be weak. | Comparison to ERRANT. | ERRANT integrated; token diff comparison stored in `results/edit_extraction/token_diff_vs_errant.json`. | Closed for pilot |
| Literature matrix is incomplete. | Related work may miss closest baselines. | Verified entries for faithfulness/simulatability and GEC explanation work. | Round 03 added a focused pass; continue before final claims. | Open |
| Local TeX compiler is unavailable. | Cannot verify final AAAI PDF rendering locally. | Installed `pdflatex`, `latexmk`, or `tectonic`. | Installed local TinyTeX and compiled `paper/main.tex`. | Closed |
| T5 predictions create many ERRANT `R:ORTH` overcorrections from spacing and punctuation normalization. | Behavior statistics may overstate substantive overcorrection. | Detokenization normalization ablation and manual review. | Round 04 normalization ablation complete; raw and normalized/substantive views must both be reported. | Closed for pilot |
| ERRANT alignment has ambiguous cases. | Some wrong/over/missed labels may be noisy. | Alignment failure report and targeted manual review. | Round 04 stable alignment audit complete; exact-only comparison shows 90 non-exact related edits recovered as wrong corrections. | Open |
