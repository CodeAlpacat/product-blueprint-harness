# Design Freeze Readiness — Design

## Product model

The harness is a product/design studio. Its output is the current experience the user approved, not a prediction that code will require no change.

```
confirmed intent
  → service graph
  → whole-service prototype
  → production visual/state evidence
  → developer-lens feasibility consultation
  → design correction + regenerated evidence
  → explicit user reapproval
  → product/design handoff
```

A later technical workflow consumes the handoff. If it discovers a new product-visible constraint, it returns that constraint to this loop before implementation changes the experience.

## Sources of truth

- `02.1-product-definition.json`: confirmed personas, mental models, requirements, entry points.
- `02.6-service-manifest.json`: stable surfaces/actions/states/operations/journeys and their continuous wiring.
- `04.37-runtime-verification.json`: current browser proof of declared prototype behavior.
- `05-design-acceptance.json`: current visual/component evidence, mental-model checks, feasibility checks, review history, and explicit approval.
- `05-engineering-handoff.md`: compatibility-named product/design handoff; never technical architecture.
- `05-readiness-report.*`: derived status; never manually promoted.

## Feasibility consultation contract

Each row has:

- stable `id`;
- `subject_kind`: surface/action/operation/journey;
- exact `subject_id`;
- `lens`: frontend/backend/platform/accessibility/security/cost;
- `verdict`: feasible / feasible-with-constraint / infeasible;
- evidence and decision reference;
- for conditional rows: concrete product-visible constraint, design resolution, and regenerated evidence refs.

Required minimum coverage:

| Subject | Required lens |
|---|---|
| every non-background P0 surface | frontend + accessibility |
| every action | frontend |
| action invoking an operation | backend also |
| every operation | backend |
| every journey | platform |

`infeasible` blocks. `feasible-with-constraint` blocks until the design visibly absorbs the constraint. Approval stores the exact set of current feasibility-check IDs and a canonical SHA-256 of their verdicts/resolutions, so changed consultation content requires user reapproval even when IDs stay stable.

The consultation may discuss latency, failure/retry, persistence/lifecycle, permissions, platform capability, accessibility, safety, and material cost. It may not choose endpoints, tables, component boundaries, libraries, migrations, or rollout.

## Stage model

| Stage | Meaning | Positive output |
|---|---|---|
| contract | confirmed intent reaches the service graph | `product_contract_ready` |
| prototype | declared graph works in the browser with required states | `prototype_ready` |
| design | complete visual/state/component/mental-model/feasibility evidence is current and user-approved | `design_accepted` |
| handoff | accepted design is packaged without architecture decisions | `design_handoff_ready`, `ready_for_technical_design` |

Compatibility fields `technical_design_ready`, `implementation_ready`, and `engineering_ready` are always false.

## Invalidation

Any change to product definition, PRD, screen/service graph, storyboard, copy, visual gate, backend systems brief, design system/workbench, demo/runtime proof, prototype test, critique, feasibility review, risk register, or visual evidence invalidates the accepted baseline. Rerun only the affected downstream chain, then obtain explicit user reapproval.

## Failure ownership

- intent/traceability → product-definition / PRD;
- surface/action/state → screen-contract;
- operation/journey → service-contract / backend-systems-brief;
- runtime → clickable-demo / prototype-test;
- feasibility verdict/coverage → feasibility-review;
- constraint absorption/evidence/approval → design-acceptance and the visual owner;
- handoff claim → engineering-handoff / decision-dashboard.

## Optional technical planning

`tech-plan` is not a validator stage and does not strengthen Product Blueprint readiness. It starts only on a separate explicit request. Any newly discovered user-visible constraint returns upstream to feasibility consultation and design reapproval.

## 시나리오 (최종) / Scenarios (final)

### Happy Path

| # | User action | Expected result | Implementation guide |
|---|---|---|---|
| H1 | Founder reviews the complete demo after all consultations and approves | design acceptance binds current sources, visuals, check IDs, and feasibility hash; handoff reports design-ready only | `skills/design-acceptance/SKILL.md`, `scripts/validate_service_blueprint.py` |

### Exception Path

| # | Situation | Expected behavior | Implementation guide |
|---|---|---|---|
| E1 | A behavior is infeasible | fail with `FEASIBILITY_BLOCKER_OPEN`; route to feasibility/design owner | validator feasibility block + `skills/feasibility-review/SKILL.md` |
| E2 | A conditional constraint lacks relevant regenerated evidence | fail with `FEASIBILITY_CONSTRAINT_UNABSORBED` | subject-to-surface evidence validation |
| E3 | Founder has not approved the revised result | fail with design/reapproval findings | acceptance status, source hashes, check IDs, canonical feasibility hash |

### Boundary Cases

| # | Condition | Verification point | Implementation guide |
|---|---|---|---|
| B1 | Same stable feasibility ID, changed verdict/evidence | old approval hash fails | canonical JSON SHA-256 of `feasibility_checks` |
| B2 | Handoff stage passes without any tech plan | design handoff fields true; technical/implementation/engineering false | `_report` stage model |
| B3 | Standard vs Lite initialization | Standard receives pending acceptance; Lite receives only contract artifacts | `scripts/init_prd_project.py` tests |

## Change history from plan

| Plan decision | Design refinement |
|---|---|
| approval references current checks | added content hash so same-ID changes also invalidate approval |
| conditional constraints need evidence | constrained evidence to current visual rows depicting the affected subject |
| preserve compatibility | added canonical `design-readiness`; old implementation name cannot produce a positive claim |
