# Service Contract — canonical implementation-readiness model

Use this reference when creating or consuming `02.6-service-manifest.json`. Markdown explains intent; this manifest is the machine-readable identity and wiring source for readiness.

## Stable IDs

- IDs match `[a-z][a-z0-9-]*` and survive label, route, and file-number changes.
- Use the same surface/action/state/operation/journey ID in PRD, screen contract, storyboard, demo DOM, prototype test, handoff, and optional tech plan.
- `S1`, `screen-3`, array positions, and visible Korean/English labels are not stable identity.

## Collections

- `release_profile`: roles, platforms/viewports, explicit exclusions, accepted limitations.
- `surfaces`: screens and overlay-like surfaces. `background` is allowed only with an inspect/recovery surface.
- `actions`: every product button/link/navigation/effect with source, target/effect, feedback, and accessibility.
- `states`: required non-happy states with reproducible prototype evidence.
- `operations`: product-level frontend/backend/data responsibility, not endpoint/table design.
- `ai_assists`: every AI claim's input → result widget → editable unit → save destination → failure UI.
- `journeys`: persona start, ordered actions, expected end, exception/recovery, refresh/back/cross-device behavior.

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

## Operation boundary

Operations define what implementation must preserve without prematurely choosing schema/API:

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
python3 <plugin-root>/scripts/validate_service_blueprint.py <planning-dir> --stage prototype --no-write
python3 <plugin-root>/scripts/validate_service_blueprint.py <planning-dir> --stage handoff
```

- `contract`: graph, references, operations, journey lifecycle. Prototype may not exist yet.
- `prototype`: DOM evidence, states, controls, transitions. Handoff may not exist yet.
- `handoff`: full artifact set and authoritative `05-readiness-report.{json,md}`.

Failure codes route back to the owning skill. Do not edit the generated report to manufacture a pass.
