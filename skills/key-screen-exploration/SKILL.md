---
name: key-screen-exploration
description: Creates and iterates one representative high-fidelity screen after visual-direction approval, records narrow and wide viewport evidence plus critical states, and blocks design-system expansion until the user explicitly approves the quality ceiling. Use only in the optional design-production workflow before full-system production.
---

# Key Screen Exploration

Create one representative screen before expanding a visual system.

## Preconditions

- `visual-direction` validation passes.
- `03.5-art-direction-brief.md` codifies the selected direction.
- `00-workflow-state.json` records the design-entry and visual-direction decisions.

## Work

1. Select one P0 surface that exposes the product's hardest hierarchy, brand expression, and recovery state.
2. Produce the same surface at one narrow and one wide viewport from the same source.
3. Include its most important non-default state.
4. Use available frontend-design and image-generation skills where appropriate. State capability limits instead of presenting generic output as production quality.
5. Critique product fit, hierarchy, visual specificity, responsive behavior, accessibility, and state clarity.
6. Iterate on this screen only. Do not build the remaining screen set yet.
7. Present current evidence to the user and wait for explicit approval.

## Outputs

- `03.8-key-screen-review.md`
- `03.8-key-screen-review.json`, starting from `assets/templates/key-screen-review.json`
- current local image evidence for narrow and wide viewports

Each JSON evidence row includes a stable ID, local file, SHA-256, viewport, state IDs, and render-source reference. Record `status: user-approved` only after the user reviews the current evidence. Append `00-decision-log.md`, then update the `key-screen` gate with `scripts/workflow_state.py confirm <planning-dir> --gate key-screen ...` using the same decision reference.

## Exit

Run:

```bash
python3 scripts/validate_service_blueprint.py <planning-dir> --stage key-screen
```

Only `key-screen-pass` permits `design-system`, `ux-writing`, and `design-system-workbench` to expand the approved direction.
