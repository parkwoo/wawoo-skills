# 記憶ツールの優先順位（Kilo / Cursor / MCP）

複数の記憶手段が同時に使えるときの**競合時ルール**。詳細手順は `.kilo/skills/memory/SKILL.md`。

## 取得（recall）

| 順位 | 手段 | 使う条件 |
|------|------|----------|
| 1 | MCP `memory_recall` | Cursor／MCP 接続時。`docs/memory/` をチャンク単位で返す |
| 2 | `docs/memory/INDEX.md` を読む | MCP 無し・軽量確認 |
| 3 | `docs/memory/<topic>.md` | トピックが分かっているとき |
| 4 | Kilo `kilo_memory_recall` | Kilo ネイティブが有効なとき。**ファイルと矛盾したらファイルを正**とし、Kilo 側を更新する |

## 保存（save）

| 順位 | 手段 | 使う条件 |
|------|------|----------|
| 1 | MCP `memory_save` | INDEX＋topic ファイルへ構造化追記（推奨） |
| 2 | 手動で `INDEX`／`<topic>.md` 追記 | テンプレは `TEMPLATE.md` |
| 3 | Kilo `kilo_memory_save` | 補助。**必ず** `docs/memory/` に同内容を反映（または export） |

## 正本（SSOT）

このキットでは **`docs/memory/` の Markdown** が正本。Kilo 内蔵メモリはセッション補助に留める。

## 工程との接続

- **D7／P4**（振り返りの還元）: 新しい制約・落とし穴・決定は `memory` に残す。`docs/PROCESS-PHILOSOPHY.md` §11 P4。
