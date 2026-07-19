# Product Blueprint Quality Bar

Use this to judge whether the plugin output is industry-usable.

## Not Enough

- It has a PRD but no evidence.
- It makes product-direction, safety, monetization, design, or handoff decisions without asking the user.
- It carries assumptions without writing them down.
- It has screenshots but no mental model.
- It copies reference visuals without deconstructing product logic, gates, states, and trust surfaces.
- It locks into one concept without comparing alternatives.
- It draws screens before defining what each screen is allowed and forbidden to do.
- It has screens but no product mechanism contracts.
- It has UI polish but unresolved user trust questions.
- It has art direction words but no product world, anti-aesthetic, image rules, or signature element.
- It claims production design while still looking like a generic AI mockup.
- It has design tokens that are not visible in components, state examples, or production screen mockups.
- It uses a convenience HTML storyboard as if it were production-grade UI.
- It approves a React-looking screen whose component board and product screens use different source implementations.
- It produces one polished screen while the service's design system, state lab, and P0 surfaces remain abstract.
- It leaves the user to ask for obvious missing surfaces, components, or states one by one.
- It converts an unstable planning board into React before the screen contracts and P0 surface list are coherent.
- It claims the prototype works without task-based prototype testing.
- It skips structured critique or treats critique as taste feedback.
- It jumps from storyboard to DB/API design.
- It treats technical architecture as part of the default planning workflow instead of a post-handoff follow-up.
- It skips backend/system responsibilities for memory, judging, ranking, permissions, billing, safety, or creator publishing.
- It hides unverified reference flows.
- It treats AI behavior as magic: "AI remembers", "AI judges", "AI recommends" without inputs, outputs, controls, and failure UX.

## Usable Standard

- Every major feature has a user promise and a core loop.
- User decisions, assumptions, gate status, and next recommended skill are recorded in `00-decision-log.md` or the phase artifact.
- Reference claims point to screenshots or are labeled assumptions.
- Reference deconstruction extracts product principles and anti-copy rules.
- Parallel concepts compare at least two viable directions before convergence, unless explicitly timeboxed.
- Product-defining mechanisms are described before UI polish.
- Priority screens have contracts: purpose, allowed actions, forbidden shortcuts, entry/exit paths, and states.
- Storyboards show entry points, states, transitions, and unverified gaps.
- Art direction defines a product-specific visual thesis before high-fidelity UI.
- Visual quality gate checks reference fidelity, AI-slop signals, state coverage, and mechanism visibility before production design is accepted.
- Design system follows approved product behavior and has a named art direction tied to the audience and product loop.
- A dependency-light React workbench renders ComponentBoard, DepthBoard, FlowPreview, token modes, state lab, and every P0 surface from shared sources.
- One high-risk screen may receive an additional React high-fidelity specimen after the workbench, but it is not a substitute for the workbench.
- Backend systems brief states product-level responsibilities, data categories, lifecycle, permissions, and high-risk invariants without deciding schema or API.
- Prototype testing uses concrete tasks and screenshots to verify comprehension and flow gates.
- Design critique reports product/UX/visual/system issues by severity before feasibility review.
- Feasibility review separates product intent from implementation tradeoffs.
- Engineering handoff gives developers the product intent, non-negotiables, mechanism contracts, backend/system invariants, tradeoffs, scope-out candidates, and technical design questions.
- Technical planning begins only after explicit approval to continue beyond product planning.

## Mechanism Gate

Before storyboard/design, ask:

- What invisible judgment or memory does the product rely on?
- What will users see when it works?
- What will users see when it fails?
- Can users inspect, correct, retry, or appeal?
- Is money, ranking, safety, or creator reputation affected?
- What must engineering later validate without deciding it now?

## Design Gate

Before production-grade visual design, ask:

- What is this screen's single job?
- What action must be forbidden on this screen?
- What reference principle are we using, and what are we refusing to copy?
- Which concept did we choose, and why did it beat the alternatives?
- What product world and signature element make the design specific?
- What task will prove the prototype works?
- Which P0 surfaces must appear in the React design-system workbench?
- Which components and states must be visible before the team discusses implementation?
- Which one screen, if any, deserves an extra pixel-level React pass after the workbench?

## Conversation Gate

Before moving to the next phase, ask:

- Is this a reversible assumption or a product decision?
- Does this affect scope, safety, monetization, visual direction, or handoff readiness?
- Is user approval needed before proceeding?
- If proceeding without approval, where is the assumption recorded?
