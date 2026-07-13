---
name: implementation-readiness
description: Deterministically checks whether Product Blueprint artifacts form a continuous implementation-ready service contract. Validates required files, stable IDs, surface/action/state wiring, prototype DOM evidence, frontend feedback, backend/data operation ownership, journeys, responsive evidence, explicit deferrals, and readiness claims; generates the authoritative readiness report. Use after screen contracts, after clickable prototype work, before engineering handoff approval, or whenever a dashboard claims planning is complete.
---

# Product Blueprint Implementation Readiness

Use this gate instead of asking the same agent whether its own work is complete. Read `${CLAUDE_PLUGIN_ROOT}/references/service-contract.md` for the contract and failure ownership model.

## Choose the stage

- `contract`: after PRD/screen/service-contract, before storyboard. Checks graph, references, operations, journey lifecycle, exclusions.
- `prototype`: after clickable demo and browser walkthrough. Adds DOM surface/action/state evidence, `data-go`/`data-effect`, reachability, responsive evidence, dead/uncontracted controls, and current hash-bound runtime evidence for every transition/effect/state.
- `handoff`: after a draft `05-engineering-handoff.md`. Checks the full artifact set and writes the authoritative report.

## Run

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage <contract|prototype> --no-write
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_service_blueprint.py" <planning-dir> --stage handoff
```

Never edit the report to create a pass. Fix the owning artifact and rerun.

## Failure routing

- PRD/baseline/exclusion → `prd`
- surface/action/state/entry/exit → `screen-contract`
- operation, lifecycle, AI assist → `service-contract` or `backend-systems-brief`
- missing/mismatched DOM evidence → `clickable-demo`
- task/user evidence → `prototype-test`
- stale or false ready claim → `decision-dashboard` / `engineering-handoff`

Use the error code and `owner` returned by the validator. Do not patch unrelated downstream files to hide an upstream failure.

## Handoff close procedure

1. Ensure handoff frontmatter says `planning-readiness: pending` while drafting.
2. Run the handoff stage. It writes `05-readiness-report.json` and `.md`.
3. If status is `fail`, leave handoff/dashboard not-ready, show the failure ledger, and route fixes upstream.
4. If status is `pass`, update handoff to `planning-readiness: pass` and dashboard root to `data-readiness-status="pass"`; display report status, manifest SHA-256, user-validation status, and accepted limitations.
5. Rerun handoff stage with `--no-write` to prove the consumers do not contradict the report.

`user_validated=false` does not necessarily block engineering readiness, but it must remain visible. Lite may return `lite-pass`; it is never engineering-ready.

## Output

- `05-readiness-report.json`: machine status and findings
- `05-readiness-report.md`: founder/engineer failure ledger
- Updated dashboard/handoff status only after a real pass

## Next Step

- On failure: run the reported owner skill, then rerun the same stage.
- On handoff pass: present the report and vertical implementation slices for user approval. Use `tech-plan` only when the user requests concrete API/DB/frontend/backend architecture.
