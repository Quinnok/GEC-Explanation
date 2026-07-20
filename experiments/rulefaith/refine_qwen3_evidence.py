from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.rulefaith import build_qwen3_manual_audit as audit

DEFAULT_INPUT = ROOT / "results" / "rulefaith" / "qwen3_v2_smoke10_candidates.jsonl"
DEFAULT_OUTPUT = ROOT / "results" / "rulefaith" / "qwen3_v2_smoke10_evidence_refined_candidates.jsonl"
DEFAULT_STATS = ROOT / "results" / "rulefaith" / "qwen3_v2_smoke10_evidence_refinement_stats.json"
DEFAULT_AUDIT_MD = ROOT / "results" / "rulefaith" / "qwen3_v2_smoke10_evidence_refinement_audit.md"
DEFAULT_RAW_DIR = ROOT / "results" / "rulefaith" / "qwen3_v2_smoke10_evidence_refinement_raw"
DEFAULT_CONFIG = ROOT / "configs" / "rulefaith" / "qwen3_8b_teacher.yaml"

PROMPT_VERSION = "rulefaith_qwen3_evidence_refine_v2_compact_source_only_json"


def generator_module() -> Any:
    from experiments.rulefaith import generate_teacher_candidates as gen

    return gen


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Bad JSON in {path}:{lineno}: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"JSONL row is not an object in {path}:{lineno}")
            rows.append(row)
    if not rows:
        raise ValueError(f"Input file is empty: {path}")
    return rows


def append_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, obj: Any, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass --overwrite to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(text)
        return loaded if isinstance(loaded, dict) else {}
    except ModuleNotFoundError:
        config: dict[str, Any] = {}
        current_list_key: str | None = None
        for raw_line in text.splitlines():
            line = raw_line.split("#", 1)[0].rstrip()
            if not line.strip():
                continue
            if line.startswith("  - ") and current_list_key:
                config.setdefault(current_list_key, []).append(line[4:].strip().strip('"'))
                continue
            if ":" not in line or raw_line.startswith(" "):
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_list_key = None
            if value == "":
                config[key] = []
                current_list_key = key
            elif value.lower() in {"true", "false"}:
                config[key] = value.lower() == "true"
            else:
                config[key] = value.strip('"')
        return config


def candidate_as_row(record: dict[str, Any]) -> dict[str, Any]:
    row = dict(record)
    row["prediction"] = record.get("model_prediction", "")
    row["predicted_edit"] = record.get("model_edit", {})
    return row


def evidence_checks_for_record(record: dict[str, Any], parsed: dict[str, Any] | None = None) -> dict[str, Any]:
    parsed_output = parsed if parsed is not None else record.get("parsed_output") or {}
    if not isinstance(parsed_output, dict):
        parsed_output = {}
    return audit.evidence_checks(
        str(record.get("source", "")),
        str(record.get("model_prediction", "")),
        record.get("model_edit") or {},
        parsed_output.get("evidence_spans", []),
    )


def needs_evidence_refinement(record: dict[str, Any]) -> bool:
    checks = evidence_checks_for_record(record)
    return bool(checks["missing_evidence"] or checks["wrong_evidence_auto"] or checks["evidence_text_found_in_prediction_only"])


def source_token_table(source: str) -> str:
    return "\n".join(f"{idx}: {token}" for idx, token in enumerate(source.split()))


def compact_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


def edit_text(edit: dict[str, Any]) -> str:
    op = edit.get("operation", "")
    start = edit.get("start", "")
    end = edit.get("end", "")
    src = edit.get("source_text", "")
    tgt = edit.get("target_text", "")
    if op == "replace":
        return f'replace "{src}" with "{tgt}" at SOURCE token span [{start},{end})'
    if op == "insert":
        return f'insert "{tgt}" at SOURCE token span [{start},{end})'
    if op == "delete":
        return f'delete "{src}" at SOURCE token span [{start},{end})'
    return f"{op or 'unknown'} edit at SOURCE token span [{start},{end})"


def refinement_prompt(record: dict[str, Any], before_checks: dict[str, Any]) -> str:
    parsed = record.get("parsed_output") or {}
    if not isinstance(parsed, dict):
        parsed = {}
    edit = record.get("model_edit") or {}
    failure_summary = {
        key: before_checks.get(key)
        for key in [
            "missing_evidence",
            "wrong_evidence_auto",
            "evidence_error_types",
            "evidence_text_found_in_prediction_only",
        ]
    }
    original = {
        key: parsed.get(key)
        for key in [
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
        ]
    }
    return (
        "Repair SOURCE evidence for one GEC edit. Output JSON only.\n\n"
        f"SOURCE:\n{record.get('source', '')}\n\n"
        f"SOURCE_TOKENS:\n{source_token_table(str(record.get('source', '')))}\n\n"
        f"MODEL_PREDICTION:\n{record.get('model_prediction', '')}\n\n"
        f"ONLY_MODEL_EDIT:\n{edit_text(edit)}\n\n"
        f"ORIGINAL_JSON:\n{compact_json(original)}\n\n"
        f"FAILED_CHECKS:\n{compact_json(failure_summary)}\n\n"
        "Rules: evidence_spans must be SOURCE token spans only; start/end are whitespace-token offsets; "
        "text must exactly equal SOURCE tokens[start:end]. Never cite target-only or MODEL_PREDICTION text. "
        "For grammar, cite contextual triggers such as subject, head noun, determiner, tense cue, antecedent, governor, or collocation. "
        "Use the edited token alone only for spelling/capitalization/punctuation. If no reliable SOURCE evidence exists, use evidence_spans=[], confidence<=0.4, and abstain=true.\n\n"
        "Return exactly one JSON object with keys: edit_description, edit_validity, rule_id, rule_text, evidence_spans, applicability_conditions, rationale, confidence, abstain, abstain_reason."
    )


def existing_original_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    ids = set()
    for row in read_jsonl(path):
        original = row.get("original_candidate_id")
        if original:
            ids.add(str(original))
    return ids


def parse_last_json_object(text: str) -> dict[str, Any] | None:
    starts = [idx for idx, char in enumerate(text) if char == "{"]
    for start in reversed(starts):
        depth = 0
        in_string = False
        escape = False
        for idx in range(start, len(text)):
            char = text[idx]
            if in_string:
                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    try:
                        obj = json.loads(text[start : idx + 1])
                    except json.JSONDecodeError:
                        break
                    return obj if isinstance(obj, dict) else None
    return None


def parse_model_output(raw: str, record: dict[str, Any]) -> tuple[dict[str, Any], str, str]:
    gen = generator_module()
    parsed, parse_error = gen.extract_json_object(raw)
    if parsed is None:
        parsed = parse_last_json_object(raw)
        if parsed is not None:
            parse_error = "last_json_object_fallback"
    parsed_output, parse_status = gen.coerce_candidate(parsed, raw, candidate_as_row(record), "evidence_refined")
    if parse_error == "last_json_object_fallback" and parse_status == "parsed_json":
        parse_status = "parsed_json_fallback"
    return parsed_output, parse_status, parse_error


def build_refined_record(
    original: dict[str, Any],
    parsed_output: dict[str, Any],
    raw: str,
    parse_status: str,
    parse_error: str,
    before_checks: dict[str, Any],
    after_checks: dict[str, Any],
    latency_seconds: float,
    request_id: str,
    usage: dict[str, Any],
    raw_path: str,
    model_id: str,
    model_version: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    candidate_id = f"{original['candidate_id']}::evidence_refined"
    return {
        "candidate_id": candidate_id,
        "original_candidate_id": original.get("candidate_id"),
        "rulefaith_pool_id": original.get("rulefaith_pool_id"),
        "edit_id": original.get("edit_id"),
        "sample_id": original.get("sample_id"),
        "dataset": original.get("dataset"),
        "model_key": original.get("model_key"),
        "model_family": original.get("model_family"),
        "rulefaith_split": original.get("rulefaith_split"),
        "source": original.get("source"),
        "model_prediction": original.get("model_prediction"),
        "model_edit": original.get("model_edit"),
        "error_type": original.get("error_type"),
        "error_category": original.get("error_category"),
        "candidate_type": "evidence_refined",
        "original_candidate_type": original.get("candidate_type"),
        "provider": "qwen3_8b_evidence_refiner",
        "teacher_model": model_id,
        "model_version": model_version,
        "prompt_version": PROMPT_VERSION,
        "base_prompt_version": config.get("prompt_version"),
        "generator_input_fields": ["source", "model_prediction", "model_edit", "original_explanation", "strict_evidence_failures"],
        "uses_reference_in_generator": False,
        "uses_gold_edit_in_generator": False,
        "uses_behavior_label_in_generator": False,
        "uses_human_label_in_generator": False,
        "parsed_output": parsed_output,
        "raw_response": raw,
        "parse_status": parse_status,
        "parse_error": parse_error,
        "before_evidence_checks": before_checks,
        "after_evidence_checks": after_checks,
        "evidence_contextual_improved": bool(not before_checks["evidence_contextual"] and after_checks["evidence_contextual"]),
        "wrong_evidence_fixed": bool(before_checks["wrong_evidence_auto"] and not after_checks["wrong_evidence_auto"]),
        "prediction_only_evidence_regressed": bool(not before_checks["evidence_text_found_in_prediction_only"] and after_checks["evidence_text_found_in_prediction_only"]),
        "request_id": request_id,
        "token_usage": usage,
        "latency_seconds": round(latency_seconds, 4),
        "estimated_cost_usd": 0.0,
        "api_response_path": raw_path,
        "created_at": utc_now(),
        "is_human_gold": False,
        "label_source": "teacher_generated_refinement_not_gold",
    }


def write_raw_response(raw_dir: Path, candidate_id: str, payload: dict[str, Any]) -> str:
    raw_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", candidate_id)
    path = raw_dir / f"{safe_name}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def summarize(input_rows: list[dict[str, Any]], selected: list[dict[str, Any]], refined: list[dict[str, Any]]) -> dict[str, Any]:
    refined_by_original = {row["original_candidate_id"]: row for row in refined}

    def checks_for(row: dict[str, Any]) -> dict[str, Any]:
        replacement = refined_by_original.get(row.get("candidate_id"))
        if replacement:
            return replacement["after_evidence_checks"]
        return evidence_checks_for_record(row)

    original_checks = [evidence_checks_for_record(row) for row in input_rows]
    selected_before = [evidence_checks_for_record(row) for row in selected]
    selected_after = [row["after_evidence_checks"] for row in refined]
    full_after = [checks_for(row) for row in input_rows]

    def count(checks: list[dict[str, Any]], key: str) -> int:
        return sum(1 for item in checks if item.get(key))

    parse_status_counts = Counter(row.get("parse_status") for row in refined)
    summary = {
        "generated_at": utc_now(),
        "git_commit": audit.git_commit(),
        "prompt_version": PROMPT_VERSION,
        "input_count": len(input_rows),
        "selected_for_refinement_count": len(selected),
        "refined_count": len(refined),
        "parse_status_counts": dict(parse_status_counts),
        "original_full": {
            "contextual_source_evidence": count(original_checks, "evidence_contextual"),
            "missing_evidence": count(original_checks, "missing_evidence"),
            "prediction_only_evidence": count(original_checks, "evidence_text_found_in_prediction_only"),
            "wrong_evidence_auto": count(original_checks, "wrong_evidence_auto"),
        },
        "selected_before": {
            "contextual_source_evidence": count(selected_before, "evidence_contextual"),
            "missing_evidence": count(selected_before, "missing_evidence"),
            "prediction_only_evidence": count(selected_before, "evidence_text_found_in_prediction_only"),
            "wrong_evidence_auto": count(selected_before, "wrong_evidence_auto"),
        },
        "selected_after": {
            "contextual_source_evidence": count(selected_after, "evidence_contextual"),
            "missing_evidence": count(selected_after, "missing_evidence"),
            "prediction_only_evidence": count(selected_after, "evidence_text_found_in_prediction_only"),
            "wrong_evidence_auto": count(selected_after, "wrong_evidence_auto"),
        },
        "full_after_replacing_selected": {
            "contextual_source_evidence": count(full_after, "evidence_contextual"),
            "missing_evidence": count(full_after, "missing_evidence"),
            "prediction_only_evidence": count(full_after, "evidence_text_found_in_prediction_only"),
            "wrong_evidence_auto": count(full_after, "wrong_evidence_auto"),
        },
        "improvement_counts": {
            "evidence_contextual_improved": sum(1 for row in refined if row["evidence_contextual_improved"]),
            "wrong_evidence_fixed": sum(1 for row in refined if row["wrong_evidence_fixed"]),
            "prediction_only_evidence_regressed": sum(1 for row in refined if row["prediction_only_evidence_regressed"]),
        },
    }
    if (
        summary["selected_after"]["contextual_source_evidence"] > summary["selected_before"]["contextual_source_evidence"]
        and summary["selected_after"]["prediction_only_evidence"] <= summary["selected_before"]["prediction_only_evidence"]
    ):
        summary["decision"] = "keep_refinement_prompt_for_20_edit_probe_with_manual_spot_check"
    else:
        summary["decision"] = "revise_refinement_prompt_before_scaling"
    return summary


def audit_markdown(summary: dict[str, Any], refined: list[dict[str, Any]]) -> str:
    lines = [
        "# Qwen3 Evidence Refinement Smoke Audit",
        "",
        "## Loop",
        "",
        "- Loop ID: Loop C / targeted evidence refinement smoke.",
        "- Bottleneck: Qwen3 prompt-v2 reduces prediction-only evidence but still misses contextual source evidence.",
        "- Hypothesis: an evidence-only repair prompt can improve contextual SOURCE evidence without adding target/prediction leakage.",
        "- Success criterion: selected refined outputs increase contextual evidence and do not increase prediction-only evidence.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        if isinstance(value, dict):
            lines.append(f"- `{key}`: `{value}`")
        else:
            lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Refined Cases", ""])
    for row in refined:
        parsed = row.get("parsed_output") or {}
        before = row.get("before_evidence_checks", {})
        after = row.get("after_evidence_checks", {})
        lines.extend(
            [
                f"### {row['candidate_id']}",
                "",
                f"- original: `{row.get('original_candidate_id')}`; parse: `{row.get('parse_status')}`; latency: `{row.get('latency_seconds')}`",
                f"- before: `{before}`",
                f"- after: `{after}`",
                f"- rule: {parsed.get('rule_text', '')}",
                f"- evidence: `{compact_json(parsed.get('evidence_spans', []))}`",
                f"- rationale: {parsed.get('rationale', '')}",
                "",
            ]
        )
    return "\n".join(lines)


def generate_refinements(args: argparse.Namespace, config: dict[str, Any], selected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gen = generator_module()
    import torch
    from huggingface_hub import model_info
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if not selected:
        return []

    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    model_id = args.qwen_model or config.get("teacher_model", "Qwen/Qwen3-8B")
    local_files_only = bool(config.get("local_files_only", False))
    trust_remote_code = bool(config.get("trust_remote_code", False))
    device = gen.preferred_torch_device(torch, config)
    revision = "unknown"
    try:
        revision = model_info(model_id).sha or "unknown"
    except Exception:
        revision = "unknown_local_or_unresolved"

    tokenizer = AutoTokenizer.from_pretrained(model_id, local_files_only=local_files_only, trust_remote_code=trust_remote_code)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        local_files_only=local_files_only,
        trust_remote_code=trust_remote_code,
        torch_dtype=gen.qwen_dtype(torch, device),
        low_cpu_mem_usage=True,
    ).to(device)
    model.eval()
    torch.set_num_threads(int(config.get("num_threads", 4)))

    records: list[dict[str, Any]] = []
    seen = existing_original_ids(args.output) if args.resume else set()
    for record in selected:
        original_id = str(record.get("candidate_id"))
        if original_id in seen:
            continue
        before_checks = evidence_checks_for_record(record)
        prompt = refinement_prompt(record, before_checks)
        messages = [
            {"role": "system", "content": gen.system_prompt()},
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
        max_input_length = int(args.max_input_length or config.get("max_input_length", 1024))
        inputs = tokenizer([chat_text], return_tensors="pt", truncation=True, max_length=max_input_length)
        inputs = {key: value.to(device) for key, value in inputs.items()}
        generate_kwargs: dict[str, Any] = {
            "max_new_tokens": int(args.max_new_tokens or config.get("max_new_tokens", 384)),
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
        raw = gen.strip_thinking_blocks(tokenizer.decode(generated_ids, skip_special_tokens=True))
        latency = time.time() - started
        parsed_output, parse_status, parse_error = parse_model_output(raw, record)
        after_checks = evidence_checks_for_record(record, parsed_output)
        request_id = f"qwen-refine-local-{uuid.uuid4()}"
        usage = {
            "input_tokens": int(inputs["input_ids"].shape[-1]),
            "output_tokens": int(generated_ids.shape[-1]),
            "total_tokens": int(inputs["input_ids"].shape[-1] + generated_ids.shape[-1]),
        }
        candidate_id = f"{record['candidate_id']}::evidence_refined"
        raw_path = write_raw_response(
            args.raw_dir,
            candidate_id,
            {
                "provider": "qwen3_8b_evidence_refiner",
                "teacher_model": model_id,
                "model_version": revision,
                "prompt_version": PROMPT_VERSION,
                "prompt": prompt,
                "raw_response": raw,
                "request_id": request_id,
                "usage": usage,
                "enable_thinking": bool(config.get("enable_thinking", False)),
            },
        )
        refined = build_refined_record(
            original=record,
            parsed_output=parsed_output,
            raw=raw,
            parse_status=parse_status,
            parse_error=parse_error,
            before_checks=before_checks,
            after_checks=after_checks,
            latency_seconds=latency,
            request_id=request_id,
            usage=usage,
            raw_path=raw_path,
            model_id=model_id,
            model_version=revision,
            config=config,
        )
        append_jsonl(args.output, [refined])
        records.append(refined)
    if args.resume and args.output.exists():
        existing = read_jsonl(args.output)
        generated_originals = {row.get("original_candidate_id") for row in records}
        records = [row for row in existing if row.get("original_candidate_id") in {item.get("candidate_id") for item in selected}] + [
            row for row in records if row.get("original_candidate_id") not in generated_originals
        ]
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run targeted Qwen3 evidence refinement on teacher candidates.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stats-output", type=Path, default=DEFAULT_STATS)
    parser.add_argument("--audit-md-output", type=Path, default=DEFAULT_AUDIT_MD)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--qwen-config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--qwen-model", default=None)
    parser.add_argument("--limit", type=int, default=0, help="Maximum candidates to refine after filtering; 0 means all.")
    parser.add_argument("--max-new-tokens", type=int, default=0)
    parser.add_argument("--max-input-length", type=int, default=0)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Select and audit candidates without loading Qwen.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.input = resolve(args.input)
    args.output = resolve(args.output)
    args.stats_output = resolve(args.stats_output)
    args.audit_md_output = resolve(args.audit_md_output)
    args.raw_dir = resolve(args.raw_dir)
    args.qwen_config = resolve(args.qwen_config)

    if args.output.exists() and args.overwrite:
        args.output.unlink()
    if args.output.exists() and not args.resume:
        raise FileExistsError(f"{args.output} exists; pass --overwrite or --resume")

    rows = read_jsonl(args.input)
    candidate_ids = [row.get("candidate_id") for row in rows]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Duplicate candidate_id in input")
    selected = [row for row in rows if needs_evidence_refinement(row)]
    if args.limit > 0:
        selected = selected[: args.limit]
    config = load_yaml(args.qwen_config)
    if args.dry_run:
        refined: list[dict[str, Any]] = []
    else:
        refined = generate_refinements(args, config, selected)
    summary = summarize(rows, selected, refined)
    summary["input_file"] = str(args.input)
    summary["output_file"] = str(args.output)
    summary["dry_run"] = bool(args.dry_run)
    summary["selected_original_candidate_ids"] = [row.get("candidate_id") for row in selected]
    write_json(args.stats_output, summary, args.overwrite)
    write_text(args.audit_md_output, audit_markdown(summary, refined), args.overwrite)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
