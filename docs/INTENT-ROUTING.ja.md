# 意図ルーティング（Workflow 選定）

ユーザー依頼を **16 種の workflow**（`.kilo/commands/<id>.md`）のどれで進めるか選び、必要な MCP ツールだけ使えるようにする機能です。**別の LLM API は不要** — Cursor / Kilo の会話モデルが短い JSON でスコアを返します。

本キットは **単体の汎用リポジトリ**です。社内 LLM API（co.taro.bz 等）とは別プロジェクトで、API 側が必要なときだけ `WAWOO_SKILLS_ROOT` で本 MCP を参照します。

- 実装の詳細: `mcp/README.md`
- MCP ツール一覧: [../mcp/README.md](../mcp/README.md)

---

## 1. いつ使うか

| 使う | 使わなくてよい |
|------|----------------|
| 依頼がどの workflow か曖昧 | 最初から `/delivery-lite` や `/research` を明示している |
| チームで同じ言い回しを学習させたい | 散文だけで `@.kilo/commands/...` を開く運用で足りている |

**儀式レベル L0–L3**（`AGENTS.md` §3）とは別の **ルート層** です。ここでは次の **L0 / L1 / L2 / L3（委譲）** を指します。

| 層 | 意味 | 例 |
|----|------|-----|
| **L0** | ユーザー明示（slash / command） | `/research 調査して` |
| **L1** | 学習済み trigger（SQLite） | 過去に高スコアで覚えたフレーズ |
| **L2** | 上流 LLM が workflow 適合度を付与 | `needs_scoring` → JSON 1 行 |
| **L3** | workflow 実行中の subagent 委譲 | `delegate_subtask`（実行は IDE の Task 等） |

> **注**: ここでの `L0–L3` は**ルート層**（依頼がどうルーティングされるか）です。`AGENTS.md` §3 の**儀式レベル** `L0–L3`（タスクが背負うプロセスの重さ）とは**別の軸**。同じ文字・別の意味。

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

**Amend / steer**: `steer_task {text}` は**実行中計画を文脈**に `amend` 指示を返す。`op` 無しは `needs_classification`（ホスト LLM が add/reorder/reprioritize/scope_change/abort と target を決め `op`/`target` 付きで再呼び出し）。計画ファイルは書かず、ホストが**ステップ境界**で適用する。


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
- `workflow` は 16 id のいずれか。台帳外は学習・採用されない。

---

## 3.1 解決の層（決定論 → 学習 → 上流）

`interpret_intent` は **L0 slash → L1 学習（learned）→ L2 上流スコア（LLM）** の順で解決する。

- **L0 slash**: `/workflow ...` は明示として即時採用（`route_layer: "L0"`）。
- **L1 学習（learned）**: `data/intent_learned.db`（SQLite）の高信頼ルートに部分一致すれば採用（`source: "learned"`）。多言語を人手で並べる**静的 trigger 表は廃止**（`TRIGGER_KEYWORDS`/`WEAK_TRIGGERS` は撤去）。
- **seed**: 空の学習 DB は **catalog（workflow id）から自動 seed** してブートストラップ。旧語彙はローカルの学習 DB に移行する（**配布しない**）。
- **L2 上流スコア**: 一致しなければ `needs_scoring: true` を返し、ホスト LLM が `workflow`+`score` を付けて再呼び出しする（`source: "upstream"`）。
- **言語非依存**: 語彙メンテをやめ、**learned（利用で育つ）＋ upstream（LLM）** に委ねる（多言語耐性）。

## 3.2 フェーズ（workflow の分解）

各 workflow は **phase** に分解され、`schedule.phases` と `workflow_get {name, phase:<id>}` で取得できる。

```json
{"id":"audit","goal":"読み取り専用の審査","agent":"security-reviewer",
 "skills":["security-review"],"mcp_tools_allow":["skill_get","memory_recall","…"],
 "exit_criteria":["所見と証跡（重要度付き）"],"parallel_group":"readonly-parallel"}
```

- **P2: phase 単位の道具立て** — `audit`/`research`/`verify` は `readonly-parallel`（並列可・読み取り中心）。実装系の workflow だけが `implement` を持つ。
- **監査系に `implement` は無い** — `design-review`・`compliance-review`・`release-review`・`self-review` では `schedule.gate` が非空になり、実装が必要なら **workflow 切替を宣言**する。
- **P3: 並列委譲** — 独立した対象は `delegate_subtask {subtask, phase}` で phase の `exit_criteria` を添えて subagent に渡す（MCP は子セッションを作らない）。
- **P4: 完了条件** — `exit_criteria` を満たすまで phase を閉じない（例: `verify` は「未収束 FAILED 0／残留コンテナ 0」）。

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
| `WAWOO_INTENT_SESSION` | セッション永続化ファイル（ゲート最小項目のみ。既定 `<root>/data/intent_session.json`） |
| `WAWOO_INTENT_RESUME` | `1`/`true` で再起動後に永続ゲートを復元（既定 off。有効時のみ書込） |
| `WAWOO_INTENT_CLIENT` | クライアント別セッション名（`intent_session.<client>.json`）で混線回避 |

---

## 6. テスト

```bash
python3 scripts/e2e_flows.py   # 公開 E2E（interpret/route・ツールゲート・L3 を含む）
# 単体テスト（test_intent*・test_server）は internal/tests/（非公開・メンテナのみ）
```

---

## 7. OpenCode / Kilo の subagent との違い

| | OpenCode/Kilo | wawoo-skills |
|--|----------------|--------------|
| workflow 選定 | 主にユーザーが agent 選択 | L0–L2 + 学習 trigger |
| 並列 subagent | ランタイムが子セッション作成 | **L3 は指示 JSON のみ**（IDE が実行） |
| ツール制限 | agent permission | **`mcp_tools_allow` ゲート** |

並列・探索が多い skill（`implement-spec` 等）は、L3 JSON を受け取った **上流エージェント**が Task を並列起動する想定です。

**委譲の所有権**: サブタスクは生成した呼び出し／phase が所有。abort は下から上へ伝播。foreground はターンとともに abort、background は追跡＋後始末。`delegate_subtask` は指示のみ（実行はホスト）。


---

## 8. 更新履歴

| 日付 | 内容 |
|------|------|
| 2026-10-26 | 対外ガイド初版（L0–L3・MCP ゲート・delegate） |
| 2026-10-28 | 静的 trigger 表を撤去し、解決順を slash → 学習（seed）→ 上流 に変更。`NAME.ja.md`（日本語版）を追加 |
