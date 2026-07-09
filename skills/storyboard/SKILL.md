---
name: storyboard
description: Creates Figma-like HTML storyboards and screen-flow boards from PRDs, mechanism contracts, and research evidence, wiring user flows, states, transitions, and engineering-review notes. Use when the user wants visualized planning artifacts, screen-by-screen flows, product storyboards, or designer-style handoff before high-fidelity design or technical design.
---

# Product Blueprint Storyboard

Create a planning board, not a fake finished app and not the default clickable demo.

The default storyboard artifact is a Figma-like HTML board that lays out screens side by side. Use it to inspect information architecture, screen coverage, transitions, and product assumptions at a glance. Create a clickable demo only later through `product-blueprint:prototype-test` or a separate prototype artifact when the flow is stable enough to validate by interaction. Create React only later through `product-blueprint:design-system-workbench` when tokens, components, states, and production screen mockups need to be visualized.

## Output Language And Stage Exit

- Default to the user's conversation language for board headings, captions, explanatory notes, decision prompts, and final guidance.
- If the user is Korean, write storyboard explanations and review prompts in Korean. Keep product names, deliberate UI labels, and technical component names in English only when useful.
- End with:
  1. `지금 확인할 산출물`
  2. `사용자가 결정할 것`
  3. `수정이 필요하면 어디를 바꿀지`
  4. `다음 추천 스킬`

## Required Inputs

- Research or ideation artifact
- PRD or at least a stable MVP loop
- Experience mechanism contracts for memory, judging, scoring, recommendations, paid actions, or other hidden system behavior
- Screenshot evidence when using references
- List of verified and unverified flows

## Board Structure

1. Cover: product thesis and scope
2. Evidence strip: screenshots shown uncropped with links to originals
3. IA map: navigation, entry points, lifecycle
4. Core loops: user flow lanes
5. Screen frames: each screen with purpose, user decision, states, and transition annotations outside the mocked product UI
6. Mechanism surfaces: where memory/judging/scoring/recommendations affect the flow, and whether they are background, inline, side-panel, modal, settings, or dedicated-screen surfaces
7. Feature storyboards: one board row per major feature
8. Component candidates
9. Engineering review notes: product data/state needed, action implied, trust risks, feasibility questions, and user-facing consequence of compromise
10. Completeness matrix: observed, proposed, unverified

## Frame Contract

Every screen frame must show or annotate outside the product screen:

- Entry source: where the user came from.
- User decision: what the user decides on this screen.
- Primary action: exactly where the happy path exits.
- Secondary exits: back, cancel, view detail, settings, support, or recovery.
- State represented: default, empty, returning, locked, paid, error, loading, or success.
- Evidence status: observed, user-confirmed, proposed, assumed, or unverified.

If any priority screen from the screen contract has no frame, the storyboard fails.

## Visual Rules

- Use screenshots as evidence and never crop critical content. Prefer `object-fit: contain`.
- Use meaningful visual assets inside product frames. For character, media, marketplace, venue, or object-focused products, do not leave hero/card areas as abstract gradients when a reference image or generated bitmap asset would make the flow understandable.
- Do not leave card thumbnails, avatars, hero slots, or media wells visually empty. If only one safe placeholder image exists, reuse it with varied crops or subtle treatments instead of falling back to blank gradients.
- If no safe product asset exists, generate a small set of non-branded placeholder images with `imagegen`, copy them into the project, and reference them from the storyboard.
- Separate `Observed`, `Assumption`, and `Improvement`.
- For reference-based flows, include screenshots for lower-scroll/detail-tab/side-panel evidence, not only first viewport screenshots.
- Include baseline category surfaces such as search for discovery products unless the PRD explicitly scoped them out.
- Use user-facing words inside product frames. Do not put internal planning terms such as "relationship grammar" into search placeholders, buttons, tabs, or card copy; use concrete labels and examples users recognize.
- For discovery-first products, keep home focused on discovery unless the screen contract approved a returning-user module. Show ongoing conversations in a conversations/library surface or secondary entry, not as the default home hero.
- Keep text readable. If a screenshot is too small, link to the original image.
- Do not make a high-fidelity product UI until product flow is understood. HTML storyboard quality should be readable and polished, but it is not the final production design surface.
- Do not hide long-term memory, mission judging, ranking, recommendations, or paid actions behind vague labels. Show the user-facing state and failure recovery where the user actually needs to inspect, correct, confirm, or recover them.
- Do not make a product mechanism visually dominant just because it is important internally. Preserve the surface level approved in the screen contract.
- For character-chat products, storyboard persona/setup as an entry gate after character detail and before chat room. Do not render it as a home feature, bottom-nav item, or primary navigation destination unless the screen contract explicitly approved that.
- Do not storyboard P1/P2 differentiators as P0 frames. Put them in a deferred-features row or completeness matrix.
- For every priority frame, show entry source, user decision, and next destination as storyboard annotations outside the mocked product screen. Do not put planning labels, wiring notes, PRD explanations, or reviewer guidance inside the app UI frame.
- Inside the mocked product screen, show only what the real user would plausibly see: navigation, content, controls, system states, empty/error/recovery copy, and product-specific visual assets.

## Output

Create `03-storyboard.html` plus `screenshots/<storyboard-proof>.png` after browser verification.

## Next Step

- Use `product-blueprint:art-direction-brief` before high-fidelity visual design.
- Then use `product-blueprint:visual-quality-gate` after a rendered mockup, storyboard proof, or visual direction exists.
- After the design-system brief, use `product-blueprint:design-system-workbench` if the team needs production-grade visual direction and future frontend portability.
