"""Public-export tests use synthetic evidence, never a private project path."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.export_public_provenance import (  # noqa: E402
    EXERCISES, build_public_provenance, export_provenance,
    file_hash, relative_path, validate_public_artifacts,
)


def digest(value: bytes) -> str:
    return sha256(value).hexdigest()


class PublicProvenanceTests(unittest.TestCase):
    def setUp(self):
        # Remain inside the checkout even when the test runner's TMPDIR differs.
        self.scratch = tempfile.TemporaryDirectory(prefix=".provenance_test_", dir=ROOT)
        self.addCleanup(self.scratch.cleanup)
        self.base = Path(self.scratch.name)
        self.source = self.base / "local-evidence"
        self.output = self.base / "public-checkout"
        self.source.mkdir()
        self.output.mkdir()
        self.private_path = "/PRIVATE_FIXTURE_ONLY/student/notes"
        runner = b"print('synthetic fixture runner')\n"
        (self.source / "run_study.py").write_bytes(runner)
        (self.output / "run_study.py").write_bytes(runner)
        listed = []
        for name in EXERCISES:
            relative = Path("runs/first_study") / name
            source_run = self.source / relative
            output_run = self.output / relative
            source_run.mkdir(parents=True)
            output_run.mkdir(parents=True)
            input_bytes = (json.dumps({"exercise": name, "synthetic_fixture": True}) + "\n").encode()
            code = {"__init__.py": b"# synthetic snapshot\n", f"{name}.py": b"def compute(): return 1\n"}
            artifacts = {
                "provenance/input.json": input_bytes,
                "metrics.json": b'{"all_checks_passed": true, "value": 1}\n',
                "result.csv": b"x,y\n0,1\n",
                "figure.png": b"synthetic figure bytes used only for hash verification",
                "execution.log": ("Original fixture command at " + self.private_path + "\n").encode(),
            }
            for filename, content in code.items():
                artifacts[f"provenance/code/{filename}"] = content
            for filename, content in artifacts.items():
                path = source_run / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
                if filename != "execution.log":
                    public = output_run / filename
                    public.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(path, public)
            config = self.output / "data" / f"{name}.json"
            config.parent.mkdir(parents=True, exist_ok=True)
            config.write_bytes(input_bytes)
            manifest = {
                "exercise": name, "status": "COMPLETE",
                "started_at_utc": "2026-10-26T17:00:00+00:00",
                "finished_at_utc": "2026-10-26T17:00:01+00:00",
                "command": [self.private_path + "/python", "--input", self.private_path + "/input.json"],
                "working_directory": self.private_path,
                "python_executable": self.private_path + "/python",
                "input_requested": self.private_path + "/input.json",
                "output_directory": self.private_path + "/output",
                "python_version": "3.13.5", "platform": "synthetic-test-arm64",
                "packages": {"numpy": "2.3.4", "matplotlib": "3.10.7"},
                "input_sha256": digest(input_bytes),
                "source_sha256": {filename: digest(content) for filename, content in code.items()},
                "artifacts_sha256": {filename: digest(content) for filename, content in artifacts.items()},
            }
            (source_run / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
            listed.append({
                "exercise": name, "exit_code": 0, "manifest": f"{name}/manifest.json",
                "command": [self.private_path + "/python", "-m", name],
            })
        study = {
            "status": "COMPLETE", "started_at_utc": "2026-10-26T17:00:00+00:00",
            "finished_at_utc": "2026-10-26T17:00:03+00:00",
            "runs": listed, "runner_sha256": digest(runner),
        }
        (self.source / "runs/first_study/study_manifest.json").write_text(json.dumps(study, indent=2) + "\n")

    @staticmethod
    def inventory(root):
        return {str(path.relative_to(root)): file_hash(path) for path in root.rglob("*") if path.is_file()}

    def source_manifest(self, name="charge_states"):
        return self.source / "runs/first_study" / name / "manifest.json"

    def change_source_manifest(self, key, value):
        path = self.source_manifest()
        manifest = json.loads(path.read_text())
        manifest[key] = value
        path.write_text(json.dumps(manifest))

    def test_export_retains_exact_original_hashes_status_and_versions(self):
        record = export_provenance(self.source, self.output)
        study_hash = file_hash(self.source / "runs/first_study/study_manifest.json")
        self.assertEqual(record["study"]["original_local_study_manifest_sha256"], study_hash)
        self.assertFalse(record["policy"]["original_local_records_modified"])
        self.assertEqual(len(record["exercises"]), 3)
        for exercise in record["exercises"]:
            name = exercise["exercise"]
            self.assertEqual(exercise["original_local_manifest_sha256"], file_hash(self.source_manifest(name)))
            self.assertEqual(exercise["status"], "COMPLETE")
            self.assertEqual(exercise["python_version"], "3.13.5")
            self.assertEqual(exercise["packages"]["numpy"], "2.3.4")
            self.assertFalse(exercise["original_manifest_available_publicly"])

    def test_export_is_path_free_and_discloses_redaction(self):
        record = export_provenance(self.source, self.output)
        serialized = json.dumps(record) + (self.output / "references/public_provenance.md").read_text()
        self.assertNotIn(self.private_path, serialized)
        self.assertNotIn(str(self.base), serialized)
        for name in ["command", "working_directory", "python_executable", "input_requested", "output_directory"]:
            self.assertIn(name, record["policy"]["redacted_fields"])
            for exercise in record["exercises"]:
                self.assertNotIn(name, exercise)
        for locator in record["published_files_sha256"]:
            self.assertFalse(Path(locator).is_absolute())
            self.assertNotIn("..", Path(locator).parts)

    def test_no_source_evidence_or_existing_public_artifact_changes(self):
        source_before = self.inventory(self.source)
        public_before = self.inventory(self.output)
        export_provenance(self.source, self.output)
        self.assertEqual(source_before, self.inventory(self.source))
        public_after = self.inventory(self.output)
        for name, hash_before in public_before.items():
            self.assertEqual(hash_before, public_after[name])
        self.assertEqual(set(public_after) - set(public_before), {
            "references/public_provenance.json", "references/public_provenance.md"
        })

    def test_withheld_log_hash_is_not_a_published_file_link(self):
        record = export_provenance(self.source, self.output)
        for exercise in record["exercises"]:
            withheld = exercise["withheld_artifacts"]
            self.assertEqual(len(withheld), 1)
            relative = withheld[0]["relative_path"]
            self.assertTrue(relative.endswith("/execution.log"))
            self.assertEqual(withheld[0]["sha256"], file_hash(self.source / relative))
            self.assertIn("not a download link", withheld[0]["reason"])
            self.assertNotIn(relative, exercise["published_artifacts_sha256"])
            self.assertNotIn(relative, record["published_files_sha256"])

    def test_public_snapshots_match_original_recorded_hashes(self):
        record = build_public_provenance(self.source, self.output)
        validate_public_artifacts(record, self.output)
        for exercise in record["exercises"]:
            for snapshot in exercise["published_source_snapshots"] + [exercise["published_input_snapshot"]]:
                self.assertEqual(snapshot["sha256"], file_hash(self.output / snapshot["path"]))

    def test_tampered_public_artifact_is_refused_without_writing_export(self):
        (self.output / "runs/first_study/charge_states/result.csv").write_text("tampered\n")
        with self.assertRaisesRegex(ValueError, "Hash mismatch"):
            export_provenance(self.source, self.output)
        self.assertFalse((self.output / "references/public_provenance.json").exists())

    def test_tampered_source_snapshot_is_refused(self):
        (self.source / "runs/first_study/charge_states/provenance/code/charge_states.py").write_text("changed\n")
        with self.assertRaisesRegex(ValueError, "Hash mismatch"):
            export_provenance(self.source, self.output)

    def test_changed_input_config_is_refused(self):
        (self.output / "data/charge_states.json").write_text("{}\n")
        with self.assertRaisesRegex(ValueError, "Hash mismatch"):
            export_provenance(self.source, self.output)

    def test_private_metadata_cannot_enter_whitelisted_version_fields(self):
        self.change_source_manifest("platform", self.private_path)
        with self.assertRaisesRegex(ValueError, "must not contain paths"):
            export_provenance(self.source, self.output)

    def test_source_and_output_must_be_distinct(self):
        with self.assertRaisesRegex(ValueError, "distinct curated output"):
            export_provenance(self.source, self.source)

    def test_validator_detects_later_public_changes(self):
        record = build_public_provenance(self.source, self.output)
        (self.output / "runs/first_study/hyperfine/metrics.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Hash mismatch"):
            validate_public_artifacts(record, self.output)

    def test_failed_regeneration_preserves_existing_public_export(self):
        export_provenance(self.source, self.output)
        export_file = self.output / "references/public_provenance.json"
        before = export_file.read_bytes()
        (self.output / "runs/first_study/hyperfine/result.csv").write_text("changed\n")
        with self.assertRaises(ValueError):
            export_provenance(self.source, self.output)
        self.assertEqual(export_file.read_bytes(), before)

    def test_absolute_and_traversal_artifact_paths_are_rejected(self):
        for value in ["/PRIVATE_FIXTURE_ONLY/input", "../input", "provenance/../input", "C:\\private\\input", "file://private/input"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                relative_path(value)


if __name__ == "__main__":
    unittest.main()
