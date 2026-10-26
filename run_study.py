#!/usr/bin/env python3
"""Run the three exercises in a fresh, dated folder. No simulations are hidden."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="New study folder; default runs/<UTC date-time>")
    args = parser.parse_args()
    target = args.output or ROOT / "runs" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    target = target.resolve()
    try:
        target.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.exit(2, f"Refusing to overwrite existing study: {target}\n")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    env["MPLBACKEND"] = "Agg"
    summary = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "RUNNING",
        "runs": [],
        "runner_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    summary_path = target / "study_manifest.json"
    def save():
        summary_path.write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    save()
    with (target / "execution.log").open("w") as log:
        try:
            for name in ("charge_states", "parity_mixing", "hyperfine"):
                command = [sys.executable, "-m", f"siv_study.{name}", "--input", str(ROOT / "data" / f"{name}.json"), "--output", str(target / name)]
                result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, text=True)
                summary["runs"].append({"exercise": name, "exit_code": result.returncode, "command": command, "manifest": f"{name}/manifest.json"})
                save()
                if result.returncode != 0:
                    raise RuntimeError(f"{name} failed with exit code {result.returncode}; inspect its execution.log")
            summary["status"] = "COMPLETE"
        except KeyboardInterrupt:
            summary["status"] = "INTERRUPTED"
            summary["failure"] = "Execution interrupted; partial run evidence retained."
        except Exception as exc:
            summary["status"] = "FAILED"
            summary["failure"] = {"type": type(exc).__name__, "message": str(exc)}
        finally:
            summary["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
            save()
    print(f"Study {summary['status']}: {target}")
    return 0 if summary["status"] == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
