---
name: design-acceptance
description: >-
  Runs the final iterative product-design review and freezes an explicitly user-approved implementation
  baseline. Verifies every P0 surface, release viewport, required state, component contract, mental-model
  journey, review finding, and source hash. Use after the clickable demo, prototype test, design critique,
  risk/feasibility review, and coverage audit; after user design feedback; or before engineering handoff
  and technical planning.
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
4. Run the design-stage validator while approval is pending. Fix deterministic coverage/staleness failures first.
5. Present the complete clickable service, dashboard, evidence matrix, and known limitations to the user. Do not ask them to infer missing screens from prose.
6. Record feedback as stable findings with category, severity, evidence, resolution owner, and decision ref.
7. Route findings to the earliest owning artifact. Regenerate every invalidated downstream artifact and evidence item.
8. Repeat for as many user-requested rounds as needed. Never use an autonomous retry cap to force acceptance.
9. P0 mental-model, flow, surface, responsive, visual, copy, or accessibility findings must be resolved. They cannot pass through ACCEPT-FLAG or deferral.
10. Only after the user explicitly approves the current all-P0 result, write `status: user-approved`, approval evidence, and current hashes. The agent cannot self-approve.
11. Run the design stage again. A real `design-pass` is the scope-freeze boundary.

## Mental-model review

For every persona and included P0 requirement, record the journeys walked and the observed outcome. Founder approval and heuristic walkthrough remain separate from target-user validation. Use `real-user` only with actual target-user evidence.

## Change discipline

Any accepted source change invalidates acceptance, handoff, and technical planning. Keep the old evidence as review history if useful, but never preserve its passing status or hashes.

## Next step

After `design-pass`, create the product handoff. In a build-ready run, create the technical plan from this exact baseline and run the technical stage.

