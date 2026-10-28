"""Make learned-DB writes async (do not block the response)."""
from __future__ import annotations

import os
import queue
import threading
from pathlib import Path
from typing import Any

from intent_learned_store import IntentLearnedStore

_queue: queue.Queue[tuple[str, dict[str, Any]]] | None = None
_thread: threading.Thread | None = None
_lock = threading.Lock()


def _debug(msg: str) -> None:
    if os.environ.get("WAWOO_INTENT_DEBUG", "").strip().lower() in {"1", "true", "yes"}:
        print(f"[intent-learn-queue] {msg}", file=__import__("sys").stderr)


def _store_from_payload(payload: dict[str, Any]) -> IntentLearnedStore:
    path = Path(str(payload["db_path"]))
    return IntentLearnedStore(path)


def _worker() -> None:
    while True:
        kind, payload = _queue.get()  # type: ignore[union-attr]
        try:
            store = _store_from_payload(payload)
            if kind == "promote":
                store.promote(**{k: v for k, v in payload.items() if k != "db_path"})
            elif kind == "hit":
                store.record_hit_sync(int(payload["route_id"]))
        except Exception as exc:
            _debug(f"{kind} failed: {exc}")
        finally:
            q = _queue
            if q is not None:
                q.task_done()


def _ensure() -> None:
    global _queue, _thread
    with _lock:
        if _queue is None:
            _queue = queue.Queue()
            _thread = threading.Thread(target=_worker, daemon=True, name="intent-learn-writer")
            _thread.start()


def enqueue_promote(store: IntentLearnedStore, **kwargs: Any) -> None:
    _ensure()
    _queue.put(("promote", {"db_path": str(store.db_path), **kwargs}))  # type: ignore[union-attr]


def enqueue_hit(store: IntentLearnedStore, route_id: int) -> None:
    _ensure()
    _queue.put(("hit", {"db_path": str(store.db_path), "route_id": route_id}))  # type: ignore[union-attr]


def reset_learn_queue() -> None:
    """For tests: call after draining pending jobs (the worker thread is kept)."""
    return


def flush(store: IntentLearnedStore, timeout: float = 5.0) -> None:
    """Drain the pending queue synchronously."""
    if _queue is None:
        return
    import time

    deadline = time.time() + timeout
    while time.time() < deadline:
        drained = False
        while True:
            try:
                kind, payload = _queue.get_nowait()
            except queue.Empty:
                break
            drained = True
            try:
                s = _store_from_payload(payload)
                if kind == "promote":
                    s.promote(**{k: v for k, v in payload.items() if k != "db_path"})
                elif kind == "hit":
                    s.record_hit_sync(int(payload["route_id"]))
            except Exception as exc:
                _debug(f"flush {kind} failed: {exc}")
            finally:
                _queue.task_done()
        if not drained and _queue.unfinished_tasks == 0:
            return
        time.sleep(0.02)
