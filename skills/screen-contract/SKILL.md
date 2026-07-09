---
name: screen-contract
description: Defines the contract for each product screen before storyboard or high-fidelity design, including screen purpose, allowed actions, forbidden shortcuts, entry/exit paths, states, decision points, and required evidence. Use when planning a homepage, detail page, chat entry, mission page, settings panel, or any screen where UX flow accuracy matters.
---

# Product Blueprint Screen Contract

Use this before storyboard and before high-fidelity UI. It prevents attractive screens from breaking the product flow.

## Output Language And Stage Exit

- Default to the user's conversation language.
- If the user is Korean, write screen contracts in Korean. Keep product names, UI labels under evaluation, and skill names in English only when useful.
- End with:
  1. `지금 확인할 산출물`
  2. `사용자가 결정할 것`
  3. `수정이 필요하면 어디를 바꿀지`
  4. `다음 추천 스킬`

## Contract Fields

For each screen, define:

1. **Screen purpose**: One sentence. If there are two competing purposes, split the screen.
2. **User question**: What is the user trying to decide here?
3. **Allowed actions**: Actions that may be available on this screen.
4. **Forbidden shortcuts**: Actions that must not appear here, even if tempting.
5. **Entry paths**: How users arrive.
6. **Exit paths**: Where each action leads.
7. **Required content**: Data, copy, imagery, controls, disclaimers.
8. **Required states**: Empty, loading, locked, paid, unsafe, error, returning, success.
9. **Mechanism surfaces**: Memory, judging, ranking, personalization, cost, safety.
10. **Surface level**: main content, inline hint, bottom sheet, side panel, settings, modal, dedicated screen, or background-only.
11. **Acceptance checks**: How to tell if the screen is doing its job.

## Rules

- Do not design pixels yet.
- Before writing contracts, list the product category's expected baseline screens and mark included, excluded, or intentionally deferred. For discovery products, search is baseline unless scoped out.
- Do not let a screen do an action before the user has the information needed to consent.
- Do not put global `start` actions on discovery screens unless the product has no detail gate.
- Make forbidden shortcuts explicit; this is often what protects UX quality.
- Keep copy user-facing. Avoid implementation terms.
- Avoid internal planning jargon in user-facing UI copy. Translate concepts into words users already search or tap, such as character name, title, tag, trope, situation, or creator.
- Do not give every mechanism its own tab. A mechanism appears only at the surface level required by the user task.
- If a mechanism is background-only on this screen, say so explicitly and define where the user can inspect or recover it later.
- For character-chat products, preserve the entry sequence `character detail -> persona/setup -> chat room` unless explicitly changed. Persona/setup must not be a home-screen module, bottom-nav item, or primary navigation destination.
- On discovery/home screens, forbid direct chat and persona setup actions unless a character/detail context is already selected.
- On discovery-first home screens, do not make "resume/continue conversation" the main first-viewport module unless the user explicitly approves it. Returning conversations should default to a conversations/library surface, a bottom tab, or a character-detail secondary entry.
- If a required screen is listed in the PRD, it must receive a screen contract. Do not leave it as a nav label only.
- If a feature is P1 or later, do not include it as a P0 screen. Add a deferred contract only if it affects current decisions.

## Output

Create `02.5-screen-contracts.md` with:

- Screen inventory
- Contract per screen
- Entry/exit map
- State matrix
- Forbidden shortcut list
- Acceptance checks

## Next Step

- Use `product-blueprint:storyboard` to visualize the contracted screens and transitions.
- If the screen depends on hidden system behavior, use or update `product-blueprint:experience-mechanisms` before storyboarding.
