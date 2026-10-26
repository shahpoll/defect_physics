"""Preserve the inputs, code, status and evidence of every attempted exercise."""

from __future__ import annotations

import argparse
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from hashlib import sha256
from importlib.metadata import version
import json
import math
from pathlib import Path
import platform
import shutil
import sys
import traceback


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def file_hash(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, payload):
    Path(path).write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def check_finite(value, location="metrics"):
    """Reject invalid JSON numbers, including nested metrics."""
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"nonfinite number at {location}")
    if isinstance(value, dict):
        for key, item in value.items():
            check_finite(item, f"{location}.{key}")
    elif isinstance(value, (tuple, list)):
        for index, item in enumerate(value):
            check_finite(item, f"{location}[{index}]")


def reject_json_constant(token):
    raise ValueError(f"invalid JSON number: {token}")


def execute(exercise, compute, input_path, output_path):
    """Never overwrite a run. A recorded success means the calculation completed."""
    output_path = Path(output_path).resolve()
    input_path = Path(input_path).resolve()
    # Refusal here deliberately leaves any existing run completely untouched.
    output_path.mkdir(parents=True, exist_ok=False)
    manifest = {
        "exercise": exercise,
        "status": "RUNNING",
        "started_at_utc": utc_now(),
        "command": list(sys.argv),
        "working_directory": str(Path.cwd()),
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "input_requested": str(input_path),
        "output_directory": str(output_path),
        "claim_boundary": "Educational reconstruction or illustrative model; not independent ab initio validation.",
    }
    write_json(output_path / "manifest.json", manifest)
    with (output_path / "execution.log").open("w", encoding="utf-8") as log:
        try:
            with redirect_stdout(log), redirect_stderr(log):
                print(f"Starting {exercise} at {manifest['started_at_utc']}", flush=True)
                manifest["packages"] = {name: version(name) for name in ("numpy", "matplotlib")}
                provenance = output_path / "provenance"
                provenance.mkdir()
                raw_input = input_path.read_bytes()
                (provenance / "input.json").write_bytes(raw_input)
                manifest["input_sha256"] = sha256(raw_input).hexdigest()
                code_dir = provenance / "code"
                code_dir.mkdir()
                manifest["source_sha256"] = {}
                for source in sorted(Path(__file__).parent.glob("*.py")):
                    shutil.copy2(source, code_dir / source.name)
                    manifest["source_sha256"][source.name] = file_hash(source)
                config = json.loads(raw_input, parse_constant=reject_json_constant)
                if not isinstance(config, dict):
                    raise ValueError("input JSON must be an object")
                if config.get("experiment", exercise) != exercise:
                    raise ValueError("input experiment name does not match the requested exercise")
                metrics = compute(config, output_path)
                if not isinstance(metrics, dict) or not metrics:
                    raise ValueError("calculation must return a nonempty metrics object")
                check_finite(metrics)
                checks = metrics.get("checks")
                if not isinstance(checks, dict) or not checks or any(v is not True for v in checks.values()) or metrics.get("all_checks_passed") is not True:
                    raise ValueError("calculation did not report nonempty, passing mathematical checks")
                write_json(output_path / "metrics.json", metrics)
                # Empty figures/tables are not useful evidence of completion.
                figures = list(output_path.glob("*.png"))
                tables = list(output_path.glob("*.csv"))
                if not figures or not tables or any(p.stat().st_size == 0 for p in figures + tables):
                    raise ValueError("calculation did not produce nonempty PNG and CSV outputs")
                manifest["status"] = "COMPLETE"
                print("Calculation completed; mathematical checks passed.", flush=True)
        except KeyboardInterrupt:
            manifest["status"] = "INTERRUPTED"
            manifest["failure"] = {"type": "KeyboardInterrupt", "message": "Execution interrupted; partial evidence retained."}
            traceback.print_exc(file=log)
        except Exception as exc:
            manifest["status"] = "FAILED"
            manifest["failure"] = {"type": type(exc).__name__, "message": str(exc)}
            traceback.print_exc(file=log)
        finally:
            manifest["finished_at_utc"] = utc_now()
            log.flush()
            manifest["artifacts_sha256"] = {
                str(p.relative_to(output_path)): file_hash(p)
                for p in sorted(output_path.rglob("*"))
                if p.is_file() and p.name != "manifest.json"
            }
            write_json(output_path / "manifest.json", manifest)
    return 0 if manifest["status"] == "COMPLETE" else (130 if manifest["status"] == "INTERRUPTED" else 1)


def run_cli(exercise, compute):
    parser = argparse.ArgumentParser(description=f"Run the SiV {exercise} teaching exercise.")
    parser.add_argument("--input", required=True, type=Path, help="JSON parameter file")
    parser.add_argument("--output", required=True, type=Path, help="New output directory (must not exist)")
    args = parser.parse_args()
    try:
        code = execute(exercise, compute, args.input, args.output)
    except FileExistsError:
        parser.exit(2, f"Refusing to overwrite existing run: {args.output}\n")
    print(f"{exercise}: {'COMPLETE' if code == 0 else 'FAILED'}; {args.output}")
    return code
