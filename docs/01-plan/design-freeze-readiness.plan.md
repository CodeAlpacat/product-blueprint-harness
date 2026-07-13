# Design Freeze Readiness — Plan

## 5-Q

- **Why:** prevent implementation from discovering missing screens, misunderstood flows, stale design decisions, or ungrounded technical architecture.
- **What:** add requirement/entry-point traceability, complete visual evidence, explicit design acceptance, scope invalidation, and technical readiness validation.
- **Where:** manifest templates, initializer, validator, orchestrator and downstream skills, fixtures/tests, plugin packaging.
- **WhoFor:** founders approving the product, product/UX designers refining it, and engineers receiving the frozen contract.
- **Flow diff:** documents + declared wiring → user-confirmed product definition → complete clickable/visual design → iterative review → explicit hash-bound design freeze → target-grounded tech spec → technical readiness.

## Scope out

- Building the production app.
- Treating founder approval as target-user research.
- Automatically deciding subjective visual taste.
- Adding an external database or hosted approval service.

## Business impact and success metrics

- **Target:** a founder who wants to finish product/UX/design decisions before frontend/backend implementation.
- **Current problem:** structurally valid planning can still omit an undeclared requirement, carry stale visual approval, or label a pre-technical handoff as engineering-ready. The cost appears later as screen/API/schema rework.
- **Why now:** v0.3 closed declared-flow wiring; the remaining risk is exactly at the design-acceptance and tech-spec boundary the user intends the harness to own.
- **Deterministic success:** all AC1–AC16 scenarios are automated; the valid technical fixture passes and every stale/partial fixture fails with an owning error.
- **Product success:** on the next dogfood run, the founder can review one complete clickable service and an evidence matrix, reject/revise it, explicitly freeze it, and produce a tech plan without finding an unclassified P0 screen during implementation planning.
- **Measurement:** deterministic coverage is measured by tests and stage reports. Subjective mental-model/visual fit is measured by explicit owner approval and separately labeled target-user evidence; no numeric satisfaction claim is manufactured.

## Priority

- **P0:** product-definition traceability; complete P0 visual evidence; explicit design acceptance; source-hash invalidation; honest readiness dimensions; technical traceability and blocker gate.
- **P1:** richer automated visual metrics beyond evidence/hash coverage.
- **P2:** cryptographic or hosted multi-party approval.

## Risks and mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| The same agent fabricates a complete-looking requirement set | P0 | Require user-confirmed source/decision refs, independent requirement→journey→surface set checks, and honest owner-vs-target-user validation labels |
| Visual evidence becomes screenshot bureaucracy | P1 | One evidence row per P0 surface×release viewport; required states may share a surface capture only when element IDs are enumerated |
| Hash binding creates noisy invalidation for harmless prose changes | P1 | Bind only implementation-bearing artifacts and exact evidence files; document the cascade owner for each source |
| Existing v0.3 projects all fail after upgrade | P1 | Emit actionable missing-contract findings and provide templates/migration guidance; never auto-infer approval |
| Technical manifest becomes a second architecture document | P1 | Keep JSON as traceability/readiness contract and Markdown as explanation; no duplicated prose |
| `approved` is written without real user consent | P0 | Skill contract forbids self-approval; require decision-log reference and explicit approval status, while reporting that identity is not cryptographically verified |
| Subjective design quality is overclaimed | P0 | Complete evidence and human acceptance are mandatory; target-user validation remains separate and cannot be inferred |

## Effort estimate

- Validator/contracts/tests: 2–3 engineer-days equivalent.
- Skill/orchestrator/init/docs cascade: 1–2 engineer-days equivalent.
- Review, browser fixture verification, packaging: 1 engineer-day equivalent.
- Blockers: no external service blocker; side-conversation policy prevents independent subagent review, so diff-only fresh review is the documented fallback.

## Active personas and tension log

### Product/UX

- The complete experience must follow user language and be reviewable by walking the service, not by reading disconnected documents.
- A P0 finding about mental model, flow, screen composition, copy, or visual hierarchy cannot be hidden behind an accepted limitation.

### Frontend/design systems

- Every P0 surface needs implementation-useful viewport/state evidence, token/component mapping, and interaction feedback.
- A board screenshot alone is breadth evidence, not per-screen fidelity evidence.

### Backend/technical design

- Product operations and invariants must survive the visual design without choosing schema/API too early.
- Tech planning may begin only from the current accepted baseline and must map every product contract ID.

### Resolution

Keep product definition, service graph, design baseline, and technical mapping as separate contracts linked by stable IDs and hashes. This avoids both data-mirror UI and a monolithic manifest.

## Acceptance criteria

| ID | Input | Expected output | Verification |
|---|---|---|---|
| AC1 | Product definition omits confirmation, P0 acceptance outcome, persona, or entry-point ownership | Contract stage fails with an owning error | Unit fixture mutation |
| AC2 | Included P0 requirement has no surface/action/journey mapping | Contract stage fails | Unit fixture mutation |
| AC3 | Entry point has no matching journey or wrong start surface | Contract stage fails | Unit fixture mutation |
| AC4 | Prototype has valid browser evidence but no design acceptance | Prototype may pass; design/handoff fail | Stage tests |
| AC5 | A P0 surface lacks visual evidence for one release viewport or required state | Design stage fails | Unit fixture mutation |
| AC6 | Visual evidence file hash is stale or visual verdict is not pass | Design stage fails | Unit fixture mutation |
| AC7 | Review ledger contains unresolved P0 mental-model/flow/surface/visual finding | Design stage fails | Unit fixture mutation |
| AC8 | Approval is pending or lacks explicit decision reference | Design stage fails | Unit fixture mutation |
| AC9 | Any bound product/design source changes after approval | Design, handoff, and technical stages fail stale | Hash mutation test |
| AC10 | Handoff passes without a technical plan | Product handoff ready is true; engineering/implementation ready is false | Report assertion |
| AC11 | Technical plan misses a requirement/surface/action/operation/journey mapping | Technical stage fails | Unit fixture mutation |
| AC12 | Technical plan has open blockers, unresolved invariants, or missing rollout/rollback/observability/test seams | Technical stage fails | Unit fixture mutation |
| AC13 | Current accepted design plus complete technical map passes | Technical-design and implementation readiness are true | Valid fixture |
| AC14 | Lite profile | Never design-, product-handoff-, technical-, or implementation-ready | Profile test |
| AC15 | Existing v0.3 dogfood | Fails with actionable migration findings rather than a false pass | Read-only scenario run |
| AC16 | New scaffold | Generates pending canonical contracts and no readiness claim | Initializer test |

## Verification matrix

| ID | Type | Scenario | Expected result | Evidence |
|---|---|---|---|---|
| H1 | Happy | Confirm product model, wire full demo, attach all visual evidence, approve, map tech plan | Technical stage passes; all readiness dimensions are honest | Unit + CLI fixture |
| E1 | Exception | User rejects design in review round | Approval stays pending/rejected and technical stage is blocked | Unit fixture |
| E2 | Exception | PRD/demo/design-system changes after approval | Source-hash mismatch invalidates downstream readiness | Unit fixture |
| E3 | Exception | A requirement exists but the agent forgets its screen or journey | Contract stage reports orphan requirement | Unit fixture |
| B1 | Boundary | P0 state is represented only on a board screenshot | Per-surface viewport/state matrix fails | Unit fixture |
| B2 | Boundary | Founder approves without real-user research | Design may be owner-approved; target-user validated remains false | Report assertion |
| U1 | User complaint | “개발 전에 유저의 멘탈모델에 맞는 디자인 및 유저플로우, 화면 구성을 확정” | A stale, partial, or unapproved design cannot enter tech planning | End-to-end stage chain |

## Planned artifacts

- `assets/templates/product-definition.json`
- `assets/templates/design-acceptance.json`
- `assets/templates/technical-plan.json`
- `skills/product-definition/SKILL.md`
- `skills/design-acceptance/SKILL.md`
- expanded `skills/tech-plan/SKILL.md`
- expanded `skills/implementation-readiness/SKILL.md`
- cascade updates for PRD, screen/service contract, visual workbench/gate/demo/test/critique, dashboard, handoff, feature adoption, and orchestrator
- readiness/visual/service references and README
- validator stages: contract, prototype, design, handoff, technical
- generated report: dimensioned readiness booleans and bound source hashes

## Architecture sketch

| Module | Responsibility | Boundary |
|---|---|---|
| `validate_service_blueprint.py` | Load contracts, validate cross-contract traceability and stage evidence, report readiness | Pure validation over local artifacts; report writing remains separate |
| `init_prd_project.py` | Scaffold pending contracts | No readiness decisions |
| product-definition skill | Elicit and freeze user language/requirements/entry points | No screens/API/schema |
| design-acceptance skill | Iterate review and freeze complete design evidence | No technical architecture |
| tech-plan skill | Map accepted design to implementation architecture | No product-flow reinterpretation |

## Invariants

1. Design approval can be created only after complete current visual and runtime evidence.
2. Source hash drift always invalidates downstream approval/readiness.
3. P0 mental-model/flow/surface/visual findings cannot be accepted away.
4. Founder approval and target-user validation are distinct.
5. Product handoff readiness is not technical or implementation readiness.
6. The service manifest remains the sole surface/action/state/operation/journey graph.

## Work units and commits

1. Plan/design artifacts.
2. Product-definition contract and traceability validator.
3. Design evidence/acceptance/freeze validator.
4. Technical-plan contract and readiness stage.
5. Orchestrator and skill cascade.
6. Initializer, README, packaging, cachebuster.
7. Review fixes and final verification.
