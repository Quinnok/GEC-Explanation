from __future__ import annotations

import unittest

from experiments.rulefaith import score_rulefaith_ready_candidates as scorer


class RuleFaithReadyCandidateScorerTest(unittest.TestCase):
    def test_score_row_does_not_read_validator_labels(self) -> None:
        rows = scorer.read_csv(scorer.DEFAULT_INPUT)
        row = dict(rows[0])
        altered = dict(row)
        altered["validator_overall_decision"] = "reject"
        altered["validator_rule_plausibility"] = "implausible"
        altered["validator_evidence_sufficiency"] = "insufficient"
        self.assertEqual(scorer.score_row(row), scorer.score_row(altered))

    def test_scored_rows_and_selection_summary_are_reproducible(self) -> None:
        rows = scorer.read_csv(scorer.DEFAULT_INPUT)
        scored = scorer.scored_rows(rows)
        metrics = scorer.selection_summary(scored)
        self.assertEqual(41, metrics["candidate_count"])
        self.assertEqual(23, metrics["edit_group_count"])
        self.assertEqual({"accept": 28, "refine": 9, "reject": 4}, metrics["score_bucket_counts"])
        self.assertEqual(23, metrics["top1_selection"]["covered_groups"])
        self.assertEqual(18, metrics["selective_selection"]["covered_groups"])
        self.assertEqual(0.3913, metrics["top1_selection"]["accept_rate"])


if __name__ == "__main__":
    unittest.main()
