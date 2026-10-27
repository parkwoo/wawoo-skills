# 計画・進捗（plans）

エージェント向けの**タスク状態の正本（SSOT）**を置くディレクトリ。

| ファイル | 役割 |
|----------|------|
| **`ACTIVE.md`** | **L1** 進行中タスク（状態機械） |
| **`BACKLOG.example.md`** | **L2** バックログ表の例（issue tracker のローカル写し） |
| **`RETRO.example.md`** | **L3** 振り返り・PDCA 記録の例 |
| **`CONTENT.example.md`** | **L1 知識** 章・節の進捗（`/content-delivery-lite`） |
| `<feature>.md` | 必要なときだけ `plan-md` による詳細計画（ACTIVE の id とリンク） |

チャット内の「1,2,3 やった」は**証拠にならない**。`ACTIVE.md` の `status` と `証拠` 列を更新する。

儀式の厚み（L0–L3）: `docs/METHODOLOGY.md` §5。

## 検証（Gₑ）

```bash
python3 scripts/plan_active.py docs/plans/ACTIVE.md
python3 scripts/plan_l2_backlog.py docs/plans/BACKLOG.example.md
python3 scripts/plan_l3_record.py docs/plans/RETRO.example.md
python3 scripts/plan_content.py docs/plans/CONTENT.example.md
python3 scripts/e2e_flows.py   # L0–L3 シミュレーション含む（CI 同様）
python3 scripts/cli_adapters_mock.py   # Kilo slash と Cursor @file の parity モック
./scripts/e2e_with_evidence.sh         # 上記一式 + ログを docs/plans/evidence/ に保存

ワークフローごとの E2E の深さ: [E2E-WORKFLOW-COVERAGE.md](./E2E-WORKFLOW-COVERAGE.md)
```
