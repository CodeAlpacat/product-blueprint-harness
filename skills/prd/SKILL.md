---
name: prd
description: Converts research, ideation, and mechanism artifacts into a practical pre-development PRD with MVP loops, user stories, requirements, state coverage, risks, and acceptance criteria. Use when product direction is ready to become a storyboard-ready product specification before visual design or technical design.
---

# Product Blueprint PRD

Write the PRD after research or ideation, not before.

## Output Language And Stage Exit

- Default to the user's conversation language.
- If the user is Korean, write the PRD in Korean. Keep product names, feature labels being evaluated, and skill names in English only when useful.
- End with:
  1. `지금 확인할 산출물`
  2. `사용자가 결정할 것`
  3. `수정이 필요하면 어디를 바꿀지`
  4. `다음 추천 스킬`

## PRD Structure

1. Problem and product thesis
2. Target users, situations, and anti-users
3. Core loop and activation moment
4. MVP scope and non-goals
5. User stories by persona
6. Functional requirements by feature
7. Product-experience mechanisms required for trust
8. Screen and state inventory
9. Monetization and cost moments
10. Safety, policy, age, privacy, and abuse risks
11. Metrics and qualitative success signals
12. Open questions and unverified flows
13. Acceptance criteria
14. Entry-point inventory: route/deep link, in-product navigation, auth gate, external/notification, returning/cross-device; mark `n/a` with reason

## Required Feature Table

Include a feature table before detailed requirements:

| Feature | User job | Evidence | Scope | Required screens | Explicit non-goals |
| --- | --- | --- | --- | --- | --- |

Scope values:

- Core P0
- P0 support
- P1 differentiator
- P2 expansion
- Out of scope

Evidence values:

- Observed in reference
- User-confirmed
- Agent proposal
- Assumption
- Unverified

## Rules

- Tie requirements to observed evidence or labeled assumptions.
- Do not turn an agent-proposed differentiator into MVP unless the user confirmed it belongs in P0.
- Include obvious category basics such as search for discovery products, unless explicitly scoped out.
- Keep user stories behavioral: what the user wants to decide or accomplish.
- Include empty, error, locked, loading, paid, and completion states.
- For AI/system-judged features, include user promise, controls, transparency, failure UX, and acceptance examples.
- Do not specify database tables yet. Name product concepts first.
- Give every user story a stable ID (`us-<job>-<nn>`). These IDs must survive copy and screen-number changes.
- Before detailed requirements, enumerate the product category's baseline surfaces and classify each `P0 / P1 / P2 / excluded`, with a decision reference and current-release entry behavior for every exclusion.
- Map each P0 story to its starting entry point, required end result, exception, and boundary state. A nav label is not a surface definition.

## Output

Create `02-prd.md`. End with a feature-by-feature checklist and a `Product Definition Seed` table: requirement candidate | kind | persona/mental model | entry point | required result | exception/boundary | decision evidence. Run `product-definition` next to turn this into the user-confirmed `02.1-product-definition.json`; that confirmed source set then drives screen and service contracts.

## Next Step

- Use `product-blueprint:screen-contract` to define each priority screen's job, allowed actions, forbidden shortcuts, states, and transitions.
- Then use `product-blueprint:service-contract` to bind stories, surfaces, actions, states, operations, and journeys before visual design.
- Then use `product-blueprint:storyboard`.
