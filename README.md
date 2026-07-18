# Counterfactual Edit Simulatability for GEC Explanations

This repository is an executable research workspace for an AAAI-style paper on edit-level explanation evaluation for English grammatical error correction (GEC). It studies model-produced edits, not reference edits used as predictions.

## Current Status

- Main paper: `paper/main.tex`, compiled with the AAAI-27 submission style.
- Supplementary appendix: `paper/supplementary/appendix.tex`.
- Benchmark pilot: 700 model-produced edits, 12,754 automatic explanation/control instances, and 120 counterfactual variants.
- Data sources: EXPECT and JFLEG, with license notes in `docs/license_report.md` and `docs/license_summary.md`.
- Model families: GECToR, T5 grammar correction, and a small CoEdIT-large instruction-following branch.
- Human labels: 0. The annotation package exists, but double-human annotation is blocked until real annotators complete it.

## Main Reproduction Commands

```bash
bash experiments/run_build_data.sh
bash experiments/run_model_pilot.sh
bash experiments/run_round04_audit.sh
bash experiments/run_benchmark.sh
CF_MAX_PER_MODEL=20 CHECK_SIZE=30 BOOTSTRAP_SAMPLES=200 bash experiments/run_round09.sh
EDIT_LIMIT=80 LLM_JUDGE_LIMIT=2000 RUN_LOCAL_LLM_JUDGE=1 bash experiments/run_round11.sh
bash experiments/run_round12.sh
```

## Important Boundaries

- Automatic labels are not human gold labels.
- Explicit templates and raw edit strings are leakage controls.
- Reverse reconstruction measures edit correspondence/self-consistency, not internal causal faithfulness.
- Counterfactual labels come from rerunning the original GEC models.
- Human-faithfulness and learner-helpfulness claims require real double annotation.

## Key Files

- `data/faithfulness_benchmark/`: benchmark JSON/JSONL files.
- `results/round09/`: scaled L1/L2 statistics and error analysis.
- `results/round11/`: reranking application and reward-hacking audit.
- `results/round12/paper_consistency_check.json`: paper consistency and format check.
- `results/round14/result_checksums.sha256`: checksum index for key artifacts.
- `annotation/round10/`: annotation guidelines and forms.
- `paper/rebuttal/`: rebuttal-ready responses and evidence index.
