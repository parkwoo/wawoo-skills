---
name: imagegen-frontend-mobile
description: |
  A skill for high-quality image concepts for mobile apps. Provides prompts and visual
  direction for iOS/Android screens and flows (writes no code). The detailed English
  prompt set lives under references.
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

> **Execution**: generate images with an **available image tool** (OpenAI Images / fal / an internal tool). This skill provides the **prompts / visual direction for mobile UI**. If no tool is available, deliver **prompts only**.

## Context budget (exception)

This skill is an **exception to the normal skill budget (2–4KB)**. Read only this `SKILL.md` at the entry. Open the detailed prompts and checklist in `references/mobile-image-direction.md` **only when needed** (~40KB, English).

## Steps

1. Confirm the product brief (number of screens, platform, brand tone).
2. Check whether an image tool is available. If not, assemble prompts from the reference below and **deliver text**.
3. Keep multiple screens on **one visual system** (color, type, radius, spacing).
4. Make the app UI itself the subject; if useful, show it in a restrained device frame.
5. Web LPs, desktop, and implementation code are out of scope for this skill.

## Gates

- Do not imitate real trademarks, people, or copyrighted works without permission (confirm the requester's rights).
- Do not include personal data or secrets in prompts.
- The scope of use of the output (commercial, training, etc.) is decided by the **requester / legal**. This skill makes no legal judgment.

## References (progressive disclosure)

- Full prompt guide (English): [`references/mobile-image-direction.md`](references/mobile-image-direction.md)
- License: `LICENSE` in the same directory
