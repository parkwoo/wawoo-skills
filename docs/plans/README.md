# Plans / progress (plans)

> Japanese version: [README.ja.md](README.ja.md)

A directory holding the **task-state source of truth (SSOT)** for agents.

| File | Role |
|----------|------|
| **`ACTIVE.example.md`** → copy to **`ACTIVE.md`** | **L1** in-progress tasks (state machine). The real `ACTIVE.md` is **non-public** (created per project) |
| **`BACKLOG.example.md`** | **L2** backlog table example (a local copy of an issue tracker) |
| **`RETRO.example.md`** | **L3** retro / PDCA record example |
| **`CONTENT.example.md`** | **L1 knowledge** chapter/section progress (`/content-delivery-lite`) |
| `<feature>.md` | A detailed plan via `plan-md` only when needed (linked from the ACTIVE id) |

A chat "1,2,3 done" is **not evidence**. Update the `status` and the evidence column in `ACTIVE.md`.

Ceremony weight (L0–L3): `AGENTS.md` §3.

## Validation (Gₑ)

```bash
python3 scripts/plan_active.py docs/plans/ACTIVE.md
python3 scripts/plan_l2_backlog.py docs/plans/BACKLOG.example.md
python3 scripts/plan_l3_record.py docs/plans/RETRO.example.md
python3 scripts/plan_content.py docs/plans/CONTENT.example.md
python3 scripts/e2e_flows.py   # includes the L0–L3 simulation (same as CI)
python3 scripts/cli_adapters_mock.py   # Kilo slash vs Cursor @file parity mock
# Evidence logs (`internal/scripts/e2e/e2e_with_evidence.sh` → `docs/plans/evidence/`) are internal, maintainers only
```
