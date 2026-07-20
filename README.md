# GEC Explanation Evaluation

This repository is an executable research workspace for an AAAI-style paper on edit-level explanation evaluation for English grammatical error correction (GEC). It studies model-produced edits, not reference edits used as predictions.

## Current Status

- Main paper: `paper/main.tex`, compiled with the AAAI-27 submission style.
- Supplementary appendix: `paper/supplementary/appendix.tex`.
- Benchmark pilot: 700 model-produced edits, 12,754 automatic explanation/control instances, and 120 counterfactual variants.
- Data sources: EXPECT and JFLEG, with license notes in `docs/license_report.md` and `docs/license_summary.md`.
- Model families: GECToR, T5 grammar correction, and a small CoEdIT-large instruction-following branch.
- Human-adjudicated stress-test labels: 160 edit-explanation items labeled by two independent human annotators and resolved by a human third-party adjudicator; see `annotation/round15/annotation_v2_data_card.md`.
- Current paper framing: transitioning from human-adjudicated metric stress testing to `RuleFaith-GEC`, a verifier-guided method for generating more faithful edit-level GEC explanations.
- Active method branch: `method/rulefaith-gec`, with Qwen3-8B open-teacher pilots, verifier filtering, and method-branch preregistration.

## Main Reproduction Commands

```bash
bash experiments/run_build_data.sh
bash experiments/run_model_pilot.sh
bash experiments/run_round04_audit.sh
bash experiments/run_benchmark.sh
CF_MAX_PER_MODEL=20 CHECK_SIZE=30 BOOTSTRAP_SAMPLES=200 bash experiments/run_round09.sh
EDIT_LIMIT=80 LLM_JUDGE_LIMIT=2000 RUN_LOCAL_LLM_JUDGE=1 bash experiments/run_round11.sh
bash experiments/run_round12.sh
bash experiments/run_round15.sh
```

Method-branch work starts from:

```bash
git checkout method/rulefaith-gec
```

Open-teacher method pilots:

```bash
RULEFAITH_TEACHER_PROVIDER=open_teacher RULEFAITH_TEACHER_LIMIT=80 bash experiments/rulefaith/run_teacher_pilot.sh
HF_HUB_DISABLE_XET=1 RULEFAITH_QWEN_SHARDS=2 bash experiments/rulefaith/run_qwen_teacher_pilot.sh
HF_HUB_DISABLE_XET=1 RULEFAITH_QWEN3_SHARDS=1 bash experiments/rulefaith/run_qwen3_8b_teacher_pilot.sh
```

The Qwen2.5 branch is retained as a weak open-teacher baseline. The current local open-teacher branch uses `Qwen/Qwen3-8B` with thinking disabled. Qwen outputs are model-generated candidate explanations, not human gold, and must pass RuleFaith filtering and manual spot checks before use as training positives.

## RuleFaith Method Status

The method branch currently includes:

- A 300-edit RuleFaith method pool over EXPECT/JFLEG and GECToR/T5/CoEdIT model-produced edits.
- Human-calibrated verifier diagnostics from the Round 15 pressure-test labels.
- FLAN-T5, Qwen2.5, and Qwen3-8B open-teacher candidate pilots.
- Qwen3-8B no-thinking pilot: 160 candidates for 80 edits; conservative prefilter accepted 41, marked 63 for refinement, and rejected 56.
- Next step: verifier-guided refinement and manual spot-checking of Qwen3-8B accepted/refine candidates before SFT or preference training.

## Important Boundaries

- Automatic construction labels are separate from the Round 15 human-adjudicated stress-test labels.
- Explicit templates and raw edit strings are leakage controls.
- Reverse reconstruction measures edit correspondence/self-consistency, not internal causal faithfulness.
- Counterfactual labels come from rerunning the original GEC models.
- The 160 human labels are a stress-test sample, not a natural random sample of all GEC explanations.
- Broader learner-helpfulness claims require additional annotation and user-facing evaluation.

## Key Files

- `data/faithfulness_benchmark/`: benchmark JSON/JSONL files.
- `results/round09/`: scaled L1/L2 statistics and error analysis.
- `results/round11/`: reranking application and reward-hacking audit.
- `results/round12/paper_consistency_check.json`: paper consistency and format check.
- `results/round14/result_checksums.sha256`: checksum index for key artifacts.
- `results/human_gold/`: Round 15 human-grounded metric evaluation tables and error cases.
- `annotation/round10/`: annotation guidelines and forms.
- `annotation/round15/`: final human-adjudicated labels and annotation data card.
- `paper/rebuttal/`: rebuttal-ready responses and evidence index.
