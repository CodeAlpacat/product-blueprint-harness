---
name: design-production
description: Optional visual UI and prototype production workflow for a Product Blueprint whose planning package and design brief are already approved. Compares visual directions, earns user approval on one representative screen, then expands to the full design system, screens, states, and clickable prototype.
---

# Design Production

Run this workflow only when the user explicitly asks to continue from planning into visual UI, screens, or a prototype.

## Preconditions

1. `python3 scripts/validate_service_blueprint.py <planning-dir> --stage planning` passes.
2. `03-design-brief.md` is current.
3. The user understands that this is a separate visual exploration and approval loop.

Add the optional design scaffolds without overwriting planning work:

```bash
python3 scripts/init_prd_project.py "<product name>" --root <planning-root> --with-design
```

If dedicated frontend or visual-design capabilities are unavailable, state the limitation. Do not equate generic generated screens with production-grade design.

## Production sequence

### 1. Establish taste and evidence

Review the design brief with the user. Gather their positive and negative references, aesthetic preferences, brand constraints, and the representative P0 screen that will serve as the quality ceiling.

Use `product-blueprint:visual-directions` to create two or three genuinely different visual directions. Each direction must connect its visual choices to the product’s audience, behavior, and positioning.

### 2. Compare visual directions

Show comparable evidence for all directions at the same fidelity. The user chooses one, requests a revision, or pauses. Do not self-select and propagate a direction as if it were approved.

After the user chooses, use `product-blueprint:art-direction-brief` to codify that direction before producing a representative screen.

### 3. Produce one representative screen

Use the chosen direction on one high-value screen with its critical states and at least one narrow and one wide viewport. Use suitable frontend-design and image-generation capabilities where available.

Run `product-blueprint:visual-quality-gate` and `product-blueprint:design-critique`. Return the evidence to the user. Iterate until the user explicitly approves the visual direction and quality ceiling.

### 4. Expand the system

Only after that approval:

- use `product-blueprint:design-system`
- use `product-blueprint:ux-writing`
- use `product-blueprint:design-system-workbench`
- use `product-blueprint:high-fidelity-screen` for the remaining P0 screens and states
- use `product-blueprint:art-production` when product-specific imagery is necessary

Every component and screen must inherit the approved direction rather than restarting from generic defaults.

### 5. Build and test the prototype

Use `product-blueprint:clickable-demo`, then `product-blueprint:prototype-test`. Verify happy paths, non-happy states, responsive behavior, keyboard/focus behavior, and transitions against the service manifest.

### 6. Critique, revise, and request acceptance

Run `product-blueprint:design-critique` and `product-blueprint:feasibility-review`. Resolve critical and major findings. Use `product-blueprint:design-acceptance` only after the user has reviewed current visual evidence.

The workflow may then use `product-blueprint:engineering-handoff` and validate the later stage:

```bash
python3 scripts/validate_service_blueprint.py <planning-dir> --stage handoff
```

This proves an accepted product/design handoff, not technical or implementation readiness.

## Change control

- Visual choices may change visual hierarchy and expression, but may not silently change personas, journeys, screen purposes, required states, operations, or first-version scope.
- When design exposes a product-contract problem, edit the upstream planning artifact, rerun the planning review and validator, and obtain any affected user decision again.
- User acceptance is required; agent critique cannot substitute for it.
- Expand from one approved screen, not from a full unreviewed batch.
