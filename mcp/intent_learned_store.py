"""学習済み意図ルート（動的・SQLite）。高信頼 LLM 判定だけを蓄積する。"""
from __future__ import annotations

import os
import re
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from intent_catalog import WORKFLOW_AGENTS

PatternKind = Literal["substring", "regex"]

_MAX_REGEX_LEN = 160
_FORBIDDEN_REGEX = re.compile(r"(\(\?|\(\*|\+|\{\d*,\d*\}|\\1)")


def default_db_path(root: Path | None = None) -> Path:
    env = os.environ.get("WAWOO_INTENT_LEARN_DB", "").strip()
    if env:
        return Path(env).expanduser()
    base = root or Path(__file__).resolve().parents[1]
    data = base / "data"
    data.mkdir(parents=True, exist_ok=True)
    return data / "intent_learned.db"


@dataclass
class LearnedRoute:
    route_id: int
    trigger: str
    kind: PatternKind
    workflow: str
    confidence: float
    hit_count: int

    def matches(self, text: str) -> bool:
        lower = text.lower()
        if self.kind == "substring":
            return self.trigger in lower
        try:
            return bool(re.search(self.trigger, text, re.IGNORECASE))
        except re.error:
            return False


class IntentLearnedStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS learned_routes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trigger_text TEXT NOT NULL,
                    kind TEXT NOT NULL DEFAULT 'substring',
                    workflow TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    hit_count INTEGER NOT NULL DEFAULT 0,
                    created_at REAL NOT NULL,
                    last_hit_at REAL,
                    UNIQUE(trigger_text, kind, workflow)
                )
                """
            )
            conn.commit()

    @staticmethod
    def safe_regex(pattern: str) -> str | None:
        p = (pattern or "").strip()
        if not p or len(p) > _MAX_REGEX_LEN:
            return None
        if _FORBIDDEN_REGEX.search(p):
            return None
        try:
            re.compile(p, re.IGNORECASE)
        except re.error:
            return None
        return p

    def find_match(self, text: str) -> LearnedRoute | None:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, trigger_text, kind, workflow, confidence, hit_count
                FROM learned_routes
                ORDER BY LENGTH(trigger_text) DESC, confidence DESC, hit_count DESC
                """
            ).fetchall()
        for row in rows:
            route = LearnedRoute(
                route_id=row[0],
                trigger=row[1],
                kind=row[2],
                workflow=row[3],
                confidence=row[4],
                hit_count=row[5],
            )
            if route.matches(text):
                return route
        return None

    def record_hit_sync(self, route_id: int) -> None:
        now = time.time()
        with self._connect() as conn:
            conn.execute(
                "UPDATE learned_routes SET hit_count = hit_count + 1, last_hit_at = ? WHERE id = ?",
                (now, route_id),
            )
            conn.commit()

    def promote(
        self,
        *,
        trigger: str,
        workflow: str,
        confidence: float,
        kind: PatternKind = "substring",
        regex_pattern: str | None = None,
    ) -> bool:
        """信頼度が閾値以上のときだけ呼ぶ。"""
        if workflow not in WORKFLOW_AGENTS:
            return False
        trigger_norm = (trigger or "").strip().lower()
        if not trigger_norm or not workflow:
            return False
        if kind == "regex":
            safe = self.safe_regex(regex_pattern or trigger)
            if not safe:
                kind = "substring"
                store_trigger = trigger_norm
            else:
                store_trigger = safe
        else:
            store_trigger = trigger_norm[:120]
            kind = "substring"

        now = time.time()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO learned_routes (trigger_text, kind, workflow, confidence, hit_count, created_at)
                VALUES (?, ?, ?, ?, 0, ?)
                ON CONFLICT(trigger_text, kind, workflow) DO UPDATE SET
                    confidence = MAX(learned_routes.confidence, excluded.confidence)
                """,
                (store_trigger, kind, workflow, confidence, now),
            )
            conn.commit()
        return True

    def stats(self) -> dict:
        with self._connect() as conn:
            total = conn.execute("SELECT COUNT(*) FROM learned_routes").fetchone()[0]
            top = conn.execute(
                "SELECT workflow, COUNT(*) FROM learned_routes GROUP BY workflow ORDER BY 2 DESC LIMIT 5"
            ).fetchall()
        return {"total": total, "by_workflow": {w: c for w, c in top}}
