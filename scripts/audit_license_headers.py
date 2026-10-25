#!/usr/bin/env python3
"""第三者 skill のライセンス表記を棚卸しする（stdlib のみ）。docs/audit に Markdown を出力。"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".kilo" / "skills"
OUT = ROOT / "docs" / "audit" / "LICENSE-HEADER-AUDIT.md"

# ATTRIBUTION の大分類（手動マッピングの補助）
OPENDESIGN = {
    "frontend-design",
    "web-design-guidelines",
    "brand-guidelines",
    "design-md",
    "design-brief",
    "design-review",
    "imagegen-frontend-mobile",
    "reference-design-contract",
    "web-experience-design",
    "slides",
}
SRE = {
    "ask-matt",
    "code-review",
    "codebase-design",
    "diagnosing-bugs",
    "domain-modeling",
    "grill-with-docs",
    "grilling",
    "handoff",
    "implement",
    "implement-spec",
    "pr",
    "prototype",
    "research",
    "retro",
    "setup-matt-pocock-skills",
    "tdd",
    "to-spec",
    "to-tickets",
    "triage",
    "wayfinder",
    "writing-for-agents",
}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def classify(name: str) -> str:
    if name in OPENDESIGN:
        return "OpenDesign (Apache-2.0)"
    if name in SRE:
        return "Skills For Real Engineers (MIT)"
    return "Kilo 組み込み / 本リポジトリ (MIT 想定)"


def main() -> None:
    rows: list[tuple[str, str, str, str, str]] = []
    issues: list[str] = []

    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            issues.append(f"SKILL.md なし: {skill_dir.name}")
            continue
        fm = frontmatter(skill_md)
        name = fm.get("name") or skill_dir.name
        lic_fm = fm.get("license", "—")
        license_file = ""
        for cand in ("LICENSE", "LICENSE.txt", "LICENSE.md"):
            if (skill_dir / cand).exists():
                license_file = cand
                break
        upstream = fm.get("od", "")
        if "upstream:" in skill_md.read_text(encoding="utf-8", errors="ignore")[:2000]:
            m = re.search(r'upstream:\s*["\']?([^"\'\n]+)', skill_md.read_text(encoding="utf-8", errors="ignore")[:4000])
            upstream = m.group(1).strip() if m else upstream
        cat = classify(name)
        if cat.startswith("OpenDesign") and not license_file:
            issues.append(f"OpenDesign 由来だがディレクトリ LICENSE なし: {name}")
        rows.append((name, cat, lic_fm, license_file or "—", upstream or "—"))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# ライセンスヘッダ監査（自動生成）",
        "",
        f"> 生成: `python3 scripts/audit_license_headers.py`（{date.today().isoformat()}）",
        "",
        "## 要約",
        f"- スキル数: **{len(rows)}**",
        f"- 要確認: **{len(issues)}** 件",
        "",
        "## 一覧",
        "",
        "| skill | 分類 | frontmatter `license` | 同梱 LICENSE | upstream |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| `{r[0]}` | {r[1]} | {r[2]} | {r[3]} | {r[4]} |")

    lines += ["", "## 要確認", ""]
    if issues:
        for i in issues:
            lines.append(f"- {i}")
    else:
        lines.append("- （自動チェック上の重大な欠落なし。法的判断は人が `LICENSES/` と各 upstream を確認。）")

    lines += [
        "",
        "## 手動確認メモ",
        "- Apache-2.0（OpenDesign・Kilo Marketplace agents）: `LICENSE`/`NOTICE` 保持義務。",
        "- MIT（SRE・本リポジトリ）: 著作権表示の保持。",
        "- 全文の著作権コメント行は skill により無し（frontmatter の `license` 参照型が多い）。",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} issues={len(issues)}")


if __name__ == "__main__":
    main()
