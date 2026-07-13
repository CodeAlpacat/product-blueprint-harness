# Design acceptance and scope freeze

`05-design-acceptance.json` is the explicit boundary between product/design iteration and technical design. It does not replace the service manifest.

## Required proof

- current hashes for every implementation-bearing product/design source;
- every non-background P0 surface at every release viewport;
- every required state visible in each surface/viewport evidence row;
- stable component IDs with variants, states, tokens, accessibility behavior, and current visual evidence;
- a completed review round covering every current visual evidence row;
- mental-model checks covering every persona and included P0 requirement through journeys;
- all P0 findings resolved;
- explicit user approval of the current all-P0 evidence.

## Honest statuses

- `user-approved` means the product owner/founder explicitly accepted the current baseline.
- `real-user` means target users completed the recorded protocol. Never infer it from owner approval or heuristic walkthrough.
- A rejected design remains pending. User-requested review rounds have no retry cap.

## Change cascade

Any source or evidence hash mismatch makes the baseline stale. Fix the owning artifact, regenerate browser/visual evidence, repeat review, and request approval again. Never update a stale hash merely to restore green status.

