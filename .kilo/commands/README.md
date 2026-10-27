# ワークフロー（commands）— プロセスの所有者

本プロジェクトは **ワークフロー主導**。プロセスは commands が所有し、**Skills For Real Engineers の思考法・解法を各ステップに埋め込む**。agent が skill を飛ばす前提で、workflow が**明示的に呼ぶ**。

## 一覧（15）

**正本**: 下表の「主なスキル鎖」は概要。手順の SSOT は各 `commands/<name>.md` 本文。

| command | 用途 | 主なスキル鎖 |
|---|---|---|
| `/delivery-lite` | **L1 コード** — ACTIVE.md 状態機械で軽量納品 | `plan-md`（任意）→`implement`→`engineering-quality`→検証 |
| `/content-delivery-lite` | **L1 知識** — 書籍・長文・レポート（CONTENT.md） | `plan-md`→`writing-for-agents`→`plan_content.py` |
| `/ui-delivery` | UI 納品（ACTIVE + DESIGN） | `web-experience-design`→実装→audit |
| `/feature-delivery` | L1 超・ゲート多め — discovery→design→implement→test→review | 本文の skill 鎖（README 表と異なる場合は**本文優先**） |
| `/design-review` | UI の設計レビュー | `design-review`→`web-design-guidelines`→`accessibility-audit` |
| `/research` | 調査→意思決定 | `research`→`research-decision-room`→`product-discovery`→`to-spec`/`plan-md` |
| `/market-plan` | 市場調査→戦略→計画 | `research`→`research-decision-room`→`product-discovery`→`marketing-psychology`→`plan-md`（`competitive-ads*` は任意） |
| `/deck` | 提案・計画デッキ | `research`/`research-decision-room`→`marketing-psychology`→`slides`（Markdown/HTML。pptx 任意） |
| `/compliance-review` | 法務・プライバシー・セキュリティのゲート | `compliance-legal`→`privacy-review`→`security-review`→`release-readiness` |
| `/release-review` | リリース前確認 | `release-readiness`→`compliance-legal`/`privacy-review`→`security-review`→`documentation-localization` |
| `/incident-response` | 障害対応 | `incident-debugging`→`engineering-quality`→`retro` |
| `/sprint-plan` | スプリント計画 | `wayfinder`→`to-tickets`→優先度/見積/容量→`plan-md` |
| `/status-report` | 進捗・状況報告 | `triage`/`to-tickets`→進捗・リスク→`plan-md` |
| `/self-review` | 自己修正 | `code-review`→`code-skeptic`→`diagnosing-bugs`/`tdd`→修正→検証→`memory` |
| `/self-improve` | 自己改善（PDCA） | `retro`→`pdca-cycle`→`self-review`/`code-simplifier`→`plan-md`→`memory` |

## ゲート（必須）
- **承認**：破壊的変更・本番・削除・外部送信・契約/規約は停止して承認。
- **証拠**：実行コマンド・結果・スクショ/diff。実測／未検証を区別。
- **失敗観察**：Skills For Real Engineers の原則（observed failure）に倣い、推測ではなく実際に起きた失敗に基づく。
- **法務**：法的判断は人が行う（`compliance-legal` は証拠とチェックのみ）。

