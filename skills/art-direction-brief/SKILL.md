---
name: art-direction-brief
description: Creates a senior-level art direction brief before high-fidelity UI, connecting audience, product behavior, references, visual world, typography, color, imagery, motion, and anti-aesthetic. Use after screen contracts/storyboard and before visual mockups or design-system work when the user wants production-grade visual design instead of generic AI output.
---

# Product Blueprint Art Direction Brief

Use this before high-fidelity design. Art direction is not decoration; it is the product's visual point of view.

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

## Output

Create `03.5-art-direction-brief.md` with:

- Design thesis
- Product world
- Reference translation
- Palette and typography rationale
- Imagery and motion rules
- Signature element
- Anti-slop checklist
- Open design risks

## Next Step

- Use `product-blueprint:visual-quality-gate` after creating a mockup or storyboard proof.
- Then use `product-blueprint:design-system` to turn the approved visual direction into reusable rules.
