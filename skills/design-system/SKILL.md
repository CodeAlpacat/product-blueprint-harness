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

## Output

Create `04.3-design-system.md` or `04.3-design-system.html` with tokens, components, examples, and screen application notes.

## Next Step

- Use `product-blueprint:design-system-workbench` when visual quality, design-system portability, or future frontend handoff matters.
- Then use `product-blueprint:prototype-test` with concrete user tasks and mobile screenshots, or `product-blueprint:high-fidelity-screen` for one screen that needs an additional pixel-level pass.
