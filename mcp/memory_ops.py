"""Read/write/recall for docs/memory (stdlib only). Used by the server and tests."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

SECRET_PATTERNS = re.compile(
    r"(sk-[A-Za-z0-9]{8,}|AKIA[0-9A-Z]{12,}|ghp_[A-Za-z0-9]{20,}|"
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|password\s*=|token\s*=)",
    re.IGNORECASE,
)

SECTION_KEYS = {
    "decision": "決定",
    "constraint": "制約・落とし穴",
    "gotcha": "制約・落とし穴",
    "fix": "再発しうる修正",
    "open": "未決",
}

TAG_ALIASES = {
    "決定": "decision",
    "制約": "constraint",
    "落とし穴": "gotcha",
    "再発": "fix",
    "未決": "open",
}


def sanitize_topic(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", name.strip().lower()).strip("-")
    return s[:64] or "general"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            meta[m.group(1)] = m.group(2).strip()
    body = text[end + 4 :].lstrip("\n")
    return meta, body


def split_memory_chunks(text: str, path_name: str) -> list[tuple[str, str, int]]:
    """List of (chunk_id, chunk_text, base_score_boost)."""
    chunks: list[tuple[str, str, int]] = []
    boost = 3 if path_name.upper() == "INDEX.MD" else 0
    meta, body = parse_frontmatter(text)
    if meta.get("tags"):
        chunks.append((f"{path_name}#fm", f"tags: {meta['tags']}\n{body[:500]}", boost + 1))

    for m in re.finditer(r"^###\s+(MEM-[^\s]+)\s*$", body, re.MULTILINE):
        start = m.start()
        nxt = re.search(r"^###\s+MEM-", body[m.end() :], re.MULTILINE)
        end = m.end() + nxt.start() if nxt else len(body)
        chunk = body[start:end].strip()
        if chunk:
            chunks.append((f"{path_name}#{m.group(1)}", chunk, boost + 2))

    for m in re.finditer(r"^##\s+(.+)$", body, re.MULTILINE):
        title = m.group(1).strip()
        start = m.end()
        nxt = re.search(r"^##\s+", body[start:], re.MULTILINE)
        end = start + nxt.start() if nxt else len(body)
        section = body[start:end].strip()
        if section and title != "履歴":
            chunks.append((f"{path_name}#{title}", f"## {title}\n{section[:800]}", boost + 1))

    if not chunks:
        chunks.append((path_name, body[:1200], boost))
    return chunks


def score_chunk(chunk: str, terms: list[str]) -> int:
    low = chunk.lower()
    if not terms:
        return 0
    return sum(low.count(t) for t in terms)


def recall_memory(memory_dir: Path, query: str, top_k: int = 5) -> str:
    q = query.lower().strip()
    terms = [t for t in re.split(r"\W+", q) if len(t) >= 2]
    hits: list[tuple[int, str, str]] = []

    if not memory_dir.is_dir():
        return "no memory matches"

    for p in sorted(memory_dir.glob("*.md")):
        if p.name.startswith("_"):
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for cid, chunk, boost in split_memory_chunks(text, p.name):
            sc = score_chunk(chunk, terms) + (boost if terms else boost // 2)
            if terms and score_chunk(chunk, terms) == 0:
                continue
            hits.append((sc, cid, chunk[:900]))

    if not terms:
        # Empty query: order by boost (INDEX and MEM headings first)
        hits = [(sc, cid, ch) for sc, cid, ch in hits if sc > 0]
        if not hits:
            idx = memory_dir / "INDEX.md"
            if idx.exists():
                tail = idx.read_text(encoding="utf-8", errors="ignore")[-1500:]
                return f"[INDEX.md]\n{tail}"
            return "no memory matches"

    hits.sort(key=lambda x: -x[0])
    if not hits:
        return "no memory matches"
    return "\n\n".join(f"[{cid} score={sc}]\n{ch}" for sc, cid, ch in hits[:top_k])


def resolve_kind_and_topic(tags: str) -> tuple[str, str]:
    """tags: 'decision,topic:kit' or a Japanese kind."""
    parts = [p.strip() for p in tags.split(",") if p.strip()]
    kind = "fix"
    topic = "general"
    for p in parts:
        low = p.lower()
        if low.startswith("topic:"):
            topic = sanitize_topic(p.split(":", 1)[1])
            continue
        if low in SECTION_KEYS:
            kind = low
            continue
        if p in TAG_ALIASES:
            kind = TAG_ALIASES[p]
            continue
        if ":" not in p and not p.startswith("MEM-"):
            topic = sanitize_topic(p)
    return kind, topic


def next_mem_id(memory_dir: Path) -> str:
    day = datetime.now(timezone.utc).strftime("%Y%m%d")
    prefix = f"MEM-{day}-"
    n = 0
    for p in memory_dir.glob("*.md"):
        for m in re.findall(rf"\b{prefix}(\d{{3}})\b", p.read_text(encoding="utf-8", errors="ignore")):
            n = max(n, int(m))
    return f"{prefix}{n + 1:03d}"


def format_entry(mem_id: str, text: str, kind: str, source: str = "") -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    section_ja = SECTION_KEYS.get(kind, "再発しうる修正")
    src_line = f"- **出典**: {source}\n" if source else ""
    return (
        f"### {mem_id}\n\n"
        f"- **日付**: {stamp}\n"
        f"- **種別**: {section_ja}\n"
        f"- **内容**: {text}\n"
        f"{src_line}"
    )


def append_to_index(index_path: Path, kind: str, mem_id: str, one_line: str) -> None:
    section_ja = SECTION_KEYS.get(kind, "再発しうる修正")
    text = index_path.read_text(encoding="utf-8", errors="ignore")
    header = f"## {section_ja}"
    bullet = f"- `{mem_id}` {one_line}"
    if header in text:
        pos = text.index(header) + len(header)
        rest = text[pos:]
        nxt = re.search(r"\n## ", rest)
        insert_at = pos + (nxt.start() if nxt else len(rest))
        text = text[:insert_at].rstrip() + "\n" + bullet + "\n" + text[insert_at:].lstrip("\n")
    else:
        text = text.rstrip() + f"\n\n{header}\n{bullet}\n"
    hist = "## 履歴"
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    hist_line = f"- {stamp} 追記 `{mem_id}`（{section_ja}）。"
    if hist in text:
        text = text.rstrip() + "\n" + hist_line + "\n"
    else:
        text = text.rstrip() + f"\n\n{hist}\n{hist_line}\n"
    index_path.write_text(text, encoding="utf-8")


def ensure_topic_file(topic_path: Path, topic: str) -> None:
    if topic_path.exists():
        return
    topic_path.write_text(
        f"---\ntags: {topic}\n---\n\n# {topic}\n\n"
        "決定・制約・落とし穴の詳細。`memory` スキルと `docs/memory/TEMPLATE.md` に従う。\n",
        encoding="utf-8",
    )


def save_memory(
    memory_dir: Path,
    text: str,
    tags: str = "",
    source: str = "",
) -> str:
    if not text.strip():
        raise ValueError("empty text")
    if SECRET_PATTERNS.search(text):
        raise ValueError("refused: possible secret detected")

    memory_dir.mkdir(parents=True, exist_ok=True)
    kind, topic = resolve_kind_and_topic(tags)
    mem_id = next_mem_id(memory_dir)
    entry = format_entry(mem_id, text.strip(), kind, source.strip())

    index_path = memory_dir / "INDEX.md"
    if not index_path.exists():
        index_path.write_text(
            "# Memory Index\n\n"
            "永続知識の索引。`docs/memory/TEMPLATE.md` を参照。\n",
            encoding="utf-8",
        )

    one_line = text.strip().replace("\n", " ")[:200]
    append_to_index(index_path, kind, mem_id, one_line)

    topic_path = memory_dir / f"{topic}.md"
    ensure_topic_file(topic_path, topic)
    with topic_path.open("a", encoding="utf-8") as f:
        f.write("\n" + entry + "\n")

    return (
        f"saved {mem_id} -> {index_path.name} + {topic_path.name} "
        f"(kind={kind}, topic={topic})"
    )


def scan_memory_secrets(memory_dir: Path) -> list[str]:
    issues: list[str] = []
    if not memory_dir.is_dir():
        return issues
    for p in sorted(memory_dir.glob("*.md")):
        if p.name.startswith("_"):
            continue
        body = p.read_text(encoding="utf-8", errors="ignore")
        if SECRET_PATTERNS.search(body):
            issues.append(f"possible secret in memory file: docs/memory/{p.name}")
    return issues
