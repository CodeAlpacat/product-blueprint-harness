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
- `02.6-service-manifest.json`
- Latest prototype-stage validator result and prototype-test evidence

## Handoff Contents

1. Product thesis and MVP loop.
2. User journeys and screen map.
3. Product non-negotiables that must survive implementation.
4. Mechanism contracts requiring engineering design, such as memory, judging, ranking, scoring, recommendations, paid actions, moderation, and creator validation.
5. Backend/system responsibilities and high-risk invariants.
6. Approved compromises and staged versions from feasibility review.
7. Scope-out candidates and user-facing consequences.
8. **Entity & State Contract (required — this is what lets a developer start architecting)**:
   - **Entities**: every product object the screens and mechanisms imply (descriptive: name, key fields in product language, relationships/cardinality — e.g. "a mission scopes to a category and connects many-to-many with characters"). This is a domain model, NOT a storage schema — no tables, columns, or types.
   - **Per-screen state machines**: take each screen contract's state list and write the transitions (state → event → state), including error/retry and recovery paths.
   - **Invariants as testable assertions**: rewrite forbidden shortcuts and mechanism promises as assertions a developer can enforce structurally and test (e.g. "unverified accounts' list responses contain zero age-gated items — server-side, not a client filter", "paid tool execution and ledger deduction are one atomic operation").
   A handoff without this section hands over questions, not contracts — developers cannot begin. Prose questions belong in section 9, not here.
9. Open questions for engineering, product, design, legal/safety, and data/AI.
10. Evidence links: screenshots, storyboard frames, and mechanism examples.
11. High-fidelity visual evidence: design-system workbench screenshots, clickable-demo link, token/component/state coverage, and optional single-screen pixel pass when the product requires production-grade UI confidence before technical design.
12. Risk register status: P0 risks and their mitigations (from `04.55-risk-register.md` when it exists); handoff is not ready with unmitigated P0 risks.
13. Readiness checklist for starting technical design.
14. **Vertical implementation slices**: journey-by-journey table with journey IDs, surfaces, actions, operations, persistence/invariants, and verification seam. Each slice reaches one user-visible result across UI and backend/data responsibility.
15. **Readiness status block**: frontmatter starts as `planning-readiness: pending`; final pass/fail is owned by `implementation-readiness`, not this document.

## Rules

- Do not write database schema, API routes, service architecture, queues, model choices, or storage strategy. The Entity & State Contract stays descriptive (behavior and relationships), never prescriptive (storage and endpoints).
- Do translate product/design intent into engineering review questions.
- Do include backend/system risks that would break user trust if mishandled.
- Preserve user experience requirements even when they are difficult.
- Mark each unresolved question as `must decide before build`, `can decide during technical design`, or `experiment required`.
- If no React design-system workbench exists and visual quality was a user concern, mark technical design readiness as conditional.
- Do not write `planning-readiness: pass`, “ready for engineering,” or equivalent from prose review. Create the handoff draft, then call `product-blueprint:implementation-readiness` at handoff stage.
- Use exact service-manifest IDs in journeys, state machines, invariants, and vertical slices. A handoff row without IDs cannot be traced back to the prototype.

## Output

Create `05-engineering-handoff.md` as a draft with `planning-readiness: pending`, then run `product-blueprint:implementation-readiness`. The generated `05-readiness-report.{json,md}` is the readiness verdict. Use `product-blueprint:tech-plan` only if the user explicitly asks to proceed from this handoff into technical architecture.

## Next Step

- 사용자가 결정할 것: validator pass 이후 핸드오프 승인, 그리고 남은 open question 각각의 오너/시점 지정.
- Stop here by default. This is the end of Product Blueprint's pre-development workflow.
- If visual quality is still the main risk, use `product-blueprint:design-system-workbench` before `product-blueprint:tech-plan`.
- Use `product-blueprint:tech-plan` only when the user explicitly asks to proceed into implementation architecture.
