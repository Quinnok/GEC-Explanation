# Open Issues

Last updated: 2026-07-18

## P0

| Issue | Impact | Required Evidence | Proposed Resolution | Status |
|---|---|---|---|---|
| Novelty against reverse reconstruction, simulatability, and rationale faithfulness is unverified. | The paper may not have a distinct contribution. | Focused literature review. | Search and verify closest work before finalizing claims. | Open |
| Reconstruction may copy explicit edit text. | Core method could be invalid. | Leakage-control ablations. | Compare explicit, implicit, masked, rule-only, source-only, explanation-only, and raw-edit settings. | Open |
| No real pilot data exists locally. | No empirical claim can be made. | Real GEC predictions and explanations. | Build or download data after checking licenses and size. | Open |
| Human agreement is unavailable. | Automatic metric may not be credible. | Human-labeled faithfulness sample. | Design annotation protocol and request user decision before manual annotation. | Open |

## P1

| Issue | Impact | Required Evidence | Proposed Resolution | Status |
|---|---|---|---|---|
| Edit extraction currently uses a simple token diff, not ERRANT. | Error types and edit boundaries may be weak. | Comparison to ERRANT. | Add ERRANT integration or document fallback. | Open |
| Literature matrix is incomplete. | Related work may miss closest baselines. | Verified entries for faithfulness/simulatability and GEC explanation work. | Continue literature pass. | Open |
| Local TeX compiler is unavailable. | Cannot verify final AAAI PDF rendering locally. | Installed `pdflatex`, `latexmk`, or `tectonic`. | Install or use another machine with TeX; then compile `paper/main.tex`. | Open |
