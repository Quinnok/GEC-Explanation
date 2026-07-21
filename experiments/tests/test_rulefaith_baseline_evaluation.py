from __future__ import annotations

import unittest

from experiments.rulefaith import evaluate_rulefaith_baselines as baselines


class RuleFaithBaselineEvaluationTest(unittest.TestCase):
    def test_teacher_baselines_include_qwen2_and_qwen3_same_setting(self) -> None:
        rows = baselines.teacher_baseline_rows()
        by_system = {row["system"]: row for row in rows}
        self.assertIn("Qwen2.5-0.5B direct", by_system)
        self.assertIn("Qwen3-8B direct", by_system)
        self.assertEqual("160", by_system["Qwen2.5-0.5B direct"]["n"])
        self.assertEqual("160", by_system["Qwen3-8B direct"]["n"])
        self.assertGreater(
            int(by_system["Qwen3-8B direct"]["accepted"]),
            int(by_system["Qwen2.5-0.5B direct"]["accepted"]),
        )
        self.assertLess(
            float(by_system["Qwen3-8B direct"]["rule_edit_copy_rate"]),
            float(by_system["Qwen2.5-0.5B direct"]["rule_edit_copy_rate"]),
        )

    def test_method_gate_rows_preserve_pseudo_validation_boundary(self) -> None:
        rows = baselines.method_gate_rows()
        self.assertEqual("Qwen3 direct prefilter", rows[0]["stage"])
        self.assertEqual("Codex pseudo-validation", rows[-1]["stage"])
        self.assertEqual("41", rows[-1]["n"])
        self.assertEqual("codex_ai_pseudo_validation_not_human", rows[-1]["label_source"])

    def test_selection_baselines_cover_twenty_three_edit_groups(self) -> None:
        rows = baselines.selection_baseline_rows()
        by_strategy = {row["strategy"]: row for row in rows}
        self.assertEqual("23", by_strategy["First candidate"]["edit_groups"])
        self.assertEqual("23", by_strategy["Rule-grounded candidate"]["edit_groups"])
        self.assertEqual("23", by_strategy["Pseudo-validator selective accept"]["edit_groups"])
        self.assertEqual("11", by_strategy["Pseudo-validator selective accept"]["covered_groups"])
        self.assertEqual("1.000", by_strategy["Pseudo-validator selective accept"]["accept_rate"])
        self.assertGreater(
            float(by_strategy["Rule-grounded candidate"]["accept_rate"]),
            float(by_strategy["First candidate"]["accept_rate"]),
        )


if __name__ == "__main__":
    unittest.main()
