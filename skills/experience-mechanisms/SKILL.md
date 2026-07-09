---
name: experience-mechanisms
description: Defines product-experience mechanisms before technical architecture, such as long-term memory, mission judging, scoring, recommendations, ranking, personalization, safety gates, and creator tools. Use when a feature needs believable system behavior, user trust, fairness, transparency, or product completeness before storyboard/design/engineering decisions.
---

# Product Blueprint Experience Mechanisms

Use this between research/ideation and storyboard. The goal is not to choose the implementation. The goal is to define the product promise, user-facing behavior, trust boundaries, and later feasibility questions.

## Intent Before Mechanism

Before writing a mechanism contract, restate the feature in concrete user behavior:

- Trigger: when the user invokes it.
- Input: what object or state it acts on.
- Output: what new object, state, or visible result appears.
- Scope: whether it is Core P0, P0 support, P1 differentiator, P2 expansion, or out of scope.
- User wording: the label the user would understand.

If the feature name is ambiguous, ask or mark it as unconfirmed. Do not infer the mechanism from the name alone.

Examples:

- `checkpoint` is not automatically a save/branch system. It may mean "copy this chat room from turn N into a new chat room."
- `memory` is not automatically a main tab. It may be hidden recall with a review/correction surface.
- `persona` is not automatically a relationship contract. It may be a simple chat-entry identity setup.

## Mechanism Contract

For each product-defining mechanism, write:

1. **User promise**: what the user believes the system can do.
2. **Terminology mapping**: internal planning name, user-facing label, and user-confirmed wording.
3. **Moment of use**: where the mechanism affects the journey.
4. **Default visibility**: background, inline, side panel, settings, modal, dedicated screen, or primary navigation.
5. **Inputs**: what signals the product may use, in product language.
6. **Outputs**: what the user sees or receives.
7. **User controls**: inspect, edit, retry, hide, reset, override, report.
8. **Transparency**: how the product explains why something happened.
9. **Failure modes**: wrong, missing, delayed, unfair, unsafe, too expensive.
10. **Recovery UX**: what the user can do when it fails.
11. **Acceptance examples**: sample scenarios that prove the experience.
12. **Feasibility questions**: questions for engineering later, without preselecting architecture.
13. **Scope decision**: Core P0, P0 support, P1 differentiator, P2 expansion, or out of scope.
14. **Evidence status**: observed, user-confirmed, proposed, assumed, or unverified.

## Surface Discipline

Product-critical does not mean main-screen-visible.

- Separate system behavior from UI surface. A mechanism can be important while staying mostly invisible.
- Do not create a tab, card, panel, or main-screen block for a mechanism unless the moment of use requires user inspection, correction, confirmation, or recovery.
- If the user has clarified that two terms are the same concept, preserve that mapping. For example, a relationship setup may simply be part of persona; do not split it into a separate feature unless approved.
- Persona/setup is normally an entry gate between character detail and chat room. Do not promote it to home, bottom navigation, or primary navigation. If reusable persona management is needed, treat it as secondary account/settings management, not the core product path.
- For long-term memory, remember that the source is usually change during chat. Default to background behavior plus user-accessible review/correction surfaces, not permanent main-screen exposure.
- If surface level is uncertain, write the alternatives and ask before screen contracts.
- If scope is uncertain, keep it out of P0 until the user confirms it belongs in the first usable loop.

## Common Mechanisms

Use `references/mechanism-patterns.md` for examples covering:

- Long-term memory
- Mission judging
- Recommendation and next-message suggestions
- Relationship/route state
- Ranking and scoring
- Creator publishing and validation
- Paid actions and cost trust

## Rules

- Do not write database tables, model choices, queues, vector stores, or exact algorithms here.
- Do define what must be true for users to trust the feature.
- Separate product non-negotiables from negotiable implementation ideas.
- If a mechanism cannot be explained to the user, mark it as a trust risk.
- If the mechanism affects money, rankings, age gates, safety, or creator reputation, add explicit audit and appeal/recovery UX.

## Output

Create `02-mechanisms.md` or add a `Product Mechanisms` section to the PRD. Every major storyboard frame should point back to at least one mechanism contract when its behavior depends on hidden system judgment.

## Next Step

- Use `product-blueprint:prd` if product requirements are not yet written.
- Use `product-blueprint:screen-contract` once the MVP scope and priority screens are clear.
