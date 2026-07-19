# Why The Workflow Is Staged — Senior Team Process Rationale

Read this when the user asks why there are phases at all, why they can't jump straight to screens, or what a "senior team" would actually do.

## The core claim

A senior cross-functional team (PM, researcher, brand strategist, product designer, UX writer, design-systems designer, with engineering consulted throughout) does not produce quality by talent alone — it produces quality by **sequence and tension**:

1. **Sequence**: each stage locks a cheap-to-change decision before the next stage makes it expensive. Direction is cheaper than scope; scope is cheaper than flows; flows are cheaper than pixels; pixels are cheaper than code. Reversing this order is why "start from screens" products get rebuilt three times.
2. **Tension**: quality comes from disagreement rituals — design critique, engineering feasibility pushback, risk review. A single voice (human or AI) converges to its own average. That is why this harness forces parallel concepts before lock, an adversarial fresh-context gate on visuals, a red-team pass on the PRD, and a feasibility checkpoint *before* screens are finalized — not because process is virtuous, but because each ritual is a stand-in for a colleague who would have said "no."

## What each stage is a stand-in for

| Harness stage | The senior-team ritual it replaces |
|---|---|
| Brief / intake | PM kickoff: "what are we actually building and for whom" |
| Research + reference deconstruction | UX researcher's competitive teardown with evidence, not vibes |
| Parallel concepts + direction lock | Design leadership reviewing 2–3 directions before committing |
| Positioning & brand | Brand strategist: name, voice, promise — decided before pixels inherit them |
| Mechanisms + PRD | PM + systems designer writing behavior contracts for the invisible parts |
| Screen contracts | Product designer's IA pass: each screen has one job, forbidden shortcuts named |
| Feasibility checkpoint | The engineer in the room saying "that costs three sprints" BEFORE mockups promise it |
| Storyboard | Flow review on a wall — the whole journey visible at once |
| Art direction (measured) | Art director handing a spec, not adjectives |
| Design system + React boards + flow preview | Design-systems team: branded tokens, reusable components, states, Depth screens, and all P0 flows from one source — not one hero shot |
| Adversarial visual gate | The critique where a fresh pair of eyes fails your favorite screen |
| Risk register | Legal/policy reviewer who reads it before launch, not after the incident |
| Engineering handoff | The handoff meeting where developers can start architecting, not start asking |

## The two failure modes this prevents

- **The waterfall skip**: jumping to high-fidelity screens with no contracts under them. Screens look done, so nobody re-opens scope; the product ossifies around the first pretty mockup.
- **The single-voice collapse**: one generator grading its own homework. Every gate in this harness that matters is either measurable (numbers) or fresh-context (a critic who didn't build it). Self-graded adjectives are treated as no gate at all.
- **The prototype rewrite**: approving standalone HTML, then rebuilding components and layouts in the app. The React component/state board and Depth screens must use the same sources, so later work attaches behavior and data instead of redesigning the UI.

## When to compress

Stages are not sacred; the decisions are. The Lite path keeps the decision sequence (direction → scope → flows) and drops the production-design stages. What is never skippable: the decision log, user decision gates, and labeling assumptions. A two-day plan with honest labels beats a two-week plan with hidden guesses.
