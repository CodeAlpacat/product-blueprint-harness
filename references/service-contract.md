# Service Contract — canonical product/design continuity model

Use this reference when creating or consuming `02.6-service-manifest.json`. Markdown explains intent; this manifest is the machine-readable identity and wiring source for product/design readiness.

`02.05-planning-quality-review.json` proves that concept, brand, mechanisms, and PRD received all six planning lenses, that P0/P1 findings were resolved, that source hashes are current, and that the user confirmed the first-version scope. `02.1-product-definition.json` is then the confirmed source set. The service manifest does not decide which user requirements or entry points exist; it proves how that set becomes surfaces, actions, operations, states, and journeys.

## Stable IDs

- IDs match `[a-z][a-z0-9-]*` and survive label, route, and file-number changes.
- Use the same surface/action/state/operation/journey ID in PRD, screen contract, storyboard, demo DOM, prototype test, feasibility consultation, design acceptance, and handoff.
- `S1`, `screen-3`, array positions, and visible Korean/English labels are not stable identity.

## Collections

- `release_profile`: roles, platforms/viewports, explicit exclusions, accepted limitations.
- `surfaces`: screens and overlay-like surfaces. `background` is allowed only with an inspect/recovery surface.
- `actions`: every product button/link/navigation/effect with source, target/effect, feedback, and accessibility.
- `states`: required non-happy states with reproducible prototype evidence.
- `operations`: product-level frontend/backend/data responsibility, not endpoint/table design.
- `ai_assists`: every AI claim's input → result widget → editable unit → save destination → failure UI.
- `journeys`: persona start, ordered actions, expected end, exception/recovery, refresh/back/cross-device behavior.

Traceability rules: every included P0 requirement reaches a surface and journey; interaction requirements reach an action; system requirements reach an operation; every entry point reaches a journey with the same persona.

The full starter shape lives at `assets/templates/service-manifest.json`.

## Maturity

Each P0 surface carries five booleans. Never replace them with `complete: true`.

1. `defined`: purpose, scope, entry/exit, and required states exist.
2. `prototyped`: the surface and required states exist in the demo DOM.
3. `wired`: actions and transitions use the same IDs in contract and DOM.
4. `contracted`: frontend feedback and operation/data responsibilities are resolved.
5. `verified`: stage validator and required scenario/browser evidence passed.

## DOM evidence protocol

```html
<section id="surface-item-detail" data-surface="item-detail">
  <button
    id="action-start-checkout"
    data-action="start-checkout"
    data-go="checkout"
  >Continue</button>
</section>
```

- Product surfaces: `id` + `data-surface`.
- Product buttons/links: `id` + `data-action`.
- Navigation/overlay transitions: `data-go` equals `target.surface_id`.
- Same-surface effects: `data-effect` equals the stable `target.effect` ID.
- Review-only jump bars/toggles: `data-demo-control`; never count them as product UI.
- IDs must be unique in the HTML document.

Static DOM agreement is not runtime proof. Browser-drive every manifest transition/effect and required state, then write `04.37-runtime-verification.json` with `runner: browser`, current manifest/demo SHA-256 values, and one pass/fail row per action/state. The prototype/handoff gates reject missing, incomplete, failed, or stale reports.

## Operation boundary

Operations define the product behavior and constraints the design must represent without prematurely choosing schema/API:

- owner and source of truth
- input/output user promise
- authorization and persistence
- idempotency, consistency, conflict strategy
- failure and recovery
- audit/retention, latency/cost, observability, abuse boundary

Use `n/a:<reason>` when a field truly does not apply. Use `decision-needed:<decision-id>` only while blocked; readiness fails until resolved.

## Stage validation

```bash
python3 <plugin-root>/scripts/validate_service_blueprint.py <planning-dir> --stage contract --no-write
python3 <plugin-root>/scripts/validate_service_blueprint.py <planning-dir> --stage planning --no-write
python3 <plugin-root>/scripts/validate_service_blueprint.py <planning-dir> --stage prototype --no-write
python3 <plugin-root>/scripts/validate_service_blueprint.py <planning-dir> --stage design --no-write
python3 <plugin-root>/scripts/validate_service_blueprint.py <planning-dir> --stage handoff
```

- `contract`: graph, references, operations, journey lifecycle. Prototype may not exist yet.
- `planning`: contract plus feasibility notes, coverage audit, low-fidelity flows, systems constraints, and a design brief. Visual UI does not exist yet.
- `prototype`: DOM evidence, states, controls, transitions. Handoff may not exist yet.
- `design`: visual/state evidence, feasibility consultation, absorbed constraints, and explicit user approval.
- `handoff`: full product/design artifact set and authoritative `05-readiness-report.{json,md}`. It does not claim technical or implementation readiness.

Failure codes route back to the owning skill. Do not edit the generated report to manufacture a pass.
