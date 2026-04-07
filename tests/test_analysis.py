"""Regression tests for the MBSE model registry."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mbse_model_registry.analysis import analyze_packages
from mbse_model_registry.cli import run
from mbse_model_registry.data import load_packages


DATA_FILE = ROOT / "data" / "model_packages.json"


class ModelRegistryTests(unittest.TestCase):
    def test_clean_dataset_passes(self) -> None:
        result = analyze_packages(load_packages(DATA_FILE))
        self.assertEqual(result.errors, [])
        self.assertEqual(result.summary["package_count"], 5)

    def test_missing_views_is_detected(self) -> None:
        packages = load_packages(DATA_FILE)
        packages[0]["view_types"] = []
        result = analyze_packages(packages)
        self.assertTrue(any("view_types must contain at least one entry" in item for item in result.errors))

    def test_cli_exports_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            exit_code = run(["catalog", "--data-file", str(DATA_FILE), "--export-dir", temp_dir])
            self.assertEqual(exit_code, 0)
            export_dir = Path(temp_dir)
            self.assertTrue((export_dir / "model-summary.md").exists())
            self.assertTrue((export_dir / "model-catalog.csv").exists())
            self.assertTrue((export_dir / "repo-coverage.csv").exists())
            self.assertTrue((export_dir / "model-dashboard.html").exists())


if __name__ == "__main__":
    unittest.main()
