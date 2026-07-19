---
name: engineering-handoff
description: Creates the final product/design handoff packet from an accepted whole-service design without deciding API, DB, frontend architecture, or backend architecture. Use after design acceptance when the team needs one continuous record of user intent, flows, states, feasibility constraints, evidence, and accepted limitations.
---

# Product Blueprint Product/Design Handoff

Use this as the final default phase of Product Blueprint. The filename remains `05-engineering-handoff.md` for compatibility, but its product meaning is an accepted product/design contract. It is not technical architecture and does not claim implementation readiness.

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
- Current `05-design-acceptance.json` with a passing design-stage report

## Handoff Contents

1. Product thesis and MVP loop.
2. User journeys and screen map.
3. Product non-negotiables that must survive implementation.
4. Mechanism contracts requiring engineering design, such as memory, judging, ranking, scoring, recommendations, paid actions, moderation, and creator validation.
5. Backend/system responsibilities and high-risk invariants.
6. Approved compromises and staged versions from feasibility review.
7. Scope-out candidates and user-facing consequences.
8. **Entity & State Contract (required — this preserves the accepted user model)**:
   - **Entities**: every product object the screens and mechanisms imply (descriptive: name, key fields in product language, relationships/cardinality — e.g. "a mission scopes to a category and connects many-to-many with characters"). This is a domain model, NOT a storage schema — no tables, columns, or types.
   - **Per-screen state machines**: take each screen contract's state list and write the transitions (state → event → state), including error/retry and recovery paths.
   - **Invariants as testable assertions**: rewrite forbidden shortcuts and mechanism promises as assertions a developer can enforce structurally and test (e.g. "unverified accounts' list responses contain zero age-gated items — server-side, not a client filter", "paid tool execution and ledger deduction are one atomic operation").
   A handoff without this section loses the behavior the user approved. Prose questions belong in section 9, not here.
9. Open questions for engineering, product, design, legal/safety, and data/AI.
10. Evidence links: screenshots, storyboard frames, and mechanism examples.
11. High-fidelity visual evidence: reusable React source manifest, ComponentBoard/DepthBoard/FlowPreview refs, token/component/state coverage, release-viewport screenshots, optional HTML behavior-demo link, and optional ceiling-screen pass.
12. Risk register status: P0 risks and their mitigations (from `04.55-risk-register.md` when it exists); handoff is not ready with unmitigated P0 risks.
13. Design-handoff completeness checklist.
14. **Journey continuity matrix**: journey-by-journey table with journey IDs, entry points, surfaces, actions, states, operations, recovery, and accepted feasibility constraints. This proves that the approved flow does not break between screens; it is not an implementation sequence.
15. **Readiness status block**: frontmatter starts as `planning-readiness: pending`; final pass/fail is owned by `design-readiness`, not this document.

## Rules

- Do not write database schema, API routes, service architecture, queues, model choices, or storage strategy. The Entity & State Contract stays descriptive (behavior and relationships), never prescriptive (storage and endpoints).
- Do translate product/design intent into engineering review questions.
- Do include backend/system risks that would break user trust if mishandled.
- Preserve user experience requirements even when they are difficult.
- Product-visible feasibility questions must be resolved before design approval. Pure architecture questions may be labeled `outside Product Blueprint; decide during technical design` and cannot change the accepted UX silently.
- Do not draft a ready handoff before `design-pass`. Missing/stale approval is a blocker, not a conditional visual note.
- Do not write `planning-readiness: pass`, “implementation ready,” or equivalent from prose review. Create the handoff draft, then call `product-blueprint:design-readiness` at handoff stage.
- Use exact service-manifest IDs in journeys, state machines, invariants, and the continuity matrix. A handoff row without IDs cannot be traced back to the prototype.

## Output

Create `05-engineering-handoff.md` as a draft with `planning-readiness: pending`, then run `product-blueprint:design-readiness` at handoff stage. A pass means `design_handoff_ready=true` and `ready_for_technical_design=true`; technical and implementation readiness remain outside this harness.

## Next Step

- 사용자가 결정할 것: validator pass 이후 핸드오프 승인, 그리고 남은 open question 각각의 오너/시점 지정.
- Stop here by default. This is the end of Product Blueprint's pre-development workflow.
- If visual quality is still the main risk, return to `product-blueprint:design-system-workbench`, regenerate evidence, and request user reapproval.
- Use `product-blueprint:tech-plan` only when the user explicitly asks to proceed into implementation architecture.
