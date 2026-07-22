---
name: orchestrate
description: End-to-end product planning orchestration from an early idea through research, concept and brand direction, PRD, cross-functional review, product definition, screen and service contracts, flows, and a design handoff brief. Stops before visual UI production unless the user explicitly starts design-production.
---

# Product Blueprint Orchestrator

Turn an early product idea into a reviewed planning package that a designer and an engineer can understand. This is the default entry point.

The default finish line is **planning complete**, not “the product is designed.” High-fidelity UI, component styling, rendered screens, and clickable prototypes belong to the separate `product-blueprint:design-production` workflow and begin only after the user explicitly asks to continue.

## Choose the depth

| Mode | Use when | Planning finish line |
| --- | --- | --- |
| Lite | The user wants a fast direction check | Compact concept, working brand direction, PRD, critical flows, design brief |
| Standard | Default for a real product | Evidence-backed concept, reviewed PRD, complete P0 contracts and design brief |
| Deep | The product is novel, regulated, expensive, or high-risk | Broader evidence, failure and policy coverage, deeper feasibility and risk review |

If the user does not choose, use Standard. Record the mode in the decision log and service manifest.

## What this workflow owns

- product problem, target users, core loop, differentiation, and scope
- positioning, working name, brand voice, and brand principles
- product mechanisms and trust behavior
- PRD, non-goals, success signals, and open questions
- screen purposes, entry points, flows, states, and recovery behavior
- product-level service responsibilities and feasibility constraints
- a concise brief that lets visual design start without reopening every planning document

It does not claim to produce final visual quality, a production design system, or an implementation-ready application.

## User decisions that cannot be self-approved

Ask for explicit user confirmation at these four boundaries:

1. **Product direction** — the selected concept and why it wins.
2. **Brand direction** — positioning, voice, naming direction, and what to avoid.
3. **First-version scope** — the included loop, excluded work, and accepted limitations.
4. **Product definition** — personas, mental models, entry points, journeys, and required outcomes.

Record each decision in `00-decision-log.md`. Also record it in `00-workflow-state.json` with `scripts/workflow_state.py confirm`. A prose claim or agent-authored `explicit-user` string without matching conversation evidence and user history does not satisfy the gate. Do not hide decisions behind internal terms such as “lock” in user-facing summaries.

## Planning sequence

### 0. Create or resume the workspace

Run:

```bash
python3 scripts/init_prd_project.py "<product name>" --root <planning-root>
```

Use `--lite` or `--deep` only when the chosen mode differs from Standard. Resume existing artifacts without overwriting them. On every resume, inspect state before choosing a skill:

```bash
python3 scripts/workflow_state.py status <planning-dir> --json
```

Route from `next_gate`; do not infer progress from the largest or newest Markdown file. If status reports `validation-stale`, rerun the validator, identify the earliest changed decision, and invalidate from that gate before continuing. The validator regenerates `00-review-dashboard.html`, so do not hand-author readiness badges in it.

#### Lite compact branch

For Lite, do not run the Standard artifact sequence below and do not add design-production scaffolds. Keep the seven-file scaffold compact:

1. Fill `00-brief.md` and capture evidence or clearly labeled assumptions in `01-lite-direction.md`.
2. Compare product directions, obtain the user's product-direction confirmation, then define and confirm the brand direction in the same compact direction file.
3. Write `02-lite-plan.md` with the first-version loop, exclusions, user/job, entry points, critical screens/actions/states, service responsibility, risks, and acceptance outcomes.
4. Obtain separate explicit confirmations for first-version scope and the user-language product definition; record all four planning gates with `workflow_state.py`.
5. Bring `02.6-service-manifest.json` and `03-design-brief.md` in line with the compact plan.
6. Run `--stage planning`. Report `lite-planning-pass` only as a compact planning result. Lite cannot enter visual-direction, prototype, design, or handoff stages; upgrade to Standard first.

For Standard and Deep, continue with the full sequence below.

### 1. Clarify the brief

Fill `00-brief.md` with the idea, intended user, core job, constraints, references, known facts, assumptions, and unanswered questions. Label evidence as observed, user-confirmed, proposed, assumed, or unverified.

### 2. Build product evidence

- With named references, use `product-blueprint:research` and `product-blueprint:reference-deconstruction`.
- Without useful references, use `product-blueprint:ideation`.
- Never present inferred target-user needs as research findings.

### 3. Compare product directions

Use `product-blueprint:parallel-concepts` to compare meaningfully different product concepts, not cosmetic variants. Show the recommendation and tradeoffs. Continue only after the user confirms a product direction. Append the decision log and run `workflow_state.py confirm --gate product-direction` with the actual conversation reference.

### 4. Establish the brand direction

Use `product-blueprint:positioning-brand`. Define positioning, voice, naming direction, and brand principles. Availability checks are signals, not trademark clearance. Continue only after the user confirms the direction; a working name is acceptable. Record it with `workflow_state.py confirm --gate brand-direction`.

### 5. Define product mechanisms and draft the PRD

Use `product-blueprint:experience-mechanisms` for memory, ranking, generation, missions, rewards, moderation, or other behavior that cannot be explained as a simple screen. Then use `product-blueprint:prd`.

The PRD must include the first-version loop, user stories, feature and surface scope, explicit non-goals, states and entry points, success signals, and unresolved questions.

### 6. Run the planning review

Use `product-blueprint:planning-quality-gate`. It reviews the plan through six evidence-linked lenses: product strategy, user evidence, brand, PRD quality, service feasibility, and growth/risk. When one agent runs all six, call them review perspectives rather than independent reviewers. Standard and Deep cannot pass without a substantive research or ideation artifact bound into the review JSON, and each lens records its own evidence references.

Resolve all critical and major findings. Present the recommended first-version scope in plain language, then continue only after explicit user confirmation.

### 7. Confirm the product definition

Use `product-blueprint:product-definition`. Confirm personas, mental models, entry points, journeys, required outcomes, exceptions, and priorities. This is the canonical product contract from which screens are derived.

### 8. Define screens, service behavior, and feasibility

Run, in order:

1. `product-blueprint:screen-contract`
2. `product-blueprint:service-contract`
3. `product-blueprint:feasibility-review` as an early product feasibility checkpoint
4. coverage self-audit into `02.8-undefined-surfaces.md`

Validate the contract:

```bash
python3 scripts/validate_service_blueprint.py <planning-dir> --stage contract
```

Fix errors before proceeding. The validator checks consistency; it does not replace user judgment.

### 9. Map the experience without designing pixels

Use `product-blueprint:storyboard` to show P0 journeys, navigation, overlays, states, and recovery paths. Treat it as a low-fidelity behavior board. Do not use this phase to claim a visual direction or final UI quality.

In Standard and Deep, use `product-blueprint:backend-systems-brief` to record product-visible system responsibilities. Keep it compact and mark inapplicable concerns with reasons for simple products; expand it for persistence, permissions, ranking, generation, payment, or moderation behavior. Lite may omit it when those concerns are genuinely absent.

### 10. Create the design handoff brief

Use `product-blueprint:design-brief` to create `03-design-brief.md`. It must summarize what visual design may explore and what product behavior must not change silently.

Validate the planning package:

```bash
python3 scripts/validate_service_blueprint.py <planning-dir> --stage planning
```

The validator writes `00-validation-report.{json,md}` and regenerates the dashboard from current state and findings. Then stop. Report **planning structure passed** only when it returns `planning-structure-pass` and all required user decisions are recorded. This is not a claim that market demand or planning quality has been proven.

## Optional continuation: visual design and prototype

If the user explicitly asks for UI design, screens, or a prototype, start `product-blueprint:design-production`. Do not silently continue into it.

Record a separate `design-entry` user gate. That workflow first compares two or three visual directions, validates `--stage visual-direction`, applies the chosen direction to one representative screen through `key-screen-exploration`, validates `--stage key-screen`, and only then expands to the full screen set and prototype.

## Quality rules

- Prefer a useful decision over a large volume of prose.
- Keep user-facing language plain; put schemas, hashes, severity codes, and validator mechanics in technical documentation.
- A complete file is not the same as a confirmed decision.
- A storyboard is not visual design.
- A generated screen is not an accepted design.
- If visual exploration reveals a product change, return to the affected planning artifact and reconfirm it.
- Use `workflow_state.py invalidate --from-gate ...` when an upstream artifact or decision changes; never refresh downstream hashes as a substitute for re-review.
- Do not claim target-user validation without real target-user evidence.
- Do not claim trademark clearance from search signals.
- Do not claim technical or implementation readiness; those require a later project-specific workflow.

## Planning outputs

The default workflow produces:

- a product and audience brief
- concept and brand direction
- PRD and cross-functional review
- confirmed product definition
- screen, service, state, and flow contracts
- feasibility and unresolved-surface notes
- a low-fidelity storyboard
- `03-design-brief.md`
- a review dashboard and decision log

Visual tokens, polished screens, React workbenches, screenshots, prototypes, design acceptance, and engineering handoff are optional design-production outputs, not default planning outputs.
