# 意図ルーティング（Workflow 選定）

ユーザー依頼を **15 種の workflow**（`.kilo/commands/<id>.md`）のどれで進めるか選び、必要な MCP ツールだけ使えるようにする機能です。**別の LLM API は不要** — Cursor / Kilo の会話モデルが短い JSON でスコアを返します。

本キットは **単体の汎用リポジトリ**です。社内 LLM API（co.taro.bz 等）とは別プロジェクトで、API 側が必要なときだけ `WAWOO_SKILLS_ROOT` で本 MCP を参照します。

- 実装の詳細・常駐受信器: [design/INTENT-RECEIVER.md](design/INTENT-RECEIVER.md)
- MCP ツール一覧: [../mcp/README.md](../mcp/README.md)

---

## 1. いつ使うか

| 使う | 使わなくてよい |
|------|----------------|
| 依頼がどの workflow か曖昧 | 最初から `/delivery-lite` や `/research` を明示している |
| チームで同じ言い回しを学習させたい | 散文だけで `@.kilo/commands/...` を開く運用で足りている |

**儀式レベル L0–L3**（`METHODOLOGY.md` §5）とは別の **ルート層** です。ここでは次の **L0 / L1 / L2 / L3（委譲）** を指します。

| 層 | 意味 | 例 |
|----|------|-----|
| **L0** | ユーザー明示（slash / command） | `/research 調査して` |
| **L1** | 学習済み trigger（SQLite） | 過去に高スコアで覚えたフレーズ |
| **L2** | 上流 LLM が workflow 適合度を付与 | `needs_scoring` → JSON 1 行 |
| **L3** | workflow 実行中の subagent 委譲 | `delegate_subtask`（実行は IDE の Task 等） |

---

## 2. 推奨フロー（MCP）

```text
interpret_intent(text)
  → schedule（workflow, agent, mcp_tools_allow, command_path）
  → workflow_get(name)
  → skill_get … / memory_recall …
  → （並列サブタスク）delegate_subtask(subtask)
  → workflow_clear()
```

1. **`interpret_intent`** — 入力を渡す。`needs_scoring: true` のときはプロンプトに従い **思索モードなし**で JSON 1 行だけ返し、再度 `interpret_intent` に `scoring` を渡す。
2. **`schedule` 確定後** — その workflow で **許可されていない MCP ツールは拒否**される（例: `compliance-review` では `memory_save` 不可）。
3. **`workflow_get`** — `schedule.workflow` と同じ id の command を読む。
4. **`delegate_subtask`** — 大きい作業を切り出すとき。返る JSON を **Cursor Task / Kilo subagent** で実行する（MCP は子セッションを作らない）。
5. **`workflow_clear`** — ゲート解除。別 workflow に切り替える前にも呼ぶ。

人間向けテキストだけ欲しい場合は **`route_task`**（`needs_scoring` 時は誤ルートせず `NEEDS SCORING` を表示）。

---

## 3. `interpret_intent` の返却（要約）

**ルート済み**

```json
{
  "ok": true,
  "route_layer": "L0",
  "schedule": {
    "workflow": "research",
    "workflow_slash": "/research",
    "agent": "product-owner",
    "route_layer": "L0",
    "command_path": ".kilo/commands/research.md",
    "workflow_description": "調査と意思決定…",
    "mcp_tools_allow": ["capabilities", "skill_get", "…"],
    "delegation_hint": "upstream-subagent"
  }
}
```

**スコア待ち（L2）**

```json
{
  "ok": true,
  "needs_scoring": true,
  "route_layer": "L2",
  "upstream_prompt": "…候補(id:いつ使う)=delivery-lite:…|…",
  "no_thinking": true,
  "workflow_catalog": [{"id": "delivery-lite", "description": "…"}]
}
```

**上流 JSON 契約**（1 行・フィールドのみ）

```json
{"workflow":"deck","score":0.88,"trigger":"投資家向け"}
```

- `learn: true` は **再適用時のみ**（高スコアを SQLite に非同期登録。既定は `false`）。
- `workflow` は 15 id のいずれか。台帳外は学習・採用されない。

---

## 4. 常駐受信器（任意）

MCP を都度起動する代わりに、ソケットで常駐させる場合:

```bash
export WAWOO_INTENT_SOCKET=/tmp/wawoo-intent.sock
python3 mcp/intent_receiver.py --socket "$WAWOO_INTENT_SOCKET"
```

MCP で `interpret_intent` に `via_receiver: true` を付与。**未起動ならエラー**（ローカル解釈にフォールバックしない）。

---

## 5. 環境変数

| 変数 | 説明 |
|------|------|
| `WAWOO_SKILLS_ROOT` | キット root（MCP と同じ） |
| `WAWOO_INTENT_LEARN_DB` | 学習 DB パス（既定 `data/intent_learned.db`） |
| `WAWOO_INTENT_SOCKET` | 常駐受信器の Unix ソケット |

---

## 6. テスト

```bash
python3 mcp/test_intent.py
python3 mcp/test_intent_session.py   # ツールゲート・L3
python3 mcp/test_server.py
```

---

## 7. OpenCode / Kilo の subagent との違い

| | OpenCode/Kilo | wawoo-skills |
|--|----------------|--------------|
| workflow 選定 | 主にユーザーが agent 選択 | L0–L2 + 学習 trigger |
| 並列 subagent | ランタイムが子セッション作成 | **L3 は指示 JSON のみ**（IDE が実行） |
| ツール制限 | agent permission | **`mcp_tools_allow` ゲート** |

並列・探索が多い skill（`implement-spec` 等）は、L3 JSON を受け取った **上流エージェント**が Task を並列起動する想定です。

---

## 8. 更新履歴

| 日付 | 内容 |
|------|------|
| 2026-10-26 | 対外ガイド初版（L0–L3・MCP ゲート・delegate） |
