---
name: service-contract
description: Creates and maintains the machine-readable service manifest that connects Product Blueprint user stories, screens, actions, states, frontend feedback, backend/data responsibilities, journeys, and prototype evidence. Use after PRD and screen contracts, after any screen/flow/scope change, or whenever implementation-readiness must be checked without relying on prose self-assessment.
---

# Product Blueprint Service Contract

Create or update `02.6-service-manifest.json`. This is the stable identity and wiring source for implementation readiness; markdown remains the human explanation.

Read `${CLAUDE_PLUGIN_ROOT}/references/service-contract.md` before editing the manifest. Start from `${CLAUDE_PLUGIN_ROOT}/assets/templates/service-manifest.json` for a new project.

## Inputs

- `00-decision-log.md`
- `02-prd.md`
- `02-mechanisms.md` when mechanisms exist
- `02.5-screen-contracts.md`
- `02.7-feasibility-checkpoint.md` when it exists
- existing demo/prototype-test evidence when updating a later-stage manifest

## Workflow

1. Set release profile, roles, platforms/viewports, explicit exclusions, and accepted limitations with decision references.
2. Assign stable IDs to every P0/P1 surface, action, required state, operation, and journey. Preserve existing IDs during edits.
3. Make action source/target match each surface's entry/exit lists exactly.
4. Attach T0/During/Done feedback and keyboard/focus/announcement behavior to every action.
5. Define product-level operation ownership and failure/lifecycle boundaries for every read/write/destructive/external action. Do not choose endpoints or tables here.
6. For every AI-assisted action, fill input, result widget, editable unit, save destination, and failure/truncation UI.
7. Write happy, exception, and boundary journeys, including refresh, back, and cross-device behavior.
8. Set maturity booleans only when their evidence exists. Never use one `complete` flag.
9. Run the contract-stage validator and fix every error before visual design:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage contract --no-write
```

## Change discipline

Any PRD scope, screen, state, action, mechanism, risk mitigation, or feature-adoption change updates this manifest in the same phase. Then cascade only to downstream consumers: storyboard → UX copy/workbench → demo → prototype test → readiness/handoff.

Do not infer legacy markdown into a ready manifest. Migrate it, run the validator, and keep unresolved values as `decision-needed:<id>` blockers.

## Output and gate

- Output: `02.6-service-manifest.json`
- Pass: validator returns `contract-pass` with zero findings.
- Fail: do not proceed to storyboard; route each failure to its reported owner.

## Next Step

- Use `product-blueprint:feasibility-review` checkpoint mode, then `product-blueprint:storyboard`.
- After the demo exists, run `product-blueprint:implementation-readiness` at prototype stage.

