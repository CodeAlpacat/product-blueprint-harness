# Research Checklist — Complex Feature/Reference Coverage

Use when a reference product or a single feature is complex enough that ad-hoc exploration will miss things. Work the list; mark each row 관찰 / 미확인 / n.a.

## Per reference product

- [ ] Entry: first-run experience, onboarding steps, permissions asked, defaults chosen for the user
- [ ] Core loop walked end-to-end at least once, with screenshots at every state change
- [ ] Discovery surfaces: home modules, categories/filters, search (query → result → detail), rankings
- [ ] Detail surfaces: what convinces the user to commit (copy, imagery, social proof, gates)
- [ ] Commit gates: what stands between browsing and the core action (login, setup, payment, verification)
- [ ] The core action itself: happy path + at least one non-happy path (error, empty, retry)
- [ ] Return path: how the product brings users back (library/history, notifications, streaks, saved state)
- [ ] Monetization moments: where money appears, what is gated, price display, first-payment flow
- [ ] Safety/policy surfaces: age gates, content filters, report/block, moderation traces
- [ ] Empty/edge states: new account with zero data, no search results, expired/locked content
- [ ] Scroll depth: every long page scrolled to the bottom before claiming its structure is understood
- [ ] Logged-out vs logged-in differences noted; flows behind login/payment marked 미확인 if not accessible

## Per complex feature (memory, scoring, missions, checkpoints, etc.)

- [ ] What the user is PROMISED (the label and marketing copy, verbatim)
- [ ] What the user can inspect, edit, undo, or delete
- [ ] When it surfaces in the journey (moment of use) and where (inline / sheet / settings / dedicated screen)
- [ ] What happens on failure or dispute
- [ ] Whether it is free, metered, or paid — and how cost is disclosed
- [ ] What the feature name could ALSO mean (ambiguity list) — do not assume the first interpretation

## Evidence discipline

- Every claim points to a screenshot, URL, or DOM snapshot. No screenshot → label 미확인.
- Record the capture date; reference products change.
- Separate "what it does" (관찰) from "why we think they did it" (제안).
