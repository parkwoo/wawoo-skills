# システム監査（汎用キット）

対象：`.kilo`（skills 55・agents 21・commands 13）＋ `mcp`＋`scripts`＋`.cursor`。

## 1. 信頼性
| 検査 | 結果 |
|---|---|
| 件数・`name=dir`・`description`・`mode` | ✅ |
| command→agent 参照・skill 参照解決 | ✅ |
| readiness・JSON（kilo.json／.cursor/mcp.json） | ✅ |
| MCP（initialize/tools/call/パストラバーサル/evidence） | ✅ |
| 秘密スキャン | ✅（プレースホルダのみ） |

## 2. 警告（判断事項）
- **W-1 名称の重なり**：`design-review`・`research` が skill と command に同名。名前空間は別（slash vs モデル選択）だが曖昧。→ 望むなら command を `/ui-review`・`/discovery` に改名。
- **W-2 大きい skill**：`imagegen-frontend-mobile`（約1490行）。必要時のみ取得する設計だが、読込時はトークン大。→ 要約モード推奨。
- **W-3 外部前提**：`to-spec`/`to-tickets`/`triage` は issue tracker 設定が必要。
- **W-4 Cursor**：slash／agent／SKILL をネイティブ実行しない（`AGENTS.md`＋rules＋MCP＋`@file`）。
- **W-5 パス**：`.cursor/mcp.json` は絶対パス。環境差で調整。
- **W-6 ライセンス**：公開のため NOASSERTION 3 件とライセンス不明 1 件を除外済。

## 3. 最適化（推奨）
1. **CI 化**：`validate_assets`＋`gen_capabilities`＋`mcp/test_server`。
2. **計測**：workflow 成功率・平均トークン・再試行・ゲート通過率。
3. **`skill_get` 要約モード**（見出し＋先頭 N 行）で大規模 skill のトークン対策。
4. **command 名の一意化**（W-1）を望む場合。
5. **`evidence_check` の許可制拡張**（lint/test を明示 scope で）。

## 4. 総評
- 構造・参照・MCP は緑。**Kilo はネイティブ、Cursor は rules＋MCP で再現**。
- 残る焦点は**外部前提（tracker）**・**計測**・**大規模 skill のトークン**。
