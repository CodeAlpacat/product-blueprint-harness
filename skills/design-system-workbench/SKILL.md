---
name: design-system-workbench
description: Creates an implementation-fidelity React design workbench with brand tokens, reusable components, exhaustive states, Depth-level screens, and complete P0 fixture-data flows. Use after design-system when visual UX must be approved before API/DB wiring or when extending an existing product without redesign drift.
---

# Product Blueprint Design System Workbench

Use this after `product-blueprint:design-system` and before visual acceptance. Read `${CLAUDE_PLUGIN_ROOT}/references/implementation-fidelity-design.md`, `token-substrate.md`, `anti-slop-doctrine.md`, and `craft-loop.md`.

The output is functional-data-free but implementation-faithful React source. A self-contained HTML workbench cannot pass this phase.

## Runtime modes

- **Existing product**: extend its real tokens and shared React components. Render the boards in its preview route or existing Storybook. Do not add Storybook solely for Product Blueprint.
- **Greenfield**: create dependency-light React source using only React, local CSS tokens, local assets, semantic HTML, and local components. Do not require Tailwind, shadcn, Radix, Storybook, or a specific bundler.
- Both use representative fixture UiModels/FormValues. API, DB, auth, query, and mutation wiring are out of scope.

## Inputs

- reference evidence or a user-approved direction interview;
- `02.5-screen-contracts.md` and `02.6-service-manifest.json`;
- `03-storyboard.html`, `03.5-art-direction-brief.md`, `03.7-ux-writing.md`;
- approved `03.8-key-screen-review.json` and its current narrow/wide evidence;
- `04.1-visual-quality-gate.md`, `04.3-design-system.md`, and `DESIGN.md`;
- existing product tokens/components/screenshots when extending a product.

## Required outputs

- `04.32-design-system-workbench.md`;
- stable tokens and reusable React component sources;
- a React `ComponentBoard` rendering component anatomy, variants, and states;
- a React `DepthBoard` separating global shell, Depth 1, Depth 2, and overlays/sheets;
- a React `FlowPreview` wiring every P0 journey with fixture state;
- full-size browser screenshots for every P0 release viewport and required state;
- an all-P0 coverage matrix and implementation-fidelity manifest for design acceptance.

For a greenfield project, use `visual-workbench/`. For an existing app, keep source in its normal token/component/preview locations and record repo-relative refs.

## Workbench contract

1. **Brand thesis**: audience, promise, anti-aesthetic, imagery rules, and one recurring signature device.
2. **Foundations**: primitive/semantic/component tokens for color, type, space, radius, elevation, imagery, and motion; show real usage and measured contrast.
3. **Component board**: stable component ID, purpose, anatomy, variants, states, behavior, a11y, content rules, token refs, and do/don't. Form controls render default/focus/filled/error/disabled/pending/long-content, not a legend.
4. **Pattern library**: product-specific component compositions derived from the PRD and screen contracts.
5. **State lab**: loading, empty, error/retry, locked/safety, permission, success, image failure, paid confirmation when relevant, long content, and recovery.
6. **Depth board**: full-size global shell, 1 Depth, 2 Depth, and overlay/sheet frames. Planning labels stay outside product frames.
7. **P0 screen set**: every P0 surface at every release viewport, using real copy, coherent fixtures, and the same shared React components.
8. **Flow preview**: every entry, exit, back action, exception path, and required state is reachable. Product controls have stable action IDs matching the service manifest.
9. **Responsive grammar**: mobile, tablet, desktop, and relevant landscape are rendered. Do not leave mobile behavior as prose.
10. **Governance**: token/component addition rules, source locations, component-to-screen matrix, state ownership, and change invalidation.

## Craft sequence

Begin from the already approved key-screen ceiling and reuse its measured choices. Run structure → layout → typography → color/material → imagery → density/polish → distinctiveness passes on each expansion while checking for drift. Then propagate the exact tokens/components to all P0 screens; propagation without a rendered screen is not coverage.

## Pass

- ComponentBoard, DepthBoard, and FlowPreview import the same React components and tokens.
- Every P0 surface, viewport, and required state is browser-rendered and screenshot-tested.
- The visual direction is product-specific, accessible, and free of S1–S14 slop signatures.
- Existing projects preserve the real shell, density, interaction grammar, and component conventions.
- The user explicitly approves the current browser evidence.

## Fail

- output is only markdown, storyboard frames, static images, or a standalone HTML workbench;
- boards and screens use copied markup or different component implementations;
- a component library or build dependency is added only to make the planning artifact;
- the design system has tokens but no rendered variants/states;
- only one polished screen exists, obvious P0 surfaces are inferred, or mobile is prose;
- API/DB structure drives the screen before visual approval.

## Next step

Use `product-blueprint:prototype-test` against `FlowPreview`, then `product-blueprint:design-critique` and `product-blueprint:design-acceptance`. Use `high-fidelity-screen` only when the ceiling screen needs another focused pass.
