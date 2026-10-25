---
name: web-experience-design
description: Design, implement, audit, and hand off web interfaces with evidence for user tasks, visual hierarchy, responsive behavior, accessibility, and production readiness. Use for pages, components, design-system changes, UI bugs, or web-design reviews; not for generating a visual redesign without inspecting the existing product and requirements.
license: MIT
---

# Web Experience Design

Treat web design as a user-facing engineering change: solve a defined task, preserve the product's visual system, and verify the rendered result.

## Discover before designing

1. Read applicable project instructions, inspect the current UI, and identify existing tokens, components, breakpoints, content constraints, and browser support.
2. Define the primary user, task, success state, content hierarchy, and the screens or states affected. Do not substitute aesthetic preference for a product requirement.
3. Identify functional states before implementation: loading, empty, error, disabled, long text, narrow screens, keyboard focus, and localization expansion where relevant.

## Design and implementation

1. Make the smallest design change that improves the stated task. Reuse existing patterns and tokens unless the task includes a design-system change.
2. Establish hierarchy through layout, spacing, typography, contrast, and progressive disclosure. Do not rely on colour alone to communicate state.
3. Use semantic HTML and accessible labels. Maintain keyboard operation, visible focus, target sizes, readable contrast, and meaningful alternative text.
4. Design responsive behavior intentionally. Verify desktop and mobile layouts rather than merely shrinking a desktop component.
5. Keep content, interaction state, and styling separate enough to make changes testable and maintainable.

## Visual and interaction audit

Inspect the rendered interface using a browser or screenshots whenever available. Check:

- the primary action is discoverable, correctly enabled, and visually prioritized;
- alignment, widths, spacing, overflow, truncation, wrapping, and scroll behavior at representative viewport sizes;
- hover, focus, active, disabled, error, empty, and loading states where applicable;
- keyboard navigation, focus order, screen-reader names, contrast, and reduced-motion behavior;
- translated or long text does not break the layout;
- images, fonts, scripts, and responsive assets do not create avoidable performance or layout-shift regressions.

Do not claim a visual result was verified if a real rendered inspection was unavailable. State the missing environment or viewport explicitly.

## Handoff report

Provide:

- **User outcome and design intent** — what task is improved and why;
- **Implementation** — components, tokens, styles, content, and interaction changes;
- **Verification evidence** — tested viewport sizes, browser or screenshot evidence, automated checks, and accessibility checks;
- **Not verified / known limitations** — unavailable devices, browsers, data states, or design decisions still requiring review;
- **Risk and rollback** — compatibility, analytics, performance, or content risks and the safe reversion path.

For a non-trivial UI change, use `change-readiness` before handoff so visual evidence and unverified states are explicit.

## Approval boundaries

Obtain approval before a brand redesign, external asset purchase, production publishing, analytics change, cookie or tracking change, or replacement of established brand assets.
