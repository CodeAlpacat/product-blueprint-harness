---
name: prototype-test
description: Tests clickable or screenshot-based prototypes against concrete user tasks before engineering design. Use after storyboard, design-system workbench, mockup, or high-fidelity HTML/Figma/React screens when the team needs to verify flow comprehension, action gates, state coverage, and whether users can complete the intended task without misleading shortcuts.
---

# Product Blueprint Prototype Test

Use this before accepting a storyboard, design-system workbench, or high-fidelity mockup. The goal is not code QA; it is product-flow validation.

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

## Checks

- Can the user tell what this screen is for in 5 seconds?
- Does the prototype hide actions that require prior detail/consent?
- Are cost, safety, and system-judged outcomes clear before commitment?
- Are empty, locked, paid, and error states represented?
- Does the prototype work at the target mobile viewport?
- Are screenshots readable and uncropped?

## Rules

- Do not call a prototype tested because it renders.
- Do not use developer knowledge as user evidence.
- Mark simulated interactions clearly.
- If a task fails because the product requirement is unclear, go back to PRD or screen contract.

## Output

Create `04.4-prototype-test.md` with:

- Test tasks
- Pass/fail table
- Confusion log
- Required revisions
- Screenshots or links to prototype evidence
- Decision: pass, conditional pass, or fail

## Next Step

- Use `product-blueprint:design-critique` for structured product/UX/visual/systems critique.
- If the prototype passes, proceed to `product-blueprint:feasibility-review`.
