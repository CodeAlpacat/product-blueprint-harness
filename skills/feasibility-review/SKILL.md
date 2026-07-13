---
name: feasibility-review
description: Brings a developer lens into product/design decisions without turning the work into implementation planning. Use before visual design and again before final design acceptance to decide whether promised behaviors are feasible, which product-visible constraints the design must absorb, and which flows must be redesigned or scoped out.
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

Use after product/design artifacts exist and before final design acceptance. This is a product/design consultation with an engineer in the room, not a tech spec. Reconcile against Mode A: any screen rendered against a conditional verdict must show the condition in the current user flow, state, copy, or limitation.

## Review Inputs

- PRD
- Experience mechanism contracts
- Storyboard
- Backend systems brief
- Design-system direction
- Verified and unverified reference flows
- Current `02.6-service-manifest.json`

## Workflow

1. Enumerate every P0 surface, action, operation, and journey by its stable service-manifest ID.
2. Review each through the required developer lens: surface=`frontend`+`accessibility`, action=`frontend` (+`backend` when it invokes an operation), operation=`backend`, journey=`platform`.
3. Give each row a final verdict: `feasible`, `feasible-with-constraint`, or `infeasible`.
4. State only product-visible constraints: latency, failure/retry, persistence/lifecycle, permission, platform capability, accessibility, safety, or material cost. Do not choose endpoints, tables, component architecture, state libraries, migrations, or rollout.
5. For `feasible-with-constraint`, identify the earliest product/design owner and the exact evidence that must be regenerated. For `infeasible`, offer a closest feasible experience and block approval.
6. Route constraints back into PRD/screen/service contract/storyboard/copy/design/demo as appropriate. Rerun the prototype and visual proof.
7. Write the final rows into `05-design-acceptance.json.feasibility_checks`; user approval happens only after these rows and regenerated evidence are current.

## Rules

- Do not silently downgrade the product to what is easy to build.
- Do not force one architecture before engineering review.
- Do not let technical convenience redefine the user's mental model. The consultation changes design only when a real platform/product constraint demands it.
- Do not treat unresolved feasibility as a reason to erase the user experience requirement.
- Distinguish `must-have for MVP`, `can be approximated`, `needs experiment`, and `scope out`.
- A changed verdict updates the affected contract, design, evidence, and approval state in the same phase; do not leave feasibility and the accepted experience disagreeing.

## Output

Create `04.5-feasibility-review.md` with:

- Product non-negotiables
- Mechanism risk table
- Tradeoff options
- Scope-out candidates
- Questions for engineering/design/product
- Decision log
- Stable-ID feasibility matrix and regenerated-evidence references

Then use `product-blueprint:design-acceptance`. Conditional constraints are not complete until the design evidence is regenerated and the user explicitly approves the revised whole.

## Next Step

- 사용자가 결정할 것: infeasible/conditional 판정 메커니즘의 staged 대안 채택 또는 scope-out.
- Use `product-blueprint:design-acceptance` after all infeasible rows are redesigned/scoped and all conditional rows are visibly absorbed.
