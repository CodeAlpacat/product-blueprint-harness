---
name: decision-dashboard
description: Regenerates the Product Blueprint review dashboard from workflow state and validator findings. Use when the user wants a current review surface without trusting hand-authored readiness badges or reading every artifact.
---

# Product Blueprint Decision Dashboard

The dashboard is a generated validation view, not a source of truth and not a place to author approval. Its status comes only from the current validator run.

## Refresh

1. Run `scripts/workflow_state.py status <planning-dir> --json` to identify the current gate.
2. Choose the boundary actually being reviewed: `contract`, `planning`, `visual-direction`, `key-screen`, `prototype`, `design`, or `handoff`.
3. Run the validator without `--no-write`:

   ```bash
   python3 scripts/validate_service_blueprint.py <planning-dir> --stage <stage>
   ```

This atomically writes `00-validation-report.{json,md}` and regenerates `00-review-dashboard.html`. Handoff additionally writes `05-readiness-report.{json,md}`.

## What the generated view shows

- current stage, profile, and exact validator status
- every recorded user-decision gate and its decision reference
- artifacts required at the selected stage, with local links and present/missing state
- current structural-consistency findings and their owning artifact
- an explicit limitation that the validator does not prove market demand, planning quality, design taste, or implementation readiness

## Rules

- Never hand-edit a green badge or `data-readiness-status`.
- An empty or stale dashboard is not an input pass condition; rerun the validator to replace it.
- Early in planning, a failing dashboard with missing artifacts is expected. The next workflow gate comes from `workflow_state.py status`, not from hiding those findings.
- Keep user decisions in the decision log and workflow state. The dashboard only displays recorded state.
- A `planning-structure-pass` still requires human review of product judgment. A `design-pass` is not a handoff pass.
- When a source decision changes, invalidate the earliest affected gate and regenerate downstream work before refreshing the dashboard.

## Next Step

Return the user to the `next_skill` reported by workflow state, or to the finding owner when validation fails.
