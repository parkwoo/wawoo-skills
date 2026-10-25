---
name: deployment
description: Plan, execute, and verify a deployment or release (Docker Compose, image tagging, environment, migrations, health checks, rollback). Use when preparing or running a deploy/release, or debugging deployment.
---

# Deployment

## 前提
- 秘密は `.env` のみ。**コミットしない**。
- 対象環境・バックアップ・**ロールバック手順**を先に確認する。

## 手順
1. **事前確認**：`git status`（意図した変更のみ）、`docker compose config`（環境）、バックアップ。
2. **ビルド**：`docker compose build`。イメージに**不変タグ**を付ける（ロールバック用）。
3. **マイグレーション**（ある場合）：バックアップ → 前進 → 戻し手順を用意。
4. **起動**：`docker compose up -d`。
5. **ヘルス**：`curl -s http://127.0.0.1:8080/health` 等。
6. **スモーク**：主要エンドポイント（認証・非stream/SSE 等）。
7. **負荷の確認**（任意）：代表的な同時接続でスモーク。
8. **ロールバック**：前イメージタグへ戻す。DB は復元手順に従う。
9. **証拠**：実行コマンド・結果・未検証項目を記録。

## 禁止
- 秘密・鍵をログや文書に残さない。
- 承認なしの本番反映・破壊的 DB 操作。
