# Design acceptance and scope freeze

`05-design-acceptance.json` is the explicit boundary between product/design iteration and a later technical-design process. It proves design acceptance, not implementation readiness, and does not replace the service manifest.

## Required proof

- current hashes for every implementation-bearing product/design source;
- every non-background P0 surface at every release viewport;
- every required state visible in each surface/viewport evidence row;
- stable component IDs with variants, states, tokens, accessibility behavior, and current visual evidence;
- a completed review round covering every current visual evidence row;
- developer-lens feasibility checks for every P0 surface/action/operation/journey at the required frontend/backend/platform/accessibility lenses;
- every conditional constraint absorbed into current design/prototype evidence, with no infeasible behavior left open;
- mental-model checks covering every persona and included P0 requirement through journeys;
- all P0 findings resolved;
- explicit user approval of the current all-P0 evidence, every current feasibility check ID, and the canonical feasibility-check SHA-256.

## Honest statuses

- `user-approved` means the product owner/founder explicitly accepted the current baseline.
- `real-user` means target users completed the recorded protocol. Never infer it from owner approval or heuristic walkthrough.
- A rejected design remains pending. User-requested review rounds have no retry cap.
- `ready_for_technical_design` means an engineer may begin a separate architecture process without first rediscovering product-visible constraints. It does not mean implementation can begin unchanged.

## Change cascade

Any source, feasibility verdict, or evidence mismatch makes the baseline stale. Fix the owning artifact, regenerate browser/visual evidence, repeat review, and request approval again. Never update a stale hash merely to restore green status.
