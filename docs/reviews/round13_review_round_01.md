# Round 13 Review Round 01

| Role | Summary | Strengths | Weaknesses | Questions | Missing Experiments | Novelty Concerns | Soundness Concerns | Reproducibility Concerns | Ethical Concerns | Score | Confidence |
|---|---|---|---|---|---|---|---|---|---|---:|---:|
| GEC expert | Useful edit-level diagnostic for GEC explanations. | Real GEC models, ERRANT, behavior labels. | JFLEG uses reference 0; CoEdIT small. | How often are alternatives valid? | Multi-reference accept-if-any. | CLEME2.0/EXCGEC close. | ERRANT boundary noise. | Good logs. | Learner harm if automatic labels are overused. | 5 | 4 |
| Explainability expert | Clear separation of correspondence and behavior. | Avoids claiming reconstruction equals faithfulness. | Title sounds too strong. | Are explanations natural enough? | Human preference. | General simulatability prior work. | Automatic labels dominate. | Good code paths. | Need stronger caveat. | 5 | 4 |
| Faithfulness expert | Counterfactual framing is promising. | Reruns original models. | L2 simulator is weak. | Does L2 test causes or only behavior? | Stronger simulator and human labels. | Hase/Bansal and faithfulness surveys must be centered. | Counterfactual validity uncertain. | Sufficient for pilot. | Avoid causal language. | 4 | 5 |
| Evaluation expert | Metrics are broad and well separated. | Bootstrap CIs and negative controls. | Many numbers from synthetic labels. | Which metric should reviewers trust? | Human correlation. | Benchmark contribution could be enough if framed. | Reward hacking under reranking. | Strong traceability. | No fabricated labels. | 5 | 4 |
| Counterfactual learning expert | Actual reruns are the right label source. | Keeps competing edits separate. | Variant generator is heuristic. | Are rule-relevant variants valid? | Validity audit. | COCOGEC is close. | Model instability may dominate. | Rerun logs exist. | None beyond caveats. | 4 | 4 |
| Educational NLP expert | Learner-facing caution is valuable. | Separates helpfulness from faithfulness. | No learner/user study. | Would selected explanations help students? | Human helpfulness annotation. | GEE already studies explanations. | Automatic rules may be simplistic. | Annotation package ready. | Must avoid deploying as feedback. | 4 | 4 |
| Reproducibility reviewer | Project is unusually traceable. | Git commits, scripts, checks, licenses. | Some assets are generated LaTeX rather than plots. | Can others download all models? | Artifact checksum. | Not applicable. | CPU-only CoEdIT small. | Strong. | License restrictions clear. | 6 | 5 |
| Skeptical Reviewer 2 | Interesting but oversold. | Negative results are honest. | No human labels; weak L2; template artifacts. | Why AAAI without human eval? | Real annotations. | May be incremental to GEE/EXCGEC/COCOGEC. | Automatic faithfulness labels questionable. | Good, but bulky. | Potential learner misdirection. | 3 | 4 |
| Area Chair | Borderline workshop-to-conference unless claims are narrowed. | Strong engineering and transparent limitations. | Main contribution must be benchmark/diagnostic, not solved method. | What is the final claim? | Human labels or narrower claim. | Needs careful related work. | Avoid causal/internal faithfulness. | Good package. | Acceptable with caveats. | 4 | 4 |

## P0 Actions After Round 01

- Changed title from promising faithful explanations to evaluating explanations.
- Added Introduction sentence stating this is not a new explanation generator.
- Strengthened related-work boundary against EXCGEC, GEE, Prompt Insertion, and COCOGEC.
- Preserved no-human-gold caveat in Abstract, Introduction, Results, Human Evaluation, Limitations, and Conclusion.

## P1 Actions Queued

- Add supplementary note on counterfactual validity and pilot scope.
- Add artifact/rebuttal evidence for reproducibility and license constraints in Round 14.
