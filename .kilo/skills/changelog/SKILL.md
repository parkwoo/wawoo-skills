---
name: changelog
description: Generate and maintain user-facing changelog/release notes from git history (Conventional Commits) and keep version/tags consistent. Use before a release or when preparing a PR. Complements release-readiness; does not publish anything.
---

# Changelog / Version

## 前提
- `release-readiness` が版・法務ファイル・タグを確認する。本スキルは**変更履歴の生成**を担う。
- **公開・タグ・push は承認後**（`/release-review`）。

## 手順
1. 範囲を決める：`git log <base>..HEAD --oneline`（前回タグ〜HEAD）。
2. **分類**（Conventional Commits を推奨）：
   - `feat`（新機能）／`fix`（修正）／`perf`／`refactor`／`docs`／`chore`／`BREAKING CHANGE`。
   - ユーザー向け文言に変換（技術的コミットをそのまま載せない）。
3. `CHANGELOG.md` を更新（版・日付・セクション・PR リンク）。
4. **版**：SemVer（`MAJOR.MINOR.PATCH`）。破壊的変更は MAJOR。
5. **タグ/リリースノート**の下書きを作る（公開は承認後）。
6. 証拠：範囲・コミット・分類・版の根拠を示す。

## 注意
- 秘密・個人情報・内部 URL を changelog に載せない。
