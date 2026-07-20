import unittest

from experiments.rulefaith import refine_qwen3_evidence as refine


class Qwen3EvidenceRefinementTest(unittest.TestCase):
    def candidate(self, evidence_spans):
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
            },
            "parsed_output": {
                "edit_description": "The model replaces goes with go.",
                "edit_validity": "valid",
                "rule_text": "Plural subjects take the base verb form.",
                "evidence_spans": evidence_spans,
                "applicability_conditions": ["plural subject"],
                "rationale": "The plural subject requires the base verb.",
                "confidence": 0.8,
                "abstain": False,
                "abstain_reason": "",
            },
        }

    def test_source_token_table_uses_whitespace_offsets(self):
        table = refine.source_token_table("A small test .")
        self.assertEqual(table.splitlines(), ["0: A", "1: small", "2: test", "3: ."])

    def test_needs_refinement_for_prediction_only_evidence(self):
        record = self.candidate([{"text": "go", "start": 2, "end": 3, "role": "correction"}])
        self.assertTrue(refine.needs_evidence_refinement(record))

    def test_does_not_need_refinement_for_contextual_source_evidence(self):
        record = self.candidate([{"text": "students", "start": 1, "end": 2, "role": "grammatical_subject"}])
        self.assertFalse(refine.needs_evidence_refinement(record))

    def test_refinement_prompt_includes_source_only_constraints(self):
        record = self.candidate([{"text": "go", "start": 2, "end": 3, "role": "correction"}])
        prompt = refine.refinement_prompt(record, refine.evidence_checks_for_record(record))
        self.assertIn("SOURCE_TOKENS", prompt)
        self.assertIn("MODEL_PREDICTION text", prompt)
        self.assertIn("Return exactly one JSON object", prompt)

    def test_parse_last_json_object_uses_final_balanced_object(self):
        raw = 'MODEL_EDIT: {"bad": true} </think> {"rule_text":"x","evidence_spans":[]}'
        parsed = refine.parse_last_json_object(raw)
        self.assertEqual(parsed, {"rule_text": "x", "evidence_spans": []})


if __name__ == "__main__":
    unittest.main()
