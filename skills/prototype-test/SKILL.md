---
name: prototype-test
description: Tests clickable or screenshot-based prototypes against concrete user tasks before engineering design. Use after storyboard, design-system workbench, mockup, or high-fidelity HTML/Figma/React screens when the team needs to verify flow comprehension, action gates, state coverage, and whether users can complete the intended task without misleading shortcuts.
---

# Product Blueprint Prototype Test

Use this before accepting a storyboard, design-system workbench, or high-fidelity mockup. The goal is not code QA; it is product-flow validation.

Use `02.6-service-manifest.json` journeys as the task inventory. Do not invent a task path in this artifact; if a real task is missing, add the journey and rerun the contract/prototype gates.

## Test Setup

Define 5 to 8 task prompts:

- First-time user task
- Returning user task
- Discovery-to-detail task
- Paid or mission-cost task
- Safety/locked content task
- Error or empty state recovery
- Creator or advanced user task when relevant

For each task, record:

- Starting screen
- Expected user interpretation
- Required action path
- Misleading action to watch for
- Pass/fail signal
- Observed confusion or evidence gap
- Journey ID, action IDs, expected end surface ID, and exception state/recovery IDs

## Checks

- Can the user tell what this screen is for in 5 seconds?
- Does the prototype hide actions that require prior detail/consent?
- Are cost, safety, and system-judged outcomes clear before commitment?
- Are empty, locked, paid, and error states represented?
- Does the prototype work at the target mobile viewport?
- Are screenshots readable and uncropped?

## Two Levels — never conflate them

1. **Heuristic walkthrough (always run)**: you execute the tasks against the demo/workbench yourself, adversarially. This catches flow breaks, hidden gates, unclear copy. It is NOT user evidence.
2. **Real-user protocol (recommend when stakes justify it)**: 5 target-audience users, the same task prompts, think-aloud, success signal per task, confusion notes. Provide the ready-to-run protocol in the artifact (tasks, script, what to record) so the founder can execute it without design-research background.

Until level 2 runs, every downstream artifact that claims the flow "works" carries the label **`실사용자 미검증`** — the handoff readiness checklist must show it. A heuristic pass upgraded to "validated" is a false claim.

After testing, update manifest `user_validation.status/evidence` and the affected surface `verified` fields. Then rerun the prototype-stage validator; heuristic evidence may pass the structural gate but keeps `user_validated=false`.

Copy the same honest validation status into the pending design-acceptance contract. Owner design approval never upgrades heuristic evidence to `real-user`.

## Rules

- Do not call a prototype tested because it renders.
- Do not use developer knowledge as user evidence.
- Mark simulated interactions clearly.
- If a task fails because the product requirement is unclear, go back to PRD or screen contract.

## Output

Create `04.4-prototype-test.md` with:

- Test tasks
- Pass/fail table (heuristic) + real-user protocol (ready to run) + validation status label
- Confusion log
- Required revisions
- Screenshots or links to prototype evidence
- Decision: pass or fail (plus ACCEPT-FLAG rows if capped — see `references/quality-bar.md`)

## Next Step

- 사용자가 결정할 것: 실사용자 검증(레벨 2) 실행 여부와 시점 — 미실행이면 "실사용자 미검증" 라벨이 핸드오프까지 따라간다.
- Use `product-blueprint:design-critique` for structured product/UX/visual/systems critique.
- If the prototype passes, proceed to `product-blueprint:feasibility-review`.
