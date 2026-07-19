from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def classify(flag: Dict[str, Any]) -> str:
    if flag.get("parse_status") != "parsed_json":
        return "rejected"
    if not flag.get("alignment_proxy_pass"):
        return "rejected"
    if flag.get("missing_rule_text"):
        return "rejected"
    if not flag.get("rule_is_edit_copy") and flag.get("has_contextual_evidence"):
        return "accepted"
    if not flag.get("rule_is_edit_copy") or flag.get("has_contextual_evidence"):
        return "refine"
    return "rejected"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply a conservative RuleFaith prefilter to teacher candidates.")
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--diagnostics", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--stats", type=Path, required=True)
    parser.add_argument("--prefix", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    candidates = {row["candidate_id"]: row for row in read_jsonl(resolve(args.candidates))}
    diagnostics = json.loads(resolve(args.diagnostics).read_text(encoding="utf-8"))
    buckets: Dict[str, List[Dict[str, Any]]] = {"accepted": [], "refine": [], "rejected": []}
    reasons: Counter[str] = Counter()
    for flag in diagnostics.get("flags", []):
        candidate_id = flag["candidate_id"]
        row = candidates.get(candidate_id)
        if row is None:
            reasons["missing_candidate"] += 1
            continue
        bucket = classify(flag)
        enriched = dict(row)
        enriched["rulefaith_prefilter"] = {
            "bucket": bucket,
            "alignment_proxy_pass": flag.get("alignment_proxy_pass"),
            "rule_is_edit_copy": flag.get("rule_is_edit_copy"),
            "missing_rule_text": flag.get("missing_rule_text"),
            "has_contextual_evidence": flag.get("has_contextual_evidence"),
            "parse_status": flag.get("parse_status"),
            "raw_markdown_json": flag.get("raw_markdown_json"),
            "high_risk": flag.get("high_risk"),
        }
        buckets[bucket].append(enriched)
        if flag.get("parse_status") != "parsed_json":
            reasons["non_json_or_wrapped"] += 1
        if not flag.get("alignment_proxy_pass"):
            reasons["alignment_proxy_fail"] += 1
        if flag.get("missing_rule_text"):
            reasons["missing_rule_text"] += 1
        if flag.get("rule_is_edit_copy"):
            reasons["rule_edit_copy"] += 1
        if not flag.get("has_contextual_evidence"):
            reasons["weak_or_missing_contextual_evidence"] += 1

    output_dir = resolve(args.output_dir)
    for bucket, rows in buckets.items():
        write_jsonl(output_dir / f"{args.prefix}_{bucket}.jsonl", rows)
    total = sum(len(rows) for rows in buckets.values())
    stats = {
        "candidate_count": total,
        "bucket_counts": {bucket: len(rows) for bucket, rows in buckets.items()},
        "bucket_rates": {bucket: round(len(rows) / total, 4) if total else 0.0 for bucket, rows in buckets.items()},
        "provider_counts": dict(Counter(row.get("provider", "") for rows in buckets.values() for row in rows)),
        "candidate_type_counts": dict(Counter(row.get("candidate_type", "") for rows in buckets.values() for row in rows)),
        "risk_reason_counts": dict(reasons),
        "policy": {
            "accepted": "parsed JSON, alignment proxy pass, explicit non-edit-copy rule, contextual evidence present",
            "refine": "parsed JSON, alignment proxy pass, explicit rule, and at least one of non-edit-copy rule or contextual evidence",
            "rejected": "all remaining candidates",
        },
    }
    write_json(resolve(args.stats), stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
