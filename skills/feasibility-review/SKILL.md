---
name: feasibility-review
description: Facilitates product-design-backend-to-engineering feasibility review without prematurely locking technical architecture. Use after PRD, mechanisms, storyboard, backend systems brief, and design direction when the team needs to identify feasibility risks, tradeoffs, scope-outs, staged compromises, or technical questions before implementation planning.
---

# Product Blueprint Feasibility Review

Use this after product/design artifacts exist and before engineering handoff. This is a meeting-prep artifact for product, design, and engineering. It should protect product intent while making hard tradeoffs visible.

## Review Inputs

- PRD
- Experience mechanism contracts
- Storyboard
- Backend systems brief
- Design-system direction
- Verified and unverified reference flows

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

- Use `product-blueprint:engineering-handoff` when tradeoffs and unresolved questions are documented.
