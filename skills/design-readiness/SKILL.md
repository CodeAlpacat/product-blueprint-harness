---
name: design-readiness
description: Deterministically validates a continuous Product Blueprint from confirmed user requirements through wired prototype behavior, developer-lens feasibility consultation, absorbed design constraints, explicit user approval, and product/design handoff. Use at contract, prototype, design, or handoff boundaries; never use it to claim technical or implementation readiness.
---

# Product Blueprint Design Readiness

Use the validator instead of asking the producing agent whether its own work is complete. Read `references/service-contract.md` and `references/design-acceptance.md` for the owning contracts.

## Stages

| Stage | Checks | Positive dimension |
|---|---|---|
| `contract` | confirmed personas, requirements, entry points, and service-graph coverage | `product_contract_ready` |
| `prototype` | contract plus DOM wiring and current browser transition/effect/state proof | `prototype_ready` |
| `design` | prototype plus complete P0 surface×viewport×state evidence, component contracts, mental-model review, developer-lens feasibility coverage, absorbed constraints, and explicit current user approval | `design_accepted` |
| `handoff` | accepted design plus a product/design handoff that preserves behavior, state, constraints, and open limitations without choosing implementation architecture | `design_handoff_ready`, `ready_for_technical_design` |

Lite never sets these dimensions true.

## Run

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage contract --no-write
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage prototype --no-write
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage design --no-write
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage handoff
```

Handoff writes `05-readiness-report.{json,md}`.

## Feasibility boundary

The developer lens answers product/design questions only:

- can the promised behavior exist on the intended platform;
- which latency, failure, persistence, permission, cost, safety, or accessibility constraints must the user experience expose;
- which option is impossible or materially misleading.

It does not choose endpoints, tables, component architecture, state libraries, migrations, or rollout plans. `infeasible` blocks acceptance. `feasible-with-constraint` routes back to design, requires regenerated subject-matched evidence, and requires explicit user reapproval bound to every current check ID and the canonical feasibility SHA-256.

## Failure routing

- requirement/persona/entry point → `product-definition` or `prd`
- surface/action/state → `screen-contract`
- operation/journey → `service-contract` or `backend-systems-brief`
- DOM/runtime → `clickable-demo`
- task/target-user status → `prototype-test`
- feasibility coverage/blocker → `feasibility-review`
- absorbed constraint/evidence/reapproval → `design-acceptance` and the named visual owner
- handoff → `engineering-handoff`
- dashboard claim → `decision-dashboard`

Never edit a report or stale hash to create a pass. Fix the earliest owning artifact, regenerate invalidated evidence, request user approval again, and rerun the same stage.

## Honest interpretation

- `design_owner_approved` means explicit owner/founder approval of the current evidence.
- `user_validated` means real target-user evidence only.
- `ready_for_technical_design` means a later engineer may begin technical design from a complete, accepted product/design contract.
- `technical_design_ready`, `implementation_ready`, and `engineering_ready` remain false compatibility fields because this harness does not own those claims.

## Next step

Stop at `handoff-pass` by default. Use `tech-plan` only when the user separately asks to begin technical architecture.
