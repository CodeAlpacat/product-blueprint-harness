# Direction Challenges — the harness challenges itself so the founder doesn't have to

Dogfood evidence: the founder's direction challenges — not completeness questions — produced the biggest quality jumps: "does the persona gate need to be a SCREEN?", "desktop should extend mobile, not invent a new grammar", "is wholesale transplant really better?". These are patternable. This catalog makes the harness fire them at the right lock points, answer them honestly in writing, and self-correct BEFORE presenting.

## How to run a challenge pass

At each lock point below, take the applicable challenge classes, answer each in 1–3 lines in the decision log (`[CHALLENGE]` entry: question → honest answer → keep/change). If a challenge wins, self-correct the artifact before showing it. A fresh-context subagent pass is better when the artifact is large (self-review bias); inline is acceptable for small locks. **A lock without a recorded challenge pass is not a lock.**

## Challenge classes

### C1 · Surface-level — "does this deserve to be a screen?" (fires: screen-contract lock, before demo)
For EVERY contracted screen: in the REPEAT-use flow (not first-use), is this a wasted hop? Is this "gate" actually a data contract (enforce in schema/API) wearing a screen costume — could it be a sheet/dialog/moment over its parent context? Smells: full-screen for a pick-or-confirm task; a step returning users click through unchanged; context (hero, detail) hidden by a screen that decides ABOUT that context.

### C2 · Responsive grammar — "did desktop invent a new product?" (fires: before any desktop rendering)
Desktop must be the mobile experience extended: app max-width cap, nav promotion, same content column. Smells: 3+ column editorial grids, split layouts, desktop-only modules. A persistent panel is only the opened form of an existing mobile sheet.

### C3 · Data-mirror IA — "is this the user's mental model or the database's?" (fires: IA/screen-contract lock, form design)
Tabs/forms/fields organized by table structure instead of user tasks. Smells: one tab per entity, forms demanding completeness the user doesn't care about, "manage X" screens for things users never manage.

### C4 · Reuse strategy — "wholesale anything is wrong" (fires: tech-plan)
Neither "transplant everything" nor "rewrite everything" survives scrutiny. Per domain: money/legal + production mileage → transplant; high coupling + simpler requirements → reference-rewrite. Name fork-drift cost.

### C5 · Monetization trust — "would this embarrass us in a screenshot?" (fires: any paid surface)
Undisclosed deduction, expiry-without-notice terms, hidden cancel, refund friction, gacha-gating the core loop. The trust copy (price/refund BEFORE payment) is part of the design, not legal boilerplate.

### C6 · Deferral honesty — "is P1 a decision or an escape?" (fires: scope lock, coverage audit)
Every deferral must answer "what does its P0 entry point look like?" (none / teaser / registry mini-contract). Smells: deferring precisely the hard parts (auth, deletion, refunds), "나중에 검증" without a plan. Account deletion is a store requirement, not a P1.

### C7 · Over-engineering — "who asked for this?" (fires: every artifact)
Additions justified by "consistency/safety/completeness" the user never requested. Also its mirror: complexity that trades stability for implementation speed.

### C8 · Identity coherence — "does this decision fight the product's DNA?" (fires: feature adoption, any borrowed pattern)
Borrowed features carry their source product's philosophy. Smells: adopting a mechanic that contradicts a locked principle (e.g., user-editable stats in a system-owned emotion model), source jargon leaking into UI copy, a feature that exists because the reference had it.

## Recommended-default doctrine (decision quality for passive users)

A user who only accepts defaults must still land on a coherent, tasteful product. Therefore every user-decision gate ships as: **권장안 먼저 + 근거 1–2줄 + "반대안이 이기는 조건" 1줄** — never a flat option menu. Recommendations are judged by "works well" (root-cause, maintainable, deterministic), not "fastest". If the harness cannot form a recommendation, that is a research gap — close it before asking.
