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
# Design Brief (I-Lang → DESIGN.md)

Turn a structured brief (I-Lang or natural language) into `DESIGN.md` and a preview HTML.

## Context budget

- Entry: this `SKILL.md`.
- The 8 dimensions, the mapping table, and the full workflow: [`references/design-brief-guide.md`](design-brief-guide.md).

## Gates

- **Flag** unspecified dimensions explicitly; do not fill them in on your own.
- Match the artifact to the consuming project's `DESIGN.md` path (`design-systems/` in this kit is a reference example).

## License

Apache-2.0 — see `LICENSE.txt` / `NOTICE.txt` in the same directory.
