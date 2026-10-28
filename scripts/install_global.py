#!/usr/bin/env python3
"""wawoo-skills を Kilo グローバル設定へ配置する（冪等・再実行可能）。

配置先: $KILO_GLOBAL_DIR（既定 ~/.config/kilo）
  - .kilo/{skills,agents,commands} を同期（既定でミラー＝キット外の余剰を削除）
  - kilo.jsonc（無ければ kilo.json）の mcp に `wawoo-skills` を冪等登録
    （絶対 python3 ＋ WAWOO_SKILLS_ROOT／WAWOO_MEMORY_READONLY）
  - AGENTS.md にキット適用範囲の節を冪等追記
  - 最後に validate_assets と MCP スモークを実行

使い方:
  python3 scripts/install_global.py             # ミラー（完全置換）
  python3 scripts/install_global.py --no-delete # 余剰を残す
  python3 scripts/install_global.py --memory-writable  # memory_save を有効化（既定は recall-only）
  python3 scripts/install_global.py --dry-run   # 変更内容のみ表示
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "mcp" / "server.py"
GLOBAL_DIR = Path(os.environ.get("KILO_GLOBAL_DIR", "")).expanduser() if os.environ.get("KILO_GLOBAL_DIR") else Path.home() / ".config" / "kilo"
KIT_MARKER = "wawoo-skills kit"
ASSET_DIRS = {
    "skills": ROOT / ".kilo" / "skills",
    "agents": ROOT / ".kilo" / "agents",
    "commands": ROOT / ".kilo" / "commands",
}

AGENTS_NOTE = f"""
# {KIT_MARKER} (globally registered)

- Global skills/agents/commands and MCP server `wawoo-skills` come from the wawoo-skills kit (source: `{ROOT}`).
- Some kit commands/skills assume the kit's repo-relative SSOT: `docs/plans/ACTIVE.md`, `docs/plans/CONTENT.md`, `docs/memory/`, `.kilo/CAPABILITIES.md`, `scripts/plan_*.py`, `scripts/validate_assets.py`.
- Those paths are valid **only in the wawoo-skills repository** (or a project that adopts the same layout). In any other project:
  - If a path does not exist, **skip** that step; do not create `docs/plans/` or `docs/memory/` implicitly.
  - Kit entry commands/skills may still be used, but re-map SSOT steps to the project's existing planning/tracking.
- Globally, MCP `memory_save` is disabled (recall only) unless installed with `--memory-writable`. Persist durable memory only inside the wawoo-skills repository.
"""


def log(ok: bool, msg: str) -> None:
    print(f"{'OK  ' if ok else 'WARN'} {msg}")


def strip_jsonc(text: str) -> str:
    text = re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    return text


def valid_jsonc(text: str) -> bool:
    try:
        json.loads(strip_jsonc(text))
        return True
    except Exception:
        return False


def mcp_entry(memory_readonly: bool = True) -> str:
    py = sys.executable or "/usr/bin/python3"
    ro = "1" if memory_readonly else "0"
    return (
        '    "wawoo-skills": {\n'
        '      "type": "local",\n'
        f'      "command": ["{py}", "{SERVER}"],\n'
        '      "environment": {\n'
        f'        "WAWOO_SKILLS_ROOT": "{ROOT}",\n'
        f'        "WAWOO_MEMORY_READONLY": "{ro}"\n'
        "      },\n"
        '      "enabled": true\n'
        "    }"
    )


def ensure_mcp(path: Path, dry: bool, memory_readonly: bool = True) -> str:
    if not path.exists():
        return f"skip (no config file: {path})"
    text = path.read_text(encoding="utf-8")
    if '"wawoo-skills"' in text:
        return "already registered"
    entry = mcp_entry(memory_readonly)
    m = re.search(r'"mcp"\s*:\s*\{', text)
    if m:
        new = text[: m.end()] + "\n" + entry + ",\n" + text[m.end() :]
    else:
        i = text.find("{")
        if i == -1:
            return "skip (malformed config)"
        new = text[: i + 1] + '\n  "mcp": {\n' + entry + "\n  },\n" + text[i + 1 :]
    if not valid_jsonc(new):
        return f"ERROR validation failed, left unchanged: {path}"
    if dry:
        return f"would register mcp.wawoo-skills -> {path}"
    shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
    path.write_text(new, encoding="utf-8")
    return f"registered mcp.wawoo-skills -> {path}"


def config_path() -> Path:
    for name in ("kilo.jsonc", "kilo.json"):
        p = GLOBAL_DIR / name
        if p.exists():
            return p
    return GLOBAL_DIR / "kilo.jsonc"


def sync_assets(dry: bool, mirror: bool) -> None:
    for name, src in ASSET_DIRS.items():
        dst = GLOBAL_DIR / name
        if dry:
            log(True, f"would sync {src} -> {dst} (mirror={mirror})")
            continue
        if dst.exists() and mirror:
            shutil.rmtree(dst)
        shutil.copytree(src, dst, dirs_exist_ok=True)
        if name == "commands":
            (dst / "README.md").unlink(missing_ok=True)
        log(True, f"synced {src} -> {dst} (mirror={mirror})")


def ensure_agents(dry: bool) -> str:
    path = GLOBAL_DIR / "AGENTS.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if KIT_MARKER in text:
        return "already present"
    if dry:
        return f"would append kit note -> {path}"
    path.write_text(text.rstrip() + "\n" + AGENTS_NOTE, encoding="utf-8")
    return f"appended kit note -> {path}"


def generate_router(dry: bool) -> str:
    """ROUTER.md をグローバル設定ディレクトリへ生成する（gen_router.py に委譲）。"""
    out = GLOBAL_DIR / "ROUTER.md"
    if dry:
        return f"would generate {out}"
    env = dict(os.environ, KILO_GLOBAL_DIR=str(GLOBAL_DIR))
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "gen_router.py")],
        cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=60,
    )
    tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
    return tail[0] or f"generated {out}"


def ensure_instructions(path: Path, dry: bool) -> str:
    """config.instructions に ROUTER.md の**絶対パス**を冪等登録（相対は注入されない）。"""
    target = str(GLOBAL_DIR / "ROUTER.md")
    if not path.exists():
        return f"skip (no config file: {path})"
    text = path.read_text(encoding="utf-8")
    m = re.search(r'"instructions"\s*:\s*\[(.*?)\]', text, re.S)
    if m:
        items = [s.strip().strip('"') for s in m.group(1).split(",") if s.strip()]
        if target in items:
            return "already absolute"
        items = [i for i in items if i and i != "ROUTER.md"]
        items.append(target)
        literal = "[" + ", ".join(f'"{i}"' for i in items) + "]"
        new = text[: m.start()] + f'"instructions": {literal}' + text[m.end():]
    else:
        i = text.find("{")
        if i == -1:
            return f"skip (malformed config: {path})"
        new = text[: i + 1] + f'\n  "instructions": ["{target}"],' + text[i + 1 :]
    if not valid_jsonc(new):
        return f"ERROR instructions validation failed, left unchanged: {path}"
    if dry:
        return f"would ensure instructions -> {target}"
    shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
    path.write_text(new, encoding="utf-8")
    return f"instructions -> {target}"


def ensure_json_field(path: Path, field: str, literal: str, replace: bool, dry: bool) -> str:
    """トップレベルの JSON フィールドを冪等に設定する（既定では既存値を尊重）。"""
    if not path.exists():
        return f"skip (no config file: {path})"
    text = path.read_text(encoding="utf-8")
    m = re.search(rf'"{re.escape(field)}"\s*:\s*([^\n,]+)', text)
    if m:
        if not replace:
            return "already set"
        new = text[: m.start(1)] + literal + text[m.end(1) :]
    else:
        i = text.find("{")
        if i == -1:
            return f"skip (malformed config: {path})"
        new = text[: i + 1] + f'\n  "{field}": {literal},' + text[i + 1 :]
    if not valid_jsonc(new):
        return f"ERROR {field} validation failed, left unchanged: {path}"
    if dry:
        return f"would set {field} = {literal}"
    shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
    path.write_text(new, encoding="utf-8")
    return f"set {field} = {literal}"


def verify() -> bool:
    ok = True
    try:
        v = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_assets.py")],
            cwd=str(ROOT), capture_output=True, text=True, timeout=120,
        )
        tail = (v.stdout + v.stderr).strip().splitlines()[-1:] or [""]
        log(v.returncode == 0, f"validate_assets: {tail[0]}")
        ok = ok and v.returncode == 0
    except Exception as exc:
        log(False, f"validate_assets failed to run: {exc}")
        ok = False
    try:
        s = subprocess.run(
            [sys.executable, str(ROOT / "mcp" / "test_server.py")],
            cwd=str(ROOT), capture_output=True, text=True, timeout=120,
        )
        tail = (s.stdout + s.stderr).strip().splitlines()[-1:] or [""]
        log(s.returncode == 0, f"mcp smoke: {tail[0]}")
        ok = ok and s.returncode == 0
    except Exception as exc:
        log(False, f"mcp smoke failed to run: {exc}")
        ok = False
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description="Install wawoo-skills into the global Kilo config (idempotent).")
    ap.add_argument("--no-delete", action="store_true", help="keep extra files in target asset dirs (default: mirror)")
    ap.add_argument("--dry-run", action="store_true", help="show actions without writing")
    ap.add_argument("--default-agent", default="wawoo-router", help="default_agent to register (default: wawoo-router)")
    ap.add_argument("--no-default-agent", action="store_true", help="do not touch default_agent")
    ap.add_argument("--force-default-agent", action="store_true", help="overwrite an existing default_agent")
    ap.add_argument(
        "--memory-writable",
        action="store_true",
        help="register MCP with memory_save enabled (WAWOO_MEMORY_READONLY=0). Default keeps recall-only.",
    )
    args = ap.parse_args()

    if not SERVER.exists():
        log(False, f"missing MCP server: {SERVER}")
        return 1

    print(f"repo root : {ROOT}")
    print(f"target    : {GLOBAL_DIR}")
    print(f"mirror    : {not args.no_delete}")
    print("---")
    sync_assets(args.dry_run, not args.no_delete)
    log(True, f"mcp: {ensure_mcp(config_path(), args.dry_run, memory_readonly=not args.memory_writable)}")
    log(True, f"agents: {ensure_agents(args.dry_run)}")
    log(True, f"router: {generate_router(args.dry_run)}")
    cfg = config_path()
    log(True, f"instructions: {ensure_instructions(cfg, args.dry_run)}")
    if not args.no_default_agent:
        log(True, f"default_agent: {ensure_json_field(cfg, 'default_agent', json.dumps(args.default_agent), args.force_default_agent, args.dry_run)}")
    if args.dry_run:
        return 0
    print("---")
    ok = verify()
    print("---")
    print("RESULT:", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
