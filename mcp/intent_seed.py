"""Startup learned-DB seed (fresh-install bootstrap).

Since the static trigger table was removed, an empty learned DB is seeded **from the catalog**.
Multilingual and ambiguous inputs are handled by upstream (L2 LLM score); learned grows with use.
"""
from __future__ import annotations

from intent_catalog import WORKFLOWS
from intent_learned_store import IntentLearnedStore

# seed only the distinctive workflow id (do not add common description words; they cause false matches)
_SEED_CONF = 0.8


def seed_learned_store(store: IntentLearnedStore) -> int:
    """Seed an empty learned DB from the catalog (idempotent).

    Does nothing if entries already exist. Returns the number inserted.
    """
    if int(store.stats().get("total", 0)) > 0:
        return 0
    n = 0
    for wid in sorted(WORKFLOWS):
        if store.promote(trigger=wid, workflow=wid, confidence=_SEED_CONF):
            n += 1
    return n
