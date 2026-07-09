---
name: research
description: Deep product-reference research with browser exploration, screenshots, interaction tracing, and feature mental-model extraction. Use when the user provides a reference website/app, asks to benchmark competitors, capture screenshots, map flows, or understand how an existing product really works before planning.
---

# Product Blueprint Research

Use browser tools when a live service or reference URL exists. Screenshots are evidence, not the final storyboard.

## Workflow

1. Define research questions: target user, core loop, monetization, feature being studied, and actions that must not be executed without approval.
2. Explore from public entry to authenticated state when credentials are provided by the user.
3. Capture screenshots for each meaningful surface: home, search, detail, entry gate, workspace/chat, side panels, settings, empty states, modals, paid prompts, and result states.
4. Scroll and tab through each product-defining page. For detail pages, inspect top, lower content, tabs, sticky CTAs, action sheets, comments/community surfaces, and paid/support surfaces when safe.
5. Trace feature closure, not just entry. If the feature is a mission, editor, memory, ranking, search, persona gate, or paid loop, inspect the working surface and result state when safe.
6. Trace interactions until the feature's mental model is clear. For every feature, answer: what is the user trying to accomplish, what must they decide, what system state changes, and what risks appear?
7. Identify experience mechanisms behind the UI: memory, judging, scoring, personalization, recommendation, moderation, pricing, ranking, search, or creator validation.
8. Build an evidence log. Each claim must point to a screenshot, observed text, URL, DOM snapshot, or an explicit inference.
9. Mark unverified behavior. Do not hide gaps behind polished mockups.

## Live Exploration Rules

- Stop before paid, destructive, adult-gated, privacy-sensitive, publishing, or account-changing actions unless the user explicitly approves.
- If a flow requires payment or many turns, document the remaining unknown and design a follow-up research script.
- Revisit side panels and secondary tabs. Many product-defining features live outside the happy path.
- For scrollable reference pages, capture lower sections. If only the first viewport was inspected, label the page as partially explored.
- For discovery products, research search separately from home recommendations and category/ranking browsing.
- If a feature outcome depends on hidden system judgment, capture how the product explains or fails to explain that judgment.

## Output Contract

Produce `01-reference-research.md` with:

- Reference scope and account state
- Screenshot inventory
- Coverage table: page, top inspected, lower scroll inspected, tabs inspected, modal/sheet inspected, result/empty state inspected
- Feature map
- Core loops
- Screen-by-screen observations
- Interaction and state table
- Monetization moments
- Confusions, dead ends, and trust risks
- Opportunities for our product
- Product mechanism candidates
- Verified vs unverified flow list

Use `references/research-checklist.md` when the feature is complex.

## Next Step

- Use `product-blueprint:reference-deconstruction` to turn screenshots and observations into product principles, screen gates, and anti-copy rules.
- If no reference evidence was found, use `product-blueprint:ideation` instead.
