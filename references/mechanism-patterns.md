# Mechanism Patterns — worked examples for experience-mechanism contracts

Each pattern shows the questions a mechanism contract must answer. Use as templates; replace the domain examples with your product's.

## Pattern anatomy (every mechanism)

1. **User promise** — the sentence the user believes (verbatim, user language)
2. **Inputs → outputs** — what feeds it, what it produces, when it runs
3. **User controls** — inspect / edit / undo / delete / opt out
4. **Transparency & recovery** — what the user sees when it works, errs, or is disputed
5. **Cost & metering** — free / metered / paid; how cost is disclosed BEFORE commitment
6. **Acceptance examples** — 2–3 concrete input→output cases a tester can verify
7. **Feasibility questions** — what engineering must confirm (flag for the checkpoint)

## 1. Long-term memory

- Promise: "it remembers what mattered between sessions."
- Source is usually change during interaction, not explicit user entry. Default surface: background behavior + a review/correction surface (side panel/sheet) — never a main tab.
- Controls: review list, edit, forget, undo-forget (forgetting must be reversible for a window).
- Failure: wrong memory surfaced → correction path in ≤2 taps; disputed memory → show provenance ("from the conversation on …").
- Feasibility: extraction quality, storage growth, retrieval latency, cost per session.

## 2. Judging / scoring (missions, evaluations)

- Promise: "the outcome follows from what I did, and I can see why."
- Outputs: verdict + reason string + delta, logged with timestamps. Users NEVER edit scores directly (trust collapses); they influence through action.
- Transparency: recent-changes log with causes beats a bare number.
- Failure: unfair-feeling verdict → show the reason; appeal path if stakes are high.
- Feasibility: judge consistency, prompt cost per turn, adversarial gaming.

## 3. Recommendation / next-step suggestion

- Promise: "it offers me a good next thing without taking over."
- Surface: inline, dismissible, never auto-executing. Paid suggestions show cost on the chip itself.
- Cold start: what first-time users see (curated set, not empty).
- Feasibility: signal availability at cold start, latency budget in the hot path.

## 4. Relationship / progression state

- Promise: "our history changes how this behaves."
- Multi-axis state (e.g., 6 emotion axes) needs: current tier + label, per-axis values, recent deltas WITH causes, and a read-only guarantee.
- Surface: compact glimpse in the core surface (chip) → full view on demand (dedicated view, not a main tab).
- Feasibility: state update reliability per turn, drift over long histories.

## 5. Ranking / leaderboards

- Promise: "the ordering is fair and fresh."
- Define: window, tie-breaking, abuse counters (self-boosting, bots), and what new items get (cold-start slot?).
- Feasibility: recompute cadence vs cost, abuse detection.

## 6. Creator publishing / validation

- Promise: "I can publish, and the platform catches problems before my audience does."
- Pipeline states: draft → submitted → checks (policy/quality) → published → reported → actioned. Each state has a user-visible status and a next action.
- Feasibility: review throughput, automated-check precision.

## 7. Paid actions / cost trust

- Promise: "I always know the price before I commit, and failures don't charge me."
- Non-negotiables: price visible on the trigger itself; deduction and execution atomic; failed execution auto-refunds visibly ("charged nothing" copy).
- Feasibility: ledger atomicity, refund path, double-spend prevention.

## 8. Safety gates (age, content tiers)

- Promise: "restricted content is truly separated, not hidden behind a blur."
- Structural rule: unverified users' listings EXCLUDE gated items server-side (not client filter). Verification stronger than self-declared birth date. Verification data disposed after check; only the boolean + date kept.
- Feasibility: verification vendor, disposal compliance, cross-market rules.
