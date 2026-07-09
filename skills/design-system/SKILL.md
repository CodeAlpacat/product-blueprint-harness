---
name: design-system
description: Turns an approved PRD, storyboard, and visual quality gate into a production design brief, visual direction, design-system candidates, component inventory, and screen design rules. Use after product flow/storyboard approval and visual-quality review when the user wants real product design direction without pretending frontend implementation is complete.
---

# Product Blueprint Design System

Use this after storyboard approval and `product-blueprint:visual-quality-gate`. The design system should serve the product thesis, not decorate the board. This is a production design brief, not frontend implementation.

HTML storyboards are acceptable inputs here because they are flow/IA contracts. Do not treat them as final visual UI. If the user wants production-grade design quality or future frontend portability, the next visual artifact should be a React design-system workbench through `product-blueprint:design-system-workbench`, not a single isolated screen.

## Output Language And Stage Exit

- Default to the user's conversation language.
- If the user is Korean, write the design-system brief in Korean. Keep token names, component names, and product labels in English only when useful.
- End with:
  1. `지금 확인할 산출물`
  2. `사용자가 결정할 것`
  3. `수정이 필요하면 어디를 바꿀지`
  4. `다음 추천 스킬`

## Workflow

1. Define brand position, audience emotion, and anti-aesthetic.
2. Define a named art direction tied to product behavior and references.
3. Create design principles tied to product behavior.
4. Define candidate tokens: color, typography, spacing, radius, elevation, motion.
5. Define component inventory from storyboard screens.
6. Define visible states for mechanism-heavy features: memory summaries, judging progress, evidence ledgers, score/rank, paid action confirmations, uncertainty, and recovery.
7. Create screen-level design rules: hierarchy, density, responsive behavior, empty/error/locked states.
8. Produce a design-system board or document.
9. Identify what still requires a human designer, React design-system workbench, high-fidelity screen specimen, or frontend implementation workflow.

## Rules

- Do not use generic SaaS or AI-gradient styling by default.
- Do not hide unresolved product questions with polish.
- Every component must map back to a storyboard screen or known state.
- Design components should make trust-critical mechanisms legible without pretending the implementation is solved.
- Do not claim final production UI unless the actual rendered artifact passes `visual-quality-gate` and browser screenshot review.
- Do not write frontend architecture, routing, or component implementation here.
- Include accessibility, mobile layout, and text overflow constraints.
- Do not claim that the HTML storyboard is production-grade UI. It remains a planning reference.
- Recommend `product-blueprint:design-system-workbench` when design quality needs to be raised before engineering handoff. Recommend one decisive React screen only after the workbench shows the system across P0 surfaces.

## Portable DESIGN.md (AI-consumable design system — required)

Beyond the analysis brief, emit a single **portable `DESIGN.md`** at the planning-folder root (it moves to the repo root when the project graduates to code). This is the file any AI assistant or developer reads to produce consistent, on-brand UI — the same role as the `design.md` convention (getdesign.md): a self-contained, human- and AI-readable design system spec.

`DESIGN.md` must be concrete enough to build from without further taste calls:

- **One-liner + "works best for / anti"** — the DNA in a sentence and where it applies / must not.
- **Design DNA** — the few rules that, if broken, break the brand.
- **Color** — role table with OKLCH values + measured contrast pairs (`X on Y = N:1`) + do/don't.
- **Typography** — families + the named ramp (size/line-height/weight/tracking/role) + do/don't.
- **Space / radius / elevation / motion** — the numeric scales.
- **Components** — for each: anatomy, variants, states, token mapping, do/don't.
- **Imagery** — aspect/crop/treatment/fallback.
- **Signature element** and **Voice / UX writing**.
- **Anti-slop rules** — the S1–S14 scan items to refuse.

Keep the three layers in sync: `tokens/<product>.*` (machine), `DESIGN.md` (portable AI/human spec), and the rendered visual page from `design-system-workbench` (`prototypes/<product>-design-system.html` — swatches, type specimens, live components, states). `DESIGN.md` is the source a coding agent reads; the rendered page is how a human reviews it; the tokens are what code imports.

## Output

Create `04.3-design-system.md` or `04.3-design-system.html` with tokens, components, examples, and screen application notes — **plus the portable `DESIGN.md`** above.

## Next Step

- Use `product-blueprint:design-system-workbench` when visual quality, design-system portability, or future frontend handoff matters.
- Then use `product-blueprint:prototype-test` with concrete user tasks and mobile screenshots, or `product-blueprint:high-fidelity-screen` for one screen that needs an additional pixel-level pass.
