---
name: visual-directions
description: Produces and compares two or three genuinely different visual UI directions from an approved design brief and user taste evidence before any direction expands to a full screen set. Use only in the optional design-production workflow.
---

# Visual Directions

Create `03.4-visual-directions.md`, `03.4-visual-directions.json` from `assets/templates/visual-direction-review.json`, and comparable visual evidence for two or three directions. This is the divergent gate of the optional design-production workflow.

## Preconditions

- The planning-stage validator passes.
- `03-design-brief.md` is current.
- The user has explicitly asked to begin visual design.
- Positive and negative taste references, or an honest note that they are missing, are recorded.

## Direction contract

Each direction must define:

- a distinct design thesis tied to audience, positioning, and product behavior
- typography character, color behavior, density, spatial rhythm, shape, imagery, and motion principles
- one product-specific signature element
- how the same representative P0 screen and critical state would differ
- accessibility and responsive implications
- reference principles used and patterns deliberately rejected
- main quality risk and the condition under which the direction should lose

Directions that differ only by palette, font, border radius, or theme fail.

## Comparable evidence

Show every direction at the same fidelity, on the same representative screen, state, content, and viewport. A material board plus a focused screen crop is acceptable. Do not build a full screen set for any direction yet.

Use suitable frontend-design and image-generation capabilities when available. When they are unavailable, state the limitation and keep the comparison at art-direction fidelity rather than presenting weak mockups as production UI.

## User decision

Recommend one direction with evidence and say when another would win. Ask the user to choose, request a revision, or pause. Record the decision and reviewed evidence in `00-decision-log.md`. After explicit approval, record the same reference with `scripts/workflow_state.py confirm <planning-dir> --gate visual-direction ...`.

Do not self-approve. Do not continue into the design system or remaining screens until the user confirms a direction.

## Output

`03.4-visual-directions.md` contains:

- user taste evidence and gaps
- shared comparison setup
- two or three direction briefs
- links to comparable evidence
- comparison table
- recommendation and tradeoffs
- explicit user decision status
- chosen direction, when confirmed

The JSON binds the shared comparison setup, each direction's local evidence and SHA-256, the selected direction, explicit approval evidence, and hashes for the design brief and Markdown comparison. Keep it pending until the user reviews current evidence.

After confirmation, run `validate_service_blueprint.py <planning-dir> --stage visual-direction`. Only after `visual-direction-pass`, use `product-blueprint:art-direction-brief` to codify the chosen direction, then use `product-blueprint:key-screen-exploration` for one representative high-fidelity screen.
