---
name: engineering-handoff
description: Creates a pre-development engineering handoff packet from approved product planning artifacts without deciding API, DB, frontend architecture, or backend architecture. Use after PRD, mechanisms, storyboard, visual quality gate, backend systems brief, design direction, design-system workbench, and feasibility review when the team needs to brief engineers on product intent, non-negotiables, backend/system invariants, tradeoffs, open questions, and implementation-readiness before technical design.
---

# Product Blueprint Engineering Handoff

Use this as the final default phase of Product Blueprint. It is not the technical architecture. It is the product/design package engineers need before they create architecture, API, DB, and implementation plans.

## Inputs

- Brief
- Reference research or ideation
- Product-experience mechanism contracts
- PRD
- Storyboard
- Design-system direction
- Design-system workbench when visual quality or frontend portability is a known risk
- High-fidelity screen specimen when one screen received an extra pixel-level pass
- Backend systems brief
- Feasibility review

## Handoff Contents

1. Product thesis and MVP loop.
2. User journeys and screen map.
3. Product non-negotiables that must survive implementation.
4. Mechanism contracts requiring engineering design, such as memory, judging, ranking, scoring, recommendations, paid actions, moderation, and creator validation.
5. Backend/system responsibilities and high-risk invariants.
6. Approved compromises and staged versions from feasibility review.
7. Scope-out candidates and user-facing consequences.
8. Open questions for engineering, product, design, legal/safety, and data/AI.
9. Evidence links: screenshots, storyboard frames, and mechanism examples.
10. High-fidelity visual evidence: design-system workbench screenshots, token/component/state coverage, and optional single-screen pixel pass when the product requires production-grade UI confidence before technical design.
11. Readiness checklist for starting technical design.

## Rules

- Do not write database schema, API routes, service architecture, queues, model choices, or storage strategy.
- Do translate product/design intent into engineering review questions.
- Do include backend/system risks that would break user trust if mishandled.
- Preserve user experience requirements even when they are difficult.
- Mark each unresolved question as `must decide before build`, `can decide during technical design`, or `experiment required`.
- If no React design-system workbench exists and visual quality was a user concern, mark technical design readiness as conditional.

## Output

Create `05-engineering-handoff.md`. Use `product-blueprint:tech-plan` only if the user explicitly asks to proceed from this handoff into technical architecture.

## Next Step

- Stop here by default. This is the end of Product Blueprint's pre-development workflow.
- If visual quality is still the main risk, use `product-blueprint:design-system-workbench` before `product-blueprint:tech-plan`.
- Use `product-blueprint:tech-plan` only when the user explicitly asks to proceed into implementation architecture.
