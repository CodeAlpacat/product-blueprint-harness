# Design Freeze Readiness — Plan

## Why / What / Where / WhoFor / Flow Diff

- **Why:** prevent missing screens, broken flows, and late technical constraints from causing redesign during implementation.
- **What:** enforce a complete, feasibility-checked, evidence-backed, explicitly user-approved product/design contract.
- **Where:** Product Blueprint templates, skills, validator, fixtures, initializer, README, and handoff/report semantics.
- **WhoFor:** founders and product/UX designers who want the experience settled before a separate engineering architecture phase.
- **Flow diff:** declared documents → confirmed product definition → wired whole-service prototype → production design evidence → developer-lens feasibility consultation → design revision/evidence regeneration → explicit user reapproval → design handoff.

## Non-negotiable boundary

The validator must never set `engineering_ready`, `technical_design_ready`, or `implementation_ready`. Compatibility fields remain false. `ready_for_technical_design` means only that a later engineer can begin architecture from a stable product/design baseline.

## Acceptance criteria

| ID | Scenario | Expected |
|---|---|---|
| AC1 | Confirmed P0 persona/requirement/entry point lacks service mapping | contract stage fails with an owning traceability error |
| AC2 | Prototype lacks a declared transition/effect/state or browser proof | prototype stage fails |
| AC3 | P0 surface lacks a release viewport or required-state visual | design stage fails |
| AC4 | P0 surface lacks frontend/accessibility consultation | design stage fails `FEASIBILITY_COVERAGE_MISSING` |
| AC5 | Action/operation/journey lacks its required developer lens | design stage fails `FEASIBILITY_COVERAGE_MISSING` |
| AC6 | Any check is `infeasible` | design acceptance is blocked |
| AC7 | Conditional verdict omits concrete constraint, design resolution, or regenerated evidence refs | design acceptance is blocked |
| AC8 | Approval does not reference every current feasibility check or its current content hash | design stage fails `FEASIBILITY_REAPPROVAL_REQUIRED` |
| AC9 | Any bound source/evidence changes after approval | design/handoff fail stale |
| AC10 | Owner approval exists without target-user study | `design_owner_approved=true`, `user_validated=false` |
| AC11 | Complete accepted package passes handoff | `design_handoff_ready=true`, `ready_for_technical_design=true` |
| AC12 | Any handoff pass | technical/implementation/engineering readiness remain false |
| AC13 | CLI design/handoff pass | exits zero and writes only the design-readiness report at handoff |
| AC14 | New standard project is initialized | product-definition and design-acceptance templates exist |

## Scenarios

### Happy

| ID | Scenario | Expected proof |
|---|---|---|
| H1 | Founder walks all P0 flows, developer lenses find only absorbed constraints, founder approves current evidence | design and handoff stages pass; only design-handoff dimensions are true |

### Exception

| ID | Scenario | Expected proof |
|---|---|---|
| E1 | Developer lens marks a promised behavior infeasible | design stage blocks until redesign or explicit scope-out |
| E2 | Conditional constraint exists but the flow/screens do not show its consequence | design stage blocks on missing subject-matched evidence |
| E3 | User rejects the revised whole-service design | status stays pending; no retry cap or self-approval creates a pass |

### Boundary

| ID | Scenario | Expected proof |
|---|---|---|
| B1 | Feasibility content changes while its stable ID stays the same | canonical hash mismatch requires user reapproval |
| B2 | Founder approves without a real target-user study | owner approval and target-user validation remain separate |
| B3 | Handoff passes with no technical plan | ready-for-technical-design is true; all implementation fields remain false |

## Review UX requirements

- The dashboard shows the complete clickable service and the few decisions the founder must inspect, not a document dump.
- Conditional feasibility constraints appear beside the affected surface/action/journey and link to regenerated evidence.
- The final status uses “design accepted / ready to begin technical design,” never “implementation ready.”
- Any changed design or feasibility evidence visibly returns approval to pending.

## Risks and mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| feasibility review drifts into architecture | P0 | allowed subject/lens/verdict schema plus explicit out-of-scope rules |
| same-ID verdict change preserves old approval | P0 | canonical feasibility SHA-256 bound to approval |
| evidence refs are decorative or unrelated | P0 | validate refs against current visual rows and affected subject surfaces |
| compatibility names mislead existing users | P1 | new `design-readiness` canonical skill; old implementation name is a warning-only router |
| deterministic pass is mistaken for user satisfaction | P1 | keep owner approval, heuristic review, and real-user validation separate |

## Success metrics and effort

- Deterministic: all validator/initializer tests pass; valid fixture returns `design-pass` and `handoff-pass`; no technical validator stage exists.
- Qualitative: the next dogfood run reaches explicit design approval without asking the founder to infer missing screens or treating tech architecture as a prerequisite.
- Measurement: failure codes and generated report fields; qualitative result requires actual founder review and is not claimed by tests.
- Estimated effort: validator/tests 1 day; skills/docs/initializer/package cascade 1 day; review/dogfood/release 0.5–1 day. No external blocker.

## Implementation units

1. Preserve product-definition and design-acceptance contracts already added.
2. Remove the technical validator stage and technical-plan acceptance artifacts.
3. Add stable-ID feasibility checks and reapproval binding to design acceptance.
4. Add `design-readiness`; retain `implementation-readiness` only as a compatibility router.
5. Reframe feasibility, orchestrator, dashboard, handoff, README, references, and initializer.
6. Add fixtures/tests for missing coverage, infeasible behavior, unabsorbed constraints, reapproval, honest handoff semantics, and initialization.
7. Package, reinstall, dogfood, then commit/push/PR/release by work unit.

## Residual product judgment

The validator can prove coverage, freshness, and explicit decisions. It cannot prove that a visual style is tasteful or that real target users are satisfied; those remain separately evidenced review dimensions.
