# Experience Mechanism Patterns

## Long-Term Memory

Product question:

> What does the user expect the character or system to remember, and how can the user trust or correct that memory?

Contract fields:

- Memory types: facts, relationship events, promises, boundaries, preferences, unresolved plot threads, emotional state.
- Visibility: hidden, summarized, user-readable, or editable.
- Controls: pin, correct, forget, merge, mark private, exclude from a chat, reset route.
- Freshness: immediate, after session, after summary, manual save.
- Failure UX: "he forgot", "he remembers wrong", "memory is too much", "memory leaks across routes."
- Acceptance examples:
  - Character remembers a promise made three sessions ago.
  - User corrects a wrong relationship fact and future replies stop using it.
  - A new route does not inherit memories unless the user imports them.
- Feasibility questions for later:
  - What memory classes can be deterministic?
  - Which memories require user confirmation?
  - What is the cost/latency budget for memory retrieval?

## Mission Judging

Product question:

> How does the user know a mission was fairly completed or failed?

Contract fields:

- Goal types: explicit goal, sub-goal, hidden goal, score threshold, ending condition.
- Evidence: which user/character messages counted.
- Timing: live progress, end-only judging, checkpoint judging.
- Visibility: visible objective, hinted hidden objective, spoiler-protected result.
- Controls: force end, retry, replay from checkpoint, appeal/report unclear judging.
- Failure UX: success not recognized, bad ending feels arbitrary, hidden condition impossible to infer.
- Acceptance examples:
  - User receives true ending only after all visible goals and the hidden condition are satisfied.
  - Result screen explains which messages satisfied the confession condition.
  - If judging is uncertain, the product says so and lets the user continue or force evaluation.
- Feasibility questions for later:
  - Which conditions can be rule-like versus LLM-judged?
  - What evidence must be stored for audit?
  - How much explanation can be shown without spoiling hidden goals?

## Recommendation And Next-Message Suggestions

- Promise: help the user continue in the desired tone without taking control away.
- Controls: choose, regenerate, edit, dismiss, change intent.
- Failure UX: suggestions break character, ignore boundaries, spend currency without value.
- Acceptance examples: suggestion matches selected mode and does not auto-send.

## Relationship / Route State

- Promise: relationship progress is legible and affects future scenes.
- Controls: inspect, correct, branch, rewind, lock route.
- Failure UX: romance jumps too fast, conflict forgotten, route state contradicts chat.
- Acceptance examples: jealousy flag changes scene suggestions but does not override user boundaries.

## Ranking And Scoring

- Promise: scores compare similar attempts fairly.
- Controls: see scoring basis, filter by character/period, hide run, report suspicious rank.
- Failure UX: ranking rewards loopholes, different character difficulty makes scores meaningless.
- Acceptance examples: ranking shows character used, score, ending, update time, and my best run.

## Creator Publishing And Validation

- Promise: creators can publish playable content without invisible broken conditions.
- Controls: preview variables, test judge conditions, simulate sample turns, draft save.
- Failure UX: published mission cannot be cleared, variables render wrong, unsafe content leaks.
- Acceptance examples: creator tests happy/bad/true ending with sample transcripts before publishing.

## Paid Actions And Cost Trust

- Promise: users know when money/currency is consumed and what they get.
- Controls: confirm, cancel, insufficient balance, receipt/history.
- Failure UX: paid action has no visible result, cost repeats unexpectedly, failed generation consumes currency.
- Acceptance examples: regeneration shows price before click and does not charge on failed generation.
