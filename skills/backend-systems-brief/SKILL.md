---
name: backend-systems-brief
description: Creates a product-level backend and systems brief that gives designers the constraints needed to finalize flows without deciding schema, APIs, or implementation. Use during product/design definition when the experience depends on memory, judging, ranking, billing, moderation, permissions, publishing, safety, analytics, or other system behavior.
---

# Product Blueprint Backend Systems Brief

Use this inside product/design definition. It is not a DB/API design. It exposes system behavior and failure boundaries that the user experience must represent before approval.

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
- `02.6-service-manifest.json` actions and operations
- Storyboard flows
- Feasibility checkpoint verdicts (`02.7-feasibility-checkpoint.md`) — carry them forward; do not re-litigate settled verdicts
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

## Operation Contract Matrix (required)

For every P0 read/write/destructive/external action in the service manifest, fill the operation row in product language:

- owner and source of truth
- input/output user promise
- authorization and persistence
- idempotency, consistency, and conflict strategy
- failure and recovery
- audit/retention, latency/cost, observability, and abuse boundary

Use `n/a:<reason>` when inapplicable. Use `decision-needed:<id>` only for a real blocker; readiness will fail until it is resolved. Keep endpoints, tables, providers, queues, and framework choices out of this artifact.

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
- Scope-out and staged experience options
- Operation matrix keyed by the exact IDs in `02.6-service-manifest.json`; update the manifest in the same change

Use `references/backend-brief-checklist.md` for detailed prompts.

## Next Step

- Use `product-blueprint:feasibility-review` in checkpoint mode if backend/system risks still need a product tradeoff.
- Then use `product-blueprint:design-brief` to carry product-visible constraints into the planning handoff.
- Visual system work starts later through `product-blueprint:design-production` only when the user requests it.
