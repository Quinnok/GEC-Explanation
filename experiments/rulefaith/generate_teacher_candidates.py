from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "data" / "rulefaith" / "edit_pool.jsonl"
DEFAULT_OUTPUT = ROOT / "data" / "rulefaith" / "teacher_candidates_pilot.jsonl"
DEFAULT_STATS = ROOT / "results" / "rulefaith" / "teacher_generation_stats.json"
DEFAULT_PARSE_FAILURES = ROOT / "results" / "rulefaith" / "teacher_parse_failures.jsonl"
DEFAULT_RAW_DIR = ROOT / "results" / "rulefaith" / "teacher_raw_responses"
GPT_CONFIG = ROOT / "configs" / "rulefaith" / "gpt55_teacher.yaml"
OPEN_CONFIG = ROOT / "configs" / "rulefaith" / "open_teacher.yaml"
QWEN_CONFIG = ROOT / "configs" / "rulefaith" / "qwen_small_teacher.yaml"

VALID_EDIT_VALIDITY = {"valid", "acceptable_alternative", "invalid", "stylistic", "uncertain"}
OPENAI_DOCS_RESPONSES_CREATE = "https://developers.openai.com/api/reference/resources/responses/methods/create"


RULEFAITH_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "edit_description",
        "edit_validity",
        "rule_id",
        "rule_text",
        "evidence_spans",
        "applicability_conditions",
        "rationale",
        "confidence",
        "abstain",
        "abstain_reason",
    ],
    "properties": {
        "edit_description": {"type": "string"},
        "edit_validity": {
            "type": "string",
            "enum": ["valid", "acceptable_alternative", "invalid", "stylistic", "uncertain"],
        },
        "rule_id": {"type": "string"},
        "rule_text": {"type": "string"},
        "evidence_spans": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["text", "start", "end", "role"],
                "properties": {
                    "text": {"type": "string"},
                    "start": {"type": "integer"},
                    "end": {"type": "integer"},
                    "role": {"type": "string"},
                },
            },
        },
        "applicability_conditions": {"type": "array", "items": {"type": "string"}},
        "rationale": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "abstain": {"type": "boolean"},
        "abstain_reason": {"type": "string"},
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_yaml(path: Path) -> Dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}


def stable_hash(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:12], 16)


def normalized_edit(row: Dict[str, Any]) -> Dict[str, Any]:
    edit = row.get("predicted_edit") or {}
    return {
        "operation": edit.get("operation") or row.get("operation") or "",
        "start": edit.get("start", row.get("edit_start")),
        "end": edit.get("end", row.get("edit_end")),
        "source_text": edit.get("source_text", row.get("source_text", "")),
        "target_text": edit.get("target_text", row.get("target_text", "")),
        "error_type": edit.get("error_type", row.get("error_type", "")),
    }


def select_pilot_rows(rows: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    if limit <= 0:
        return []
    sorted_rows = sorted(rows, key=lambda row: (row.get("model_key", ""), stable_hash(row.get("rulefaith_pool_id", row.get("edit_id", "")))))
    by_model: Dict[str, List[Dict[str, Any]]] = {}
    for row in sorted_rows:
        by_model.setdefault(row.get("model_key", "unknown"), []).append(row)
    model_keys = sorted(by_model)
    selected: List[Dict[str, Any]] = []
    selected_ids = set()
    per_model = max(1, limit // max(1, len(model_keys)))
    for model_key in model_keys:
        for row in by_model[model_key][:per_model]:
            selected.append(row)
            selected_ids.add(row.get("rulefaith_pool_id"))
    for row in sorted_rows:
        if len(selected) >= limit:
            break
        if row.get("rulefaith_pool_id") not in selected_ids:
            selected.append(row)
            selected_ids.add(row.get("rulefaith_pool_id"))
    return selected[:limit]


def system_prompt() -> str:
    return (
        "You are an expert English grammarian generating structured explanations for grammatical error correction model edits. "
        "Explain only the displayed atomic MODEL_EDIT. Do not infer hidden neural reasoning. "
        "Do not assume the edit is correct; honestly mark invalid, stylistic, optional, or uncertain edits. "
        "Return strict JSON only."
    )


def user_prompt(row: Dict[str, Any], candidate_type: str) -> str:
    edit = normalized_edit(row)
    return (
        f"SOURCE:\n{row.get('source', '')}\n\n"
        f"MODEL_PREDICTION:\n{row.get('prediction', '')}\n\n"
        "MODEL_EDIT:\n"
        f"operation={edit['operation']}\n"
        f"span=[{edit['start']},{edit['end']})\n"
        f"source_text={edit['source_text']}\n"
        f"target_text={edit['target_text']}\n\n"
        f"CANDIDATE_TYPE:\n{candidate_type}\n\n"
        "Write one explanation candidate as JSON with keys: edit_description, edit_validity, rule_id, rule_text, "
        "evidence_spans, applicability_conditions, rationale, confidence, abstain, abstain_reason. "
        "The rationale should be specific to the edit and should not merely copy the source-target pair."
    )


def open_user_prompt(row: Dict[str, Any], candidate_type: str) -> str:
    edit = normalized_edit(row)
    if edit["operation"] == "replace":
        edit_text = f'replacing "{edit["source_text"]}" with "{edit["target_text"]}"'
    elif edit["operation"] == "insert":
        edit_text = f'inserting "{edit["target_text"]}"'
    elif edit["operation"] == "delete":
        edit_text = f'deleting "{edit["source_text"]}"'
    else:
        edit_text = f'applying a {edit["operation"]} edit'
    style = {
        "natural": "Give a natural one-sentence explanation.",
        "rule_grounded": "Give one sentence that states the grammar or usage rule.",
        "evidence_grounded": "Give one sentence that names the sentence evidence supporting the edit.",
        "concise": "Give a concise explanation.",
        "uncertainty_aware": "If the edit seems optional or invalid, say that clearly in one sentence.",
    }.get(candidate_type, "Give a specific one-sentence explanation.")
    return (
        "Explain the grammar correction. Do not output the corrected sentence.\n"
        "Example source: The students goes to school.\n"
        "Example edit: replacing \"goes\" with \"go\"\n"
        "Example explanation: The plural subject \"students\" takes the base present-tense verb \"go\".\n\n"
        f"Source: {row.get('source', '')}\n"
        f"Model prediction: {row.get('prediction', '')}\n"
        f"Current edit: {edit_text} at source token span [{edit['start']},{edit['end']}).\n"
        f"Instruction: {style}\n"
        "Explanation:"
    )


def qwen_user_prompt(row: Dict[str, Any], candidate_type: str) -> str:
    edit = normalized_edit(row)
    if edit["operation"] == "replace":
        exact_edit = f'The only edit to explain is: replace "{edit["source_text"]}" with "{edit["target_text"]}" at source token span [{edit["start"]},{edit["end"]}).'
    elif edit["operation"] == "insert":
        exact_edit = f'The only edit to explain is: insert "{edit["target_text"]}" at source token span [{edit["start"]},{edit["end"]}).'
    elif edit["operation"] == "delete":
        exact_edit = f'The only edit to explain is: delete "{edit["source_text"]}" at source token span [{edit["start"]},{edit["end"]}).'
    else:
        exact_edit = f'The only edit to explain is the {edit["operation"]} operation at source token span [{edit["start"]},{edit["end"]}).'
    return (
        user_prompt(row, candidate_type)
        + "\n\n"
        + exact_edit
        + " Do not explain any other change in the sentence. If the edit is only punctuation, capitalization, or spacing, say that directly. "
        "Evidence spans must come from SOURCE only, never from MODEL_PREDICTION. "
        "The evidence_spans start/end values are whitespace token offsets in SOURCE, and the text must exactly equal SOURCE tokens[start:end]. "
        "Do not put corrected target phrases, target-only words, or MODEL_PREDICTION spans in evidence_spans. "
        "For grammar rules, cite contextual triggers such as subject, head noun, tense cue, antecedent, governor, or collocation; do not cite only the modified token unless the edit is spelling, capitalization, or punctuation. "
        "If no reliable source evidence can be identified, set evidence_spans=[] and lower confidence or abstain. "
        "If the edit appears wrong, optional, or stylistic, do not rationalize it as required grammar; mark edit_validity honestly. "
        "Return ONLY one valid JSON object. Do not use markdown, code fences, bullets, or extra commentary. "
        "Do not include hidden reasoning, chain-of-thought, or <think> blocks. "
        "Use exact lowercase edit_validity values: valid, acceptable_alternative, invalid, stylistic, uncertain. "
        "Every evidence_spans item must include text, start, end, and role. "
        "applicability_conditions must be a list of strings. abstain must be true or false. "
        "If the model edit appears invalid or optional, say so honestly in edit_validity and rationale."
    )


def extract_json_object(text: str) -> Tuple[Optional[Dict[str, Any]], str]:
    stripped = text.strip()
    if not stripped:
        return None, "empty_response"
    try:
        obj = json.loads(stripped)
        if isinstance(obj, dict):
            return obj, ""
        return None, "json_not_object"
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
    if not match:
        return None, "no_json_object_found"
    try:
        obj = json.loads(match.group(0))
        if isinstance(obj, dict):
            return obj, "extracted_json_from_text"
        return None, "extracted_json_not_object"
    except json.JSONDecodeError as exc:
        return None, f"json_decode_error:{exc.msg}"


def strip_thinking_blocks(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE).strip()


def normalize_edit_validity(value: Any) -> str:
    normalized = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    mapping = {
        "valid": "valid",
        "acceptable": "acceptable_alternative",
        "acceptable_alternative": "acceptable_alternative",
        "alternative": "acceptable_alternative",
        "invalid": "invalid",
        "stylistic": "stylistic",
        "style": "stylistic",
        "uncertain": "uncertain",
        "unknown": "uncertain",
        "not_sure": "uncertain",
    }
    return mapping.get(normalized, "uncertain")


def coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value or "").strip().lower()
    if normalized in {"true", "yes", "y", "1", "abstain", "abstained"}:
        return True
    if normalized in {"false", "no", "n", "0", ""}:
        return False
    return False


def coerce_conditions(value: Any) -> List[str]:
    if not isinstance(value, list):
        return []
    conditions: List[str] = []
    for item in value:
        if isinstance(item, str):
            text = item.strip()
        elif isinstance(item, dict):
            text = str(item.get("condition") or item.get("text") or item.get("description") or "").strip()
        else:
            text = str(item).strip()
        if text:
            conditions.append(text)
    return conditions


def coerce_evidence_spans(value: Any) -> List[Dict[str, Any]]:
    if not isinstance(value, list):
        return []
    spans: List[Dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        try:
            start = int(item.get("start", -1))
            end = int(item.get("end", -1))
        except (TypeError, ValueError):
            start, end = -1, -1
        spans.append(
            {
                "text": str(item.get("text") or ""),
                "start": start,
                "end": end,
                "role": str(item.get("role") or "unspecified"),
            }
        )
    return spans


def coerce_string(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    if text.strip().lower() in {"none", "null", "n/a", "na"}:
        return ""
    return text


def coerce_candidate(obj: Optional[Dict[str, Any]], raw: str, row: Dict[str, Any], candidate_type: str) -> Tuple[Dict[str, Any], str]:
    if obj is None:
        rationale = " ".join(raw.replace("\n", " ").split())[:1000]
        return (
            {
                "edit_description": edit_description(row),
                "edit_validity": "uncertain",
                "rule_id": "",
                "rule_text": "",
                "evidence_spans": [],
                "applicability_conditions": [],
                "rationale": rationale,
                "confidence": 0.25 if rationale else 0.0,
                "abstain": False if rationale else True,
                "abstain_reason": "" if rationale else "empty teacher response",
            },
            "wrapped_non_json_response",
        )
    candidate = {
        "edit_description": coerce_string(obj.get("edit_description", edit_description(row))),
        "edit_validity": normalize_edit_validity(obj.get("edit_validity", "uncertain")),
        "rule_id": coerce_string(obj.get("rule_id", "")),
        "rule_text": coerce_string(obj.get("rule_text", "")),
        "evidence_spans": coerce_evidence_spans(obj.get("evidence_spans")),
        "applicability_conditions": coerce_conditions(obj.get("applicability_conditions")),
        "rationale": coerce_string(obj.get("rationale", "")),
        "confidence": obj.get("confidence", 0.5),
        "abstain": coerce_bool(obj.get("abstain", False)),
        "abstain_reason": coerce_string(obj.get("abstain_reason", "")),
    }
    try:
        confidence = float(candidate["confidence"])
    except (TypeError, ValueError):
        confidence = 0.5
    candidate["confidence"] = min(1.0, max(0.0, confidence))
    return candidate, "parsed_json"


def edit_description(row: Dict[str, Any]) -> str:
    edit = normalized_edit(row)
    op = edit["operation"]
    src = edit["source_text"]
    tgt = edit["target_text"]
    span = f"[{edit['start']},{edit['end']})"
    if op == "replace":
        return f'The model replaces "{src}" with "{tgt}" at source token span {span}.'
    if op == "insert":
        return f'The model inserts "{tgt}" at source token span {span}.'
    if op == "delete":
        return f'The model deletes "{src}" at source token span {span}.'
    return f"The model applies a {op or 'unknown'} edit at source token span {span}."


def candidate_record(
    row: Dict[str, Any],
    provider: str,
    teacher_model: str,
    model_version: str,
    prompt_version: str,
    candidate_type: str,
    raw_response: str,
    parsed_output: Dict[str, Any],
    parse_status: str,
    parse_error: str,
    latency_seconds: float,
    request_id: str,
    usage: Dict[str, Any],
    estimated_cost_usd: float,
    api_response_path: str,
) -> Dict[str, Any]:
    edit = normalized_edit(row)
    base_id = row.get("rulefaith_pool_id") or row.get("edit_id") or row.get("sample_id")
    candidate_id = f"{base_id}::{provider}::{candidate_type}"
    return {
        "candidate_id": candidate_id,
        "rulefaith_pool_id": row.get("rulefaith_pool_id"),
        "edit_id": row.get("edit_id"),
        "sample_id": row.get("sample_id"),
        "dataset": row.get("dataset"),
        "model_key": row.get("model_key"),
        "model_family": row.get("model_family"),
        "rulefaith_split": row.get("rulefaith_split"),
        "source": row.get("source"),
        "model_prediction": row.get("prediction"),
        "model_edit": edit,
        "error_type": row.get("error_type"),
        "error_category": row.get("error_category"),
        "candidate_type": candidate_type,
        "provider": provider,
        "teacher_model": teacher_model,
        "model_version": model_version,
        "prompt_version": prompt_version,
        "generator_input_fields": ["source", "model_prediction", "model_edit", "edit_span"],
        "uses_reference_in_generator": False,
        "uses_gold_edit_in_generator": False,
        "uses_behavior_label_in_generator": False,
        "uses_human_label_in_generator": False,
        "parsed_output": parsed_output,
        "raw_response": raw_response,
        "parse_status": parse_status,
        "parse_error": parse_error,
        "request_id": request_id,
        "token_usage": usage,
        "latency_seconds": round(latency_seconds, 4),
        "estimated_cost_usd": round(estimated_cost_usd, 8),
        "api_response_path": api_response_path,
        "created_at": utc_now(),
        "is_human_gold": False,
        "label_source": "teacher_generated_candidate_not_gold",
    }


def existing_candidate_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {json.loads(line)["candidate_id"] for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def write_raw_response(raw_dir: Path, candidate_id: str, payload: Dict[str, Any]) -> str:
    raw_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", candidate_id)
    path = raw_dir / f"{safe_name}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return display_path(path)


def generate_open_teacher(args: argparse.Namespace, config: Dict[str, Any], rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    import torch
    from huggingface_hub import model_info
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    if not rows:
        return []

    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    model_id = args.open_model or config.get("teacher_model", "google/flan-t5-small")
    candidate_types = args.candidate_types or list(config.get("candidate_types", ["natural", "rule_grounded"]))
    local_files_only = bool(config.get("local_files_only", True))
    revision = "unknown"
    try:
        revision = model_info(model_id).sha or "unknown"
    except Exception:
        revision = "unknown_local_or_unresolved"

    tokenizer = AutoTokenizer.from_pretrained(model_id, local_files_only=local_files_only)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id, local_files_only=local_files_only).to("cpu")
    model.eval()
    torch.set_num_threads(1)

    records: List[Dict[str, Any]] = []
    seen = existing_candidate_ids(args.output) if args.resume else set()
    prompts: List[Tuple[Dict[str, Any], str, str]] = []
    for row in rows:
        for candidate_type in candidate_types:
            base_id = row.get("rulefaith_pool_id") or row.get("edit_id")
            candidate_id = f"{base_id}::open_teacher::{candidate_type}"
            if candidate_id in seen:
                continue
            prompts.append((row, candidate_type, open_user_prompt(row, candidate_type)))

    batch_size = int(config.get("batch_size", 8))
    for start in range(0, len(prompts), batch_size):
        batch = prompts[start : start + batch_size]
        text_inputs = [system_prompt() + "\n\n" + prompt for _, _, prompt in batch]
        started = time.time()
        inputs = tokenizer(
            text_inputs,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=int(config.get("max_input_length", 768)),
        )
        with torch.inference_mode():
            output_ids = model.generate(
                **inputs,
                num_beams=int(config.get("num_beams", 4)),
                max_new_tokens=int(config.get("max_new_tokens", 128)),
                no_repeat_ngram_size=3,
                repetition_penalty=1.1,
            )
        decoded = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        batch_latency = (time.time() - started) / max(1, len(batch))
        new_records = []
        for (row, candidate_type, prompt), raw in zip(batch, decoded):
            parsed, parse_error = extract_json_object(raw)
            parsed_output, parse_status = coerce_candidate(parsed, raw, row, candidate_type)
            base_id = row.get("rulefaith_pool_id") or row.get("edit_id")
            request_id = f"local-{uuid.uuid4()}"
            raw_path = write_raw_response(
                args.raw_dir,
                f"{base_id}::open_teacher::{candidate_type}",
                {
                    "provider": "open_teacher",
                    "teacher_model": model_id,
                    "model_version": revision,
                    "candidate_type": candidate_type,
                    "prompt": prompt,
                    "raw_response": raw,
                    "request_id": request_id,
                },
            )
            record = candidate_record(
                row=row,
                provider="open_teacher",
                teacher_model=model_id,
                model_version=revision,
                prompt_version=config.get("prompt_version", "rulefaith_open_teacher_v1"),
                candidate_type=candidate_type,
                raw_response=raw,
                parsed_output=parsed_output,
                parse_status=parse_status,
                parse_error=parse_error,
                latency_seconds=batch_latency,
                request_id=request_id,
                usage={"input_tokens": None, "output_tokens": None, "total_tokens": None},
                estimated_cost_usd=0.0,
                api_response_path=raw_path,
            )
            records.append(record)
            new_records.append(record)
        append_jsonl(args.output, new_records)
    return records


def preferred_torch_device(torch: Any, config: Dict[str, Any]) -> str:
    configured = config.get("device")
    if configured and configured != "auto":
        return str(configured)
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def qwen_dtype(torch: Any, device: str) -> Any:
    if device == "cuda":
        return torch.float16
    if device == "mps":
        return torch.float16
    return torch.float32


def generate_qwen_small(args: argparse.Namespace, config: Dict[str, Any], rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    import torch
    from huggingface_hub import model_info
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if not rows:
        return []

    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    model_id = args.qwen_model or config.get("teacher_model", "Qwen/Qwen2.5-0.5B-Instruct")
    provider_name = args.qwen_provider_name or config.get("provider_name") or "qwen_small"
    candidate_types = args.candidate_types or list(config.get("candidate_types", ["natural", "rule_grounded"]))
    local_files_only = bool(config.get("local_files_only", False))
    trust_remote_code = bool(config.get("trust_remote_code", False))
    device = preferred_torch_device(torch, config)
    revision = "unknown"
    try:
        revision = model_info(model_id).sha or "unknown"
    except Exception:
        revision = "unknown_local_or_unresolved"

    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        local_files_only=local_files_only,
        trust_remote_code=trust_remote_code,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        local_files_only=local_files_only,
        trust_remote_code=trust_remote_code,
        torch_dtype=qwen_dtype(torch, device),
        low_cpu_mem_usage=True,
    ).to(device)
    model.eval()
    torch.set_num_threads(int(config.get("num_threads", 4)))

    records: List[Dict[str, Any]] = []
    seen = existing_candidate_ids(args.output) if args.resume else set()
    prompts: List[Tuple[Dict[str, Any], str, str]] = []
    for row in rows:
        for candidate_type in candidate_types:
            base_id = row.get("rulefaith_pool_id") or row.get("edit_id")
            candidate_id = f"{base_id}::{provider_name}::{candidate_type}"
            if candidate_id in seen:
                continue
            prompts.append((row, candidate_type, qwen_user_prompt(row, candidate_type)))

    for row, candidate_type, prompt in prompts:
        messages = [
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": prompt},
        ]
        started = time.time()
        try:
            chat_text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=bool(config.get("enable_thinking", False)),
            )
        except TypeError:
            chat_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer([chat_text], return_tensors="pt", truncation=True, max_length=int(config.get("max_input_length", 1024)))
        inputs = {key: value.to(device) for key, value in inputs.items()}
        generate_kwargs: Dict[str, Any] = {
            "max_new_tokens": int(config.get("max_new_tokens", 384)),
            "do_sample": bool(config.get("do_sample", False)),
            "repetition_penalty": float(config.get("repetition_penalty", 1.05)),
            "pad_token_id": tokenizer.eos_token_id,
        }
        if generate_kwargs["do_sample"]:
            generate_kwargs["temperature"] = float(config.get("temperature", 0.7))
            generate_kwargs["top_p"] = float(config.get("top_p", 0.9))
        with torch.inference_mode():
            output_ids = model.generate(**inputs, **generate_kwargs)
        generated_ids = output_ids[0][inputs["input_ids"].shape[-1] :]
        raw = strip_thinking_blocks(tokenizer.decode(generated_ids, skip_special_tokens=True))
        latency = time.time() - started
        parsed, parse_error = extract_json_object(raw)
        parsed_output, parse_status = coerce_candidate(parsed, raw, row, candidate_type)
        base_id = row.get("rulefaith_pool_id") or row.get("edit_id")
        candidate_id = f"{base_id}::{provider_name}::{candidate_type}"
        request_id = f"qwen-local-{uuid.uuid4()}"
        usage = {
            "input_tokens": int(inputs["input_ids"].shape[-1]),
            "output_tokens": int(generated_ids.shape[-1]),
            "total_tokens": int(inputs["input_ids"].shape[-1] + generated_ids.shape[-1]),
        }
        raw_path = write_raw_response(
            args.raw_dir,
            candidate_id,
            {
                "provider": provider_name,
                "teacher_model": model_id,
                "model_version": revision,
                "candidate_type": candidate_type,
                "device": device,
                "prompt": prompt,
                "raw_response": raw,
                "request_id": request_id,
                "usage": usage,
                "enable_thinking": bool(config.get("enable_thinking", False)),
            },
        )
        record = candidate_record(
            row=row,
            provider=provider_name,
            teacher_model=model_id,
            model_version=revision,
            prompt_version=config.get("prompt_version", "rulefaith_qwen_small_teacher_v1_json"),
            candidate_type=candidate_type,
            raw_response=raw,
            parsed_output=parsed_output,
            parse_status=parse_status,
            parse_error=parse_error,
            latency_seconds=latency,
            request_id=request_id,
            usage=usage,
            estimated_cost_usd=0.0,
            api_response_path=raw_path,
        )
        append_jsonl(args.output, [record])
        records.append(record)
    return records


def rough_token_count(text: str) -> int:
    return max(1, int(len(text.split()) * 1.35))


def estimate_gpt_cost(input_tokens: int, output_tokens: int, config: Dict[str, Any]) -> float:
    pricing = config.get("pricing", {})
    in_rate = float(os.environ.get(pricing.get("input_usd_per_million_env", ""), pricing.get("fallback_input_usd_per_million", 2.5)))
    out_rate = float(os.environ.get(pricing.get("output_usd_per_million_env", ""), pricing.get("fallback_output_usd_per_million", 10.0)))
    return (input_tokens / 1_000_000.0) * in_rate + (output_tokens / 1_000_000.0) * out_rate


def generate_gpt55(args: argparse.Namespace, config: Dict[str, Any], rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    api_key_env = config.get("api_key_env", "OPENAI_API_KEY")
    if not os.environ.get(api_key_env):
        raise RuntimeError(f"missing_{api_key_env}")
    try:
        from openai import OpenAI
    except Exception as exc:  # pragma: no cover - only used with API credentials.
        raise RuntimeError(f"openai_sdk_unavailable:{exc}") from exc

    budget = float(os.environ.get(config.get("budget_env", "RULEFAITH_API_BUDGET_USD"), config.get("default_budget_usd", 30.0)))
    model_name = os.environ.get(config.get("model_env", "RULEFAITH_GPT55_MODEL"), config.get("default_model", "gpt-5.5"))
    candidate_types = args.candidate_types or list(config.get("candidate_types", ["natural", "rule_grounded", "evidence_grounded", "concise", "uncertainty_aware"]))
    client = OpenAI()
    records: List[Dict[str, Any]] = []
    seen = existing_candidate_ids(args.output) if args.resume else set()
    spent = 0.0

    for row in rows:
        for candidate_type in candidate_types:
            base_id = row.get("rulefaith_pool_id") or row.get("edit_id")
            candidate_id = f"{base_id}::gpt55::{candidate_type}"
            if candidate_id in seen:
                continue
            prompt = user_prompt(row, candidate_type)
            projected_input = rough_token_count(system_prompt() + prompt)
            projected_output = int(config.get("max_output_tokens", 700))
            projected_cost = estimate_gpt_cost(projected_input, projected_output, config)
            if spent + projected_cost > budget:
                raise RuntimeError(f"budget_would_exceed:{spent + projected_cost:.4f}>{budget:.4f}")
            started = time.time()
            response = client.responses.create(
                model=model_name,
                input=[
                    {"role": "system", "content": system_prompt()},
                    {"role": "user", "content": prompt},
                ],
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "rulefaith_explanation_candidate",
                        "schema": RULEFAITH_SCHEMA,
                        "strict": True,
                    }
                },
                temperature=float(config.get("temperature", 0.4)),
                max_output_tokens=int(config.get("max_output_tokens", 700)),
                timeout=float(config.get("timeout_seconds", 90)),
            )
            latency = time.time() - started
            raw = getattr(response, "output_text", "") or str(response)
            parsed, parse_error = extract_json_object(raw)
            parsed_output, parse_status = coerce_candidate(parsed, raw, row, candidate_type)
            usage_obj = getattr(response, "usage", None)
            usage = {
                "input_tokens": getattr(usage_obj, "input_tokens", None),
                "output_tokens": getattr(usage_obj, "output_tokens", None),
                "total_tokens": getattr(usage_obj, "total_tokens", None),
            }
            actual_cost = estimate_gpt_cost(
                int(usage["input_tokens"] or projected_input),
                int(usage["output_tokens"] or projected_output),
                config,
            )
            spent += actual_cost
            request_id = getattr(response, "id", "") or f"openai-{uuid.uuid4()}"
            raw_path = write_raw_response(
                args.raw_dir,
                candidate_id,
                {
                    "provider": "gpt55",
                    "teacher_model": model_name,
                    "request_id": request_id,
                    "candidate_type": candidate_type,
                    "prompt": prompt,
                    "raw_response": raw,
                    "usage": usage,
                    "estimated_cost_usd": actual_cost,
                    "api_reference": OPENAI_DOCS_RESPONSES_CREATE,
                },
            )
            record = candidate_record(
                row=row,
                provider="gpt55",
                teacher_model=model_name,
                model_version=model_name,
                prompt_version=config.get("prompt_version", "rulefaith_teacher_v1"),
                candidate_type=candidate_type,
                raw_response=raw,
                parsed_output=parsed_output,
                parse_status=parse_status,
                parse_error=parse_error,
                latency_seconds=latency,
                request_id=request_id,
                usage=usage,
                estimated_cost_usd=actual_cost,
                api_response_path=raw_path,
            )
            append_jsonl(args.output, [record])
            records.append(record)
    return records


def record_parse_failures(records: List[Dict[str, Any]], path: Path) -> None:
    failures = [
        {
            "candidate_id": row["candidate_id"],
            "provider": row["provider"],
            "candidate_type": row["candidate_type"],
            "parse_status": row["parse_status"],
            "parse_error": row["parse_error"],
            "raw_response": row["raw_response"],
        }
        for row in records
        if row["parse_status"] != "parsed_json"
    ]
    if failures:
        append_jsonl(path, failures)
    elif not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")


def summarize(args: argparse.Namespace, rows: List[Dict[str, Any]], records: List[Dict[str, Any]], blocked: List[str]) -> None:
    all_output_rows = read_jsonl(args.output) if args.output.exists() else []
    stats = {
        "created_at": utc_now(),
        "input": display_path(args.input),
        "output": display_path(args.output),
        "pilot_edit_count": len(rows),
        "new_candidate_count_this_run": len(records),
        "total_candidate_count_in_output": len(all_output_rows),
        "provider_counts": dict(Counter(row.get("provider", "") for row in all_output_rows)),
        "candidate_type_counts": dict(Counter(row.get("candidate_type", "") for row in all_output_rows)),
        "parse_status_counts": dict(Counter(row.get("parse_status", "") for row in all_output_rows)),
        "model_counts": dict(Counter(row.get("model_key", "") for row in all_output_rows)),
        "estimated_total_cost_usd": round(sum(float(row.get("estimated_cost_usd", 0.0)) for row in all_output_rows), 8),
        "blocked": blocked,
        "openai_sdk_present": openai_sdk_present(),
        "openai_api_key_present": bool(os.environ.get("OPENAI_API_KEY")),
        "budget_env_present": bool(os.environ.get("RULEFAITH_API_BUDGET_USD")),
        "api_reference": OPENAI_DOCS_RESPONSES_CREATE,
        "important_note": "Teacher candidates are model-generated explanation candidates, not human gold. Prompts exclude references, human labels, and behavior labels.",
    }
    write_json(args.stats, stats)


def openai_sdk_present() -> bool:
    try:
        import importlib.util

        return importlib.util.find_spec("openai") is not None
    except Exception:
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate RuleFaith teacher explanation candidates.")
    parser.add_argument("--provider", choices=["open_teacher", "qwen_small", "gpt55", "all", "dry_run"], default="open_teacher")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stats", type=Path, default=DEFAULT_STATS)
    parser.add_argument("--parse-failures", type=Path, default=DEFAULT_PARSE_FAILURES)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--limit", type=int, default=80)
    parser.add_argument("--candidate-types", nargs="*", default=None)
    parser.add_argument("--open-model", default=None)
    parser.add_argument("--qwen-model", default=None)
    parser.add_argument("--qwen-provider-name", default=None)
    parser.add_argument("--qwen-config", type=Path, default=QWEN_CONFIG)
    parser.add_argument("--num-shards", type=int, default=1)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--resume", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.input = args.input if args.input.is_absolute() else ROOT / args.input
    args.output = args.output if args.output.is_absolute() else ROOT / args.output
    args.stats = args.stats if args.stats.is_absolute() else ROOT / args.stats
    args.parse_failures = args.parse_failures if args.parse_failures.is_absolute() else ROOT / args.parse_failures
    args.raw_dir = args.raw_dir if args.raw_dir.is_absolute() else ROOT / args.raw_dir
    args.qwen_config = args.qwen_config if args.qwen_config.is_absolute() else ROOT / args.qwen_config

    if args.num_shards < 1:
        raise ValueError("--num-shards must be >= 1")
    if args.shard_index < 0 or args.shard_index >= args.num_shards:
        raise ValueError("--shard-index must satisfy 0 <= shard_index < num_shards")

    rows = select_pilot_rows(read_jsonl(args.input), args.limit)
    if args.num_shards > 1:
        rows = [row for index, row in enumerate(rows) if index % args.num_shards == args.shard_index]
    records: List[Dict[str, Any]] = []
    blocked: List[str] = []

    if args.provider in {"open_teacher", "all"}:
        try:
            records.extend(generate_open_teacher(args, load_yaml(OPEN_CONFIG), rows))
        except Exception as exc:
            blocked.append(f"open_teacher_failed:{exc}")

    if args.provider in {"qwen_small", "all"}:
        try:
            records.extend(generate_qwen_small(args, load_yaml(args.qwen_config), rows))
        except Exception as exc:
            blocked.append(f"qwen_small_failed:{exc}")

    if args.provider in {"gpt55", "all"}:
        try:
            records.extend(generate_gpt55(args, load_yaml(GPT_CONFIG), rows))
        except Exception as exc:
            blocked.append(f"gpt55_failed:{exc}")

    if args.provider == "dry_run":
        dry_records = []
        for row in rows[: min(3, len(rows))]:
            for candidate_type in ["natural", "rule_grounded"]:
                raw = json.dumps(
                    {
                        "edit_description": edit_description(row),
                        "edit_validity": "uncertain",
                        "rule_id": "",
                        "rule_text": "",
                        "evidence_spans": [],
                        "applicability_conditions": [],
                        "rationale": "Dry-run candidate used only to validate serialization.",
                        "confidence": 0.0,
                        "abstain": True,
                        "abstain_reason": "dry run",
                    }
                )
                parsed, parse_error = extract_json_object(raw)
                parsed_output, parse_status = coerce_candidate(parsed, raw, row, candidate_type)
                dry_records.append(
                    candidate_record(
                        row,
                        "dry_run",
                        "none",
                        "none",
                        "rulefaith_teacher_dry_run",
                        candidate_type,
                        raw,
                        parsed_output,
                        parse_status,
                        parse_error,
                        0.0,
                        f"dry-{uuid.uuid4()}",
                        {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
                        0.0,
                        "",
                    )
                )
        records.extend(dry_records)
        append_jsonl(args.output, dry_records)

    record_parse_failures(records, args.parse_failures)
    summarize(args, rows, records, blocked)
    if blocked:
        for item in blocked:
            print(item, file=sys.stderr)
    return 0 if not blocked or args.provider in {"all", "dry_run"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
