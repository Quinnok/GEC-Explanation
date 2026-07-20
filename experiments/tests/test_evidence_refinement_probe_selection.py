import unittest

from experiments.rulefaith import build_evidence_refinement_probe as probe


class EvidenceRefinementProbeSelectionTest(unittest.TestCase):
    def candidate(self, candidate_id, group, dataset, model_key, operation, spans):
        return {
            "candidate_id": candidate_id,
            "rulefaith_pool_id": group,
            "dataset": dataset,
            "model_key": model_key,
            "model_family": "family-" + model_key,
            "rulefaith_split": "train",
            "candidate_type": "evidence_canonicalized",
            "original_candidate_type": "natural",
            "source": "The students goes to school .",
            "model_prediction": "The students go to school .",
            "model_edit": {
                "operation": operation,
                "start": 2,
                "end": 3,
                "source_text": "goes",
                "target_text": "go",
            },
            "parsed_output": {
                "rule_text": "Plural subjects take the base verb form.",
                "evidence_spans": spans,
                "rationale": "The subject controls the verb form.",
            },
        }

    def test_selects_only_remaining_evidence_failures_with_unique_groups(self):
        rows = [
            self.candidate("c1", "g1", "EXPECT", "gector", "replace", []),
            self.candidate("c2", "g1", "EXPECT", "gector", "replace", [{"text": "go", "start": 2, "end": 3, "role": "target"}]),
            self.candidate("c3", "g2", "JFLEG", "t5", "delete", []),
            self.candidate("c4", "g3", "JFLEG", "coedit", "insert", [{"text": "students", "start": 1, "end": 2, "role": "subject"}]),
        ]
        selected = probe.select_probe(rows, limit=2, seed=7)
        self.assertEqual(len(selected), 2)
        self.assertEqual(len({probe.group_key(row) for row in selected}), 2)
        self.assertTrue(all(row["probe_evidence_checks"]["missing_evidence"] or row["probe_evidence_checks"]["wrong_evidence_auto"] for row in selected))
        self.assertNotIn("c4", {row["candidate_id"] for row in selected})


if __name__ == "__main__":
    unittest.main()
