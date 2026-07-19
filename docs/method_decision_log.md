# RuleFaith-GEC Method Decision Log

| Date | Decision | Rationale | Risk |
|---|---|---|---|
| 2026-07-19 | Create `method/rulefaith-gec` from latest `main`. | Preserve the Round 15 stress-test paper while developing a method paper. | Later merge may need careful separation of benchmark and method claims. |
| 2026-07-19 | Treat Round 15 labels as verifier calibration and stress-test evaluation, not the final natural-explanation benchmark. | The set is human-adjudicated but intentionally adversarial and template-heavy. | Method claims need balanced natural explanations. |
| 2026-07-19 | Pre-register H1--H6 before teacher generation and method results. | Prevent after-the-fact metric or claim selection. | Hypotheses may fail and force a method pivot. |
| 2026-07-19 | Build RuleFaith edit pool from existing 700 model-produced benchmark edits rather than rerunning old data pipelines. | The user explicitly requested not to rebuild or expand the old benchmark; existing edits already cover EXPECT/JFLEG and three corrector families. | CoEdIT remains smaller, and the pool inherits JFLEG primary-reference limitations. |
| 2026-07-19 | Exclude obvious detokenization artifacts but keep a small non-artifact ORTH/PUNCT subset. | Method training should focus on substantive edits while still allowing orthography/punctuation analysis. | Punctuation coverage is low and should be reported as a subgroup, not a main claim. |
