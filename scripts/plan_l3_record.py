#!/usr/bin/env python3
"""Validate the minimal structure of an L3 retro / PDCA record. stdlib only."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Heading keywords aligned with the pdca-cycle completion criteria
REQUIRED_SECTIONS = (
    ("baseline", re.compile(r"^##\s+.*(baseline|ベースライン|現状)", re.I | re.M)),
    ("action", re.compile(r"^##\s+.*(action|実施|Do)", re.I | re.M)),
    ("evidence", re.compile(r"^##\s+.*(evidence|証拠|Check)", re.I | re.M)),
    ("decision", re.compile(r"^##\s+.*(decision|決定|Act)", re.I | re.M)),
    ("next", re.compile(r"^##\s+.*(next|次|次ステップ)", re.I | re.M)),
)


def validate_l3_record(text: str) -> list[str]:
    issues: list[str] = []
    for name, pat in REQUIRED_SECTIONS:
        if not pat.search(text):
            issues.append(f"missing section for: {name}")
    if re.search(r"^\|\s*[^|]+\|\s*done\s*\|", text, re.I | re.M):
        issues.append("L3 record should not contain ACTIVE-style task table with done rows")
    return issues


def check_file(path: Path) -> int:
    if not path.is_file():
        print(f"MISSING: {path}")
        return 1
    text = path.read_text(encoding="utf-8", errors="ignore")
    issues = validate_l3_record(text)
    if issues:
        print(f"L3 record check FAILED: {path}")
        for i in issues:
            print(" -", i)
        return 1
    print(f"L3 record OK: {path}")
    return 0


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    default = root / "docs" / "plans" / "RETRO.example.md"
    p = argparse.ArgumentParser(description="Validate L3 retro/PDCA record")
    p.add_argument("path", nargs="?", type=Path, default=default)
    return check_file(p.parse_args().path)


if __name__ == "__main__":
    sys.exit(main())
