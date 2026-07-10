---
name: high-fidelity-screen
description: Creates one production-grade React screen specimen from an approved storyboard, art direction, and design-system brief. Use after design-system when the team needs a Figma-like high-fidelity screen that can later inform real frontend implementation without turning the whole planning board into app code.
---

# Product Blueprint High-Fidelity Screen

Use this after `product-blueprint:design-system-workbench` when one decisive screen needs an additional pixel-level pass. This skill creates a single high-fidelity React screen specimen, not the full product, not frontend architecture, and not a rough HTML storyboard.

If the user expects tokens, component catalog, states, and multiple production screen mockups, use `product-blueprint:design-system-workbench` first. A single screen specimen is not enough for design-system handoff.

Read first: `${CLAUDE_PLUGIN_ROOT}/references/anti-slop-doctrine.md`, `${CLAUDE_PLUGIN_ROOT}/references/craft-loop.md`, `${CLAUDE_PLUGIN_ROOT}/references/token-substrate.md`.

## Run The Layered Craft Loop — Not One Shot

The first render is the training-average draft, not the deliverable. Craft this screen in discrete passes, re-screenshotting after each (full detail in `craft-loop.md`):

1. Structure (hierarchy, focal point) → 2. Layout & grid → 3. Typography (measured ramp) → 4. Color & material (OKLCH tokens, hairlines over shadows) → 5. Imagery (art-directed treatment, no placeholder wells) → 6. Density & polish → 7. Distinctiveness push (strengthen the signature; break the template read).

Build on the token substrate (shadcn/Radix structure, default skin stripped, product tokens applied). When Claude Code design skills are available, delegate the pixel craft to them and keep product logic here:

- If the environment provides them: `impeccable`/`craft` for shape→build, `layout`, `typeset`, `colorize`, `distill`, `polish` for passes 2–6, `bolder` for pass 7, `critique`/`audit` for review. If it provides none, apply the passes by hand — the doctrine is self-sufficient.

Render full-size at real viewport (mobile 390×844, desktop 1440), screenshot at 2x, then run the adversarial visual gate (`${CLAUDE_PLUGIN_ROOT}/references/adversarial-visual-gate.md`). Loop until it passes — conditional is not pass. This screen becomes the anchor the workbench and other screens are gated against.

## When To Use HTML vs React

- Use HTML for `03-storyboard.html`: fast Figma-like boards, IA, screen coverage, flow wiring, evidence strips, and review annotations.
- Use React + Tailwind for high-fidelity screen specimens when the target product stack supports it: production-grade visual hierarchy, tokens, component anatomy, responsive behavior, states, and a path toward real frontend implementation.
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

- Create one isolated, **self-contained** planning specimen under the product-planning folder by default. It must not be presented as production implementation. Greenfield is the default assumption: there is usually no host repo yet.
- Default to a standalone single-file artifact (self-contained HTML that inlines the OKLCH tokens per `${CLAUDE_PLUGIN_ROOT}/references/token-substrate.md`, or a standalone React + Tailwind file) in `docs/product-planning/<project>/prototypes/`. It must run locally and be screenshot-tested with no build step and no host dependencies.
- Only if a host repo/app already exists AND the user wants coupling: you *may* reuse its Tailwind tokens, `cn` helper, shared UI primitives, and icon system, or add a preview route — clearly marked non-production. Never assume any of these exist.
- Use real component names and token names that can become design-system candidates, but do not decide app routing, API, DB, query state, or backend behavior.
- Build on the shadcn/Radix structure with the default skin stripped and the product OKLCH tokens applied (per `token-substrate.md`). Keep product-specific colors in the specimen's own token layer; never ship a default component-library skin.
- Include at least these states when relevant: default, loading/skeleton, empty, error/retry, locked/unsafe, paid confirmation, success, correction.
- Use product-specific imagery. Do not leave character or media slots as blank gradients.
- Keep planning notes outside the product surface. The UI specimen must only show plausible user-facing UI.
- Produce desktop and mobile screenshots before calling it reviewed.
- Run a visual quality pass against AI-slop signals: generic gradients, glass cards, identical card grids, weak typography, one-note palette, fake stock imagery, unreadable text, overflow, and card nesting.

## Deliverables

Create or update:

- `04.35-high-fidelity-screen.md`: screen choice, design rationale, component anatomy, states, unresolved decisions, and review checklist.
- `prototypes/<product>-<screen>-react.html` or an isolated local React/Vite-style prototype under the planning folder.
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
