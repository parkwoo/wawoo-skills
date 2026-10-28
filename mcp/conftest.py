"""pytest 用の共通フィクスチャ。

`mcp/test_intent.py` は単体実行時、`main()` が隔離 DB を設定してから各テストを呼ぶ。
しかし pytest 収集では `main()` を経由しないため、学習ストア（既定 `data/intent_learned.db`）を
そのまま読み、L1 トリガ層のテストが "learned" に汚染される（例: `test_trigger_classifier_ja`）。
本フィクスチャは各テストを一時 DB に隔離して、pytest 実行でも決定的にする。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp"))

from intent_interpreter import flush_learn_writes, reset_intent_store  # noqa: E402


@pytest.fixture(autouse=True)
def _isolate_learn_db(tmp_path, monkeypatch):
    db = tmp_path / "intent_learned.db"
    monkeypatch.setenv("WAWOO_INTENT_LEARN_DB", str(db))
    reset_intent_store()
    try:
        yield
    finally:
        flush_learn_writes()
        reset_intent_store()
