# Reproduction Commands

Run from the repository root.

## Environment

```bash
python3.12 -m venv .venv311
.venv311/bin/python -m pip install -r requirements.txt
.venv311/bin/python -m spacy download en_core_web_sm
```

The local run used Python 3.12.13 and a CPU PyTorch wheel. Exact versions are listed in `requirements.txt` and `environment.yml`.

## Data and Model Pilot

```bash
bash experiments/run_build_data.sh
bash experiments/run_model_pilot.sh
bash experiments/run_round04_audit.sh
bash experiments/run_benchmark.sh
```

## Main Automatic Experiments

```bash
CF_MAX_PER_MODEL=20 CHECK_SIZE=30 BOOTSTRAP_SAMPLES=200 bash experiments/run_round09.sh
EDIT_LIMIT=80 LLM_JUDGE_LIMIT=2000 RUN_LOCAL_LLM_JUDGE=1 bash experiments/run_round11.sh
```

## Paper Assets and Compilation

```bash
bash experiments/run_round12.sh
```

This regenerates paper assets, compiles `paper/main.tex`, compiles `paper/supplementary/appendix.tex`, and writes `results/round12/paper_consistency_check.json`.

## Verification

```bash
.venv311/bin/python -m unittest discover -s experiments/tests
.venv311/bin/python -m py_compile experiments/src/build_paper_assets.py experiments/src/check_paper_consistency.py
shasum -a 256 -c results/round14/result_checksums.sha256
```

The checksum command verifies tracked key artifacts against the current Round 14 index.
