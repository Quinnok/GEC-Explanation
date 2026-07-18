# AAAI-27 Requirements Check

Checked on 2026-07-18 from official AAAI pages.

## Official Sources

- AAAI-27 main technical track call: https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/
- AAAI-27 submission instructions: https://aaai.org/conference/aaai/aaai-27/submission-instructions/
- AAAI-27 supplementary material instructions: https://aaai.org/conference/aaai/aaai-27/supplementary-material/
- AAAI-27 review process: https://aaai.org/conference/aaai/aaai-27/review-process/
- Local author kit: `AuthorKit27/` and copied style files under `paper/`.

## Verified Requirements

| Requirement | Official Requirement | Local Status |
|---|---|---|
| Template | Use AAAI-27 author kit and AAAI two-column style. | `paper/main.tex` uses `\usepackage[submission]{aaai2027}`. |
| Page limit | Main track submissions are limited to 7 pages of main content, with maximum total length 9 pages; pages beyond 7 are reserved exclusively for references. | `paper/main.pdf` is 8 pages after Round 13; references begin on page 7, so the draft is within the 9-page total limit. |
| Anonymous review | Submissions must remove author and affiliation information for double-blind review. | `paper/main.tex` uses `Anonymous Submission` and empty affiliations. |
| Abstract/full paper deadlines | Abstracts due July 21, 2026; full papers due July 28, 2026, both 11:59 PM UTC-12. | Recorded for planning; no submission performed. |
| Supplementary material/code | Supplementary material and code due July 31, 2026, 11:59 PM UTC-12; reviewers are not required to review supplementary material. | `paper/supplementary/appendix.pdf` compiles and should contain nonessential extra material. |
| Reproducibility checklist | Checklist from author kit must be completed and uploaded separately at submission. | Author kit includes `AuthorKit27/ReproducibilityChecklist.tex`; Round 14 should fill it. |
| Reproducibility evidence | Code/data needed to reproduce reported results should be provided at submission; "will release later" is not evidence. | Reproduction commands and result files are present locally; Round 14 will package checksums and artifact instructions. |
| Ethics | Authors and reviewers must follow AAAI publications ethics and code of conduct. | Main paper contains `Ethics and Broader Impact`; no fabricated references, results, or human labels are used. |
| Multiple submission policy | AAAI-27 does not allow simultaneous or overlapping archival submissions that are not distinct contributions. | No local evidence of another archival submission; keep monitoring before submission. |

## Local Consistency Result

`results/round12/paper_consistency_check.json` reports:

- main PDF pages: 8
- bibliography starts on page: 7
- appendix PDF pages: 4
- generated asset count: 11
- result-pending placeholders: 0
- main LaTeX log clean: true
- appendix LaTeX log clean: true
- anonymous submission: true
- human annotation status: `blocked_no_human_annotation`

## Risk

The paper is at the main-content limit and uses a second reference page. Further revisions should move detail to the supplementary appendix or shorten existing prose.
