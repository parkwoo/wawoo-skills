# L2 バックログ（例）

**SSOT**: issue tracker が無い場合のローカル代替。本番運用は GitHub Issues 等を正本にし、ここは同期用の写しに留める。

## バックログ

**優先度＝行の順序**。順序は `depends` 列から**自動検証**され、`--apply` で**自動整列**できる（内容・証拠は不変）。決定（D1 等）は `depends` に書かない。

| issue | status | title | evidence | depends |
|-------|--------|-------|----------|---------|
| — | — | （スプリント計画時に追加） | | |

`status`: `open` → `in_progress`（同時 1 件）→ `done`（証拠必須）／`blocked`

検証/整列: `python3 scripts/plan_l2_backlog.py docs/plans/BACKLOG.example.md [--apply]`
