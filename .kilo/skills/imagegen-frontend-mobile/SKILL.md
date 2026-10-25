---
name: imagegen-frontend-mobile
description: |
  モバイルアプリ向けの高品質画像コンセプト用スキル。iOS/Android 向け画面・フローのプロンプトとビジュアル指針を提供する（コードは書かない）。詳細な英語プロンプト集は references に分離。
triggers:
  - "mobile app image"
  - "mobile UI concept"
  - "ios app mockup"
  - "android app mockup"
od:
  mode: image
  surface: image
  platform: mobile
  scenario: design
  category: image-generation
  upstream: "https://github.com/Leonxlnx/taste-skill"
  preview:
    type: markdown
  design_system:
    requires: true
  craft:
    requires:
      - typography
      - color
      - anti-ai-slop
  example_prompt: |
    Generate premium mobile app concept frames for this product brief, with readable app-native hierarchy and a consistent visual system across screens.
---

> **実行**：画像生成は**利用可能な画像ツール**（OpenAI Images／fal／社内ツール等）で行う。本スキルは**モバイル UI のプロンプト／ビジュアル指針**を提供する。ツールが無い場合は**プロンプトのみ**納品する。

## コンテキスト予算（例外）

本スキルは **通常の Skill 予算（2〜4KB）の例外**です。入口はこの `SKILL.md` のみ読む。詳細プロンプト・チェックリストは **必要時だけ** `references/mobile-image-direction.md` を開く（約 40KB・英語）。

## 手順

1. プロダクトブリーフ（画面数・プラットフォーム・ブランドトーン）を確認する。
2. 画像ツールが使えるか確認する。無い場合は下記参照からプロンプトを組み立てて**テキスト納品**する。
3. 複数画面は**同一ビジュアルシステム**（色・タイポ・角丸・余白）で揃える。
4. 出力はアプリ UI 本体を主役にし、必要なら控えめな端末フレームで見せる。
5. ウェブ LP・デスクトップ・実装コードは本スキルの対象外とする。

## ゲート

- 実在の商標・人物・著作物を無断で模倣しない（依頼者の権利確認）。
- 個人情報や秘密をプロンプトに含めない。
- 生成物の利用範囲（商用・学習利用等）は**依頼者／法務**が決める。本スキルは法的判断をしない。

## 参照（段階的開示）

- 全文プロンプトガイド（英語）：[`references/mobile-image-direction.md`](references/mobile-image-direction.md)
- ライセンス：同ディレクトリの `LICENSE`
