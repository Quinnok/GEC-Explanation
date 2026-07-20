import csv
import tempfile
import unittest
from pathlib import Path

from experiments.rulefaith import prepare_qwen3_audit_handoff as handoff
from experiments.rulefaith import validate_qwen3_human_audit as validate


class Qwen3HumanAuditToolsTest(unittest.TestCase):
    def write_csv(self, path: Path, rows):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    def complete_form_row(self):
        row = {
            "candidate_id": "c1",
            "source": "The students goes .",
            "model_prediction": "The students go .",
            "human_notes": "",
            "human_decision": "accept",
        }
        for field in validate.ISSUE_FIELDS:
            row[field] = "no"
        return row

    def test_validate_completed_form_and_merge_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            form = tmp_path / "form.csv"
            key = tmp_path / "key.csv"
            self.write_csv(form, [self.complete_form_row()])
            self.write_csv(
                key,
                [
                    {
                        "candidate_id": "c1",
                        "bucket": "accepted",
                        "audit_priority": "p",
                        "candidate_type": "natural",
                        "behavior": "correct_correction",
                        "error_type": "R:VERB",
                        "risk_count": "0",
                        "risk_reasons": "",
                    }
                ],
            )
            summary, merged = validate.validate_rows(validate.read_csv(form), validate.read_csv(key), allow_incomplete=False)
            self.assertTrue(summary["is_complete"])
            self.assertEqual(summary["decision_counts"], {"accept": 1})
            self.assertEqual(merged[0]["bucket"], "accepted")

    def test_incomplete_form_allowed_only_with_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            form = tmp_path / "form.csv"
            key = tmp_path / "key.csv"
            incomplete = self.complete_form_row()
            incomplete["human_decision"] = ""
            self.write_csv(form, [incomplete])
            self.write_csv(key, [{"candidate_id": "c1"}])
            with self.assertRaises(ValueError):
                validate.validate_rows(validate.read_csv(form), validate.read_csv(key), allow_incomplete=False)
            summary, _ = validate.validate_rows(validate.read_csv(form), validate.read_csv(key), allow_incomplete=True)
            self.assertFalse(summary["is_complete"])

    def test_handoff_form_rejects_hidden_key_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            form = tmp_path / "form.csv"
            key = tmp_path / "key.csv"
            row = self.complete_form_row()
            row["bucket"] = "accepted"
            self.write_csv(form, [row])
            self.write_csv(key, [{"candidate_id": "c1"}])
            with self.assertRaises(ValueError):
                handoff.validate_form(form, key, expected_rows=1)


if __name__ == "__main__":
    unittest.main()
