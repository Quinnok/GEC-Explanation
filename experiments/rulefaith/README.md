# RuleFaith Experiments

Round 16 initializes the method branch. Later rounds add edit-pool construction, teacher generation, verifier calibration, filtering, training, and evaluation scripts here.

Qwen small teacher pilot:

```bash
HF_HUB_DISABLE_XET=1 RULEFAITH_QWEN_SHARDS=2 bash experiments/rulefaith/run_qwen_teacher_pilot.sh
```

Set `RULEFAITH_QWEN_SHARDS=1` for a single process, or increase it after the model is cached. First download is not parallelized to avoid corrupting the Hugging Face cache.

Qwen3-8B teacher pilot:

```bash
HF_HUB_DISABLE_XET=1 RULEFAITH_QWEN3_SHARDS=1 bash experiments/rulefaith/run_qwen3_8b_teacher_pilot.sh
```

Qwen3 thinking mode is disabled in the generator so the output remains strict JSON without hidden reasoning blocks.
