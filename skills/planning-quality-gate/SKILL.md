---
name: planning-quality-gate
description: Cross-reviews product concept, positioning and brand, experience mechanisms, and PRD through independent product-strategy, user-evidence, brand, requirements, service-feasibility, and growth-risk lenses before the user confirms the first-version scope and product definition.
---

# Planning Quality Gate

Review the planning package before the user confirms the first-version scope. This is a critique and revision gate, not a document-count check or a market-validation claim.

## Inputs

Read these artifacts completely:

- `00-brief.md`
- `00-decision-log.md`
- the active research or ideation artifact
- `01.6-parallel-concepts.md`
- `01.8-positioning-brand.md`
- `02-mechanisms.md`
- `02-prd.md`

Use `assets/templates/planning-review.json` for the machine-readable review. Produce:

- `02.05-planning-quality-review.md` for the founder-facing review
- `02.05-planning-quality-review.json` for the deterministic gate

## Independent Lenses

Run all six lenses. Keep their findings separate before reconciling them.

1. `product-strategy`: target/job clarity, core-loop pull, differentiation, MVP coherence, non-goals.
2. `user-evidence`: observed vs assumed claims, reference limits, user language, unsupported demand claims.
3. `brand`: positioning contrast, naming fit, voice consistency, brand/product fit, availability caveats.
4. `prd`: story completeness, stable IDs, feature evidence, baseline surfaces, boundary states, measurable acceptance.
5. `service-feasibility`: lifecycle continuity, invisible mechanisms, trust/recovery, operational or cost constraints that change the product promise.
6. `growth-risk`: activation, retention, monetization trust, safety/privacy/policy exposure, scope lies.

Use subagents only when the user explicitly approves delegation and the environment supports it. Otherwise run the lenses sequentially with a fresh review pass for each lens. Never let one lens copy another lens's conclusion without checking the source artifacts.

## Finding Contract

Every finding includes:

- stable `id`
- `lens_id`
- severity: `P0` blocker, `P1` must fix before the first-version scope is confirmed, or `P2` follow-up
- status: `open`, `resolved`, or `accepted`
- owner artifact or skill
- concrete problem
- evidence references
- required change

Do not write vague findings such as “needs more detail.” Name the missing decision, broken promise, unsupported assumption, unowned state, or scope conflict and point to its source.

## Review Loop

1. Hash the five required planning sources listed in the JSON template.
2. Run each lens independently and record findings.
3. Reconcile duplicates without erasing disagreements.
4. Fix every P0 and P1 finding in its owning upstream artifact.
5. Re-run affected lenses after edits and refresh source hashes.
6. Present the recommended first-version scope: included work, non-goals, main risk, and the condition under which an alternative wins.
7. Keep `status: draft` and the internal `mvp_lock.status: pending` field until the user explicitly confirms. Do not show “MVP lock” as the user-facing decision label.
8. After explicit confirmation, record `status: user-confirmed`, confirmation evidence, and the decision-log reference.
9. Run `design-readiness --stage contract` only after `product-definition`, screen contracts, and the service manifest exist.

An accepted P0 or P1 is not a pass. If the user knowingly carries one forward, record an `ACCEPT-FLAG` in the decision log and keep this gate blocked. Open P2 findings may remain when they have an owner and next validation point.

## Markdown Output

Write `02.05-planning-quality-review.md` in the user's language with:

- executive verdict
- six lens summaries
- findings table
- changes applied to source artifacts
- recommended first-version scope
- known limits: no target-user validation or trademark clearance claim
- user decision needed
- next step

## Exit

Pass only when:

- all six lenses are present
- no P0 or P1 finding is open or accepted
- the required source hashes match current files
- the user explicitly confirms the first-version scope
- the decision log and review dashboard reflect the same state

Next use `product-blueprint:product-definition`, then `screen-contract` and `service-contract`.
