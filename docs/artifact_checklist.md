# Artifact Checklist

## Included

- Source code for data processing, edit extraction, benchmark construction, counterfactuals, baselines, reranking, paper asset generation, and checks.
- Versioned pilot benchmark files under `data/faithfulness_benchmark/`.
- Results for Round 09, Round 10, Round 11, and Round 12.
- Annotation package under `annotation/round10/`.
- Main paper source and supplementary appendix source.
- Result checksums in `results/round14/result_checksums.sha256`.
- Reproduction commands in `docs/reproduction_commands.md`.
- Model/data download notes in `docs/model_data_downloads.md`.
- License summary in `docs/license_summary.md`.

## Excluded

- Downloaded raw repositories under `data/downloads/`.
- Local Python environments and TeX installation.
- Hugging Face model weights and caches.
- LaTeX build products and PDFs, which can be regenerated locally.

## Known Blockers

- No double-human annotation has been completed.
- No human-faithfulness correlation or learner-helpfulness result can be claimed.
- CoEdIT evidence is a small CPU pilot branch.
- JFLEG uses reference 0 for primary ERRANT extraction in this pilot.

## Submission Checklist

- Recheck AAAI-27 official requirements before upload.
- Run `bash experiments/run_round12.sh`.
- Run unit tests.
- Verify checksums or regenerate `results/round14/result_checksums.sha256` after any file changes.
- Fill the AAAI reproducibility checklist from `AuthorKit27/ReproducibilityChecklist.tex`.
- Include code/data supplement at submission; do not rely on "will release after acceptance".
