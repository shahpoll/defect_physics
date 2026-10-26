"""Evidence-preservation checks, independent of the physics implementations."""

import json
from pathlib import Path
import tempfile
import unittest

from siv_study.run_support import check_finite, execute, file_hash


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.input = self.base / "input.json"
        self.input.write_text('{"a": 1}\n')
        self.output = self.base / "run"

    def manifest(self):
        return json.loads((self.output / "manifest.json").read_text())

    def test_invalid_input_is_preserved_and_failed(self):
        self.input.write_text('{bad json')
        self.assertEqual(execute("test", lambda c, p: {}, self.input, self.output), 1)
        self.assertEqual(self.manifest()["status"], "FAILED")
        self.assertEqual((self.output / "provenance/input.json").read_bytes(), self.input.read_bytes())
        self.assertEqual(self.manifest()["failure"]["type"], "JSONDecodeError")
        self.assertIn("JSONDecodeError", (self.output / "execution.log").read_text())

    def test_existing_output_is_untouched(self):
        self.output.mkdir()
        marker = self.output / "keep.txt"
        marker.write_text("original evidence")
        before = file_hash(marker)
        with self.assertRaises(FileExistsError):
            execute("test", lambda c, p: {}, self.input, self.output)
        self.assertEqual(before, file_hash(marker))
        self.assertEqual(list(self.output.iterdir()), [marker])

    def test_missing_input_has_typed_failure(self):
        self.input.unlink()
        self.assertEqual(execute("test", lambda c, p: {}, self.input, self.output), 1)
        self.assertEqual(self.manifest()["failure"]["type"], "FileNotFoundError")

    def test_nonfinite_metrics_cannot_complete(self):
        self.assertEqual(execute("test", lambda c, p: {"x": float("nan")}, self.input, self.output), 1)
        self.assertEqual(self.manifest()["status"], "FAILED")
        self.assertIn("nonfinite", self.manifest()["failure"]["message"])
        self.assertFalse((self.output / "metrics.json").exists())

    def test_nonfinite_inputs_cannot_complete(self):
        self.input.write_text('{"a": NaN}')
        self.assertEqual(execute("test", lambda c, p: {"x": 1}, self.input, self.output), 1)
        self.assertEqual(self.manifest()["status"], "FAILED")

    def test_missing_figures_and_tables_cannot_complete(self):
        self.assertEqual(execute("test", lambda c, p: {"x": 1, "checks": {"one": True}, "all_checks_passed": True}, self.input, self.output), 1)
        self.assertEqual(self.manifest()["status"], "FAILED")
        self.assertIn("PNG and CSV", self.manifest()["failure"]["message"])

    def test_failed_mathematical_check_cannot_complete(self):
        self.assertEqual(execute("test", lambda c, p: {"checks": {"one": False}, "all_checks_passed": False}, self.input, self.output), 1)
        self.assertIn("passing mathematical checks", self.manifest()["failure"]["message"])

    def test_interrupt_is_preserved(self):
        def stop(config, output):
            raise KeyboardInterrupt()
        self.assertEqual(execute("test", stop, self.input, self.output), 130)
        self.assertEqual(self.manifest()["status"], "INTERRUPTED")
        self.assertEqual(self.manifest()["failure"]["type"], "KeyboardInterrupt")

    def test_preserved_code_matches_recorded_hash(self):
        execute("test", lambda c, p: {}, self.input, self.output)
        for name, digest in self.manifest()["source_sha256"].items():
            self.assertEqual(file_hash(self.output / "provenance/code" / name), digest)

    def test_nested_nonfinite_numbers(self):
        with self.assertRaisesRegex(ValueError, r"metrics.a\[1\].b"):
            check_finite({"a": [0, {"b": float("inf")}]})


if __name__ == "__main__":
    unittest.main()
