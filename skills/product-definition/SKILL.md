---
name: product-definition
description: >-
  Creates and explicitly confirms the canonical user-language product definition before screen design:
  personas and mental models, included/excluded requirements, entry points, lifecycle contexts,
  acceptance outcomes, and decision evidence. Use after PRD and before screen contracts, after scope
  or user-model changes, or when a service manifest may be internally consistent but incomplete.
---

# Product Definition

Create or update `02.1-product-definition.json` from `assets/templates/product-definition.json`. This is the source set that the service manifest must cover; it is not a screen map or technical model.

## Inputs

- brief, research/reference deconstruction, concept and brand decisions
- PRD, current `02.05-planning-quality-review.json`, and decision log
- the user's own terms for personas, jobs, objects, entry triggers, and expected outcomes

## Workflow

1. Verify the planning review is current and its first-version scope is explicitly user-confirmed. The JSON stores that decision under `mvp_lock`; keep that field name internal. If it is not confirmed, return to `planning-quality-gate`.
2. Write each persona's mental model in user language. Do not use tables, routes, or implementation nouns as the explanation.
3. Give stable IDs to every included or excluded requirement. Classify each as `journey`, `content`, `interaction`, `system`, or `quality`.
4. Record P0/P1/P2, affected persona IDs, source refs, decision ref, and observable acceptance outcomes.
5. Enumerate every entry path: first use, returning, external result/import, edit, post-success redirect, refresh, back, cross-device, and offline when applicable.
6. For exclusions, state what the current-release entry point shows. “Later” without current behavior is not an exclusion.
7. Present the user-language definition and entry-point map to the user. Keep `status: draft` until they explicitly confirm it.
8. Only after explicit confirmation, write `status: user-confirmed` and the decision-log evidence. Record the identical decision reference with `scripts/workflow_state.py confirm <planning-dir> --gate product-definition ...`. The agent must never self-approve this file.
9. Run the contract stage after screen/service contracts exist. Any orphan requirement or entry point returns to this file or its downstream owner.

## Coverage semantics

- Every included P0 requirement must reach a surface and journey.
- `interaction` additionally reaches an action.
- `system` additionally reaches an operation and an inspect/recovery surface.
- Every entry point reaches at least one journey with the same persona.
- Founder confirmation is not target-user research. Preserve the separate real-user validation status.

## Change rule

Changing this file invalidates screen/service contracts, visual acceptance, handoff, and technical planning. Run `scripts/workflow_state.py invalidate <planning-dir> --from-gate product-definition ...`; do not update downstream hashes in place. Regenerate downstream work and request affected approval again.

## Next step

Use `screen-contract`, then `service-contract` and the contract-stage readiness check.
