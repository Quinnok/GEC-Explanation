from __future__ import annotations

import json
from pathlib import Path


def summary_to_latex(summary_path: Path, output_path: Path) -> None:
    data = json.loads(summary_path.read_text())
    metrics = data.get("macro_average", {})
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "\\begin{tabular}{lr}",
        "\\toprule",
        "Metric & Value \\\\",
        "\\midrule",
    ]
    for key, value in sorted(metrics.items()):
        lines.append(f"{key.replace('_', ' ')} & {value:.3f} \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    output_path.write_text("\n".join(lines))


if __name__ == "__main__":
    summary_to_latex(Path("results/summary.json"), Path("results/tables/toy_summary.tex"))

