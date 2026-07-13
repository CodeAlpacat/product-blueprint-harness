---
name: clickable-demo
description: Build a single-file clickable HTML prototype containing every P0 screen with real transitions, plus a Figma-like board mode showing all screens at once and a rendered non-happy-states sample. Use after the design system and screen mockups exist, when the user wants a clickable demo, a prototype to walk through, or a final screen collection to review.
---

# Clickable Demo — the final review artifact

One self-contained HTML file = the product, walkable. This is usually the single most valuable artifact a founder reviews: they click through the real flow instead of imagining it from documents. It doubles as the screen-collection ("Figma board") deliverable.

## Inputs (hard prerequisites)

- `02.5-screen-contracts.md` — the P0 screen list and the entry/exit map (transitions MUST match it)
- `02.6-service-manifest.json` — authoritative surface/action/state/operation/journey IDs; the contract-stage validator MUST pass
- `tokens/` + `DESIGN.md`/`04.3-design-system.md` — all styling from tokens; no new colors/type
- The passing ceiling screen (from the workbench/hi-fi pass) — its markup patterns propagate

## Output

`prototypes/<product>-demo.html` + a short `04.36-clickable-demo.md` (what's wired, what's mocked, known gaps). No build step, no framework, no external requests — pure HTML/CSS/JS that opens from disk.

## Required structure

1. **Phone frame demo mode**: one `.screen` section per P0 screen, absolutely stacked in a fixed-size frame; only the active screen visible; internal scroll per screen. Every root has a unique `id` and `data-surface="<manifest-id>"`.
2. **Contracted controls**: every product button/link has a unique `id` and `data-action="<manifest-action-id>"`. Navigation/open actions also carry `data-go="<target-surface-id>"`; same-surface effects carry `data-effect="<manifest-effect-id>"`. Overlay surfaces keep the screen beneath visible. Review-only controls carry `data-demo-control`.
3. **Board mode**: a toggle that lays ALL screens out in a grid at readable scale with title labels — the Figma-like all-screens view. Same file, no duplication.
4. **Jump bar** (outside the frame): one button per screen for direct access during review. Mark demo controls visually as "not the product".
5. **States sample screen**: one extra screen rendering the non-happy states as visual contracts — empty results, first-user empty (mascot moment if the brand has one), loading skeleton (same shape as the real screen), error/retry, image-load fallback, and any domain-specific empty. Every required manifest state points to a real unique element ID here or in its surface, with a stable board/hash/jump reproduction path.
6. **Responsive grammar screens (mandatory for responsive-web products)**: at least discovery, detail, and the core-action screen rendered at desktop width inside the same file — as the MOBILE EXPERIENCE EXTENDED: one app max-width cap (visible margin outside the cap), one breakpoint, bottom nav promoted to a sidebar, the content column keeping the mobile layout (no desktop-only grids/splits). A persistent side panel is allowed only as the opened form of an existing mobile sheet (same content and order — single SoT). State the derivation rule for undrawn screens.
7. **Real copy, real names**: use the locked brand name, voice rules, and evocative content from the planning artifacts. Lorem or "Item 1" fails the gate.
8. **Coherent story**: pick ONE concrete content storyline (one character/product/scenario) and thread it through all screens — detail → gate → core action → status must be the same story, not disconnected samples.

## Verification (mandatory, not optional)

- **Transition-map check**: script-drive the demo (or click through in a browser tool) and assert every entry/exit edge in the screen contract is reachable and lands on the right screen. Record the pass as a list of `from → to ⇒ landed`. A wired demo with unverified transitions is not done.
- **Runtime report**: browser-drive every manifest transition, same-surface effect, and required state reproduction. Write `04.37-runtime-verification.json` with `runner: browser`, current manifest/demo SHA-256 values, and pass/fail rows keyed by action/state ID. A hand-written claim without current hashes is stale evidence.
- **Deterministic contract check**: run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage prototype --no-write`. Fix every missing DOM ID, uncontracted control, mismatched `data-go`/`data-effect`, unreachable P0 surface, and unreproducible state.
- **Render check**: open in a real browser, screenshot demo mode (2–3 key screens) AND board mode (full page). Fix visual defects before declaring done.
- **Gate**: run `product-blueprint:visual-quality-gate` over the board-mode screenshot — this is where all-P0 coverage is easiest to scan at once.

## Forbidden

- A demo that invents screens or transitions not in the contract (or silently drops contracted ones) — contract wins; propose changes explicitly.
- Product buttons/links without `data-action`, duplicate DOM IDs, `href="#"` dead controls, and review controls not marked `data-demo-control`.
- External CDNs/fonts/images that break file:// opening.
- "It should work" — every claim about the demo is backed by a screenshot or a transition-check list.

## Next Step

- 다음 추천: `product-blueprint:prototype-test` (이 데모로 실제 태스크 워크스루) → `product-blueprint:design-critique`.
- 사용자가 결정할 것: 데모가 보여준 흐름/카피 승인, 화면 추가·수정 요청.
