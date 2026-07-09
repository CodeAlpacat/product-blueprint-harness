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

1. **Current Status**: phase, pass/conditional/fail, and why.
2. **Review This First**: 3 to 6 visual cards linking to storyboard, workbench, screenshots, or key artifacts.
3. **Decision Queue**: each decision as `Approve`, `Change`, or `Hold`; include impact and the file that changes.
4. **Flow Snapshot**: compact user-flow map with entry, gate, commitment, result, and recovery.
5. **Design Snapshot**: current visual direction, missing design work, and quality risks.
6. **Scope Snapshot**: P0/P1/P2 and explicit scope-out.
7. **Evidence / Gaps**: what is observed, user-confirmed, proposed, assumed, or unverified.
8. **Next Step**: one recommended skill, why, and what it will produce.

## Rules

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
