---
name: backend-systems-brief
description: Creates a pre-architecture backend and systems brief from product mechanisms without deciding schema, APIs, or implementation. Use before technical design when the product depends on memory, judging, ranking, billing, moderation, permissions, creator publishing, safety, analytics, or other server-side/system behavior.
---

# Product Blueprint Backend Systems Brief

Use this before technical architecture. It is not a DB/API design. It prepares backend engineers to evaluate product-critical system behavior.

## Output Language And Stage Exit

- Default to the user's conversation language.
- If the user is Korean, write the backend systems brief in Korean. Keep domain entity names, API-like labels, and skill names in English only when useful.
- End with:
  1. `지금 확인할 산출물`
  2. `사용자가 결정할 것`
  3. `수정이 필요하면 어디를 바꿀지`
  4. `다음 추천 스킬`

## Inputs

- Product mechanisms
- PRD requirements
- Storyboard flows
- Feasibility review
- Monetization, safety, creator, and result-state requirements

## Brief Sections

1. **System responsibilities in product language**
   - What must the system make true for users?
2. **Trust-critical mechanisms**
   - Memory, mission judging, scoring, ranking, paid actions, moderation, creator validation.
3. **Data categories**
   - User-visible data, hidden system evidence, audit data, user-editable data, sensitive data, disposable data.
4. **Lifecycle**
   - Create, update, summarize, judge, publish, archive, delete, recover, appeal.
5. **Permissions and boundaries**
   - User, creator, moderator, admin, public/private, safe/unsafe, age-gated.
6. **Failure and dispute handling**
   - Wrong memory, unfair mission result, failed paid generation, ranking abuse, unsafe content.
7. **Operational questions**
   - Cost, latency, observability, audit, abuse prevention, data retention, rollback.
8. **Engineering decisions later**
   - Questions for architecture, not decisions.

## Rules

- Do not write tables, columns, endpoints, queues, cron jobs, model providers, or storage choices.
- Do define product invariants backend must preserve.
- Include user-facing consequences of backend compromise.
- Treat billing, ranking, judging, permissions, deletion, and safety as high-risk by default.

## Output

Create `04.2-backend-systems-brief.md` with:

- Product-level system responsibilities
- Mechanism-by-mechanism backend questions
- Data category map
- Permission and lifecycle map
- High-risk invariants
- Scope-out and staged implementation questions

Use `references/backend-brief-checklist.md` for detailed prompts.

## Next Step

- Use `product-blueprint:design-system` if visual direction is ready.
- Use `product-blueprint:feasibility-review` if backend/system risks need tradeoff discussion before more design work.
