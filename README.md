# wawoo-skills

AI コーディングエージェント向けの**再利用可能な skills／agents／workflows／MCP サーバ**の汎用キット。
Kilo と Cursor の両方で使える（Cursor は MCP／rules／AGENTS.md 経由）。

## 収録

| 種別 | 件数 | 場所 |
|---|---|---|
| Skills | **55** | `.kilo/skills/<name>/SKILL.md` |
| Agents | **21** | `.kilo/agents/<name>.md` |
| Workflows | **13** | `.kilo/commands/<name>.md` |
| MCP サーバ | 1 | `mcp/server.py`（stdio・stdlib のみ） |
| Cursor ルール | 3 | `.cursor/rules/*.mdc` |

- カタログ（自動生成）：`.kilo/CAPABILITIES.md`
- Readiness：`scripts/readiness.json`／`docs/plans/SKILLS-READINESS.md`
- 呼び出し・コンテキスト設計：`docs/plans/AGENT-INVOCATION-AND-CONTEXT.md`

## クイックスタート

### Kilo
```bash
# このディレクトリを開く（.kilo/ を自動探索、kilo.json で MCP 有効）
```
- ワークフロー：`/feature-delivery` など
- スキル：`/` やモデルが `SKILL.md` を選択

### Cursor
1. このディレクトリを開く（`AGENTS.md` と `.cursor/rules` を読む）
2. **Settings → MCP** で `wawoo-skills` を有効化（`.cursor/mcp.json`）
3. `capabilities`／`skill_search`／`skill_get` をツールとして利用
- **slash command／agent は非対応**。手順は `@.kilo/commands/<name>.md` を開いて適用。
- 詳細：`docs/plans/CURSOR-SETUP.md`

### MCP
```bash
python3 mcp/server.py        # stdio（通常はクライアントが起動）
python3 mcp/test_server.py   # スモークテスト
```

## 保守

```bash
python3 scripts/validate_assets.py   # 資産検証（name=dir・参照・重複・JSON）
python3 scripts/gen_capabilities.py  # カタログ再生成（手編集しない）
python3 mcp/test_server.py           # MCP スモーク
```

## ディレクトリ

```
.kilo/{skills,agents,commands,CAPABILITIES.md}
.cursor/{rules,mcp.json}
mcp/{server.py,test_server.py,README.md}
scripts/{gen_capabilities.py,validate_assets.py,readiness.json}
docs/{plans,memory}
LICENSES/
AGENTS.md
kilo.json
```

## ライセンス・帰属

- 同梱スキルは複数由来（MIT／Apache-2.0／第三者）。詳細は `.kilo/skills/ATTRIBUTION.md` と `LICENSES/`。
- **ライセンス未確認の第三者資産**は再配布しない（`docs/plans/SKILLS-READINESS.md`・`SYSTEM-AUDIT.md`）。
- 本リポジトリは**個人・非公開**前提。

## 注意

- `imagegen-frontend-mobile` はプロンプト指針（画像生成ツールは同梱しない）。
- `to-spec`/`to-tickets`/`triage` は issue tracker 設定が必要。
- 秘密（API キー・トークン）をコミットしない。
