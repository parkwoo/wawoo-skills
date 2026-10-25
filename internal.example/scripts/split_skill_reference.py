#!/usr/bin/env python3
"""SKILL.md の本文を references/ に移し、入口をコンパクトにする（stdlib のみ）。"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def split_after_frontmatter(skill_md: Path, ref_name: str, intro_lines: list[str]) -> None:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit(f"no frontmatter: {skill_md}")
    end = text.find("\n---", 3)
    if end == -1:
        raise SystemExit(f"bad frontmatter: {skill_md}")
    fm_block = text[: end + 4]
    body = text[end + 4 :].lstrip("\n")
    ref_dir = skill_md.parent / "references"
    ref_dir.mkdir(parents=True, exist_ok=True)
    ref_path = ref_dir / ref_name
    ref_path.write_text(body, encoding="utf-8")
    intro = "\n".join(intro_lines).rstrip() + "\n"
    skill_md.write_text(fm_block + "\n" + intro, encoding="utf-8")
    print(f"split {skill_md.relative_to(ROOT)} -> {ref_path.relative_to(ROOT)} ({len(body)} bytes body)")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("skill_dir", type=Path)
    p.add_argument("ref_name")
    p.add_argument("--intro-file", type=Path, help="Markdown intro appended after frontmatter")
    args = p.parse_args()
    skill_md = args.skill_dir / "SKILL.md"
    intro = args.intro_file.read_text(encoding="utf-8").splitlines() if args.intro_file else []
    split_after_frontmatter(skill_md, args.ref_name, intro)


if __name__ == "__main__":
    main()
