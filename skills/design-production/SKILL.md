---
name: design-production
description: Optional visual UI and prototype production workflow for a Product Blueprint whose planning package and design brief are already approved. Compares visual directions, earns user approval on one representative screen, then expands to the full design system, screens, states, and clickable prototype.
---

# Design Production

Run this workflow only when the user explicitly asks to continue from planning into visual UI, screens, or a prototype.

## Preconditions

1. The project is Standard or Deep and `python3 scripts/validate_service_blueprint.py <planning-dir> --stage planning` returns `planning-structure-pass`.
2. `03-design-brief.md` is current.
3. The user explicitly chooses to enter this separate visual exploration and approval loop. Append the decision log and record the same reference with `scripts/workflow_state.py confirm <planning-dir> --gate design-entry ...`.

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

Write both `03.4-visual-directions.md` and `03.4-visual-directions.json`, bind current evidence and source hashes, record the matching `visual-direction` workflow gate, and run:

```bash
python3 scripts/validate_service_blueprint.py <planning-dir> --stage visual-direction
```

Do not continue unless it returns `visual-direction-pass`.

### 3. Produce one representative screen

Use `product-blueprint:key-screen-exploration` to apply the chosen direction to one high-value screen with its critical states and at least one narrow and one wide viewport. Use suitable frontend-design and image-generation capabilities where available.

Return the current evidence to the user and iterate under that owning skill until the user explicitly approves the quality ceiling. Record `03.8-key-screen-review.{md,json}` and the matching `key-screen` workflow gate, then run:

```bash
python3 scripts/validate_service_blueprint.py <planning-dir> --stage key-screen
```

Do not use the generic final `design-critique` artifact here and do not expand the system unless this returns `key-screen-pass`.

### 4. Expand the system

Only after that approval:

- use `product-blueprint:design-system`
- use `product-blueprint:ux-writing`
- use `product-blueprint:design-system-workbench` for the remaining P0 screens and states
- optionally use `product-blueprint:high-fidelity-screen` for one additional risk-heavy screen that needs a pixel-level pass
- use `product-blueprint:art-production` when product-specific imagery is necessary
- run the all-P0 `product-blueprint:visual-quality-gate` after current rendered evidence exists

Every component and screen must inherit the approved direction rather than restarting from generic defaults.

### 5. Build and test the prototype

Use `product-blueprint:clickable-demo`, then `product-blueprint:prototype-test`. Verify happy paths, non-happy states, responsive behavior, keyboard/focus behavior, and transitions against the service manifest.

Run `--stage prototype` and fix structural or runtime evidence failures before acceptance work.

### 6. Critique, revise, and request acceptance

Run the final `product-blueprint:design-critique` and `product-blueprint:feasibility-review`. Resolve critical and major findings. Use `product-blueprint:design-acceptance` only after the user has reviewed current visual evidence, then validate `--stage design`. A `design-pass` means the current design baseline is accepted; it does not mean the handoff exists or technical design may start.

The workflow may then use `product-blueprint:engineering-handoff` and validate the later stage:

```bash
python3 scripts/validate_service_blueprint.py <planning-dir> --stage handoff
```

This proves an accepted product/design handoff, not technical or implementation readiness.

## Change control

- Visual choices may change visual hierarchy and expression, but may not silently change personas, journeys, screen purposes, required states, operations, or first-version scope.
- When design exposes a product-contract problem, edit the upstream planning artifact, rerun the planning review and validator, and obtain any affected user decision again.
- Invalidate the earliest affected workflow gate with `workflow_state.py invalidate`; do not refresh hashes around a changed decision.
- User acceptance is required; agent critique cannot substitute for it.
- Expand from one approved screen, not from a full unreviewed batch.
