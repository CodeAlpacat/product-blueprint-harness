---
name: decision-dashboard
description: Creates a visual HTML review dashboard from Product Blueprint artifacts so users can approve, request changes, or hold decisions without reading every markdown file. Use after any planning phase when markdown artifacts are too long or when the user wants fast visual review and next-step decisions.
---

# Product Blueprint Decision Dashboard

Use this whenever the planning package has several markdown artifacts and the user needs a faster review surface.

Markdown remains the source of truth. The dashboard is the user's decision cockpit: what changed, what to inspect visually, what must be decided, what is blocked, and which skill runs next.

## Inputs

- `00-decision-log.md`
- Current phase artifact
- Storyboard or workbench HTML when available
- Screenshots when available
- Open questions and gate status

## Output

Create or update:

- `00-review-dashboard.html`

## Required Sections

1. **Current Status**: phase, pass/fail (+ACCEPT-FLAG), and why.
2. **Review This First (핵심 2~4)**: the 2–4 artifacts the user must actually look at now, each marked ★, each with a one-line "what to confirm/decide." Do not list all artifacts here — only the few that matter this phase.
3. **Decision Queue**: each decision as `Approve`, `Change`, or `Hold`; include impact and the file that changes.
4. **Flow Snapshot**: compact user-flow map with entry, gate, commitment, result, and recovery.
5. **Design Snapshot**: current visual direction, missing design work, and quality risks.
6. **Scope Snapshot**: P0/P1/P2 and explicit scope-out.
7. **Artifact Map**: every artifact grouped (planning / spec / design), each with a one-line purpose + status, so the founder sees the whole package at a glance and knows which are ★-key vs supporting evidence.
8. **Evidence / Gaps**: what is observed, user-confirmed, proposed, assumed, or unverified.
9. **Next Step**: one recommended skill, why, and what it will produce.

## Rules

- **Update after every phase — mandatory, not on request.** The orchestrator finishes a phase by refreshing this dashboard. Never ship 10+ markdown files while the dashboard is still the init stub. A stale/stub dashboard while artifacts pile up is the single most common way the founder ends up overwhelmed ("too many docs, don't know what to look at").
- Do not duplicate entire markdown contents.
- Put the user's decisions and visual evidence first.
- Link to markdown files for details.
- Keep the dashboard readable in one browser tab.
- Use Korean when the user is Korean.
- Show unresolved issues honestly; do not make a polished dashboard hide missing work.
- When production design is not ready, say so visibly.

## Pass / Fail

Pass if the user can answer "what do I need to look at and decide next?" within 30 seconds.

Fail if the dashboard is just a markdown dump in HTML, hides open questions, or does not link to the concrete artifact to inspect next.

## Next Step

- 사용자가 결정할 것: 없음 — 대시보드 갱신은 매 단계 자동 의무. 유저에게는 "지금 볼 것 2~4개"만 노출.
