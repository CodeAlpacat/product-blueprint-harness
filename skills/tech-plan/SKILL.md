---
name: tech-plan
description: Optional post-handoff technical planning that converts an accepted product/design handoff into frontend, backend, API, DB, state, and verification plans. Use only when the user separately asks to leave product/design definition and begin implementation architecture; it is not part of design acceptance or Product Blueprint readiness.
---

# Product Blueprint Tech Plan

This optional skill begins a new technical-design workflow after Product Blueprint has already stopped. It does not strengthen, complete, or retroactively validate the product design.

## Boundary

1. Read the accepted product/design handoff without reinterpreting product intent.
2. Treat all feasibility constraints already absorbed into the design as non-negotiable inputs.
3. If technical investigation reveals a new product-visible constraint, stop technical planning and return it to the Product Blueprint loop:
   `feasibility consultation → design revision → regenerated evidence → explicit user reapproval`.
4. Do not mark the Product Blueprint report implementation-ready. The target project's own spec, architecture review, and verification workflow owns that claim.

## Optional workflow

1. Inspect the actual target repository or explicitly choose a greenfield stack.
2. Preserve service-manifest IDs while mapping routes, components, APIs, persistence, state ownership, and tests.
3. Define domain entities in product language first.
4. Record architecture options and unresolved decisions.
5. Plan vertical implementation slices, invariants, rollout, rollback, and verification.

## Output

Create `06-technical-plan.md` only when the user explicitly requested technical architecture. This file is downstream context, not a Product Blueprint acceptance artifact or validator stage.

## Next step

Move into the target project's normal plan/spec, design review, implementation, code review, and E2E verification workflow.
