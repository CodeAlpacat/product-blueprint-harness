---
name: feasibility-review
description: Facilitates product-design-backend-to-engineering feasibility review without prematurely locking technical architecture. Use after PRD, mechanisms, storyboard, backend systems brief, and design direction when the team needs to identify feasibility risks, tradeoffs, scope-outs, staged compromises, or technical questions before implementation planning.
---

# Product Blueprint Feasibility Review

Two modes. Both protect product intent while making hard tradeoffs visible.

## Mode A — Feasibility Checkpoint (lightweight, BEFORE visual design)

Run right after screen contracts, before the storyboard renders anything. This is the "engineer in the room" moment — it prevents mockups from promising the impossible, which is far cheaper than reconciling after screens are polished.

1. List every mechanism and operation that a P0 surface/action depends on (from `02.6-service-manifest.json` × `02-mechanisms.md`). Preserve the exact surface/action/operation IDs.
2. Give each a one-line verdict with the frontend/backend/AI lens: **feasible** / **conditional** (state the condition and rough cost driver) / **infeasible as specified** (state the closest feasible version).
3. `infeasible` or expensive-`conditional` verdicts go to the user BEFORE that screen is storyboarded — offer staged alternatives, never silently downgrade.
4. Output `02.7-feasibility-checkpoint.md`: mechanism/operation ID | depending surface/action IDs | verdict | condition/alternative | user decision needed. Keep it under a page — this is a checkpoint, not the full review.

## Mode B — Full Feasibility Review (before handoff)

Use after product/design artifacts exist and before engineering handoff. This is a meeting-prep artifact for product, design, and engineering. Reconcile against the Mode A verdicts: any screen that shipped visuals against a `conditional` verdict must show the condition was addressed.

## Review Inputs

- PRD
- Experience mechanism contracts
- Storyboard
- Backend systems brief
- Design-system direction
- Verified and unverified reference flows
- Current `02.6-service-manifest.json`

## Workflow

1. List product outcomes that must survive implementation.
2. List mechanisms that require engineering feasibility review.
3. For each mechanism, define:
   - product non-negotiable
   - negotiable experience detail
   - likely technical uncertainty
   - possible staged versions
   - explicit scope-out option
   - user-facing consequence of compromise
4. Identify decisions that need engineering input, legal/safety input, or user validation.
5. Produce a decision log with owner, deadline, and evidence needed.

## Rules

- Do not silently downgrade the product to what is easy to build.
- Do not force one architecture before engineering review.
- Do not treat unresolved feasibility as a reason to erase the user experience requirement.
- Distinguish `must-have for MVP`, `can be approximated`, `needs experiment`, and `scope out`.
- A changed verdict updates the affected manifest operation, exclusion, or accepted limitation in the same phase; do not leave feasibility and the service contract disagreeing.

## Output

Create `04.5-feasibility-review.md` with:

- Product non-negotiables
- Mechanism risk table
- Tradeoff options
- Scope-out candidates
- Questions for engineering/design/product
- Decision log

Then use `product-blueprint:engineering-handoff` for the approved pre-development package. Use `product-blueprint:tech-plan` only if the user explicitly asks to proceed into technical architecture.

## Next Step

- 사용자가 결정할 것: infeasible/conditional 판정 메커니즘의 staged 대안 채택 또는 scope-out.
- Use `product-blueprint:engineering-handoff` when tradeoffs and unresolved questions are documented.
