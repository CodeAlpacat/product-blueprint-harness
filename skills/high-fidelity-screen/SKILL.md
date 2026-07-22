---
name: high-fidelity-screen
description: Creates one production-grade React screen specimen from an approved storyboard, art direction, and design-system brief. Use after design-system when the team needs a Figma-like high-fidelity screen that can later inform real frontend implementation without turning the whole planning board into app code.
---

# Product Blueprint High-Fidelity React Screen

Use this after `product-blueprint:design-system-workbench` when one screen needs an additional pixel-level pass. This is not the initial representative-screen gate: `product-blueprint:key-screen-exploration` owns that earlier approval. This skill must inherit the approved key-screen direction and cannot replace or overwrite its review artifact.

If the user expects tokens, component catalog, states, and multiple production screen mockups, use `product-blueprint:design-system-workbench` first. A single screen specimen is not enough for design-system handoff.

Read first: `${CLAUDE_PLUGIN_ROOT}/references/anti-slop-doctrine.md`, `${CLAUDE_PLUGIN_ROOT}/references/craft-loop.md`, `${CLAUDE_PLUGIN_ROOT}/references/token-substrate.md`.

## Run The Layered Craft Loop — Not One Shot

The first render is the training-average draft, not the deliverable. Craft this screen in discrete passes, re-screenshotting after each (full detail in `craft-loop.md`):

1. Structure (hierarchy, focal point) → 2. Layout & grid → 3. Typography (measured ramp) → 4. Color & material (OKLCH tokens, hairlines over shadows) → 5. Imagery (art-directed treatment, no placeholder wells) → 6. Density & polish → 7. Distinctiveness push (strengthen the signature; break the template read).

Build on the shared React/CSS token substrate. When the user explicitly approves delegation and Claude Code design skills are available, delegate the pixel craft to them and keep product logic here:

- If the environment provides them: `impeccable`/`craft` for shape→build, `layout`, `typeset`, `colorize`, `distill`, `polish` for passes 2–6, `bolder` for pass 7, `critique`/`audit` for review. If it provides none, apply the passes by hand — the doctrine is self-sufficient.

Render full-size at real viewport (mobile 390×844, desktop 1440), screenshot at 2x, then run the adversarial visual gate (`${CLAUDE_PLUGIN_ROOT}/references/adversarial-visual-gate.md`). Loop until it passes — conditional is not pass. Compare it against the already approved key-screen quality ceiling and shared workbench rather than establishing a new direction.

## Rendering medium

- Use HTML for `03-storyboard.html`: fast Figma-like boards, IA, screen coverage, flow wiring, evidence strips, and review annotations.
- Use the intended React UI stack for high-fidelity specimens. Existing products reuse their actual tokens/components; greenfield products reuse the dependency-light React workbench.
- Do not rebuild the whole storyboard in React by default. Pick one decisive screen first.
- Do not let an HTML storyboard become the final visual quality ceiling. It is a planning contract, not production UI.

## Output Language And Stage Exit

- Default to the user's conversation language.
- If the user is Korean, write review prompts, labels outside the UI specimen, and final guidance in Korean.
- End with:
  1. `지금 확인할 산출물`
  2. `사용자가 결정할 것`
  3. `수정이 필요하면 어디를 바꿀지`
  4. `다음 추천 스킬`

## Required Inputs

- `02.5-screen-contracts.md`
- `02.6-service-manifest.json` surface/action/state IDs for the chosen specimen
- `03-storyboard.html`
- `03.5-art-direction-brief.md`
- `04.1-visual-quality-gate.md`
- `04.3-design-system.md`
- `04.32-design-system-workbench.md` or a clear reason the workbench is intentionally skipped
- Decision log with unresolved scope/design questions
- One selected screen and why it is decisive

## Screen Selection

Pick the screen that carries the highest product/design risk. Common choices:

- Character-chat product: `character detail -> persona gate -> chat entry`, because this prevents generic chatbot flow and validates the conversion gate.
- Discovery product: home or search results, because visual density, ranking, and content scanning determine activation.
- Trust-heavy product: memory/review/correction surface, because failure and recovery states determine confidence.

If the user has not chosen a screen, select the decisive one and record the assumption.

## React Specimen Rules

- Build the specimen inside the implementation-fidelity React workbench. Do not create a second component tree for a prettier isolated screen.
- Existing products must reuse their actual tokens, helpers, shared primitives, icon system, and preview environment. Greenfield products must reuse the portable React workbench sources.
- A standalone single-file HTML specimen cannot be the high-fidelity deliverable. HTML remains valid only for storyboard or behavior review.
- Use real component names and token names that can become design-system candidates, but do not decide app routing, API, DB, query state, or backend behavior.
- Follow `token-substrate.md`: semantic React components, local CSS tokens, shared source between boards and screens, and no new dependency solely for the specimen.
- Include at least these states when relevant: default, loading/skeleton, empty, error/retry, locked/unsafe, paid confirmation, success, correction.
- Use product-specific imagery. Do not leave character or media slots as blank gradients.
- Keep planning notes outside the product surface. The UI specimen must only show plausible user-facing UI.
- Produce desktop and mobile screenshots before calling it reviewed.
- Run a visual quality pass against AI-slop signals: generic gradients, glass cards, identical card grids, weak typography, one-note palette, fake stock imagery, unreadable text, overflow, and card nesting.

## Deliverables

Create or update:

- `04.35-high-fidelity-screen.md`: screen choice, design rationale, component anatomy, states, unresolved decisions, and review checklist.
- the selected screen entry inside the actual-stack React workbench.
- `screenshots/<product>-high-fidelity-<screen>-desktop.png`
- `screenshots/<product>-high-fidelity-<screen>-mobile.png`

## Pass / Fail

Pass only if:

- The specimen follows the approved screen contract.
- The screen preserves the core flow and forbidden shortcuts.
- The design feels product-specific rather than a generic AI chat/SaaS mockup.
- Tokens and components visibly map to the design-system brief.
- It has at least one non-happy state.
- It was rendered in browser and screenshot-checked on desktop and mobile.

Fail if:

- It changes product flow for aesthetics.
- It adds unapproved navigation or promotes a background mechanism into a main surface.
- It uses HTML storyboard styling as the final visual language.
- It claims production readiness without browser screenshots.
- It depends on unresolved API/DB decisions.

## Next Step

- If the specimen fails, revise `product-blueprint:art-direction-brief`, `product-blueprint:design-system`, or the selected screen contract.
- If it passes with ACCEPT-FLAG rows recorded, use `product-blueprint:prototype-test` for task-based review or `product-blueprint:design-critique` for visual/product critique.
- Use `product-blueprint:tech-plan` only after engineering handoff and explicit user approval.
