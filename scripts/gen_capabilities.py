#!/usr/bin/env python3
"""Generate .kilo/CAPABILITIES.md from skills/agents/commands frontmatter.

Stdlib only. Keeps a compact, generated routing catalog so agents can pick a
capability without loading every SKILL.md. Readiness comes from
scripts/readiness.json (skills that need external setup are marked).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KILO = ROOT / ".kilo"
READINESS = ROOT / "scripts" / "readiness.json"


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].splitlines()
    out: dict[str, str] = {}
    key = None
    buf: list[str] = []
    for line in block:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            if key:
                out[key] = " ".join(buf).strip()
            key, val = m.group(1), m.group(2).strip()
            buf = [] if (val == "" or val[0] in "|>") else [val]
        elif key and line.startswith((" ", "\t")):
            buf.append(line.strip())
    if key:
        out[key] = " ".join(buf).strip()
    return out


def one_line(s: str, n: int = 130) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def load_readiness() -> dict[str, str]:
    try:
        data = json.loads(READINESS.read_text(encoding="utf-8"))
        return {str(k): str(v) for k, v in (data.get("needs_setup") or {}).items()}
    except FileNotFoundError:
        return {}


def collect(pattern: str, needs: dict[str, str]):
    items = []
    for p in sorted(KILO.glob(pattern)):
        fm = frontmatter(p)
        name = fm.get("name") or (p.parent.name if p.name == "SKILL.md" else p.stem)
        if name in ("README",):
            continue
        desc = fm.get("description", "")
        ready = "" if name in needs else "✅"
        note = needs.get(name, "")
        items.append((name, ready, note, one_line(desc), str(p.relative_to(ROOT))))
    return items


def main() -> None:
    needs = load_readiness()
    skills = collect("skills/*/SKILL.md", needs)
    agents = collect("agents/*.md", needs)
    commands = collect("commands/*.md", needs)

    lines = [
        "# CAPABILITIES（自動生成）",
        "",
        "> `python3 scripts/gen_capabilities.py` で再生成。手で編集しない。",
        "> まず本カタログで候補を選び、必要なものだけ `SKILL.md` を開く（段階的開示）。",
        "> `⚠️` は外部セットアップが必要（`scripts/readiness.json`）。標準フローでは使わない。",
        "",
        f"## Skills（{len(skills)}）",
        "",
        "| name | ready | 説明 | path |",
        "|---|---|---|---|",
    ]
    for n, r, note, d, p in skills:
        mark = r if r else f"⚠️ {note}"
        lines.append(f"| `{n}` | {mark} | {d} | `{p}` |")

    lines += ["", f"## Agents（{len(agents)}）", "", "| name | 説明 | path |", "|---|---|---|"]
    for n, r, note, d, p in agents:
        lines.append(f"| `{n}` | {d} | `{p}` |")

    lines += ["", f"## Workflows（{len(commands)}）", "", "| name | 説明 | path |", "|---|---|---|"]
    for n, r, note, d, p in commands:
        lines.append(f"| `/{n}` | {d} | `{p}` |")

    lines += [
        "",
        "## 呼び出し規約",
        "1. Workflow（入口）を選ぶ。2. その本文の skill を**必要分だけ**開く。3. 出力スキーマとゲートに従う。",
        "詳細：`docs/USAGE.md`。",
        "",
    ]
    out = KILO / "CAPABILITIES.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}: skills={len(skills)} agents={len(agents)} commands={len(commands)} needs_setup={len(needs)}")


if __name__ == "__main__":
    main()
