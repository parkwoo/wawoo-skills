# Memory エントリテンプレート

`memory_save`（MCP）または手動追記で使う最小形式。**追記のみ**（履歴を消さない）。

## 1 件の構造（topic ファイル内）

```markdown
### MEM-YYYYMMDD-NNN

- **日付**: YYYY-MM-DD
- **種別**: 決定 | 制約・落とし穴 | 再発しうる修正 | 未決
- **内容**: 何を決めた／何に気をつけるか（1〜3 文）
- **出典**: ファイル・PR・設計書へのリンク
- **却下した代替**（任意）: 採用しなかった案と理由
```

## INDEX.md への反映

- 該当 `##` セクションに `- \`MEM-...\` 一行要約` を追記。
- `## 履歴` に追記日を 1 行。

## MCP `memory_save` の tags

| 形式 | 意味 |
|------|------|
| `decision` / `constraint` / `gotcha` / `fix` / `open` | 種別（INDEX のセクション） |
| `topic:kit` | `docs/memory/kit.md` に詳細を追記 |
| `決定,topic:cursor` | 日本語種別も可 |

`source` 引数で出典を渡せる。

## topic ファイルの frontmatter（任意）

```yaml
---
tags: cursor, constraint
---
```

想起時に `memory_recall` が参照する。

## 書かないもの

秘密・鍵・個人情報・長大ログ全文（要約＋出典のみ）。
