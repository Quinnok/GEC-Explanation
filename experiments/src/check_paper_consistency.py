from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[2]


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def pdf_pages(path: Path) -> int | None:
    try:
        output = subprocess.check_output(["pdfinfo", str(path)], text=True)
    except Exception:
        return None
    match = re.search(r"^Pages:\s+(\d+)$", output, re.MULTILINE)
    return int(match.group(1)) if match else None


def log_clean(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    patterns = [
        "LaTeX Warning",
        "Citation.*undefined",
        "Reference.*undefined",
        "Undefined control sequence",
        "Fatal error",
        "Overfull",
        "Underfull",
    ]
    return not re.search("|".join(patterns), text)


def bibliography_start_page(path: Path) -> int | None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"\(\./main\.bbl.*?\[(\d+)\]", text, re.DOTALL)
    if match and match.group(1):
        return int(match.group(1))
    return None


def section_inputs(main_tex: str) -> List[str]:
    return re.findall(r"\\input\{sections/([^}]+)\}", main_tex)


def check() -> Dict[str, Any]:
    main_tex = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
    paper_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted((ROOT / "paper" / "sections").glob("*.tex")))
    asset_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted((ROOT / "results" / "paper_assets").glob("*.tex")))
    searchable_paper_text = paper_text + "\n" + asset_text
    manifest = read_json(ROOT / "results" / "paper_assets" / "manifest.json")
    stats = read_json(ROOT / "data" / "faithfulness_benchmark" / "benchmark_stats.json")
    human = read_json(ROOT / "results" / "round10" / "human_annotation_status.json")
    required_sections = [
        "abstract",
        "introduction",
        "related_work",
        "problem_formulation",
        "benchmark_data",
        "method",
        "experimental_setup",
        "results",
        "ablation",
        "human_evaluation",
        "analysis",
        "error_analysis",
        "limitations",
        "ethics",
        "conclusion",
    ]
    inputs = section_inputs(main_tex)
    generated_assets = manifest["generated_files"]
    result_numbers_present = all(
        token in searchable_paper_text
        for token in [
            str(stats["edit_count"]),
            str(stats["explanation_instance_count"]),
            "0.640",
            "0.439",
            "0.297",
            "0.935",
            human["status"].replace("_", r"\_"),
        ]
    )
    main_pages = pdf_pages(ROOT / "paper" / "main.pdf")
    bib_start = bibliography_start_page(ROOT / "paper" / "main.log")
    total_page_status = "ok_9_pages_or_less" if (main_pages or 99) <= 9 else "over_9_pages"
    technical_page_status = (
        "ok_references_start_by_page_7"
        if (main_pages or 99) <= 9 and (bib_start is None or bib_start <= 7)
        else "check_main_content_length"
    )
    return {
        "main_pdf_pages": main_pages,
        "bibliography_start_page_from_log": bib_start,
        "main_total_page_limit_status": total_page_status,
        "main_technical_page_limit_status": technical_page_status,
        "appendix_pdf_pages": pdf_pages(ROOT / "paper" / "supplementary" / "appendix.pdf"),
        "anonymous_submission": "Anonymous Submission" in main_tex and "\\affiliations{}" in main_tex,
        "uses_aaai2027_submission_style": "\\usepackage[submission]{aaai2027}" in main_tex,
        "required_sections_present": {section: section in inputs for section in required_sections},
        "result_pending_placeholders": paper_text.count("[RESULT-PENDING]"),
        "generated_asset_count": len(generated_assets),
        "generated_assets": generated_assets,
        "required_asset_count_status": "ok" if len(generated_assets) >= 8 else "too_few",
        "main_latex_log_clean": log_clean(ROOT / "paper" / "main.log"),
        "appendix_latex_log_clean": log_clean(ROOT / "paper" / "supplementary" / "appendix.log"),
        "result_numbers_present_in_paper": result_numbers_present,
        "human_gold_count": stats["human_gold_count"],
        "human_annotation_status": human["status"],
        "no_human_claim_status": "ok_blocked_reported" if human["status"] == "blocked_no_human_annotation" else "check_human_labels",
    }


def main() -> None:
    result = check()
    out = ROOT / "results" / "round12" / "paper_consistency_check.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
