# Token substrate — dependency-light React + CSS

The portable visual baseline uses reusable React components and CSS tokens without requiring a UI library, CSS framework, or Storybook. Existing products reuse their actual substrate; greenfield output must remain easy to transplant.

## Structure before skin

- Use semantic HTML inside named React components. Do not represent every control as a styled `<div>`.
- Keep behavior and skin separate: component props and interaction states define behavior; CSS variables and component classes define appearance.
- Centralize focus, keyboard, dialog, overlay, and dismissal behavior in reusable primitives. Native `<button>`, `<input>`, `<dialog>`, landmark elements, and ARIA are the default dependency-free substrate.
- If an existing product already uses Radix, shadcn, or another primitive library, reuse it. Do not add one only for the Blueprint artifact.
- The component/state board and Depth screens import the same source files. Copied markup is a failed handoff.

## Token layers

Use primitive → semantic → component CSS variables:

```css
:root {
  --paper-50: oklch(0.98 0.008 60);
  --ink-900: oklch(0.22 0.012 60);
  --ink-600: oklch(0.46 0.012 60);
  --accent-500: oklch(0.55 0.14 20);

  --surface: var(--paper-50);
  --ink: var(--ink-900);
  --ink-muted: var(--ink-600);
  --accent: var(--accent-500);
  --accent-ink: oklch(0.98 0.01 20);
  --border-hairline: oklch(0.22 0.012 60 / 0.1);

  --control-radius: 8px;
  --control-height: 40px;
  --motion-fast: 120ms;
}
```

Components reference semantic/component tokens only. Screens must not introduce off-token color, spacing, radius, typography, or motion values.

Export stable values to:

- `tokens/<product>.tokens.json`
- `tokens/<product>.variables.css`
- `tokens/<product>.theme.css` when the target app needs a mapping layer

## Portable React artifact

The greenfield artifact contains source, not a compiled single HTML file:

```text
visual-workbench/
  tokens/
  components/
  fixtures/
  boards/ComponentBoard.tsx
  boards/DepthBoard.tsx
  FlowPreview.tsx
  index.ts
```

Keep imports limited to React, local source, and assets that can be checked into the target project. Do not require Storybook or a specific build tool. When a host app exists, render these entries through its normal preview route or Storybook without forking them.

## Accessibility and contrast obligation

Dependency-free does not mean behavior-free. Render and verify focus order, visible focus, keyboard activation, dialog focus return, labels/descriptions, pending announcements, escape/dismiss behavior, and disabled versus locked semantics.

Compute and record contrast: body text ≥ 4.5:1, large text ≥ 3:1, focus and meaningful non-text UI ≥ 3:1. Do not infer contrast from OKLCH lightness alone.

## Anti-template test

Compare the rendered neutral chrome with common SaaS/shadcn starters. If content could be swapped and the product identity disappears, fail the visual gate. The answer is stronger art direction and token/component decisions, not another dependency.

## Boundary

This React package is the executable visual design baseline, not the production app. It uses fixtures and does not decide routing, requests, cache state, API, DB, auth, or deployment.
