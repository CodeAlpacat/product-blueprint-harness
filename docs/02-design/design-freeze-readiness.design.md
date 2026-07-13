# Design Freeze Readiness — Design

## 0. Grounding

### User mental model

The harness is a product studio that lets the founder see and walk the whole service, revise it until the intended user's mental model is represented, and explicitly freeze the result before engineering architecture starts.

### Evidence

- v0.3 already has a useful single service graph and browser runtime seam. Preserve both.
- The current artifact validator checks existence but cannot prove source requirements or visual evidence completeness.
- The current report labels a product handoff `engineering_ready` although technical planning is optional.

### Minimum model

Add three contracts around the existing service manifest. Do not copy the service graph into them.

```text
02.1 product definition
  requirements/personas/entry points
             ↓ stable refs
02.6 service manifest
  surfaces/actions/states/operations/journeys
             ↓ hashes + complete visual evidence
05 design acceptance
  review ledger + explicit owner approval + frozen source hashes
             ↓ accepted baseline hash
06 technical plan
  routes/components/API/data/tests/rollout mappings
```

## 1. Product definition contract

File: `02.1-product-definition.json`

### Root

- `schema_version`: `1.0`
- `status`: `draft | user-confirmed`
- `confirmation`: explicit decision-log reference, timestamp, evidence note
- `personas[]`
- `requirements[]`
- `entry_points[]`
- `exclusions[]`

### Persona

- stable `id`
- `label`
- `mental_model` in user language
- `jobs[]`
- `source_refs[]`

### Requirement

- stable `id`
- `statement`
- `kind`: `journey | content | interaction | system | quality`
- `priority`: `P0 | P1 | P2`
- `status`: `included | excluded`
- `persona_ids[]`
- `source_refs[]`
- `decision_ref`
- `acceptance_outcomes[]`
- excluded requirements additionally need `current_entry_behavior`

### Entry point

- stable `id`
- `label`
- `persona_id`
- user-language `trigger`, `context`, `expected_outcome`
- `lifecycle`: one or more of `first-use | returning | external-result | edit | redirect | refresh | back | cross-device | offline`
- `source_refs[]`

### Contract-stage traceability

- `release_profile.roles` must reference persona IDs.
- Every included P0 requirement must map to at least one surface and journey.
- `interaction` requirements additionally need an action.
- `system` requirements additionally need an operation.
- Every entry point needs at least one journey.
- Every journey needs `persona_id`, `requirement_ids[]`, and `entry_point_ids[]` with valid references.
- Surfaces/actions/operations carry `requirement_ids[]`; surfaces also carry `persona_ids[]`.
- Product definition must be `user-confirmed` before contract pass. The skill forbids the agent from self-writing confirmation without an explicit user decision.

## 2. Design acceptance and scope-freeze contract

File: `05-design-acceptance.json`

### Approval

- `status`: `pending | rejected | user-approved`
- `kind`: `explicit-user`
- `decision_ref`, `approved_at`, `scope: all-p0`
- This is owner approval, not target-user research.

### Bound sources

`source_hashes` must include current SHA-256 values for:

- product definition, PRD, screen contracts, service manifest
- storyboard, UX writing
- visual quality gate, design system, workbench
- clickable demo, browser runtime report, prototype test, design critique
- undefined-surface audit, backend systems brief, and feasibility review

Any mismatch yields `DESIGN_BASELINE_STALE` for design/handoff/technical stages. The owning skill reruns only the affected downstream chain, then requests approval again.

### Visual evidence matrix

Each row contains:

- stable evidence `id`
- `surface_id`
- one release `viewport`
- screenshot/visual file and current SHA-256
- `state_ids[]` visible/reproducible in that evidence
- `component_ids[]`
- `visual_gate: pass`
- `review_round_id`

Required coverage:

- every non-background P0 surface × every release viewport has one current passing row;
- every required state for that surface appears in the row for every release viewport, so responsive state treatment cannot be inferred from a different layout;
- every surface row has at least one component ID;
- evidence must be an image-like artifact (`png`, `jpg`, `jpeg`, `webp`, `svg`).

### Component contracts

Each component contract has stable ID, purpose, variants, states, token refs, accessibility behavior, evidence file/hash. Every component used by a P0 visual row must resolve.

### Review loop

- `review_rounds[]`: round ID, status, reviewed evidence IDs, summary.
- `findings[]`: category (`mental-model | flow | surface | responsive | visual | copy | accessibility`), severity, status, evidence, resolution, decision ref.
- Any unresolved P0 finding blocks.
- A P0 mental-model/flow/surface/visual finding cannot use `deferred` or ACCEPT-FLAG to pass.
- At least one completed round must cover all visual evidence IDs.
- User-requested review rounds have no retry cap. Autonomous craft retries may be batched, but a rejected design always returns to the owning artifact and remains pending until the user approves a later current baseline.
- `mental_model_checks[]` must cover every persona and included P0 requirement through explicit journey IDs with a pass verdict.

### Validation distinction

- `owner_approved`: derived from the explicit approval block.
- `target_user_validated`: derived only from product-definition/prototype evidence marked real-user.
- The report displays both; one never implies the other.

## 3. Technical plan contract

Files: `06-technical-plan.md` and `06-technical-plan.json`

### Source binding

The JSON binds the current product-definition, service-manifest, and design-acceptance hashes. Drift blocks technical readiness.

### Target grounding

- `mode`: `greenfield | existing`
- repository/ref/stack
- `grounding[]`: claim + evidence + implication
- Existing target requires at least one repository path/ref claim per frontend/backend/data area used.
- Greenfield requires explicit chosen constraints instead of fake file evidence.

### Complete mappings

- every included P0 requirement → acceptance test IDs
- every P0 surface → route, component, state owner, design component IDs
- every action → handler, feedback owner, operation mapping when applicable
- every operation → service/API/data/auth/idempotency/consistency/failure/observability/rollout/rollback/test IDs
- every journey → vertical slice and end-to-end test IDs

### Technical safety

- resolved invariant rows with enforcement and test
- performance/accessibility/security/cost/observability budgets
- migration/backfill/verification/rollback, with explicit `n/a:<reason>` where irrelevant
- rollout strategy, rollback, and feature-flag decision
- no open blocker
- all referenced tests exist in the technical contract

## 4. Stage model and readiness semantics

| Stage | Requires | Positive readiness dimension |
|---|---|---|
| `contract` | confirmed product definition + traced service graph | `product_contract_ready` |
| `prototype` | contract + browser runtime proof | `prototype_ready` |
| `design` | prototype + complete current design acceptance | `design_accepted` |
| `handoff` | design + engineering handoff artifact | `product_handoff_ready` |
| `technical` | handoff + complete bound technical plan | `technical_design_ready`, `implementation_ready`, compatibility alias `engineering_ready` |

Lite may produce a compact contract but every readiness dimension above remains false.

Report status values: `contract-pass`, `prototype-pass`, `design-pass`, `handoff-pass`, `technical-pass`, `lite-pass`, `fail`.

## 5. Orchestrator flow

1. Brief/research/concepts/brand/mechanisms.
2. PRD.
3. Product-definition lock: user language, requirements, entry points, exclusions.
4. Screen/service contract and contract gate.
5. Storyboard/art direction/design system/workbench/clickable demo.
6. Prototype runtime gate and task walkthrough.
7. Critique/risk/feasibility/coverage audit.
8. Design acceptance loop:
   - assemble complete evidence;
   - show dashboard/demo/evidence matrix;
   - record user feedback;
   - route P0 findings to the owning upstream artifact;
   - regenerate and revalidate;
   - request explicit approval only when P0 findings are resolved;
   - write the hash-bound baseline after approval.
9. Product handoff.
10. In build-ready runs, create the target-grounded technical plan and run the technical stage. Design-only runs stop honestly at product handoff.

## 6. Change cascade

| Changed source | Invalidate |
|---|---|
| product definition / PRD | service graph → storyboard/design/demo → acceptance → handoff → technical plan |
| service manifest | runtime report → visual evidence/acceptance → handoff → technical plan |
| storyboard/copy/design system/workbench | visual evidence/acceptance → handoff → technical plan |
| demo | runtime report + visual evidence/acceptance → handoff → technical plan |
| design acceptance | handoff status + technical plan |

The validator detects stale hashes; skills own regeneration. Never update hashes without re-running their evidence and approval step.

## 7. Failure ownership

- product definition/traceability → `product-definition`, `prd`, `service-contract`
- missing surface/action/state/runtime → existing screen/demo skills
- missing/stale visual evidence or unresolved review → `design-acceptance` plus the named visual owner
- stale handoff → `engineering-handoff`
- technical mapping/blocker → `tech-plan`

Cross-cutting consumers that must display or preserve the new semantics: `decision-dashboard`, `engineering-handoff`, `feature-adoption`, `quality-bar`, `visual-quality-checklist`, README, initializer, plugin manifests, and all validator fixtures/tests.

## 8. Test design

- Extend the valid fixture through all five stages.
- Mutation tests for every AC1–AC16 failure class.
- Hash-change tests for each baseline layer.
- Initializer tests for pending contracts and honest dashboard/frontmatter.
- CLI tests for stage output/report writing.
- Browser verification remains responsible for actual demo interactions; technical stage consumes its current hash-bound report rather than simulating it.
