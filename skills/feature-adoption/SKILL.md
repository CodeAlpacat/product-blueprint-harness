---
name: feature-adoption
description: Deep-analyzes an existing codebase the founder already owns (a sibling product, a previous app) and maps every user-facing feature to adopt / adapt / reject decisions for the new product, including backend reuse candidates. Use when the user says "we already have X, see what's worth taking" before tech planning.
---

# Feature Adoption — mine the existing asset before building new

A founder with a mature codebase owns validated features the new plan silently forgets. Mining it changed a dogfood project's screen set and tech plan in material ways. Do this BEFORE tech-plan; feed screen deltas back into contracts/demo.

## 1. Three-axis parallel inventory (fresh subagents, feature level — not code review)

Sweep with separate explorers so each is exhaustive:
- **Core-domain internals** (e.g., in-chat features): every user-visible action, setting, and system surface.
- **Creation/authoring environment**: funnels, AI assists, publishing.
- **Platform/consumption**: discovery, search, library, social, notifications, billing, safety, auth.

Each item: name — what it does (1 line) | UI surface | file evidence path | deprecated flag. Also collect what the source product LACKS — its gaps are the new product's edge.

## 2. Adoption map (`07-feature-adoption.md`)

Per feature, verdict with reason:
- **P0 adopt (adapted)** — feeds the screen contracts and service manifest NOW (name the surface/action/operation delta).
- **P1 adopt** — contract anchor only.
- **Reject** — including features the source itself deprecated (do not inherit sunk costs) and features that conflict with the new product's identity/philosophy.
- Rewrite jargon into the new product's voice; never copy surface labels verbatim.

## 3. Reuse verdict for tech-plan (the transplant criteria)

"Reuse" is not one thing. Judge per domain with two criteria:
1. **Money/legal correctness with production mileage → transplant** (ledger, payments, identity verification, moderation): rewriting resets validation.
2. **High coupling + simpler requirements in the new product → reference-rewrite** (take the schema, edge-case list, and hook structure; write fresh): the surgery to detach exceeds rewriting, and forks drift.
Everything product-identity-specific is **new**. State fork-drift as a named cost of any transplant.

Before the next step, run `product-blueprint:service-contract` so adopted, adapted, rejected, and deferred surfaces do not live only in this report.

## Next Step

- 다음 추천: 화면 델타를 `product-blueprint:screen-contract`/`service-contract`/`clickable-demo`에 반영 → `product-blueprint:tech-plan`(§3 표를 이식/재작성 근거로 사용).
- 사용자가 결정할 것: 채택/제외 이견, 이식 범위(돈·법 영역 확인).
