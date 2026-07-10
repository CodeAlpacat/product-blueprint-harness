---
name: parallel-concepts
description: Generates and compares multiple product or screen concepts before committing to one direction. Use after ideation or reference deconstruction when the user needs senior-designer-style divergent exploration, alternative IA/layout/art-direction options, or a recommendation before PRD, screen contracts, storyboard, or high-fidelity design.
---

# Product Blueprint Parallel Concepts

Use this during the divergent half of planning. A senior designer does not jump to one polished answer; they compare viable directions against the product goal.

## Concept Set

Create 3 concepts by default:

1. **Conservative**: Close to the strongest reference mental model.
2. **Differentiated**: Same user job, stronger product identity.
3. **Risky**: One justified design or product bet that could become memorable.

For each concept define:

- Product thesis
- Core loop
- Home/screen role
- Primary user decision
- Main mechanism dependency
- Art direction summary
- Monetization or trust implication
- Biggest risk

## Comparison Criteria

- User clarity
- Differentiation
- Reference fidelity
- MVP feasibility
- Trust and safety
- Monetization fit
- Visual potential
- Scope risk

## Rules

- Concepts must differ in product logic, not only color or typography.
- **Each concept must be decidable by a non-reader.** Positioning adjectives ("curated", "retention-first") are not enough — a founder who does not read the full doc cannot tell them apart (observed failure). Give each concept a **concrete, comparable diff**: its screen/nav map, its distinguishing mechanic, and one representative visual (a small wireframe/thumbnail, or an ASCII IA sketch showing how the home/nav differs). The difference must be *seeable*, not just readable.
- Present the choice visually when possible (side-by-side IA sketches or thumbnails), so the direction-lock decision can be made from a glance, not a full read.
- Do not make all options equally good. Recommend one.
- If a concept breaks a known product gate, mark it as rejected.
- For screen concepts, each option must say what action is intentionally unavailable.

## Output

Create `01.6-parallel-concepts.md` with:

- 3 concept briefs
- Comparison table
- Rejected patterns
- Recommended direction
- Why this direction wins
- What must be validated next

## Next Step

- 사용자가 결정할 것: 컨셉 A/B/C 중 direction lock — 비교표와 대표 시각물만 보고 결정 가능해야 하며, 구분이 안 되면 컨셉을 다시 구체화한다.
- Use `product-blueprint:screen-contract` to define what each priority screen must and must not do.
- Then use `product-blueprint:experience-mechanisms` for hidden system behavior and `product-blueprint:prd` for requirements.
