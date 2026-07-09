# Token Substrate — shadcn/Radix + OKLCH

The workbench and hi-fi screens must be built on a real component substrate, not raw hand-rolled `<div>`s. Building from scratch collapses to the training average (generic cards, generic spacing). This reference defines the substrate and — critically — **how to avoid the shadcn-default sameness** (see anti-slop-doctrine §3).

## Why a substrate

- Radix primitives give correct behavior for free: focus management, keyboard nav, ARIA roles, portal/overlay/dismiss logic, controlled/uncontrolled state. Hand-rolled components get this wrong and read as amateur.
- shadcn gives component *structure* (composition, slots, variants API via `cva`) that is clean and inspectable.
- Starting from tasteful, correct primitives removes ~half of slop before any styling.

## The non-negotiable: strip the defaults

shadcn ships a recognizable skin (New York / zinc / neutral, Geist, `rounded-md`, muted-foreground). Shipping it untouched is slop v2. The substrate is skeleton only; the skin comes from the measured spec.

Do all of the following before the substrate is "yours":

1. **Replace the token layer.** Overwrite the CSS variables (`--background`, `--foreground`, `--primary`, `--muted`, `--border`, `--radius`, …) with the OKLCH values from the measured design spec. The default gray ramp and default `--radius` are banned starting values.
2. **Replace the font.** Never leave Geist/Inter default. Set the display/body/data families from the type spec, with the right feature settings (`font-variant-numeric: tabular-nums` for data, KR line-height for Korean body).
3. **Re-derive radius, border, elevation, density** from the spec — a radius *scale* by role, hairline borders preferred over shadows, real spacing scale. Do not accept `rounded-md` on everything.
4. **Add the signature element** as a real component/utility so it recurs across surfaces.
5. **Override component variants.** The default `Button`, `Card`, `Badge` looks must be re-skinned to the art direction. If `Badge` is still a gray stadium pill, you have S4.

Self-test: open the rendered screen next to a vanilla shadcn starter. If a designer can't tell which is which within the neutral chrome, the skin was not replaced.

## OKLCH token model

Use OKLCH for the palette — perceptually uniform lightness makes contrast and hover/pressed states predictable and consistent across hues.

Layer the tokens (primitive → semantic → component), the same discipline the measured spec requires:

```css
:root {
  /* primitive — raw ramps, not used directly in components */
  --paper-50:  oklch(0.98 0.008 60);
  --paper-100: oklch(0.96 0.010 60);
  --ink-900:   oklch(0.22 0.012 60);
  --ink-600:   oklch(0.46 0.012 60);
  --accent-500: oklch(0.55 0.14 20);   /* product-derived, not tech-blue */

  /* semantic — what components reference */
  --surface: var(--paper-50);
  --surface-raised: #fff;
  --ink: var(--ink-900);
  --ink-muted: var(--ink-600);
  --accent: var(--accent-500);
  --accent-ink: oklch(0.98 0.01 20);
  --border-hairline: oklch(0.22 0.012 60 / 0.10);
  --radius-md: 8px;

  /* component — optional, for one-off precise mappings */
  --card-radius: var(--radius-md);
  --card-border: 1px solid var(--border-hairline);
}
```

Then map shadcn's expected variables (`--background`, `--foreground`, `--primary`, `--border`, `--ring`, `--radius`, …) onto the semantic layer so every shadcn component inherits the product skin automatically.

Export stable values to:
- `tokens/<product>.tokens.json` — design-tokens JSON (primitive/semantic/component).
- `tokens/<product>.variables.css` — the `:root` block above.
- `tokens/<product>.theme.css` — the shadcn-variable mapping + dark mode if in scope.

## Contrast obligation

Because OKLCH lightness is explicit, verify text pairs numerically: `ink on surface ≥ 7:1`, `ink-muted on surface ≥ 4.5:1`, `accent-ink on accent ≥ 4.5:1`, semantic-on-surface per the spec. Record each pair as `X on Y = N:1` in the workbench so the gate can check it. Do not guess contrast from OKLCH lightness alone — compute the WCAG ratio.

## Planning-artifact form

This is a **planning specimen**, not the production app. Acceptable forms:
- A single self-contained HTML file that inlines the tokens as CSS variables and hand-writes the (already-skinned) component markup with Tailwind utilities — fast to render and screenshot, no build. Good for hero-screen craft and the workbench.
- A standalone React/Vite artifact using real shadcn components when the coupling to a real stack is wanted.

Either way: keep it under `docs/product-planning/<project>/prototypes/`, mark it non-production, render it in a browser, and screenshot desktop + mobile at real viewport sizes (see craft-loop.md).

## What NOT to decide here

Tokens and components are visual planning. Do not decide app routing, data fetching, query/cache state, API, or DB. Component and token *names* should be good enough to become real design-system candidates later, but implementation is a post-handoff step.
