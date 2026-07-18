from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

import torch
from huggingface_hub import model_info
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "data" / "processed" / "expect_v1_samples.jsonl"
DEFAULT_OUTPUT = ROOT / "results" / "model_predictions" / "predictions.jsonl"
DEFAULT_METADATA = ROOT / "results" / "model_predictions" / "runtime_metadata.json"
GECTOR_VERB_DICT = ROOT / "data" / "downloads" / "gector" / "verb-form-vocab.txt"


MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "gector_roberta_base": {
        "model_name": "GECToR RoBERTa base 5k",
        "model_id": "gotutiyan/gector-roberta-base-5k",
        "model_family": "sequence-to-edit",
        "license": "non-commercial only, per Hugging Face model card",
        "decoding": {
            "keep_confidence": 0.0,
            "min_error_prob": 0.0,
            "n_iteration": 5,
            "batch_size": 8,
        },
    },
    "t5_base_grammar": {
        "model_name": "T5 base grammar correction",
        "model_id": "vennify/t5-base-grammar-correction",
        "model_family": "sequence-to-sequence",
        "license": "cc-by-nc-sa-4.0, per Hugging Face model card",
        "decoding": {
            "prefix": "grammar: ",
            "num_beams": 5,
            "max_input_length": 256,
            "max_new_tokens": 128,
            "batch_size": 8,
        },
    },
    "coedit_large": {
        "model_name": "CoEdIT large instruction-tuned editor",
        "model_id": "grammarly/coedit-large",
        "model_family": "instruction-following text editor",
        "license": "cc-by-nc-4.0, per Hugging Face model card",
        "decoding": {
            "prefix": "Fix grammatical errors in this sentence: ",
            "num_beams": 4,
            "max_input_length": 256,
            "max_new_tokens": 128,
            "batch_size": 1,
        },
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def append_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def batches(rows: List[Dict[str, Any]], batch_size: int) -> Iterable[List[Dict[str, Any]]]:
    for start in range(0, len(rows), batch_size):
        yield rows[start : start + batch_size]


def hf_revision(model_id: str) -> str:
    try:
        return model_info(model_id).sha or "unknown"
    except Exception as exc:
        return f"unknown ({exc!r})"


def environment_info() -> Dict[str, Any]:
    import transformers

    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "device": "cpu",
        "cuda_available": bool(torch.cuda.is_available()),
        "mps_available": bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available()),
    }


def normalize_prediction(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())


def run_gector(samples: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    from gector.modeling import GECToR
    from gector.predict import load_verb_dict, predict
    from transformers import AutoTokenizer

    model_id = config["model_id"]
    decoding = dict(config["decoding"])
    batch_size = int(decoding["batch_size"])
    model = GECToR.from_pretrained(model_id).to("cpu")
    model.eval()
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    encode, decode = load_verb_dict(str(GECTOR_VERB_DICT))

    rows: List[Dict[str, Any]] = []
    for batch in batches(samples, batch_size):
        srcs = [item["source_text"] for item in batch]
        with torch.inference_mode(), contextlib.redirect_stdout(io.StringIO()):
            predictions = predict(
                model,
                tokenizer,
                srcs,
                encode,
                decode,
                keep_confidence=float(decoding["keep_confidence"]),
                min_error_prob=float(decoding["min_error_prob"]),
                n_iteration=int(decoding["n_iteration"]),
                batch_size=batch_size,
            )
        rows.extend(prediction_rows(batch, predictions, config))
    return rows


def run_t5(samples: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    model_id = config["model_id"]
    decoding = dict(config["decoding"])
    batch_size = int(decoding["batch_size"])
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id).to("cpu")
    model.eval()
    torch.set_num_threads(1)

    rows: List[Dict[str, Any]] = []
    for batch in batches(samples, batch_size):
        texts = [decoding["prefix"] + item["source_text"] for item in batch]
        inputs = tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=int(decoding["max_input_length"]),
        )
        with torch.inference_mode():
            output_ids = model.generate(
                **inputs,
                num_beams=int(decoding["num_beams"]),
                max_new_tokens=int(decoding["max_new_tokens"]),
                min_length=1,
            )
        predictions = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        rows.extend(prediction_rows(batch, predictions, config))
    return rows


def prediction_rows(samples: List[Dict[str, Any]], predictions: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    revision = config["model_revision"]
    rows = []
    for sample, prediction in zip(samples, predictions):
        pred = normalize_prediction(prediction)
        rows.append(
            {
                "sample_id": sample["sample_id"],
                "dataset": sample["dataset"],
                "split": sample["split"],
                "source": sample["source_text"],
                "reference": sample["target_text"],
                "prediction": pred,
                "model": config["model_name"],
                "model_key": config["model_key"],
                "model_family": config["model_family"],
                "model_id": config["model_id"],
                "model_version": revision,
                "model_license": config["license"],
                "decoding_config": config["decoding"],
                "prediction_equals_reference": pred == sample["target_text"],
                "prediction_equals_source": pred == sample["source_text"],
            }
        )
    return rows


def run_model(model_key: str, samples: List[Dict[str, Any]]) -> Dict[str, Any]:
    config = dict(MODEL_CONFIGS[model_key])
    config["model_key"] = model_key
    config["model_revision"] = hf_revision(config["model_id"])
    started = time.time()
    if model_key == "gector_roberta_base":
        rows = run_gector(samples, config)
    elif model_key in {"t5_base_grammar", "coedit_large"}:
        rows = run_t5(samples, config)
    else:
        raise ValueError(f"Unsupported model key: {model_key}")
    duration = time.time() - started
    return {
        "model_key": model_key,
        "config": config,
        "rows": rows,
        "runtime": {
            "started_at": utc_now(),
            "duration_seconds": round(duration, 3),
            "sample_count": len(samples),
            "changed_count": sum(1 for row in rows if not row["prediction_equals_source"]),
            "reference_copy_count": sum(1 for row in rows if row["prediction_equals_reference"]),
            "seconds_per_sample": round(duration / len(samples), 6) if samples else 0.0,
            "environment": environment_info(),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run public GEC models over EXPECT source sentences.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--models", nargs="+", default=["gector_roberta_base", "t5_base_grammar"])
    parser.add_argument("--sample-size", type=int, default=300)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    samples = read_jsonl(args.input)[: args.sample_size]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.overwrite and args.output.exists():
        args.output.unlink()
    all_metadata: Dict[str, Any] = {"created_at": utc_now(), "models": {}, "output": str(args.output)}
    for model_key in args.models:
        result = run_model(model_key, samples)
        append_jsonl(args.output, result["rows"])
        all_metadata["models"][model_key] = {
            "config": result["config"],
            "runtime": result["runtime"],
        }
        write_json(args.metadata, all_metadata)


if __name__ == "__main__":
    args = parse_args()
    main()
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)
