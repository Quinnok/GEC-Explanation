from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "configs" / "rulefaith" / "verifier_calibration.yaml"


def display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def as_float(value: str) -> Optional[float]:
    if value in {"", "None", "nan", "NaN"}:
        return None
    return float(value)


def metric_map(rows: List[Dict[str, str]]) -> Dict[tuple[str, str], Dict[str, Any]]:
    out = {}
    for row in rows:
        converted: Dict[str, Any] = dict(row)
        for key in [
            "accuracy",
            "auprc",
            "auroc",
            "macro_f1",
            "positive_f1",
            "negative_f1",
            "positive_precision",
            "positive_recall",
            "negative_precision",
            "negative_recall",
        ]:
            converted[key] = as_float(row.get(key, ""))
        for key in ["n", "positive_count", "negative_count", "tp", "tn", "fp", "fn"]:
            converted[key] = int(float(row[key])) if row.get(key) not in {"", None} else None
        out[(row["method"], row["target"])] = converted
    return out


def m(metrics: Dict[tuple[str, str], Dict[str, Any]], method: str, target: str, key: str) -> Optional[float]:
    row = metrics.get((method, target), {})
    value = row.get(key)
    return float(value) if value is not None else None


def ge(value: Optional[float], threshold: float) -> bool:
    return value is not None and value >= threshold


def summarize_gate(metrics: Dict[tuple[str, str], Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, Any]:
    primary = config["primary_verifier"]
    gate = config["gate_a"]
    checks = {
        "edit_alignment_auroc": {
            "value": m(metrics, primary, "edit_alignment_binary", "auroc"),
            "threshold": gate["edit_alignment_auroc_min"],
        },
        "rule_auroc": {
            "value": m(metrics, primary, "rule_correctness_binary", "auroc"),
            "threshold": gate["rule_auroc_min"],
        },
        "evidence_auroc": {
            "value": m(metrics, primary, "evidence_binary", "auroc"),
            "threshold": gate["evidence_auroc_min"],
        },
        "target_masked_alignment_auroc": {
            "value": m(metrics, "target_masked_score", "edit_alignment_binary", "auroc"),
            "threshold": gate["target_masked_alignment_auroc_min"],
        },
    }
    for item in checks.values():
        item["passed"] = ge(item["value"], item["threshold"])

    rule_primary = m(metrics, primary, "rule_correctness_binary", "auroc")
    rule_recon = m(metrics, "reverse_reconstruction", "rule_correctness_binary", "auroc")
    evidence_primary = m(metrics, primary, "evidence_binary", "auroc")
    evidence_recon = m(metrics, "reverse_reconstruction", "evidence_binary", "auroc")
    comparative = {
        "rule_above_reconstruction": {
            "primary": rule_primary,
            "reconstruction": rule_recon,
            "delta": None if rule_primary is None or rule_recon is None else rule_primary - rule_recon,
            "passed": rule_primary is not None and rule_recon is not None and rule_primary > rule_recon,
        },
        "evidence_above_reconstruction": {
            "primary": evidence_primary,
            "reconstruction": evidence_recon,
            "delta": None if evidence_primary is None or evidence_recon is None else evidence_primary - evidence_recon,
            "passed": evidence_primary is not None and evidence_recon is not None and evidence_primary > evidence_recon,
        },
    }
    passed = all(item["passed"] for item in checks.values()) and all(item["passed"] for item in comparative.values())
    return {
        "status": "conditional_pass" if passed else "fail",
        "checks": checks,
        "comparative_checks": comparative,
        "caveats": [
            "Gate A is calibrated on Round 15 pressure-test labels, not new natural explanations.",
            "Evidence Macro-F1 remains low because positive evidence labels are sparse; AUROC passes the pre-registered threshold.",
            "Target-masked reconstruction remains useful for edit alignment but not for rule/evidence correctness.",
        ],
    }


def write_error_cases(path: Path, source_error_cases: Path, gate: Dict[str, Any]) -> None:
    source_text = source_error_cases.read_text(encoding="utf-8") if source_error_cases.exists() else ""
    first_sections = source_text.split("\n## ")
    excerpt = "\n## ".join(first_sections[:4]).strip()
    lines = [
        "# RuleFaith Verifier Error Cases",
        "",
        "This file links Round 19 verifier calibration to the earlier human-gold stress-test cases.",
        "",
        "## Gate A Summary",
        "",
        f"- Status: `{gate['status']}`",
        f"- Rule AUROC delta over reverse reconstruction: `{gate['comparative_checks']['rule_above_reconstruction']['delta']}`",
        f"- Evidence AUROC delta over reverse reconstruction: `{gate['comparative_checks']['evidence_above_reconstruction']['delta']}`",
        "",
        "## Reused Stress-Test Case Excerpt",
        "",
        excerpt,
        "",
        "## Interpretation",
        "",
        "High reconstruction with low rule/evidence quality remains the main failure mode. RuleFaith should use reconstruction only as an alignment signal and must train against rule/evidence failures separately.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_design_doc(path: Path, calibration_csv: Path, metrics_json: Path, gate: Dict[str, Any]) -> None:
    lines = [
        "# RuleFaith Verifier Design",
        "",
        "Created: 2026-07-19",
        "",
        "## Role in RuleFaith-GEC",
        "",
        "The verifier stack scores teacher and student explanations along separate dimensions: edit validity, edit alignment, rule correctness, evidence correctness, leakage, and genericness. Reverse reconstruction is retained only as an edit-alignment signal.",
        "",
        "## Round 19 Calibration Source",
        "",
        "- Human labels: `annotation/round15/annotation_final_gold_v2.csv`",
        "- Metric table: `results/human_gold/main_metric_table.csv`",
        f"- Calibration output: `{display(calibration_csv)}`",
        f"- Gate output: `{display(metrics_json)}`",
        "",
        "## Gate A Result",
        "",
        f"- Status: `{gate['status']}`",
        f"- Edit Alignment AUROC: `{gate['checks']['edit_alignment_auroc']['value']}`",
        f"- Rule AUROC: `{gate['checks']['rule_auroc']['value']}`",
        f"- Evidence AUROC: `{gate['checks']['evidence_auroc']['value']}`",
        f"- Target-masked alignment AUROC: `{gate['checks']['target_masked_alignment_auroc']['value']}`",
        "",
        "## Design Decision",
        "",
        "Proceed to method-pilot filtering with the current verifier as a calibration baseline, but do not claim final generation quality until natural teacher candidates and human evaluation are available.",
        "",
        "## Required Next Improvements",
        "",
        "- Add an explicit edit-validity gate for invalid and stylistic edits.",
        "- Add rule/evidence-specific failure mining for natural teacher outputs.",
        "- Add leakage and genericness penalties before preference data construction.",
        "- Avoid using the same LLM as both sole teacher and sole final judge.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def calibrate(args: argparse.Namespace) -> None:
    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    metric_path = ROOT / config["human_gold_metrics"]
    rows = read_csv(metric_path)
    methods = [config["primary_verifier"]] + list(config["comparators"])
    targets = [
        "faithfulness_binary",
        "edit_alignment_binary",
        "rule_correctness_binary",
        "evidence_binary",
        "edit_validity_binary",
    ]
    selected = [
        row
        for row in rows
        if row["method"] in methods and row["target"] in targets
    ]
    selected = sorted(selected, key=lambda row: (row["method"], row["target"]))
    metrics = metric_map(rows)
    gate = summarize_gate(metrics, config)
    out_metrics = ROOT / config["output_metrics"]
    out_csv = ROOT / config["output_calibration"]
    out_errors = ROOT / config["output_error_cases"]
    design_doc = ROOT / "docs" / "rulefaith_verifier_design.md"

    write_csv(
        out_csv,
        selected,
        [
            "method",
            "target",
            "n",
            "accuracy",
            "macro_f1",
            "auroc",
            "auprc",
            "positive_count",
            "negative_count",
            "positive_f1",
            "negative_f1",
            "tp",
            "tn",
            "fp",
            "fn",
        ],
    )
    write_json(
        out_metrics,
        {
            "config": display(args.config),
            "human_gold_metrics": config["human_gold_metrics"],
            "calibration_source": config["calibration_source"],
            "primary_verifier": config["primary_verifier"],
            "gate_a": gate,
            "selected_metric_rows": len(selected),
            "status_note": "conditional_pass means verifier calibration is adequate for method-pilot filtering, not final generation proof.",
        },
    )
    write_error_cases(out_errors, ROOT / config["human_gold_error_cases"], gate)
    write_design_doc(design_doc, out_csv, out_metrics, gate)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    return parser.parse_args()


if __name__ == "__main__":
    calibrate(parse_args())
