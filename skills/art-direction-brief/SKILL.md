---
name: art-direction-brief
description: Codifies the user-chosen visual direction into a measured art-direction brief before one representative high-fidelity screen. Use only in the optional design-production workflow, after the design brief and visual-directions comparison.
---

# Product Blueprint Art Direction Brief

Use this before the representative high-fidelity screen. Art direction is not decoration; it is the product's visual point of view. Read `03-design-brief.md`, `03.4-visual-directions.md`, and the decision-log entry that records the user's chosen direction. Do not invent a different direction here.

Read first: `${CLAUDE_PLUGIN_ROOT}/references/anti-slop-doctrine.md` and `${CLAUDE_PLUGIN_ROOT}/references/measured-design-spec.md`. This brief is the input to the token substrate and the craft loop, so it must end in **numbers, not adjectives**.

## Adjectives Do Not Transfer Taste

The words "clean / modern / premium / editorial" produce slop, because the model already believes its average output is those things. Taste transfers through constraints with numbers and through reference decisions. Every tone word in this brief must resolve, in the Measured Spec section, to a type ramp, a spacing scale, an OKLCH color role, a grid, or an explicit `차용/거부` decision against a real reference. A brief with tone words but no measured spec is incomplete.

## Brief Sections

1. **Audience and context**: Who uses it, where, when, and with what emotional state?
2. **Product world**: What material world does the interface belong to: shelf, route map, studio, diary, console, theatre, ledger, etc.?
3. **Design thesis**: One opinionated sentence that can reject weak choices.
4. **Tone words**: 3 concrete words, not generic terms like modern or elegant.
5. **Anti-aesthetic**: What the design must not look like.
6. **Reference translation**: What to borrow as a principle, not as a visual copy.
7. **Signature element**: One memorable motif that comes from the product, not decoration.
8. **Color role**: Surface, text, accent, alert, locked, paid, success, unsafe.
9. **Typography role**: Display, body, utility, data, Korean readability.
10. **Imagery role**: What images must communicate, allowed sources, crop rules.
11. **Motion role**: What motion explains or reinforces.
12. **Accessibility and legibility constraints**.

## Rules

- Do not use purple-blue gradients, generic glass cards, blobs, or fake SaaS dashboards unless the brief explicitly justifies them.
- Do not define tokens without screen usage.
- Do not create multiple signature motifs. Pick one.
- Tie every aesthetic choice to a product behavior or audience need.
- If image generation is used, separate generated art assets from UI structure.

## Measured Spec (required — the contract the render must obey)

Before this brief exits, add a `## Measured Spec` section following `${CLAUDE_PLUGIN_ROOT}/references/measured-design-spec.md`. It must contain:

- **Reference extraction** — 3–5 real reference screenshots deconstructed into *measured* `관찰` decisions (grid px, body size/line-height, spacing unit, hue count, border-vs-shadow), each marked `차용` or `거부`. No adjective-only observations.
- **Color spec** — OKLCH values for `surface / ink / accent / border-hairline / semantic`, each text pair stated as `X on Y = N:1` (compute the contrast).
- **Type spec** — a named ramp table: `size / line-height / weight / tracking / role`, ≥3 distinct roles, consistent step ratio, Korean line-height if applicable.
- **Spacing / grid / radius / elevation / motion** — all numeric (4px scale, columns+gutter+max-width, radius-by-role, ≤2 elevation steps, motion durations+what each explains).
- **Imagery spec** — aspect + crop + treatment (overlay/duotone/grain) + source policy + fallback. Mandatory for image-heavy products.
- **Signature element** — one, product-derived, with its measured form.

Export stable values to `tokens/<product>.tokens.json`. If a spec line has no number and no reference decision, it is not done.

## Output

Create `03.5-art-direction-brief.md` with:

- Design thesis
- Product world
- Reference translation
- **Measured Spec** (numeric — per above)
- Palette and typography rationale
- Imagery and motion rules
- Signature element
- Anti-slop checklist (scan against the S1–S14 signatures in `anti-slop-doctrine.md`)
- Open design risks

## Next Step

- Produce one representative high-fidelity screen and its critical states from this brief.
- Run `product-blueprint:visual-quality-gate` and return the screen to the user for feedback.
- Use `product-blueprint:design-system` only after the representative screen establishes an explicitly approved quality ceiling.
