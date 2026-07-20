import unittest

from experiments.rulefaith import canonicalize_evidence_spans as canon


class EvidenceSpanCanonicalizerTest(unittest.TestCase):
    def candidate(self, spans):
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
            "candidate_type": "natural",
            "parsed_output": {
                "edit_description": "The model replaces goes with go.",
                "edit_validity": "valid",
                "rule_text": "Plural subjects take the base verb form.",
                "evidence_spans": spans,
                "applicability_conditions": ["plural subject"],
                "rationale": "The plural subject requires the base verb.",
                "confidence": 0.8,
                "abstain": False,
                "abstain_reason": "",
            },
        }

    def test_find_token_sequence(self):
        self.assertEqual(canon.find_token_sequence("The students goes .", "students"), [(1, 2)])

    def test_corrects_wrong_indices(self):
        record = self.candidate([{"text": "students", "start": 2, "end": 3, "role": "grammatical_subject"}])
        output, actions = canon.canonicalize_record(record, drop_prediction_only=True)
        span = output["parsed_output"]["evidence_spans"][0]
        self.assertEqual((span["start"], span["end"]), (1, 2))
        self.assertEqual(actions["corrected_indices"], 1)
        self.assertTrue(output["after_evidence_checks"]["evidence_contextual"])

    def test_drops_prediction_only_target(self):
        record = self.candidate([{"text": "go", "start": 2, "end": 3, "role": "correction"}])
        output, actions = canon.canonicalize_record(record, drop_prediction_only=True)
        self.assertEqual(output["parsed_output"]["evidence_spans"], [])
        self.assertEqual(actions["dropped_prediction_only_span"], 1)


if __name__ == "__main__":
    unittest.main()
