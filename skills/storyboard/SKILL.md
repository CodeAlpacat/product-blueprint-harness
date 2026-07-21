---
name: storyboard
description: Creates low-fidelity HTML storyboards and screen-flow boards from PRDs, mechanism contracts, and research evidence, wiring user flows, states, transitions, and review notes. Use near the end of planning before creating the design brief; it does not establish final visual design.
---

# Product Blueprint Storyboard

Create a planning board, not a fake finished app and not the default clickable demo.

The default storyboard artifact is a low-fidelity HTML board that lays out screens side by side. Use it to inspect information architecture, screen coverage, transitions, and product assumptions at a glance. Do not turn it into a visual styling exercise. Clickable demos and React screen production belong to the separate `product-blueprint:design-production` workflow.

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
- `02.6-service-manifest.json` with a passing contract-stage report
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

- Stable surface ID from the service manifest. Transition arrows carry stable action IDs.

- Entry source: where the user came from.
- User decision: what the user decides on this screen.
- Primary action: exactly where the happy path exits.
- Secondary exits: back, cancel, view detail, settings, support, or recovery.
- State represented: default, empty, returning, locked, paid, error, loading, or success.
- Evidence status: observed, user-confirmed, proposed, assumed, or unverified.

If any P0 surface from the service manifest has no frame or approved background-only treatment, the storyboard fails. The storyboard may not invent a surface/action/state outside the manifest; update the contract first.

## Visual Rules

- Use neutral wireframes and clear annotations. Do not imply that layout, color, typography, imagery, component styling, or density is approved.
- Use screenshots only in a separate evidence strip and never crop critical content. Do not blend reference screenshots into proposed product frames.
- Represent media slots with labeled neutral placeholders. Do not generate decorative product imagery during the default planning workflow.
- Separate `Observed`, `Assumption`, and `Improvement`.
- For reference-based flows, include screenshots for lower-scroll/detail-tab/side-panel evidence, not only first viewport screenshots.
- Include baseline category surfaces such as search for discovery products unless the PRD explicitly scoped them out.
- Use user-facing words inside product frames. Do not put internal planning terms such as "relationship grammar" into search placeholders, buttons, tabs, or card copy; use concrete labels and examples users recognize.
- For discovery-first products, keep home focused on discovery unless the screen contract approved a returning-user module. Show ongoing conversations in a conversations/library surface or secondary entry, not as the default home hero.
- Keep text readable. If a screenshot is too small, link to the original image.
- Optimize the board for behavior review, not visual satisfaction. Consistency and traceability matter more than polish here.
- Do not hide long-term memory, mission judging, ranking, recommendations, or paid actions behind vague labels. Show the user-facing state and failure recovery where the user actually needs to inspect, correct, confirm, or recover them.
- Do not make a product mechanism visually dominant just because it is important internally. Preserve the surface level approved in the screen contract.
- For character-chat products, storyboard persona/setup as an entry gate after character detail and before chat room. Do not render it as a home feature, bottom-nav item, or primary navigation destination unless the screen contract explicitly approved that.
- Do not storyboard P1/P2 differentiators as P0 frames. Put them in a deferred-features row or completeness matrix.
- For every priority frame, show entry source, user decision, and next destination as storyboard annotations outside the mocked product screen. Do not put planning labels, wiring notes, PRD explanations, or reviewer guidance inside the app UI frame.
- Inside the mocked product screen, show only what the real user would plausibly see: navigation, content, controls, system states, empty/error/recovery copy, and product-specific visual assets.

## Output

Create `03-storyboard.html` plus `screenshots/<storyboard-proof>.png` after browser verification.

## Next Step

- Use `product-blueprint:backend-systems-brief` when product-visible system constraints need consolidation.
- Then use `product-blueprint:design-brief` and run the planning-stage validator.
- Stop by default. Use `product-blueprint:design-production` only when the user explicitly requests visual UI or a prototype.
