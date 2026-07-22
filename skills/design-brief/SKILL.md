---
name: design-brief
description: Consolidates an approved Product Blueprint planning package into a concise visual-design handoff brief. Use after product definition, screen and service contracts, feasibility review, and low-fidelity flows; it deliberately stops before choosing UI styling, tokens, components, or high-fidelity screens.
---

# Design Brief

Create `03-design-brief.md` as the bridge between product planning and optional visual design production.

## Inputs

Read the current:

- `00-decision-log.md`
- `01.8-positioning-brand.md`
- `02-prd.md`
- `02.05-planning-quality-review.md` and `.json`
- `02.1-product-definition.json`
- `02-mechanisms.md`
- `02.5-screen-contracts.md`
- `02.6-service-manifest.json`
- `02.7-feasibility-checkpoint.md`
- `02.8-undefined-surfaces.md`
- `03-storyboard.html`
- `04.2-backend-systems-brief.md` when present
- `04.55-risk-register.md` when present

## Required sections

1. **Product in one minute** — audience, problem, promise, core loop, and first-version boundary.
2. **Brand direction** — positioning, voice, desired feeling, naming status, and explicit “do not become” rules.
3. **Experience priorities** — the moments that must feel clearest, fastest, safest, or most distinctive.
4. **Screen and flow map** — every P0 screen, overlay, entry route, decision point, and destination.
5. **State and recovery requirements** — loading, empty, error, permission, destructive, offline, paid, and success states that apply.
6. **Interaction invariants** — behavior visual design must not change without returning to product planning.
7. **Responsive and accessibility requirements** — required viewports, focus/keyboard behavior, reading order, contrast, motion, and touch constraints.
8. **System-visible constraints** — latency, persistence, permissions, moderation, payment, AI uncertainty, or other behavior that affects the UI.
9. **Reference status** — observed references, user taste signals, useful principles, and prohibited copying. Mark gaps clearly.
10. **Open design questions** — questions visual exploration should answer, separated from unresolved product questions.
11. **Acceptance criteria** — what evidence the user must see before a visual direction may expand beyond one representative screen.

## Boundary

Do not choose fonts, colors, component libraries, final layout, illustration style, or high-fidelity screen treatments here. You may describe desired qualities and constraints, but visual solutions belong to `product-blueprint:design-production`.

## Pass condition

The brief passes when a designer can begin visual exploration without reopening every planning file, can distinguish fixed product behavior from open visual choices, and knows which representative screen should be explored first.

After writing it, run the planning-stage validator; it regenerates the review dashboard from current state and findings. Stop unless the user explicitly requests visual design or a prototype.
