# Method Round 17

## Status

Round 17 substantive edit pool complete.

## Main Objective

Build a 300-edit pool for natural teacher explanation generation and RuleFaith-GEC method development.

## Highest Risk

The pool still contains common target strings crossing splits, so later target-masked and leakage-aware evaluation remains mandatory.

## Git Commit

Recorded in Git history as `Round 17 substantive edit pool`.

## Data Version

Input: `data/faithfulness_benchmark/edit_records.jsonl`.

Outputs:

- `data/rulefaith/edit_pool.jsonl`
- `data/rulefaith/train_edits.jsonl`
- `data/rulefaith/dev_edits.jsonl`
- `data/rulefaith/test_edits.jsonl`

## Model Version

No new model calls. The pool reuses existing model-produced edits from GECToR, T5, and CoEdIT artifacts.

## Work Completed

- Implemented `experiments/rulefaith/build_edit_pool.py`.
- Added frozen config `configs/rulefaith/edit_pool.yaml`.
- Selected 300 substantive edits.
- Excluded obvious detokenization, punctuation-spacing, and case/whitespace-only artifacts.
- Preserved model-family, dataset, behavior, operation, and error-category coverage.
- Built source-level train/dev/test splits.
- Ran source-cross-split, target-cross-split, and near-duplicate audits.
- Wrote `docs/rulefaith_edit_pool_card.md`.

## Files Created or Modified

- `configs/rulefaith/edit_pool.yaml`
- `experiments/rulefaith/build_edit_pool.py`
- `data/rulefaith/edit_pool.jsonl`
- `data/rulefaith/train_edits.jsonl`
- `data/rulefaith/dev_edits.jsonl`
- `data/rulefaith/test_edits.jsonl`
- `results/rulefaith/edit_pool_stats.json`
- `results/rulefaith/edit_pool_audit.md`
- `docs/rulefaith_edit_pool_card.md`

## Commands Executed

- `.venv311/bin/python -m py_compile experiments/rulefaith/build_edit_pool.py`
- `.venv311/bin/python experiments/rulefaith/build_edit_pool.py`
- `wc -l data/rulefaith/*.jsonl`

## Verified Results

- Selected edits: 300.
- Model counts: GECToR 120, T5 120, CoEdIT 60.
- Dataset counts: EXPECT 165, JFLEG 135.
- Behavior counts: correct 77, wrong 72, overcorrection 151.
- Operation counts: replace 237, insert 30, delete 33.
- Source keys crossing splits: 0.
- Near-duplicate source pairs at >=0.92 similarity: 0.
- Target strings crossing splits: 13.

## Failed Runs

None.

## Scientific Interpretation

The project now has a method-oriented edit pool suitable for natural teacher generation. It is more appropriate for RuleFaith-GEC than the older template-heavy stress-test pool, but target repetition and JFLEG multi-reference limitations remain.

## Claim-Evidence Updates

Round 17 supports the claim that a method-ready pool can be built from existing model-produced edits without rebuilding the old benchmark.

## Open Issues

- 13 target strings cross train/dev/test splits.
- CoEdIT remains smaller than the other model families.
- JFLEG multi-reference equivalence remains partially handled.

## Next Internal Action

Round 18: design GPT-5.5 and open-teacher prompt/configs, implement teacher-candidate generation with budget controls, and attempt the 80-edit pilot if API credentials are present.

