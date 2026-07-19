# Implementation-fidelity design baseline

Product Blueprint ends at an approved, branded user experience that can be implemented without redesigning it. PRD, storyboard, and standalone HTML are upstream contracts, not the final visual baseline.

## Required sequence

1. Collect reference evidence. If the user has no URL or image, run a short taste interview and compare 2–3 distinct directions before high fidelity.
2. Map the global shell, Depth 1, Depth 2, and overlay/sheet surfaces with entry, exit, and back behavior.
3. Lock screen contracts and product-visible feasibility constraints.
4. Use HTML only when a cheap flow prototype helps validate transitions, copy, and states.
5. Define the brand, measured tokens, components, variants, states, motion, and responsive grammar.
6. Render the design from reusable React source with fixture data: a component/state board, full-size Depth screens, and complete P0 flows.
7. Approve browser evidence for every release viewport and required state.
8. Only then begin technical design and attach API, DB, auth, permissions, and mutations.

## Two execution modes

### Existing product

- Extend the product's real token and shared-component sources.
- Render the component/state board and Depth previews inside the real app or its existing Storybook when available.
- Use the same React components that will ship. Do not copy markup into a separate planning UI.
- Use fixture UiModels/FormValues; do not wire production data during visual approval.

### Greenfield product

- Create a portable dependency-light React source package in the intended UI stack selected at the feasibility checkpoint.
- Include CSS tokens, reusable components, `ComponentBoard`, `DepthBoard`, and `FlowPreview` entry components.
- Do not require Storybook, Tailwind, shadcn, Radix, or another UI package. If the host later provides them, adapt the same React sources rather than maintaining a second tree.
- Treat this package as the executable design baseline for later app scaffolding; it still contains no API/DB architecture.

## Source-of-truth split

| Concern | Source of truth |
| --- | --- |
| Scope, IA, flow, states, copy | product definition, screen/service contracts, optional behavior prototype |
| Brand, visual design, responsive behavior | accepted React tokens/components/boards/previews and browser evidence |
| Functional integration | the later production app and scenario evidence |

A standalone HTML demo may remain as a portable walkthrough, but it never proves component reuse, final responsive behavior, or production visual fidelity.
