# 計画・進捗（plans）

エージェント向けの**タスク状態の正本（SSOT）**を置くディレクトリ。

| ファイル | 役割 |
|----------|------|
| **`ACTIVE.example.md`** → 複製して **`ACTIVE.md`** | **L1** 進行中タスク（状態機械）。実体 `ACTIVE.md` は**非公開**（各プロジェクトで作成） |
| **`BACKLOG.example.md`** | **L2** バックログ表の例（issue tracker のローカル写し） |
| **`RETRO.example.md`** | **L3** 振り返り・PDCA 記録の例 |
| **`CONTENT.example.md`** | **L1 知識** 章・節の進捗（`/content-delivery-lite`） |
| `<feature>.md` | 必要なときだけ `plan-md` による詳細計画（ACTIVE の id とリンク） |

チャット内の「1,2,3 やった」は**証拠にならない**。`ACTIVE.md` の `status` と `証拠` 列を更新する。

儀式の厚み（L0–L3）: `AGENTS.md` §3。

## 検証（Gₑ）

```bash
python3 scripts/plan_active.py docs/plans/ACTIVE.md
python3 scripts/plan_l2_backlog.py docs/plans/BACKLOG.example.md
python3 scripts/plan_l3_record.py docs/plans/RETRO.example.md
python3 scripts/plan_content.py docs/plans/CONTENT.example.md
python3 scripts/e2e_flows.py   # L0–L3 シミュレーション含む（CI 同様）
python3 scripts/cli_adapters_mock.py   # Kilo slash と Cursor @file の parity モック
# 証跡ログ（`internal/scripts/e2e/e2e_with_evidence.sh` → `docs/plans/evidence/`）は内部・メンテナのみ
```
