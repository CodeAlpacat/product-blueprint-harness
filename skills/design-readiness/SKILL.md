---
name: design-readiness
description: Deterministically validates a Product Blueprint at contract, planning, visual-direction, key-screen, prototype, design, or handoff boundaries. Use planning for the default design-brief finish line and later stages only in optional design production. Never treat structural validation as proof of product quality or implementation readiness.
---

# Product Blueprint Design Readiness

Use the validator instead of asking the producing agent whether its own work is complete. Read `references/service-contract.md` and `references/design-acceptance.md` for the owning contracts.

## Stages

| Stage | Checks | Positive dimension |
|---|---|---|
| `contract` | confirmed personas, requirements, entry points, and service-graph coverage | `product_contract_ready` |
| `planning` | contract plus feasibility notes, coverage audit, low-fidelity flows, systems constraints, and a current design brief | `planning_ready`, while `planning_quality_validated=false` |
| `visual-direction` | two or three comparable directions, current evidence/hashes, and explicit direction approval | `visual_direction_approved` |
| `key-screen` | approved representative surface with critical states and narrow/wide current evidence | `key_screen_approved` |
| `prototype` | contract plus DOM wiring and current browser transition/effect/state proof | `prototype_ready` |
| `design` | prototype plus hashed implementation-fidelity React sources, shared component/depth/flow boards, complete P0 surface×viewport×state evidence, component contracts, mental-model review, feasibility coverage, and explicit approval | `design_accepted` |
| `handoff` | accepted design plus a product/design handoff that preserves behavior, state, constraints, and open limitations without choosing implementation architecture | `design_handoff_ready`, `ready_for_technical_design` |

Lite may set only `planning_ready=true` and returns `lite-planning-pass`; it cannot enter visual or later stages.

## Run

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage contract
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage planning
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage visual-direction
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage key-screen
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage prototype
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage design
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage handoff
```

Every run writes `00-validation-report.{json,md}` and regenerates the review dashboard. Handoff also writes `05-readiness-report.{json,md}`.

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
- visual-direction evidence/approval → `visual-directions`
- representative-screen evidence/approval → `key-screen-exploration`
- handoff → `engineering-handoff`
- dashboard claim → `decision-dashboard`

Never edit a report or stale hash to create a pass. Fix the earliest owning artifact, regenerate invalidated evidence, request user approval again, and rerun the same stage.

## Honest interpretation

- `design_owner_approved` means explicit owner/founder approval of the current evidence.
- `design-pass` means that current product-design evidence is accepted at the design stage; `design_handoff_ready` remains false until a separate handoff-stage pass.
- `user_validated` means real target-user evidence only.
- `ready_for_technical_design` means a later engineer may begin technical design from a complete, accepted product/design contract.
- `technical_design_ready`, `implementation_ready`, and `engineering_ready` remain false compatibility fields because this harness does not own those claims.

## Next step

The default orchestrator stops at `planning-structure-pass` (or `lite-planning-pass`). The optional design-production workflow may continue to `handoff-pass`. Use `tech-plan` only when the user separately asks to begin technical architecture.
