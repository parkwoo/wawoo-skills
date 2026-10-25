# 公開範囲（外部）と内部資産

## 外部（git 管理・クローンに含まれる）

利用者向けのキット本体:

- `README.md`、`AGENTS.md`、`docs/USAGE.md`、`docs/VERSIONING.md`、`docs/memory/`
- `.kilo/`（skills / agents / commands）、`.cursor/rules`、`mcp/`
- `scripts/validate_assets.py`、`scripts/gen_capabilities.py`
- `.github/workflows/`（資産・MCP スモーク）
- `LICENSE`、`LICENSES/`、`.kilo/skills/ATTRIBUTION.md`

## 内部（git 管理外）

メンテナ・監査・実測用。**公開 clone には含まれない**。

| 配置（ローカル） | 内容 |
|---|---|
| `internal/docs/MAINTAINER.md` | メンテナ手順 |
| `internal/docs/audit/` | 監査記録・E2E 手順 |
| `internal/scripts/e2e/` | スモーク・CLI 実測スクリプト |
| `internal/docker/e2e/` | Docker 実測 |
| `internal/scripts/audit_*.py` | 監査生成 |

初回セットアップ:

```bash
./scripts/bootstrap-internal.sh
./internal/scripts/e2e/smoke.sh
```

テンプレートは **`internal.example/`**（git 管理）のみ。運用コピーは `internal/`。

## 秘密

`.env` は従来どおり gitignore（`.env.example` はキー名の例のみ）。
