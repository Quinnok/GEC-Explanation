from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from experiments.rulefaith import complete_qwen3_ready_validation_codex as complete


class Qwen3ReadyValidationCodexTest(unittest.TestCase):
    def test_label_map_covers_default_form(self) -> None:
        rows, _ = complete.read_csv(complete.DEFAULT_FORM)
        complete.validate_ids(rows)
        completed = complete.completed_rows(rows)
        self.assertEqual(len(completed), 41)
        self.assertEqual(
            {"accept": 17, "refine": 13, "reject": 11},
            dict(__import__("collections").Counter(row["validator_overall_decision"] for row in completed)),
        )

    def test_outputs_are_written_with_label_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            rows, form_fields = complete.read_csv(complete.DEFAULT_FORM)
            key_rows, _ = complete.read_csv(complete.DEFAULT_KEY)
            completed = complete.completed_rows(rows)
            merged, merged_fields = complete.merge_with_key(completed, key_rows)
            out = tmp / "completed.csv"
            merged_out = tmp / "merged.csv"
            complete.write_csv(out, completed, form_fields, overwrite=False)
            complete.write_csv(merged_out, merged, merged_fields, overwrite=False)
            with merged_out.open(newline="", encoding="utf-8") as handle:
                written = list(csv.DictReader(handle))
            self.assertEqual(41, len(written))
            self.assertTrue(all(row["label_source"] == complete.LABEL_SOURCE for row in written))


if __name__ == "__main__":
    unittest.main()
