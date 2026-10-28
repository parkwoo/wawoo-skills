"""`.kilo/commands/*.md` — L0 slash command (a fixed template + workflow id)."""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from intent_catalog import WORKFLOW_AGENTS

_SLASH_CMD_RE = re.compile(r"^/([a-z0-9][a-z0-9-]*)\b", re.IGNORECASE)


@dataclass(frozen=True)
class CommandEntry:
    stem: str
    workflow: str
    path: Path
    description: str


def _skills_root() -> Path:
    env = os.environ.get("WAWOO_SKILLS_ROOT", "").strip()
    if env:
        p = Path(env).expanduser()
        if p.exists():
            return p
    return Path(__file__).resolve().parents[1]


def _parse_frontmatter(text: str) -> dict[str, str]:
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


def load_command_index(root: Path | None = None) -> dict[str, CommandEntry]:
    base = root or _skills_root()
    commands_dir = base / ".kilo" / "commands"
    index: dict[str, CommandEntry] = {}
    if not commands_dir.is_dir():
        return index
    for path in sorted(commands_dir.glob("*.md")):
        if path.stem == "README":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        fm = _parse_frontmatter(text)
        workflow = (fm.get("workflow") or path.stem).strip().lower()
        if workflow not in WORKFLOW_AGENTS:
            continue
        index[path.stem.lower()] = CommandEntry(
            stem=path.stem.lower(),
            workflow=workflow,
            path=path,
            description=fm.get("description", ""),
        )
    return index


@dataclass(frozen=True)
class SlashCommandMatch:
    workflow: str
    command_stem: str
    clean_text: str
    command_path: str
    route_subsource: str  # workflow_slash | command_slash


def match_slash_route(text: str, root: Path | None = None) -> SlashCommandMatch | None:
    """L0: a `/workflow` slash, or one listed in the commands ledger."""
    raw = (text or "").strip()
    m = _SLASH_CMD_RE.match(raw)
    if not m:
        return None
    token = m.group(1).lower()
    rest = raw[m.end() :].strip()
    base = root or _skills_root()
    index = load_command_index(base)
    entry = index.get(token)
    if entry is not None:
        rel = str(entry.path.relative_to(base))
        sub = "command_slash" if entry.stem != entry.workflow else "workflow_slash"
        return SlashCommandMatch(
            workflow=entry.workflow,
            command_stem=entry.stem,
            clean_text=rest or raw,
            command_path=rel,
            route_subsource=sub,
        )
    if token in WORKFLOW_AGENTS:
        cmd_path = f".kilo/commands/{token}.md"
        p = (root or _skills_root()) / ".kilo" / "commands" / f"{token}.md"
        if not p.is_file():
            cmd_path = ""
        return SlashCommandMatch(
            workflow=token,
            command_stem=token,
            clean_text=rest or raw,
            command_path=cmd_path,
            route_subsource="workflow_slash",
        )
    return None
