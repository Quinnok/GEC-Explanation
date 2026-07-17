import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from edit_schema import Edit, compare_edits
from extract_edits import extract_token_diff_edits


class EditExtractionTests(unittest.TestCase):
    def test_replace_edit(self):
        edits = extract_token_diff_edits("She go home .", "She goes home .", error_type="SVA")
        self.assertEqual(len(edits), 1)
        self.assertEqual(edits[0], Edit(1, 2, "go", "goes", "replace", "SVA"))

    def test_insert_edit(self):
        edits = extract_token_diff_edits("I went school .", "I went to school .", error_type="PREP")
        self.assertEqual(edits[0], Edit(2, 2, "", "to", "insert", "PREP"))

    def test_compare_full_exact(self):
        gold = Edit(1, 2, "go", "goes", "replace", "SVA")
        pred = Edit(1, 2, "go", "goes", "replace", "SVA")
        metrics = compare_edits(pred, gold)
        self.assertEqual(metrics["full_edit_exact"], 1.0)
        self.assertEqual(metrics["span_f1"], 1.0)


if __name__ == "__main__":
    unittest.main()

