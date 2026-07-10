---
name: risk-register
description: Policy, legal, safety, and abuse risk register with concrete P0 mitigations, gated before engineering handoff. Mandatory when the product touches adult content, minors, payments, UGC, personal data, or AI-generated content. Use when the user asks about legal risk, policy risk, content moderation, or compliance readiness.
---

# Risk Register — the reviewer who reads it before launch

A product that touches adult content, payments, minors, UGC, PII, or AI generation has launch-blocking risk that no amount of visual polish fixes. This skill produces the register a legal/policy reviewer would demand — as a planning artifact with product-level mitigations, NOT legal advice (say so in the artifact; real counsel reviews before launch).

## Inputs

- `02-prd.md`, `02-mechanisms.md`, `02.5-screen-contracts.md`, `04.2-backend-systems-brief.md`, target market/jurisdiction from the brief

## Output

`04.55-risk-register.md`. Gate: engineering handoff is NOT ready while any P0 risk row has no mitigation.

## The register

One table, sorted by severity: risk | trigger surface (screen/mechanism) | jurisdiction note | P0 mitigation (what the PRODUCT does, structurally) | owner decision needed | status.

Sweep at minimum these categories (mark n.a. explicitly when they don't apply — an unexamined category is a gap, an n.a. is a decision):

1. **Age & content rating**: adult-content gating (verification strength — birth-date input alone is not verification), store rating implications, minor-protection rules in the target market.
2. **Personal data**: what is collected, where it flows (name third-party processors and their countries — cross-border transfer often requires disclosure), retention/deletion promise, verification-data disposal.
3. **Payments & virtual currency**: refund rules, disclosure before charge, subscription/renewal notice rules, virtual-currency accounting.
4. **UGC & moderation**: report/block, illegal-content handling, creator IP, impersonation of real people.
5. **AI-generated content**: disclosure obligations, likeness/IP of training-adjacent styles, hallucinated claims about real entities, AI-companion-specific rules where emerging.
6. **Platform policy**: app-store content policies for the category (often stricter than law), account deletion requirements.
7. **Accessibility & consumer law**: baseline a11y exposure, dark-pattern rules (forced continuity, hidden costs).

## Rules

- Mitigations must be structural where possible (the gate/flow makes violation impossible) rather than reactive (moderation cleans up later) — mirror the product's forbidden-shortcuts style.
- Distinguish 관찰 (regulation text/precedent found) from 가정 (our reading). Cite sources for 관찰.
- Do not soften findings to keep the plan pretty. A red row before handoff is the artifact working.

## Next Step

- 다음 추천: `product-blueprint:feasibility-review` → `product-blueprint:engineering-handoff` (P0 행 전부 mitigation 확보 후).
- 사용자가 결정할 것: 각 P0 리스크의 mitigation 채택 / 전문가(법무) 검토 시점.
