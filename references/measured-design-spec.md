# Measured Design Spec

Art direction fails to transfer taste when it stops at adjectives ("clean", "premium", "editorial"). This reference defines the **numeric contract** that art direction must output and that every rendered screen must obey. The visual quality gate checks screens against these numbers, not against vibes.

Rule: **every aesthetic word must resolve to a number, a hex/OKLCH value, or a named reference decision.** If a spec line has no number and no reference, it is not yet a spec.

Produce this as `03.5-art-direction-brief.md` → section "Measured Spec", and export stable values to `tokens/<product>.tokens.json`.

## 1. Reference extraction (numbers, not principles)

Before inventing anything, ingest 3–5 real reference screenshots (competitors + one out-of-category exemplar) and extract **measured** decisions, labeled `관찰`:

- Grid: column count, gutter px, page margin px, max content width.
- Type: body size px, line-height, the ratio between heading steps, families used.
- Spacing: the smallest repeating unit (4pt? 8pt?), card padding.
- Color: count of distinct hues, is there a gradient, border vs shadow for separation, hairline width.
- Density: items per viewport, image-to-text ratio, card vs list.

Example (good): `관찰 — Zeta 홈: 4pt grid, body 15px/1.5, no card shadow, 1px hairline dividers, 2-col character grid, image:text ≈ 60:40.`
Example (bad, banned): `관찰 — Zeta는 모던하고 깔끔함.`

Then decide, per extracted decision, `차용`(borrow the principle) or `거부`(refuse to copy) — never copy the literal skin.

## 2. Color spec (OKLCH, with roles and contrast)

Define the palette in OKLCH (perceptually uniform → predictable lightness/contrast). See `token-substrate.md` for how these become CSS variables on the shadcn substrate.

Required roles, each with a value and a contrast obligation:

- `surface` / `surface-raised` / `surface-sunken` — the neutral base. Derived from the product world, not `zinc`.
- `ink` / `ink-muted` / `ink-subtle` — text ramp. `ink` on `surface` must be ≥ 7:1 (AAA body target); `ink-muted` ≥ 4.5:1.
- `accent` + `accent-ink` (text on accent) — one brand accent. Must pass 4.5:1 for any text placed on it.
- `border-hairline` — the separation line width+color (e.g. 1px, ink at 8–12% alpha).
- Semantic: `success`, `warn`, `danger`, `locked`, `paid` — reserved for state only, each ≥ 3:1 against surface for non-text, 4.5:1 for text.

Constraints:
- Total distinct hues in the base UI (excluding imagery): ≤ 3 + semantic set. More = S14 slop.
- No two-stop tech gradient as brand (S8). A gradient is allowed only if it is a named art-direction device with a product reason, applied to one element.
- State each pair as `X on Y = N:1` so the gate can verify.

## 3. Typography spec (a real ramp)

Pick families with intent (and Korean readability if applicable — line-height ~1.6–1.75 for Korean body). Never ship the framework default font untouched (S10).

Define a named ramp — for each step: `size px / line-height / weight / letter-spacing / role`:

| Step | Size | Line-height | Weight | Tracking | Role |
|---|---|---|---|---|---|
| display | e.g. 34 | 1.1 | 700 | -0.02em | marketing / hero only, not app chrome |
| title | 22 | 1.25 | 600 | -0.01em | screen + section titles |
| body | 15–16 | 1.55 (Latin) / 1.7 (KR) | 400 | 0 | reading |
| label | 13 | 1.3 | 500 | 0 | UI labels, buttons |
| meta | 12 | 1.35 | 500 | 0.01em | timestamps, counts, captions |
| data | tabular-nums | — | 500 | 0 | numbers, ledgers, ranks |

Constraints:
- Ratio between adjacent heading steps ~1.2–1.35 and *consistent* (the gate checks scale consistency).
- ≥ 3 genuinely distinct roles visible on a screen (not just 2 sizes of one weight).
- Large sizes get negative tracking; small caps/meta get slight positive tracking.

## 4. Spacing, grid, radius, elevation, motion (all numeric)

- **Spacing scale** on a 4px base: `4, 8, 12, 16, 24, 32, 48, 64`. Every gap/padding must be on the scale (the gate checks off-grid values).
- **Grid**: mobile columns + gutter + margin; desktop columns + gutter + max-width. State them.
- **Radius scale by role**: e.g. `sm 4 / md 8 / lg 12 / full`. Assign each component a step. Not one radius everywhere (S3).
- **Elevation**: define 0–2 real steps (border-only, low shadow, overlay). Prefer hairline borders over shadows for separation. No glow (S1).
- **Motion**: durations (e.g. 120/200/320ms) + easing tokens + what each explains (enter, state-change, overlay). Motion must explain, not decorate.

## 5. Imagery spec (critical for image-heavy products)

For character-chat / media products the imagery is the product. Under-specifying it guarantees S7 slop. Define:

- Aspect ratios per placement (card thumb, hero, list row, avatar).
- Crop rule (focal point, safe area for overlays).
- Treatment: overlay gradient stops, duotone/grain, border/frame — the device that makes generated art read as *one intentional art direction* rather than mixed stock.
- Source policy: generated vs licensed; consistency rules so 20 characters look like one editorial world.
- Fallback: image-load-failure and no-image states designed (not a gray box).

## 6. Signature element (one, product-derived)

Exactly one recurring visual device that comes from the product concept and appears across surfaces (see anti-slop-doctrine §3.3). Specify what it is, where it appears, and its measured form (line weight, placement). One only — multiple signatures cancel out.

## 7. Output shape

The measured spec must be:
- **Renderable** — a developer/agent can build a pixel-accurate screen from it with no further taste calls.
- **Checkable** — the gate can verify each screen against the numbers.
- **Exported** — stable values go to `tokens/<product>.tokens.json` + `.variables.css` for the substrate.

If any screen the workbench renders violates a spec number, the screen is wrong (not the spec) unless the spec is deliberately revised and re-exported.
