---
name: design-critique
description: Runs structured design critique across product intent, UX flow, visual quality, state coverage, systems behavior, accessibility, component-system coverage, and engineering handoff readiness. Use when a storyboard, design-system workbench, high-fidelity mockup, HTML prototype, or design-system draft needs senior-review feedback before feasibility review or implementation planning.
---

# Product Blueprint Design Critique

Use this as a critique, not a compliment pass. Findings should lead.

## Critique Lenses

1. **Product intent**: Does the design support the product thesis and MVP loop?
2. **Screen contract**: Does any screen do something it should not do?
3. **UX flow**: Are entry, detail, consent, commitment, result, and recovery paths clear?
4. **Visual direction**: Does it have a product-specific art direction or generic AI polish?
5. **Content and copy**: Are labels user-facing and action-specific?
6. **State coverage**: New, returning, empty, loading, locked, paid, unsafe, error, success.
7. **System trust**: Memory, judging, ranking, cost, and safety are visible where needed.
8. **Accessibility and mobile fit**: Text, touch targets, contrast, focus, overflow.
9. **Component-system coverage**: Are tokens, components, variants, states, and P0 screen applications visible enough to move later into frontend work?
10. **Handoff readiness**: Can designers and engineers act without guessing?

## Severity

- `P0`: Breaks product promise, trust, safety, payment, or core flow.
- `P1`: Causes likely user confusion or failed task.
- `P2`: Weakens polish, clarity, consistency, or scalability.
- `P3`: Preference or future improvement.

## Rules

- Do not rewrite the design from scratch unless the critique fails the concept.
- Tie every critique item to a screen, state, or user task.
- Avoid vague feedback such as "make it cleaner" or "more premium".
- If visual quality fails, route back to `art-direction-brief` or `visual-quality-gate`.

## Output

Create `04.45-design-critique.md` with:

- Findings by severity
- Open questions
- Required revisions
- Optional improvements
- Pass/fail decision (+ACCEPT-FLAG rows)
- Handoff readiness note

## Next Step

- 사용자가 결정할 것: P0/P1 지적의 수용 여부(수용 = 수정 후 재게이트, 기각 = 사유를 결정 로그에 기록).
- If P0/P1 issues remain, revise the relevant artifact and rerun `product-blueprint:prototype-test` or `product-blueprint:visual-quality-gate`.
- If visual-system coverage is missing, use `product-blueprint:design-system-workbench`.
- If only P2/P3 issues remain, proceed to `product-blueprint:feasibility-review`.
