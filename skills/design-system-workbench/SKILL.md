---
name: design-system-workbench
description: Creates a React/Tailwind design-system workbench that visualizes tokens, components, states, and production screen mockups like Storybook or a Figma component board. Use after design-system when the user needs portable production-grade design artifacts before frontend/backend implementation.
---

# Product Blueprint Design System Workbench

Use this after `product-blueprint:design-system` and before accepting visual design as implementation-ready. This skill turns the design-system brief into a rendered React artifact that a founder, designer, and engineer can inspect.

This is not the production app. It is a portable design artifact for product planning, design review, and later frontend handoff.

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
4. **Pattern Library**: discovery grid, ranking list, detail reading flow, persona setup, chat thread, tool panel, memory correction, checkpoint copy, locked/error recovery.
5. **State Lab**: loading, empty, locked/safety, error/retry, paid confirmation, success, correction/recovery, disabled, long-content, image-failure, and permission states.
6. **Production Screen Set**: high-fidelity mockups for all P0 surfaces from the screen contracts. For character-chat products this usually means home, search/all characters, ranking, character detail, persona gate, chat, chat side panel/tools, and conversations/library.
7. **Flow Wiring**: arrows, labels, and review notes outside the product screen frames. Product frames must contain only user-facing UI.
8. **Implementation Handoff Map**: component-to-screen matrix, token-to-component matrix, state ownership, and unresolved product/design decisions.

## Product Rules

- Do not invent new primary navigation just to show components.
- Do not promote internal mechanisms into main tabs. Persona/setup belongs after character detail and before chat unless the user changed the model. Memory and checkpoint belong in the chat tool surface unless approved otherwise.
- Do not use blank image wells for character/product-heavy domains. Use reference screenshots, generated images, or repeated safe assets with different crops.
- Do not let the workbench become a generic SaaS kit. Components must use product-specific content, states, and vocabulary.
- Planning labels, arrows, and critique notes belong outside mocked product screens.
- The workbench must include enough P0 screens that the user can see how the design system behaves across a real service, not one isolated page.
- Do not reduce production screens into tiny unreadable mini-frames if doing so destroys fidelity. Use fewer larger high-fidelity frames or split the workbench into multiple sections.
- If a prior POC/storyboard has a higher visual bar, the workbench screen examples must meet or exceed it.

## Visual Quality Bar

Pass only if:

- Tokens visibly map to components and screens.
- The component catalog documents anatomy, variants, states, usage, accessibility, and token mapping.
- The screen set preserves the approved product flow and forbidden shortcuts.
- The workbench can be opened locally and screenshot-tested.
- Desktop and mobile frames are readable without cropped core content.
- It feels like a senior designer's handoff board, not a blurred wireframe or generic template.

Fail if:

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
