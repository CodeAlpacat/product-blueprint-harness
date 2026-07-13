# Design Freeze Readiness — Brief

## User mental model

Product Blueprint is a pre-development product studio. It must let the founder walk the complete service, revise it until the intended users' mental model is represented, and explicitly approve the final flow, screens, states, responsive behavior, copy, and visual system before technical design begins.

The final design is not a suggestion. It is a versioned implementation contract. Any upstream change invalidates downstream approval and technical planning until the affected evidence is regenerated and approved again.

## Current gap

The v0.3 service manifest proves that declared surfaces, actions, states, operations, and journeys agree. It does not prove that:

1. the original user requirements and entry points were all enumerated;
2. every P0 surface was visually reviewed at every release viewport;
3. the founder explicitly accepted the complete design after iterative review;
4. an upstream PRD/design change invalidates an old approval;
5. the technical plan is grounded in the frozen design and covers every product contract ID;
6. `engineering_ready` means a technical design exists rather than only a product handoff.

## Confirmed outcome

- Preserve a user-confirmed product definition before screen design.
- Trace every included P0 requirement and entry point through journeys, surfaces, actions, operations, prototype evidence, design evidence, technical mappings, and tests.
- Require a complete visual evidence matrix for every P0 surface across release viewports and required states.
- Add an iterative design review ledger. Unresolved P0 mental-model, flow, surface, or visual findings block acceptance.
- Create an explicit user-approved design baseline bound to the hashes of every upstream source and visual artifact.
- Invalidate design acceptance and technical readiness when any bound source changes.
- Separate product-contract, prototype, design-acceptance, product-handoff, and technical-design readiness.
- Make technical design consume only the current approved design baseline.

## Evidence

- Current validator checks required artifact existence at `scripts/validate_service_blueprint.py:165`, but does not parse requirement or visual-audit contents.
- Current readiness report sets `engineering_ready=true` after a handoff pass at `scripts/validate_service_blueprint.py:755`, even though `tech-plan` is optional.
- Current `skills/tech-plan/SKILL.md` has traceability guidance but no deterministic technical readiness gate.
- Current browser runtime report correctly proves declared transitions/effects/states; this remains the interaction evidence seam.

## Minimum model

Add only three durable contracts:

1. `02.1-product-definition.json`: user-confirmed personas, mental models, requirements, entry points, and exclusions.
2. `05-design-acceptance.json`: current visual evidence, review ledger, explicit user approval, and source hashes. This is also the scope-freeze baseline.
3. `06-technical-plan.json`: target-grounded implementation mapping and technical decisions bound to the accepted design.

Extend the existing validator with `design` and `technical` stages. Do not create a second screen/action graph; the service manifest remains that graph.

## Scope out

- Authentication of who typed the approval. The harness can require explicit approval evidence but cannot cryptographically prove a conversation participant's identity.
- Claiming target-user validation from heuristic or founder review. Real-user evidence remains a separate status.
- Production application implementation or deployment.
- Pixel-diffing arbitrary screenshots. The gate verifies current, complete evidence and review verdicts; visual taste still requires human acceptance.

