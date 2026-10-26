#!/usr/bin/env python3
"""Export a path-free public derivative of retained local first-study evidence.

The source manifests and logs are read without modification. The output is a
separately identified view, not a replacement execution record or a new run.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import re


EXERCISES = ("charge_states", "parity_mixing", "hyperfine")
RUN_PATH = PurePosixPath("runs/first_study")
REDACTED_FIELDS = (
    "command", "working_directory", "python_executable",
    "input_requested", "output_directory",
)
HASH_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
VERSION_PATTERN = re.compile(r"[A-Za-z0-9_.+!() -]+\Z")


def file_hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def relative_path(value: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value or "\x00" in value:
        raise ValueError("Expected a nonempty portable relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {".", ".."} for part in value.split("/")):
        raise ValueError("Absolute paths and traversal are not allowed in public records")
    return path


def checked_file(root: Path, relative: str | PurePosixPath) -> Path:
    portable = relative_path(str(relative))
    target = root.joinpath(*portable.parts)
    if not target.is_file() or target.is_symlink() or not target.resolve().is_relative_to(root):
        raise ValueError(f"Missing regular file inside the selected root: {portable}")
    return target


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path: Path) -> dict:
    def reject_constant(value):
        raise ValueError(f"Nonfinite JSON constant is not valid provenance: {value}")

    result = json.loads(path.read_text(), object_pairs_hook=_unique_object, parse_constant=reject_constant)
    if not isinstance(result, dict):
        raise ValueError("Provenance must be a JSON object")
    return result


def hash_value(value: object) -> str:
    if not isinstance(value, str) or not HASH_PATTERN.fullmatch(value):
        raise ValueError("Expected a lowercase SHA-256 digest")
    return value


def version_text(value: object) -> str:
    if not isinstance(value, str) or not VERSION_PATTERN.fullmatch(value):
        raise ValueError("Version/platform metadata must not contain paths or control characters")
    return value


def timestamp(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("A timestamp must be text")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("Provenance timestamps must include their time zone")
    return value


def _verify(root: Path, relative: str | PurePosixPath, digest: str) -> None:
    label = relative_path(str(relative))
    if file_hash(checked_file(root, label)) != hash_value(digest):
        raise ValueError(f"Hash mismatch for {label}; original evidence was not changed")


def validate_public_artifacts(record: dict, output_root: Path) -> None:
    """Verify every public file named in the export without relying on private paths."""
    root = Path(output_root).resolve()
    for relative, digest in record["published_files_sha256"].items():
        _verify(root, relative, digest)


def build_public_provenance(source_root: Path, output_root: Path) -> dict:
    source = Path(source_root).resolve()
    output = Path(output_root).resolve()
    if source == output or output.is_relative_to(source):
        raise ValueError("Use a distinct curated output checkout outside the source evidence folder")
    if not source.is_dir() or not output.is_dir():
        raise ValueError("Both source and output roots must already exist")

    summary_relative = RUN_PATH / "study_manifest.json"
    summary_path = checked_file(source, summary_relative)
    summary = read_json(summary_path)
    if summary["status"] != "COMPLETE":
        raise ValueError("The curated first-study reference requires a COMPLETE source study")
    listed = summary["runs"]
    if not isinstance(listed, list) or len(listed) != len(EXERCISES):
        raise ValueError("The source study must list exactly the three reference exercises")
    by_exercise = {row["exercise"]: row for row in listed}
    if set(by_exercise) != set(EXERCISES):
        raise ValueError("The source study has missing or duplicated reference exercises")
    published = {}
    runner_digest = hash_value(summary["runner_sha256"])
    _verify(source, "run_study.py", runner_digest)
    _verify(output, "run_study.py", runner_digest)
    published["run_study.py"] = runner_digest
    exports = []
    for name in EXERCISES:
        listed_run = by_exercise[name]
        if listed_run["exit_code"] != 0 or isinstance(listed_run["exit_code"], bool):
            raise ValueError(f"Reference exercise did not exit successfully: {name}")
        if listed_run["manifest"] != f"{name}/manifest.json":
            raise ValueError(f"Unexpected reference manifest locator: {name}")
        run_relative = RUN_PATH / name
        original_relative = run_relative / "manifest.json"
        original_path = checked_file(source, original_relative)
        original = read_json(original_path)
        if original["exercise"] != name or original["status"] != "COMPLETE":
            raise ValueError(f"Reference run is not a matching COMPLETE exercise: {name}")

        artifacts = original["artifacts_sha256"]
        sources = original["source_sha256"]
        if not isinstance(artifacts, dict) or not isinstance(sources, dict) or not sources:
            raise ValueError(f"Missing artifact/source hash map: {name}")
        input_digest = hash_value(original["input_sha256"])
        input_relative = run_relative / "provenance/input.json"
        if artifacts.get("provenance/input.json") != input_digest:
            raise ValueError(f"Input snapshot hash does not match source manifest: {name}")
        _verify(source, input_relative, input_digest)
        _verify(output, input_relative, input_digest)
        config_relative = PurePosixPath("data") / f"{name}.json"
        _verify(output, config_relative, input_digest)
        published[str(config_relative)] = input_digest

        source_snapshots = []
        for filename, digest in sorted(sources.items()):
            portable = relative_path(filename)
            snapshot_in_run = PurePosixPath("provenance/code") / portable
            if artifacts.get(str(snapshot_in_run)) != digest:
                raise ValueError(f"Source snapshot is missing from the artifact inventory: {name}/{portable}")
            snapshot = run_relative / snapshot_in_run
            _verify(source, snapshot, digest)
            _verify(output, snapshot, digest)
            source_snapshots.append({"path": str(snapshot), "sha256": hash_value(digest)})

        retained = {}
        withheld = []
        for artifact, digest in sorted(artifacts.items()):
            inside_run = relative_path(artifact)
            relative = run_relative / inside_run
            digest = hash_value(digest)
            _verify(source, relative, digest)
            target = output.joinpath(*relative.parts)
            if target.exists():
                _verify(output, relative, digest)
                retained[str(relative)] = digest
                published[str(relative)] = digest
            else:
                withheld.append({
                    "relative_path": str(relative), "sha256": digest,
                    "reason": "Local-only artifact omitted from the curated public package; hash retained as an identity commitment, not a download link.",
                })
        required = {"metrics.json", "provenance/input.json"}
        if not all(str(run_relative / item) in retained for item in required):
            raise ValueError(f"Public reference is missing metrics or input snapshot: {name}")
        packages = original["packages"]
        if not isinstance(packages, dict) or not packages:
            raise ValueError(f"Package versions are missing: {name}")
        public_packages = {}
        for package, version in sorted(packages.items()):
            if not re.fullmatch(r"[A-Za-z0-9_.-]+", package):
                raise ValueError("Unexpected package name in provenance")
            public_packages[package] = version_text(version)
        exports.append({
            "exercise": name,
            "status": original["status"],
            "started_at_utc": timestamp(original["started_at_utc"]),
            "finished_at_utc": timestamp(original["finished_at_utc"]),
            "original_local_manifest_sha256": file_hash(original_path),
            "original_manifest_available_publicly": False,
            "python_version": version_text(original["python_version"]),
            "platform": version_text(original["platform"]),
            "packages": public_packages,
            "published_input_snapshot": {"path": str(input_relative), "sha256": input_digest},
            "matching_public_input_config": str(config_relative),
            "published_source_snapshots": source_snapshots,
            "published_artifacts_sha256": retained,
            "withheld_artifacts": withheld,
        })
    record = {
        "format_version": 1,
        "view_kind": "curated_public_derivative_of_local_execution_evidence",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "policy": {
            "original_local_records_modified": False,
            "redacted_fields": list(REDACTED_FIELDS),
            "path_policy": "Paths in this view locate public files relative to the repository root; they do not restate original commands or machine paths.",
            "hash_scope": "Public artifacts are verified against the original artifact hashes. Hashes of withheld originals are identity commitments; public readers cannot inspect those private bytes here.",
            "claim_boundary": "These are educational reconstructions, a chosen teaching model, and table reanalysis. Completion is not independent ab initio validation or an independent attestation.",
        },
        "study": {
            "run_id": "first_study",
            "status": summary["status"],
            "started_at_utc": timestamp(summary["started_at_utc"]),
            "finished_at_utc": timestamp(summary["finished_at_utc"]),
            "original_local_study_manifest_sha256": file_hash(summary_path),
            "original_study_manifest_available_publicly": False,
            "matching_public_runner": {"path": "run_study.py", "sha256": runner_digest},
        },
        "exercises": exports,
        "published_files_sha256": dict(sorted(published.items())),
    }
    validate_public_artifacts(record, output)
    return record


def render_markdown(record: dict) -> str:
    lines = [
        "# Public provenance for the first study", "",
        "This is a **curated derivative of local execution evidence**, not a new execution or a rewritten original manifest. Original manifests and logs remain unchanged locally. Their machine paths and commands are not published.", "",
        "The [public JSON record](public_provenance.json) contains exact original-manifest hashes, original timestamps/status, version information, retained input/code snapshots, and hashes for the published results. Relative paths in that record locate public files; they do not claim to be the original invocation paths.", "",
        f"Source study: **{record['study']['run_id']}**, status **{record['study']['status']}**, finished `{record['study']['finished_at_utc']}`.", "",
        "| Exercise | Status | Retained run artifacts |", "|---|---|---:|",
    ]
    for exercise in record["exercises"]:
        name = exercise["exercise"]
        lines.append(f"| [{name}](../runs/first_study/{name}/metrics.json) | {exercise['status']} | {len(exercise['published_artifacts_sha256'])} |")
    lines.extend([
        "", "## What can be checked from this repository", "",
        "The published CSVs, figures, metrics, and input/code snapshots can be checked against `published_files_sha256` in the JSON record. The exporter rejects modified public artifacts or source snapshots that do not match their recorded hashes. The original study runner and public input configurations also match the execution evidence.", "",
        "## What is withheld", "",
        "Original commands, working directories, executable locations, requested local input/output paths, installation records and uncurated logs are local-only. Withheld run artifacts are named as relative identifiers with hashes and an explicit withholding reason, rather than linked as available downloads.", "",
        "A hash of an unpublished original is an identity commitment, not a way for a public reader to inspect that original or independently attest execution. The published view makes its redactions explicit and preserves the distinction between original evidence and a portable presentation.", "",
        "## Interpretation", "",
        "A COMPLETE teaching exercise passed its specified mathematical checks. It does not establish a new electronic-structure calculation, experimental measurement, converged DFT result, or independent validation of the paper. The original local manifests were not edited to make this public view.", "",
    ])
    return "\n".join(lines)


def export_provenance(source_root: Path, output_root: Path) -> dict:
    record = build_public_provenance(source_root, output_root)
    destination = Path(output_root).resolve() / "references"
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "public_provenance.json").write_text(json.dumps(record, indent=2, allow_nan=False) + "\n")
    (destination / "public_provenance.md").write_text(render_markdown(record))
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path, help="Local project containing untouched original first-study records")
    parser.add_argument("--output-root", required=True, type=Path, help="Distinct curated publication checkout")
    arguments = parser.parse_args()
    try:
        record = export_provenance(arguments.source_root, arguments.output_root)
    except (ValueError, KeyError, OSError, TypeError) as exc:
        parser.exit(1, f"Public provenance export failed: {exc}\n")
    print(f"Exported {len(record['exercises'])} exercise records; verified {len(record['published_files_sha256'])} public file hashes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
