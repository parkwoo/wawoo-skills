---
name: design-brief
description: |
  Parse a structured design brief written in I-Lang protocol format into a
  concrete design spec. Eliminates ambiguity from vague requests like
  "make it professional" by requiring explicit dimensions: palette, typography,
  layout, mood, density, and constraints.
  Trigger keywords: "design brief", "create a design brief", "ilang brief", "structured brief".
triggers:
  - "design brief"
  - "create a design brief"
  - "ilang brief"
  - "structured brief"
od:
  mode: design-system
  platform: desktop
  scenario: planning
  preview:
    type: html
    entry: brief-preview.html
    reload: debounce-100
  design_system:
    requires: false
    generates: true
    sections: [visual-theme, color-palette, typography, component-stylings, layout, depth-elevation, dos-and-donts, responsive, agent-prompt-guide]
  inputs:
    - name: brief
      type: string
      required: true
      description: "I-Lang formatted design brief or natural language description"
  outputs:
    primary: DESIGN.md
    secondary: brief-preview.html
  capabilities_required:
    - file_write
---
# Design Brief（I-Lang → DESIGN.md）

構造化ブリーフ（I-Lang または自然言語）を `DESIGN.md` とプレビュー用 HTML に落とす。

## コンテキスト予算

- 入口: 本 `SKILL.md`。
- 8 次元・マッピング表・ワークフロー全文: [`references/design-brief-guide.md`](design-brief-guide.md)。

## ゲート

- 未指定の次元は**明示的にフラグ**し、勝手に埋めない。
- 生成物は消費プロジェクトの `DESIGN.md` パスに合わせる（本キット内の `design-systems/` は参照例）。

## ライセンス

Apache-2.0 — 同ディレクトリの `LICENSE.txt` / `NOTICE.txt`。
