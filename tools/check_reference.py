#!/usr/bin/env python3
"""Verify the selected public reference files against their evidence hashes."""
import json
from pathlib import Path

from export_public_provenance import validate_public_artifacts

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    record = json.loads((ROOT / "references/public_provenance.json").read_text())
    validate_public_artifacts(record, ROOT)
    print(f"Verified {len(record['published_files_sha256'])} published reference files.")
