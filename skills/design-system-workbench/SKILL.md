---
name: design-system-workbench
description: Creates a React/Tailwind design-system workbench that visualizes tokens, components, states, and production screen mockups like Storybook or a Figma component board. Use after design-system when the user needs portable production-grade design artifacts before frontend/backend implementation.
---

# Product Blueprint Design System Workbench

Use this after `product-blueprint:design-system` and before accepting the visual design baseline. This skill turns the design-system brief into a rendered artifact that a founder, designer, and feasibility reviewer can inspect.

This is not the production app. It is a portable design artifact for product planning, design review, and later frontend handoff.

**Medium**: React + Tailwind when the environment has node tooling. In a planning-only greenfield folder (no build step available or wanted), a **self-contained no-build HTML workbench** using the same tokens is an equal-class artifact — it opens from disk, renders anywhere, and pairs naturally with the clickable demo. The substrate rules below apply identically either way (tokens, no starter look, full sections).

Read first: `${CLAUDE_PLUGIN_ROOT}/references/anti-slop-doctrine.md`, `${CLAUDE_PLUGIN_ROOT}/references/token-substrate.md`, and `${CLAUDE_PLUGIN_ROOT}/references/craft-loop.md`.

## Build On A Real Substrate — Never Raw Divs, Never Default shadcn

Two failure modes, both slop:

1. **Hand-rolled from raw Tailwind `<div>`s** → collapses to the training average (generic cards, generic spacing, S1–S14). Build components on a real substrate (shadcn/ui structure + Radix behavior) so correctness and accessibility come for free.
2. **shadcn on its defaults** (New York / zinc / Geist / `rounded-md`) → instantly recognizable "starter template" = slop v2. The substrate is skeleton only. **Strip the default skin entirely** and re-skin from the Measured Spec: overwrite the token layer with the OKLCH values, replace the font, re-derive radius/border/elevation/density, override component variants, and add the signature element. Follow `token-substrate.md` step by step.

Gate before propagating: open the workbench next to a vanilla shadcn starter — if a designer cannot tell them apart within the neutral chrome, the skin was not replaced (fail).

## Establish The Ceiling On One Screen First

Do not render all P0 screens at once at average quality. Per `craft-loop.md`: craft the single most decisive screen to the bar, pass the adversarial visual gate, then propagate the passing token/component system to the remaining P0 surfaces. Render screens full-size at real viewport (mobile 390×844, desktop 1440), one per view — never tiled into tiny phone frames, which destroys fidelity and hides slop.

## Hard Lesson

Do not call a low-fidelity storyboard decomposition a design system. A workbench made by cutting a wireframe into named cards is a failure.

A production-grade design-system workbench must look and behave closer to Storybook/Figma component documentation plus high-fidelity product examples:

- foundations and brand rules
- primitive, semantic, and component tokens
- component anatomy, variants, states, behavior, accessibility, usage, do/don't
- product patterns that combine components
- high-fidelity screen examples that meet or exceed the current POC/storyboard visual quality bar
- handoff assets that can later inform real frontend implementation

## Inputs

- `03-storyboard.html`
- `03.5-art-direction-brief.md`
- `04.1-visual-quality-gate.md`
- `04.3-design-system.md`
- Design-system research notes when quality has been challenged
- Screen contracts and PRD scope
- `02.6-service-manifest.json` (authoritative P0 surface/state/action set)
- Any reference design-system examples, token files, or style exports supplied by the user

## Output Language And Stage Exit

- Default to the user's conversation language.
- If the user is Korean, write artifact notes, review prompts, and final guidance in Korean.
- End with:
  1. `지금 확인할 산출물`
  2. `사용자가 결정할 것`
  3. `수정이 필요하면 어디를 바꿀지`
  4. `다음 추천 스킬`

## Required Artifact Shape

Create a rendered workbench, usually:

- `04.32-design-system-workbench.md`
- `prototypes/<product>-design-system-workbench.html`
- `screenshots/<product>-design-system-workbench-desktop.png`
- `screenshots/<product>-design-system-workbench-mobile.png` when the workbench itself is responsive

If the user supplied token references, also create or map:

- `tokens/<product>.tokens.json`
- `tokens/<product>.variables.css`
- `tokens/<product>.theme.css`

Do not create these token files if the values are still speculative and the user asked only for a visual board. In that case, keep them in the workbench and mark them as candidate tokens.

## Workbench Sections

The React workbench must include these sections:

1. **Design Thesis**: product promise, anti-aesthetic, and one signature visual device.
2. **Foundation Tokens**: color, typography, spacing, radius, elevation, motion. Separate primitive, semantic, and component tokens. Show real usage, not just swatches.
3. **Component Documentation**: for each priority component show purpose, anatomy, variants, states, behavior, accessibility, content rules, do/don't, and token mapping.
4. **Pattern Library**: the product's real cross-component patterns, derived from *its* PRD and screen contracts. (Example set for a character-chat product: discovery grid, ranking list, detail reading flow, persona setup, chat thread, tool panel, memory correction, checkpoint copy, locked/error recovery. Substitute your product's actual patterns — a commerce or data product will have entirely different ones.)
5. **State Lab**: loading, empty, locked/safety, error/retry, paid confirmation, success, correction/recovery, disabled, long-content, image-failure, and permission states.
6. **Production Screen Set**: high-fidelity mockups for all P0 surfaces from the service manifest. For character-chat products this usually means home, search/all characters, ranking, character detail, persona gate, chat, chat side panel/tools, and conversations/library.
7. **All-P0 Coverage Matrix (exit gate)**: a table in `04.32-design-system-workbench.md` — every P0 surface ID from `02.6-service-manifest.json` | rendered artifact (workbench section or demo screen) | required state IDs | visual-gate status. **A row with no rendered artifact fails the phase.** "Propagated from the ceiling" is a technique, not coverage — coverage is a render you can screenshot.
8. **Acceptance-ready component IDs**: give every implementation-bearing component a stable ID and record purpose, variants, states, token refs, accessibility behavior, and evidence location. `design-acceptance` consumes this inventory; unnamed visual fragments are not a handoff contract.
8. **Flow Wiring**: arrows, labels, and review notes outside the product screen frames. Product frames must contain only user-facing UI.
9. **Dark mode & motion**: a dark token pair (OKLCH makes this cheap) with at least one screen rendered dark + contrast re-checked, and a motion spec (durations, easing curve, enter/exit patterns, waiting-state behavior — motion explains, never decorates). Mark dark mode "explicitly deferred" only with a user decision logged.
10. **Governance note**: how tokens/components change after handoff — where the SoT lives (tokens files + DESIGN.md), who approves additions, and the rule that screens never introduce off-token values.
11. **Implementation Handoff Map**: component-to-screen matrix, token-to-component matrix, state ownership, and unresolved product/design decisions.

## Product Rules

- Do not invent new primary navigation just to show components.
- Do not invent surface/action/state IDs. Update the service contract first when the design reveals a real missing surface.
- Do not promote internal mechanisms into main tabs without user approval. (Domain example: for character-chat, persona/setup belongs after character detail and before chat, and memory/checkpoint belong in the chat tool surface, unless the user changed the model. For other domains, apply the neutral rule — an internal mechanism earns a primary surface only when the user's task requires it.)
- Do not use blank image wells for character/product-heavy domains. Use reference screenshots, generated images, or repeated safe assets with different crops.
- Do not let the workbench become a generic SaaS kit. Components must use product-specific content, states, and vocabulary.
- Planning labels, arrows, and critique notes belong outside mocked product screens.
- The workbench must include enough P0 screens that the user can see how the design system behaves across a real service, not one isolated page.
- Do not reduce production screens into tiny unreadable mini-frames if doing so destroys fidelity. Use fewer larger high-fidelity frames or split the workbench into multiple sections.
- If a prior POC/storyboard has a higher visual bar, the workbench screen examples must meet or exceed it.

## Visual Quality Bar

Pass only if:

- Tokens visibly map to components and screens, and text pairs pass their measured contrast (`X on Y = N:1`).
- The component catalog documents anatomy, variants, states, usage, accessibility, and token mapping.
- The screen set preserves the approved product flow and forbidden shortcuts.
- The workbench can be opened locally and screenshot-tested.
- Desktop and mobile frames are readable without cropped core content.
- The ceiling screen passed the adversarial visual gate (`${CLAUDE_PLUGIN_ROOT}/references/adversarial-visual-gate.md`) before propagation.
- It feels like a senior designer's handoff board, not a blurred wireframe or generic template.

Fail if:

- It is hand-rolled from raw divs, or it is recognizable as a default shadcn/starter skin (default skin not stripped).
- Any S1–S14 slop signature is present (per `anti-slop-doctrine.md`).

- It only produces markdown tables.
- It only produces one polished screen while the rest of the product remains abstract.
- It decomposes storyboard/wireframe UI into named boxes and calls that a design system.
- It has tokens but no semantic/component token contract.
- It has component names but no anatomy, variants, states, behavior, accessibility, or usage rules.
- Its production screen examples are lower fidelity than the project's current POC/storyboard reference.
- It uses the storyboard as final UI quality.
- It changes the product IA for visual convenience.
- It leaves the user to request obvious surfaces such as search, ranking, error, locked, or empty states one by one.

## Next Step

- Use `product-blueprint:prototype-test` to test key tasks against the workbench and screen set.
- Use `product-blueprint:design-critique` to critique product intent, visual quality, component reuse, and handoff readiness.
- Use `product-blueprint:high-fidelity-screen` only when one screen from the workbench needs an additional pixel-level pass.
