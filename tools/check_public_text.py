#!/usr/bin/env python3
"""Check public text for long dashes and dated work/status notes."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TIMESTAMP = re.compile(r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")
MONTH = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
CALENDAR = re.compile(r"\b(?:\d{1,2}\s+" + MONTH + r"|" + MONTH + r"\s+\d{1,2})(?:st|nd|rd|th)?\b", re.I)
WORK_LABEL = re.compile(r"\b(?:draft log|prepared|draft expanded|accessed|access check(?:ed)?|check date|checked on)\b", re.I)


def audit(root, paths):
    failures = []
    inspected = 0
    for relative in paths:
        path = root / relative
        if not path.is_file():
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        inspected += 1
        for number, line in enumerate(source.splitlines(), 1):
            if any(chr(code) in line for code in (0x2013, 0x2014)):
                failures.append(f"{relative}:{number}: use a hyphen or colon")
            if TIMESTAMP.search(line) or (WORK_LABEL.search(line) and CALENDAR.search(line)):
                failures.append(f"{relative}:{number}: keep exact work dates/times in local evidence")
    return inspected, failures


def main():
    result = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                            cwd=ROOT, capture_output=True, text=True, check=True)
    inspected, failures = audit(ROOT, sorted(set(filter(None, result.stdout.split("\0")))))
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Checked {inspected} public text files: punctuation and work-date policy passed.")


if __name__ == "__main__":
    main()
