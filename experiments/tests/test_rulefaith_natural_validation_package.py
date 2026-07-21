from __future__ import annotations

import csv
import json
import unittest
import zipfile
from pathlib import Path

from experiments.rulefaith import build_natural_validation_package as package


class RuleFaithNaturalValidationPackageTest(unittest.TestCase):
    def test_package_builds_two_blind_items_per_group(self) -> None:
        direct = package.read_jsonl(package.DEFAULT_DIRECT)
        ready = package.read_csv(package.DEFAULT_READY)
        scores = package.read_csv(package.DEFAULT_SCORES)
        items, key_rows, stats = package.build_items(direct, ready, scores, seed=20260721)
        self.assertEqual(46, stats["item_count"])
        self.assertEqual(23, stats["edit_group_count"])
        self.assertEqual(23, stats["system_counts"]["rulefaith_score_top1"])
        self.assertEqual(46, len(key_rows))
        groups = {}
        for item in items:
            groups.setdefault(item["edit_group_id"], set()).add(item["system_id"])
        self.assertTrue(all("rulefaith_score_top1" in systems for systems in groups.values()))
        self.assertTrue(all(any(system.startswith("qwen3_direct_") for system in systems) for systems in groups.values()))

    def test_public_forms_do_not_expose_system_or_pseudo_labels(self) -> None:
        form_path = package.DEFAULT_OUTPUT_DIR / "form_annotator_a.csv"
        with form_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(46, len(rows))
        forbidden = {
            "system_id",
            "system_label",
            "source_candidate_id",
            "rulefaith_score",
            "rulefaith_bucket",
            "validator_overall_decision",
            "pseudo_overall_decision",
        }
        self.assertTrue(forbidden.isdisjoint(rows[0].keys()))
        for row in rows:
            for label in package.LABEL_COLUMNS:
                self.assertEqual("", row[label])

    def test_handoff_zip_excludes_hidden_key(self) -> None:
        zip_path = package.DEFAULT_OUTPUT_DIR / "rulefaith_natural_validation_handoff.zip"
        with zipfile.ZipFile(zip_path) as zf:
            names = set(zf.namelist())
        self.assertIn("form_annotator_a.csv", names)
        self.assertIn("form_annotator_b.csv", names)
        self.assertIn("guidelines.md", names)
        self.assertNotIn("hidden_system_key.csv", names)

    def test_manifest_matches_package_counts(self) -> None:
        manifest_path = package.DEFAULT_OUTPUT_DIR / "manifest.json"
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(46, payload["stats"]["item_count"])
        self.assertEqual(23, payload["stats"]["edit_group_count"])
        self.assertEqual(["hidden_system_key.csv"], payload["hidden_files_not_in_zip"])


if __name__ == "__main__":
    unittest.main()
