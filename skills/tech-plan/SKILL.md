---
name: tech-plan
description: Optional post-handoff technical planning that converts approved product artifacts and engineering handoff into frontend, backend, API, DB, state, and verification plans. Use only when the user explicitly asks to proceed from Product Blueprint into implementation architecture or feature-by-feature build planning.
---

# Product Blueprint Tech Plan

Use this only after product/design intent, feasibility review, and engineering handoff are stable. This is outside the default pre-development Product Blueprint flow.

## Workflow

1. Read PRD, mechanism contracts, storyboard, design-system, feasibility-review, and engineering-handoff artifacts.
2. Preserve product non-negotiables and approved compromises.
3. Build an action map: screen, user action, precondition, result, data read/write, failure state.
4. Define domain entities in product language first.
5. Draft API contracts and event flows.
6. Draft DB/schema concepts and permissions.
7. Define frontend structure: routes, screens, components, server/client state, forms.
8. Define backend services, jobs, integrations, moderation, billing, and analytics.
9. Create verification plan from user flows and mechanism acceptance examples.

## Rules

- Do not invent entities that have no screen or action.
- Do not reinterpret product intent because the implementation is hard. Refer back to feasibility-review decisions.
- Separate product vocabulary from implementation names.
- Mark high-risk invariants: auth, billing, age gates, deletion, publishing, ranking, scoring.
- Include migration and rollout risks if building in an existing repo.

## Output

Create `06-technical-plan.md` with:

- Screen/action/API matrix
- Entity model
- API list
- DB concept plan
- Frontend plan
- Backend plan
- Verification matrix
- Open technical decisions

## Next Step

- Move into the target project's normal implementation workflow. In this repo, that means project-specific plan/spec, architecture review, implementation, and verification rather than more Product Blueprint planning.
