from __future__ import annotations

import unittest

from experiments.rulefaith import generate_rulefaith_paper_assets as assets


class RuleFaithPaperAssetsTest(unittest.TestCase):
    def test_qwen3_funnel_rows_are_generated_from_results(self) -> None:
        rows = assets.rows_from_results()
        self.assertEqual(5, len(rows))
        self.assertEqual("Field-aware gate", rows[0]["stage"])
        self.assertEqual("160", rows[0]["input"])
        self.assertEqual("58", rows[0]["kept"])
        self.assertEqual("Codex pseudo-validation", rows[-1]["stage"])
        self.assertEqual("41", rows[-1]["input"])
        self.assertEqual("17", rows[-1]["kept"])


if __name__ == "__main__":
    unittest.main()
