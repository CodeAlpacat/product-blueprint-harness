---
name: design-acceptance
description: >-
  Runs the final iterative product-design review and freezes an explicitly user-approved design baseline.
  Verifies every P0 surface, release viewport, required state, component contract, mental-model journey,
  developer-lens feasibility check, absorbed constraint, review finding, and source hash. Use after the
  clickable demo, prototype test, design critique, risk/feasibility review, and coverage audit; after user
  design feedback; or before the product/design handoff.
---

# Design Acceptance

Create and maintain `05-design-acceptance.json`. Read `references/design-acceptance.md` and start from `assets/templates/design-acceptance.json`.

## Hard prerequisites

- user-confirmed product definition and passing contract stage;
- passing browser runtime report for the whole-service demo;
- all-P0 workbench/demo, required states, responsive evidence, UX copy, critique, risk/feasibility, and undefined-surface audit;
- no unmitigated P0 product/safety finding.

## Review loop

1. Build the component contract inventory from the design system/workbench.
2. Capture one current, readable image artifact for every non-background P0 surface × release viewport. Each row lists all required state IDs and component IDs visible in that viewport contract.
3. Hash every bound product/design source and every visual evidence file.
4. Import the final developer-lens consultation from `04.5-feasibility-review.md`. Cover every P0 surface/action/operation/journey with the required lens and one verdict: `feasible`, `feasible-with-constraint`, or `infeasible`.
5. Block on `infeasible`. For every conditional constraint, revise the product/design artifact that owns the user-visible consequence, then regenerate prototype and visual evidence.
6. Run the design-stage validator while approval is pending. Fix deterministic coverage/staleness failures first.
7. Present the complete clickable service, dashboard, evidence matrix, absorbed feasibility constraints, and known limitations to the user. Do not ask them to infer missing screens from prose.
8. Record feedback as stable findings with category, severity, evidence, resolution owner, and decision ref.
9. Route findings to the earliest owning artifact. Regenerate every invalidated downstream artifact and evidence item.
10. Repeat for as many user-requested rounds as needed. Never use an autonomous retry cap to force acceptance.
11. P0 mental-model, flow, surface, responsive, visual, copy, accessibility, or feasibility findings must be resolved. They cannot pass through ACCEPT-FLAG or deferral.
12. Only after the user explicitly approves the current all-P0 result, write `status: user-approved`, approval evidence, all current `feasibility_check_ids`, their canonical `feasibility_sha256` (the pending validator finding prints the expected value), and current source hashes. The agent cannot self-approve.
13. Run the design stage again. A real `design-pass` is the scope-freeze boundary.

## Mental-model review

For every persona and included P0 requirement, record the journeys walked and the observed outcome. Founder approval and heuristic walkthrough remain separate from target-user validation. Use `real-user` only with actual target-user evidence.

## Change discipline

Any accepted source or feasibility change invalidates acceptance and handoff. Keep the old evidence as review history if useful, but never preserve its passing status or hashes.

## Next step

After `design-pass`, create the product/design handoff and stop by default. A separate technical-design workflow begins only when the user explicitly asks for it.
