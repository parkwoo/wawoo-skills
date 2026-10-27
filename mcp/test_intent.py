#!/usr/bin/env python3
"""意図解釈・学習ストア・受信器の単体テスト（stdlib のみ）。"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp"))

from intent_interpreter import (  # noqa: E402
    apply_upstream_scoring,
    flush_learn_writes,
    format_needs_scoring_text,
    interpret_intent_payload,
    reset_intent_store,
)
from intent_learned_store import IntentLearnedStore  # noqa: E402
from intent_upstream import UpstreamScoring  # noqa: E402


def test_explicit_workflow() -> None:
    p = interpret_intent_payload("/research OpenAPI の調査")
    assert p["needs_upstream"] is False
    assert p["schedule"]["workflow"] == "research"
    assert p["route_layer"] == "L0"
    assert p["schedule"]["route_layer"] == "L0"
    assert ".kilo/commands/research.md" in p["schedule"]["command_path"]
    assert p["schedule"]["workflow_description"]


def test_catalog_in_upstream_prompt() -> None:
    p = interpret_intent_payload("unique phrase xyz only")
    prompt = p["upstream_prompt"]
    assert "delivery-lite" in prompt
    assert "軽量納品" in prompt
    assert p["workflow_catalog"]


def test_route_layer_learned() -> None:
    db = _test_db()
    os.environ["WAWOO_INTENT_LEARN_DB"] = str(db)
    reset_intent_store()
    try:
        IntentLearnedStore(db).promote(trigger="監査用", workflow="compliance-review", confidence=0.9)
        p = interpret_intent_payload("監査用の確認")
        assert p["route_layer"] == "L1"
        assert "memory_save" not in p["schedule"]["mcp_tools_allow"]
        assert "evidence_check" in p["schedule"]["mcp_tools_allow"]
    finally:
        flush_learn_writes()
        reset_intent_store()
        os.environ.pop("WAWOO_INTENT_LEARN_DB", None)
        if db.exists():
            db.unlink()


def _test_db() -> Path:
    db = ROOT / "data" / "test-intent-run.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    if db.exists():
        db.unlink()
    return db


def test_learned_route() -> None:
    db = _test_db()
    os.environ["WAWOO_INTENT_LEARN_DB"] = str(db)
    reset_intent_store()
    try:
        IntentLearnedStore(db).promote(
            trigger="本番障害",
            workflow="incident-response",
            confidence=0.92,
        )
        p = interpret_intent_payload("本番障害を診断したい")
        assert p["schedule"]["workflow"] == "incident-response"
    finally:
        flush_learn_writes()
        reset_intent_store()
        os.environ.pop("WAWOO_INTENT_LEARN_DB", None)
        if db.exists():
            db.unlink()


def test_upstream_async_learn() -> None:
    db = _test_db()
    os.environ["WAWOO_INTENT_LEARN_DB"] = str(db)
    reset_intent_store()
    try:
        c = UpstreamScoring(workflow="sprint-plan", score=0.91, trigger="スプリント計画")
        apply_upstream_scoring("来週のスプリント計画", c, learn=True)
        flush_learn_writes()
        p = interpret_intent_payload("スプリント計画の見積")
        assert p["schedule"]["source"] == "learned"
    finally:
        flush_learn_writes()
        reset_intent_store()
        os.environ.pop("WAWOO_INTENT_LEARN_DB", None)
        if db.exists():
            db.unlink()


def test_promote_rejects_bad_workflow() -> None:
    db = _test_db()
    ok = IntentLearnedStore(db).promote(trigger="test", workflow="not-a-real-workflow", confidence=0.99)
    assert ok is False
    if db.exists():
        db.unlink()


def test_needs_scoring_route_text() -> None:
    p = interpret_intent_payload("only-unknown-phrase-xyz")
    text = format_needs_scoring_text(p)
    assert "NEEDS SCORING" in text
    assert "upstream_prompt" not in text or "NEEDS SCORING" in text


def test_needs_scoring() -> None:
    reset_intent_store()
    os.environ.pop("WAWOO_INTENT_LEARN_DB", None)
    p = interpret_intent_payload("unique phrase xyz only")
    assert p["needs_upstream"] is True
    assert p["needs_scoring"] is True
    assert "workflows" in p
    assert "upstream_prompt" in p
    assert "score" in p["upstream_prompt"]
    assert p.get("no_thinking") is True


def test_scoring_apply() -> None:
    p = interpret_intent_payload(
        "deck 作って",
        scoring={"workflow": "deck", "score": 0.88, "trigger": "deck作"},
    )
    assert p["schedule"]["workflow"] == "deck"
    assert p["schedule"]["source"] == "upstream"


def test_receiver_ndjson() -> None:
    receiver = ROOT / "mcp" / "intent_receiver.py"
    proc = subprocess.Popen(
        [sys.executable, str(receiver)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(ROOT),
    )
    try:
        line = json.dumps(
            {
                "id": "t1",
                "text": "投資家向け",
                "classification": {"workflow": "deck", "score": 0.9, "trigger": "投資家向け"},
            }
        ) + "\n"
        proc.stdin.write(line)
        proc.stdin.flush()
        out = proc.stdout.readline()
        data = json.loads(out)
        assert data["schedule"]["workflow"] == "deck"
    finally:
        proc.stdin.close()
        proc.wait(timeout=5)


def test_receiver_socket() -> None:
    receiver = ROOT / "mcp" / "intent_receiver.py"
    with tempfile.TemporaryDirectory() as tmp:
        sock = Path(tmp) / "intent.sock"
        proc = subprocess.Popen(
            [sys.executable, str(receiver), "--socket", str(sock)],
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(ROOT),
        )
        try:
            for _ in range(50):
                if sock.exists():
                    break
                time.sleep(0.05)
            import socket as sock_mod

            payload = json.dumps({"id": "s1", "text": "/deck 提案"}) + "\n"
            with sock_mod.socket(sock_mod.AF_UNIX, sock_mod.SOCK_STREAM) as client:
                client.settimeout(2.0)
                client.connect(str(sock))
                client.sendall(payload.encode("utf-8"))
                chunks = b""
                while b"\n" not in chunks:
                    chunks += client.recv(4096)
            data = json.loads(chunks.decode("utf-8").split("\n", 1)[0])
            assert data["schedule"]["workflow"] == "deck"
        finally:
            proc.terminate()
            proc.wait(timeout=5)


def main() -> int:
    test_explicit_workflow()
    test_catalog_in_upstream_prompt()
    test_route_layer_learned()
    test_learned_route()
    test_upstream_async_learn()
    test_promote_rejects_bad_workflow()
    test_needs_scoring()
    test_needs_scoring_route_text()
    test_scoring_apply()
    test_receiver_ndjson()
    test_receiver_socket()
    print("intent tests: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
