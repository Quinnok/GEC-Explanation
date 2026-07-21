import unittest

from experiments.rulefaith import repair_qwen3_needs_refinement as repair
from experiments.rulefaith import select_qwen3_field_aware_rulefaith as field_select
from experiments.rulefaith import validate_qwen3_target_masked as target_masked


class Qwen3TargetedRepairTest(unittest.TestCase):
    def row(self, reasons=None):
        return {
            "candidate_id": "c1",
            "source": "The students goes to school .",
            "model_prediction": "The students go to school .",
            "model_edit": {
                "operation": "replace",
                "start": 2,
                "end": 3,
                "source_text": "goes",
                "target_text": "go",
                "error_type": "R:VERB:SVA",
            },
            "parsed_output": {
                "rule_text": "Plural subjects require the base present-tense verb form.",
                "rationale": "Replace goes with go because the subject is plural.",
                "evidence_spans": [{"text": "students", "start": 1, "end": 2, "role": "grammatical_subject"}],
                "confidence": 0.95,
            },
            "rulefaith_rule_plausibility_audit": {
                "reasons": reasons or ["rationale_edit_copy"],
            },
        }

    def test_replaces_rationale_edit_copy(self):
        repaired = repair.repair_row(self.row())
        self.assertFalse(field_select.leakage_by_field(repaired)["rationale_edit_copy"])
        self.assertIn("students", repaired["parsed_output"]["rationale"])
        self.assertIn("replaced_rationale_edit_copy", repaired["rulefaith_targeted_repair"]["actions"])

    def test_appends_evidence_to_rationale(self):
        row = self.row(["evidence_not_mentioned_in_rule_or_rationale"])
        row["parsed_output"]["rationale"] = "This rule applies to the sentence."
        repaired = repair.repair_row(row)
        self.assertTrue(target_masked.evidence_mentioned_in_text(repaired, repaired["parsed_output"]["rationale"]))
        self.assertIn("appended_source_evidence_to_rationale", repaired["rulefaith_targeted_repair"]["actions"])

    def test_caps_high_confidence(self):
        repaired = repair.repair_row(self.row(["evidence_not_mentioned_in_rule_or_rationale"]))
        self.assertEqual(repaired["parsed_output"]["confidence"], 0.8)
        self.assertIn("capped_confidence_at_0.8", repaired["rulefaith_targeted_repair"]["actions"])


if __name__ == "__main__":
    unittest.main()
