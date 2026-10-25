# バージョン管理

## 方式
- **Semantic Versioning**：`MAJOR.MINOR.PATCH`（例 `1.4.2`）。
- **`VERSION` が唯一の正本**（リポジトリ直下）。
- 変更履歴は **`CHANGELOG.md`** に追記。
- Git タグ：`v<MAJOR>.<MINOR>.<PATCH>`（例 `v0.1.0`）。

## 何を上げるか
| 変更 | 上げる桁 |
|---|---|
| skill/agent/command の**削除・改名**、MCP ツールの入出力や名前の破壊的変更 | **MAJOR** |
| skill/agent/command の**追加**、後方互換の機能追加 | **MINOR** |
| 誤字修正・文言・内部リファクタ（互換維持） | **PATCH** |

## リリース手順
1. `VERSION` を更新（例 `0.1.0` → `0.2.0`）。
2. `CHANGELOG.md` の先頭に `## [0.2.0] - YYYY-MM-DD` を追加（Added/Changed/Fixed/Removed）。
3. 検証：
   ```bash
   python3 scripts/validate_assets.py
   python3 scripts/gen_capabilities.py
   python3 mcp/test_server.py
   ```
4. コミット：
   ```bash
   git add -A
   git commit -m "release: v0.2.0"
   ```
5. タグ：
   ```bash
   git tag -a v0.2.0 -m "v0.2.0"
   ```
6. 公開（承認後のみ）：
   ```bash
   git push origin master
   git push origin v0.2.0
   ```

## 注意
- カタログ `.kilo/CAPABILITIES.md` は**生成物**。手で編集せず、`gen_capabilities.py` で更新する。
- 破壊的変更（改名・削除）は **CHANGELOG に明記**し、必要なら移行手順を書く。
- ライセンスが不明な資産は追加しない（`ATTRIBUTION.md`）。
