# Research Materials Summary

Last updated: 2026-07-18

## Opening Report

Source file: `王千予-华东师范大学研究生学位论文开题报告登记表-中文统一版.pdf`

The opening report frames a broader master's thesis on GEC robustness and explainability. For this AAAI paper, the relevant subset is the edit-level explainability branch:

- GEC systems may produce unstable, wrong, missed, or overcorrected edits.
- Explanations should correspond to specific edits, including location, direction, error type, and grammatical rationale.
- The report proposes checking whether explanations can be mapped back to the relevant edit.
- The thesis-level robustness branch around CoCoGEC is useful background but is not the main scope of the independent AAAI paper unless later evidence suggests combining both branches.

## Local AAAI Template

The AAAI 2027 author kit is available under `AuthorKit27/`. The paper project uses copied `aaai2027.sty` and `aaai2027.bst` under `paper/`.

## Local Data and Code

At startup, no real GEC dataset, model output, explanation dataset, experiment result, README, or existing codebase was found in the working directory. The current implementation therefore creates executable scaffolding and a toy sanity-check dataset only.

## Safety Notes

The current directory is not a Git repository. Work is being added in new project directories (`paper/`, `experiments/`, `docs/`, `data/`, `results/`, `logs/`) to avoid overwriting user material.

