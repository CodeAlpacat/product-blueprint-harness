---
name: orchestrate
description: End-to-end pre-development product planning orchestration from vague idea and optional reference services to research, reference deconstruction, parallel concepts, positioning and brand naming, mechanism contracts, PRD, screen contracts, feasibility checkpoint, storyboard, art direction, visual quality gate, UX writing, backend systems brief, design system, workbench, high-fidelity screen, clickable demo, prototype test, design critique, risk register, feasibility review, and engineering handoff. Supports Lite/Standard/Deep modes and run-through pacing, and always ends each response with the recommended next step. Use when the user wants to plan a new product, structure an app idea, analyze references, run staged planning with expert agents, or create a product planning workflow before technical design and implementation.
---

# Product Blueprint Orchestrate

Use this as the master pre-development workflow. Do not start from screens, API, DB, architecture, or implementation. Turn a vague product idea into staged artifacts that a founder, designer, and engineer can review before technical design starts.

Read `references/pro-design-process.md` when the user asks why the workflow is staged this way or wants senior designer process guidance.

## How To Run — modes and effort (tell the user this up front)

When a run starts, state the chosen mode and its rough effort in one line, and confirm it. Three depths, plus a pacing switch:

| Mode | Phases | Output files | Rough effort | For |
|---|---|---|---|---|
| **Lite** | Brief → Research/Ideation → PRD → Screen contracts (경량) → Storyboard → Dashboard | ~8 | one short session | small products, validating an idea, "간단히" |
| **Standard** (default) | Full phase order below, single pixel ceiling + workbench | ~20 | several sessions | real product heading to build |
| **Deep** | Standard + richer evidence, more alternatives, stronger state coverage, full risk register | ~25 | multi-day | production launch, regulated/sensitive domains |

Pacing switch — **run-through mode ("쭉 진행")**: when the user says "쭉 진행해", "알아서 진행", "한번에 해줘", or approves run-through at intake, chain phases WITHOUT stopping for review between them — pause ONLY at the User Decision Gates listed below (direction lock, MVP lock, brand lock, surface lock, hi-fi entry, design acceptance, handoff). Everything else proceeds, with assumptions labeled and logged. In run-through mode the phase-exit block still appears after every phase so the user can scan what happened.

**Every response in an orchestrate run — regardless of mode — ends with a `다음 단계` block**: (1) 추천 다음 스킬 1개 + 이유 1줄, (2) 사용자가 결정할 것 (없으면 "없음 — 그대로 진행 가능"), (3) 진행 중 위치 (단계 N/총단계). A response that ends without this block is an unfinished response. This is how the user always knows what to do next without reading the pipeline docs.

## Phase 0 — Workspace detection (resume / redo / fresh)

Before initializing anything, check whether the planning folder already exists (`docs/product-planning/<slug>/` or the folder the user names):

- **No folder** → fresh run: initialize (see Required Outputs), then start at Brief.
- **Folder exists, user continues the same product** → resume: read `00-decision-log.md` (decisions + gate status) and the dashboard FIRST, report "지금 어디까지 왔고, 다음은 X" — never restart phases that passed.
- **User asks to redo one part** ("아트디렉션만 다시", "이름 다시 짓자") → rerun ONLY that skill, then cascade: list which downstream artifacts consume it (e.g., art direction → design system → workbench → demo) and update only those, farthest-upstream first. Do not touch unaffected artifacts.
- **User pivots the product** → archive: move the old folder to `<slug>-archive-<date>/`, start fresh, and carry over only what the user explicitly keeps.

## Visual Craft Spine (Anti-Slop) — the part that decides production quality

Product logic in this workflow is strong; the historical failure was visual craft producing AI slop that the gate self-passed. The visual phases (art direction → token substrate → hi-fi screen → workbench → gate) run on a shared anti-slop spine. Before any visual phase, read:

- `${CLAUDE_PLUGIN_ROOT}/references/anti-slop-doctrine.md` — why slop happens, the S1–S14 signature taxonomy + fixes, the shadcn-sameness defense, the two survival tests.
- `${CLAUDE_PLUGIN_ROOT}/references/measured-design-spec.md` — art direction must output numbers (type ramp, OKLCH roles, grid, spacing), not adjectives.
- `${CLAUDE_PLUGIN_ROOT}/references/token-substrate.md` — build on shadcn/Radix with the default skin stripped and product OKLCH tokens applied; never raw divs, never default shadcn.
- `${CLAUDE_PLUGIN_ROOT}/references/craft-loop.md` — layered passes (structure→layout→type→color→imagery→polish→distinctiveness), ceiling-on-one-screen-first, full-viewport rendering.
- `${CLAUDE_PLUGIN_ROOT}/references/adversarial-visual-gate.md` — fresh-critic + measurable checks + loop-until-clean.

**Delegate pixel craft to Claude Code's design skills when the environment provides them** (they are engineered against these signatures): `impeccable`/`craft` (shape→build), `layout`, `typeset`, `colorize`, `distill`, `polish`, `bolder` (distinctiveness), `critique`/`audit` (adversarial review). If the environment provides none, the `references/` doctrine is self-sufficient — apply the craft passes by hand. Either way this plugin owns product logic, IA, screen contracts, states, the measured spec, and the gate; the craft owns the pixels. Never let craft change product IA (e.g. promoting an internal mechanism to primary navigation) for visual convenience — the screen contract wins.

**Ceiling-first ordering.** Do not render all P0 screens at average quality at once. Craft the single most decisive screen to the bar, pass the adversarial gate, then propagate the passing token/component system to the rest. One screen at the ceiling beats eight at the average.

## Visual-First Review (mandatory) — the founder does not read 20 markdown files

A solo founder reviews **visually**, not by opening every `.md`. Producing a wall of markdown with no visual review surface is a failure mode, even if the markdown is excellent. Enforce:

- **After every phase, update `00-review-dashboard.html`** via `product-blueprint:decision-dashboard`. This is not optional and not "when asked" — it is part of finishing a phase. Never leave the dashboard as the init stub while shipping 10+ markdown files. If you produced artifacts and did not update the dashboard, the phase is not done.
- **The dashboard is THE review surface.** It answers, in <30s: where are we, what are the 2–4 things to look at now (with ★), what decisions are pending, and what each artifact is for. Markdown is the detail SoT; the founder should never be told "read these 20 files."
- **Visuals are first-class deliverables, not decoration.** The review layer is the dashboard + the storyboard flow board + screen mockups. When the user says "there are too many documents / I don't know what to look at / I don't read them one by one," that is a signal the visual review layer is missing — build/repair it, do not answer with more prose.
- **Visualize decisions and expected outcomes**, not just status: a decision→implication map and a flow board let the founder *see* what the plan produces without reading contracts. Prefer a legible flow/IA diagram over tiny pixel mockups (tiny tiled frames destroy fidelity — that is the storyboard's flow-contract role, distinct from the workbench's full-fidelity role).

## Output Language And Stage Exit

- Default to the user's conversation language for planning artifacts, review prompts, decision logs, PRD summaries, storyboards, critique notes, and final guidance.
- If the user is Korean, write planning artifacts in Korean. Keep product names, UI labels under evaluation, API-like identifiers, and skill names in English only when useful.
- Do not leave the user guessing what to review. At the end of every phase, include:
  1. `지금 확인할 산출물`
  2. `사용자가 결정할 것`
  3. `수정이 필요하면 어디를 바꿀지`
  4. `다음 추천 스킬`

## Conversation Contract

Product Blueprint is guided planning, not autopilot. Ask the user when a decision would change the product direction, research scope, design direction, safety boundary, monetization model, or engineering handoff.

Start with a short intake if the request is vague. Ask at most 5 questions at once:

1. What product idea or user problem are we planning?
2. Are there reference services, screenshots, or competitors to inspect?
3. Who is the primary user and what should the product feel like?
4. What must be included or avoided in the first version?
5. What output depth is wanted: quick concept, standard PRD/storyboard, or deep full handoff?

Proceed without asking only when the missing information is non-blocking and reversible. In that case, write an `Assumptions` section and mark what should be confirmed later.

## Artifact Maturity Bar

`orchestrate` must not behave like a rough outline generator when the user asks for a standard or deep planning package. The first complete pass should be reviewable by a founder, product designer, and engineer even if it is not final.

Default depth (see the mode table in "How To Run"):

- If the user says "쭉 진행", "orchestrate부터", "전체 기획", "프로덕션급", or gives a reference service for benchmarking, treat the request as `standard` unless they explicitly ask for a quick sketch. "쭉 진행" additionally enables run-through pacing.
- `lite` stops at brief, PRD, light screen contracts, and storyboard — but never skips the decision log, user decision gates, or assumption labels.
- `standard` must produce the full product-flow package, positioning/brand, a readable storyboard, design-system + workbench, and the clickable demo before engineering handoff.
- `deep` must additionally include richer reference evidence, more alternative concepts, stronger state coverage, visual critiques, the full risk register, feasibility options, and handoff risks.

Minimum standard/deep completeness:

- Include all obvious core surfaces for the product category. For discovery-heavy products, search is a default surface unless explicitly scoped out.
- Wire each major screen to previous and next screens with storyboard annotations outside the mocked product UI. A frame without entry/exit is incomplete; a frame that puts planning labels inside the app screen is also incomplete.
- Storyboard frames must be visually legible as screen frames, not blurred wireframes. Use reference screenshots, existing product imagery, or generated bitmap assets for character/product/place visuals when the product domain depends on visual appeal. Storyboards can be HTML because they are flow/IA contracts, not final UI.
- For production-grade design expectations, do not stop at `04.3-design-system.md` or one polished screen. Create a React design-system workbench with token swatches, component catalog, state lab, and P0 production screen mockups.
- A high-fidelity screen specimen is a pixel-level pass for one screen, not a replacement for the workbench.
- Separate first-time, returning, empty, locked/safety, paid, and error states when relevant.
- Include a `Known Missing / Not Yet Explored` section instead of hiding gaps.
- Include a `Next Decision` after each artifact. If the user cannot decide what to review next, the phase is incomplete.
- Do not mark any phase as pass when reference fidelity, P0 scope, or screen wiring is materially incomplete.
- Do not mark design as complete while the user still has to request obvious missing screens, components, or states one by one.
- Do not force the user to read every markdown file to understand the state. Maintain `00-review-dashboard.html` as the fast visual review surface; markdown files are the detailed source of truth.

## Evidence And Assumption Discipline

Never mix observed reference behavior, user-confirmed requirements, and agent-proposed ideas in the same bullet without labels.

Use these labels throughout artifacts:

- `관찰`: Seen in screenshots, DOM, live exploration, user-provided screenshots, or quoted source.
- `사용자 확정`: The user explicitly confirmed this direction or constraint.
- `제안`: Product idea proposed by the agent or expert lens.
- `가정`: Needed to proceed but not yet verified.
- `미확인`: Known research gap.

Rules:

- Every reference-derived claim must point to a screenshot, URL, DOM snapshot, or explicit inference.
- If a referenced page has scrollable lower content, inspect and capture the lower content before claiming the page structure is understood.
- If login/session access is unavailable, say so and mark the affected flows as unverified.
- Never use a polished storyboard to cover missing research.

## Feature Intent Clarification

Before turning a named feature into screens or requirements, restate the user's intended behavior in concrete terms.

Ask or label as unconfirmed when a term can mean multiple products:

- `checkpoint` may mean manual save, branch point, undo state, version history, or "copy this chat room from turn N into a new chat room."
- `memory` may mean hidden system recall, user-visible notes, editable long-term memory, summary, or per-chat state.
- `persona` may mean user identity, role, relationship premise, account-level profile, or per-character setup.
- `mission` may mean quest, achievement, paid challenge, creator-authored task, or conversation scoring.

If the user clarifies the meaning, update the decision log and remove the incorrect interpretation from PRD, screen contracts, storyboard, backend brief, and handoff.

Do not promote a feature into P0 just because it sounds powerful. Classify each feature as:

- `Core P0`: Required for the main product loop.
- `P0 support`: Required only to make the loop usable, safe, searchable, or recoverable.
- `P1 differentiator`: Strong feature, but not needed for the first usable loop.
- `P2 expansion`: Needs core loop validation first.
- `Out of scope`: Not part of the product direction.

## Concept-To-Surface Discipline

Do not turn internal planning concepts into tabs, screens, or primary UI without checking the product logic and the user's language.

> Domain neutrality: the character-chat examples in this section and throughout this skill (persona-as-entry-gate, memory, checkpoint) are illustrations of *one* domain. This harness is product-agnostic — substitute your product's real concepts and IA. Apply the neutral rules; treat the chat-specific defaults as examples, not universal law.

For every major concept or mechanism, separate these levels:

1. **Internal concept**: the planning term used by the team.
2. **User-facing feature**: the label and promise users should understand.
3. **Moment of use**: when the feature affects the journey.
4. **Default visibility**: background, inline hint, bottom sheet, side panel, settings, modal, dedicated screen, or primary navigation.
5. **User control**: what the user can inspect, edit, correct, hide, retry, or undo.
6. **Surface decision**: whether this deserves a persistent UI surface or only appears during setup, review, correction, or recovery.

Rules:

- Never assume a mechanism deserves a main tab because it is product-critical.
- Never promote a system behavior into a visible screen before defining the moment when users need to see or control it.
- Treat persona/setup as a chat-entry gate by default: it belongs after character detail and before the chat room. Do not place persona on the home screen, bottom navigation, primary navigation, or discovery surface unless the user explicitly changes the product model.
- Preserve user terminology when the user has clarified it. If the user says a concept is just persona, memory, setup, or a background change, do not split it into a separate product object unless they approve.
- If a planning term could change the IA or screen map, ask the user before locking it.
- Mark surface assumptions explicitly in the decision log.
- When reference evidence and user intent conflict, user intent wins and the reference is treated as benchmark evidence, not a requirement.

Example distinction:

- Persona/setup may include relationship premise, role, tone, pace, and boundaries. Its default flow is `character detail -> persona/setup -> chat room`. Do not create a separate "relationship contract" tab, home module, or navigation item unless the user wants that surface.
- Long-term memory may be generated by changes during chat. Do not place it on the main screen by default. Define whether it is background behavior, a side-panel review surface, an inline suggestion, or a correction/recovery tool.

## User Decision Gates

Ask for user input before crossing these gates:

- **Research access**: login, paid, adult-gated, destructive, publishing, account, or privacy-sensitive exploration.
- **Direction lock**: choosing the winning concept from `parallel-concepts`.
- **Brand lock**: confirming positioning, product name, and mascot direction from `positioning-brand`.
- **MVP lock**: finalizing PRD scope and non-goals.
- **Surface lock**: deciding that a mechanism becomes a visible tab, main-screen component, persistent panel, or primary navigation item.
- **Screen contract lock**: accepting allowed actions and forbidden shortcuts.
- **High-fidelity design**: moving from storyboard/art direction into realistic visual mockups.
- **Design acceptance**: treating visual quality gate, design-system, or prototype test as pass.
- **Engineering handoff**: declaring the planning package ready for technical design.

At the end of every phase, include:

- `Status`: pass, fail, or ACCEPT-FLAG (recorded limitation — see `references/quality-bar.md`; "conditional pass" is not a status)
- `What changed`
- `User decisions needed`
- `Assumptions carried forward`
- `Next recommended skill`
- `Why this next`

## Phase Order

Lite mode runs phases 1, 2, 7, 8, 10 only (with the dashboard). Standard/Deep run all.

1. **Brief**: Define target user, job, core loop, reference services, constraints, and unknowns.
2. **Research Or Ideation**: If reference products exist, use `product-blueprint:research`. If not, use `product-blueprint:ideation` with assumptions clearly labeled.
3. **Reference Deconstruction**: Use `product-blueprint:reference-deconstruction` when references exist. Turn screenshots into product principles, gates, and anti-copy rules.
4. **Parallel Concepts**: Use `product-blueprint:parallel-concepts`. Explore multiple product/screen directions before committing to one. Concepts must differ at screen/mechanic level with a representative visual each — a non-reader must be able to choose.
5. **Positioning & Brand**: Use `product-blueprint:positioning-brand`. Positioning statement, name (taste-first rounds → availability signals), voice one-pager, mascot/wordmark direction. Runs BEFORE art direction because the name, voice, and mascot constrain the visual world.
6. **Experience Mechanisms**: Use `product-blueprint:experience-mechanisms` for invisible product behavior such as memory, judging, ranking, scoring, recommendations, personalization, safety gates, and paid actions.
7. **User Stories And PRD**: Use `product-blueprint:prd`. Define MVP loops, requirements, non-goals, states, risks, and mechanism-dependent requirements. **Red-team this phase**: when multi-agent support exists, spawn a fresh-context critic to attack the PRD (missing loop steps, unowned states, scope lies) before MVP lock; inline adversarial pass otherwise. Record what it found.
8. **Screen Contracts**: Use `product-blueprint:screen-contract`. Define each priority screen's purpose, allowed actions, forbidden shortcuts, states, entry paths, and exit paths.
9. **Feasibility Checkpoint (lightweight, BEFORE any visual design)**: Use `product-blueprint:feasibility-review` in checkpoint mode. Every mechanism a P0 screen depends on gets a verdict — feasible / conditional (state the condition) / infeasible — so mockups never promise the impossible. Output `02.7-feasibility-checkpoint.md`. An `infeasible` verdict goes back to the user BEFORE the storyboard renders that screen. This is the "engineer in the room" moment; do not defer it to the full feasibility review (phase 22).
10. **Storyboard Board**: Use `product-blueprint:storyboard`. Visualize flows screen-by-screen with evidence, state, transition wiring, and mechanism surfaces as a Figma-like board. This is the default visual planning artifact; do not replace it with a rough clickable demo.
11. **Art Direction Brief**: Use `product-blueprint:art-direction-brief`. Define product world, design thesis, imagery, typography, color roles, signature element, and anti-aesthetic — consuming the brand lock (wordmark face, mascot palette rule, voice).
12. **Visual Quality Gate**: Use `product-blueprint:visual-quality-gate` before accepting any visual direction. Fail generic AI-slop, flow-inaccurate, unreadable, or state-poor design artifacts.
13. **UX Writing**: Use `product-blueprint:ux-writing`. Microcopy sheet (labels, empties, errors, loading, confirmations, CTA verbs) for every P0 screen. Downstream mockups use these strings verbatim.
14. **Backend Systems Brief**: Use `product-blueprint:backend-systems-brief` for memory, judging, ranking, billing, permissions, safety, creator publishing, and other backend/system concerns before technical architecture.
15. **Design System / Visual Direction**: Use `product-blueprint:design-system` only after storyboard, art direction, and visual quality gate are stable. This creates a production design brief, not frontend implementation or frontend architecture.
16. **Design System Workbench**: Use `product-blueprint:design-system-workbench` to render tokens, component catalog, state lab, and P0 production screen mockups. **All-P0 coverage matrix is the exit gate**: every P0 screen from the contracts → a workbench/demo mockup → visual-gate pass. A missing row fails the phase; "propagated from the ceiling" without a rendered artifact is not coverage.
17. **High-Fidelity Screen Specimen**: Use `product-blueprint:high-fidelity-screen` only when one screen from the workbench needs an additional pixel-level pass. This is the ceiling screen, not a substitute for all-P0 coverage.
18. **Clickable Demo**: Use `product-blueprint:clickable-demo`. Single-file HTML: every P0 screen, real transitions matching the contract map (script-verified), board mode for Figma-like review, rendered non-happy-states sample. This is the founder's primary review artifact.
19. **Prototype Test**: Use `product-blueprint:prototype-test` for concrete user tasks against the demo/workbench. Distinguish heuristic self-walkthrough (always) from a real-user protocol (recommend when stakes justify it); the loop stays labeled "실사용자 미검증" until real users run it.
20. **Design Critique**: Use `product-blueprint:design-critique` to review product intent, UX flow, visual quality, states, system trust, component reuse, and handoff readiness.
21. **Risk Register**: Use `product-blueprint:risk-register` when the product touches adult content, minors, payments, UGC, PII, or AI-generated content (mandatory then; recommended otherwise). P0 risks need mitigations before handoff.
22. **Feasibility Review (full)**: Use `product-blueprint:feasibility-review` to prepare product/design/engineering tradeoff discussions without silently downgrading the product. Reconcile against the phase-9 checkpoint verdicts.
23. **Engineering Handoff**: Use `product-blueprint:engineering-handoff` as the default final phase. Must include the Entity & State Contract (entities/relationships, per-screen state machines, invariants as testable assertions) so a developer can start architecting — not a list of open questions.

After each phase, explicitly recommend one next phase and explain why (the `다음 단계` block — mandatory on every response). If required inputs for the next phase are missing, stop and ask the user for those inputs instead of proceeding with invented assumptions.

After each phase that produces or changes multiple artifacts, update `product-blueprint:decision-dashboard`. The dashboard is the user's review entry point; do not make the user inspect long markdown files first.

Use `product-blueprint:tech-plan` only when the user explicitly asks to continue into technical architecture after the handoff.

## Expert Lenses

Run these lenses inline by default. Use subagents only when the environment has safe multi-agent support and the user approves the cost.

- Product owner: scope, MVP loop, sequencing
- UX researcher: reference evidence, user intent, confusion
- Service designer: cross-screen journey and lifecycle
- Product designer: screen hierarchy, storyboard clarity
- UX writer: labels, promises, empty/error states
- Art director: product world, visual thesis, image rules, signature motif
- Visual design director: reference fidelity, art direction, anti-slop quality, state completeness
- Frontend lead: interaction feasibility and design-system constraints only; implementation planning happens in the actual app workflow later
- Backend lead: product invariants, system responsibilities, permissions, lifecycle, audit, cost and operational concerns
- AI/Systems behavior lead: memory, judging, recommendations, scoring, uncertainty
- Growth/monetization: activation, retention, paid moments
- Risk reviewer: policy, age, safety, abuse, legal ambiguity

## Gates

- No storyboard before research or ideation mental model.
- No high-fidelity screen before a screen contract exists.
- No single concept lock-in before at least two alternatives have been considered, unless the user explicitly asks for speed.
- No storyboard for AI/system-judged behavior before an experience mechanism contract exists.
- No high-fidelity design before PRD, screen contracts, storyboard, art direction, and visual-quality gate are coherent.
- No design-system claim before tokens are shown on components and P0 screen mockups. For production-grade visual direction, create a React design-system workbench instead of treating the HTML storyboard or markdown token table as the visual ceiling.
- No production design claim without screenshot verification and critique against AI-slop signals.
- No React conversion of the entire planning board by default. Convert design-system foundations, reusable components, state lab, and P0 production screen mockups into a React workbench after the design system exists.
- No engineering handoff readiness if visual quality was a user concern and the workbench is missing, unrendered, or screenshot-untested.
- No backend architecture during default Product Blueprint workflow. Create a backend systems brief first.
- No API/DB design during the default Product Blueprint workflow. Stop at engineering handoff unless the user explicitly asks for technical planning.
- Mark unverified flows explicitly. Never invent reference behavior.
- Paid, destructive, age-gated, or account-affecting actions require user approval before live exploration.
- Do not erase a product requirement because it sounds technically hard. Mark it for feasibility review with staged options — but get the feasibility checkpoint verdict BEFORE the screen is visually designed.
- No visual design (storyboard onward) for a P0 screen whose mechanisms lack a feasibility-checkpoint verdict.
- No handoff readiness while the all-P0 coverage matrix has missing rows or the risk register has unmitigated P0 rows (when the register is mandatory).
- **Retry cap + ACCEPT-FLAG**: any gate loops at most 3 fix cycles per artifact. Still failing → do not loop forever, do not silently pass: record ACCEPT-FLAG in the decision log (what failed, why accepted, later fix) and surface it in the dashboard and handoff. See `references/quality-bar.md`.
- Non-visual red-team: PRD/mechanism lock gets a fresh-context adversarial pass (subagent when available, inline otherwise) — the visual gate must not be the only place a critic exists.

## Required Outputs

Create or update a folder such as `docs/product-planning/<slug>/` with:

> File numbers are folder-sort order for review, not execution order — the Phase Order above governs sequencing (e.g. the visual gate runs before `03.7-ux-writing.md`; the risk register runs before `04.5-feasibility-review.md`).

- `00-brief.md`
- `00-decision-log.md`
- `00-review-dashboard.html`
- `01-reference-research.md` or `01-ideation.md`
- `01.5-reference-deconstruction.md` when references exist
- `01.6-parallel-concepts.md`
- `01.8-positioning-brand.md`
- `02-mechanisms.md`
- `02-prd.md`
- `02.5-screen-contracts.md`
- `02.7-feasibility-checkpoint.md`
- `03-storyboard.html`
- `03.5-art-direction-brief.md`
- `03.7-ux-writing.md`
- `04.1-visual-quality-gate.md`
- `04.2-backend-systems-brief.md`
- `04.3-design-system.md` or `.html`
- `04.32-design-system-workbench.md`
- `prototypes/<product>-design-system-workbench.html` or equivalent isolated workbench
- `tokens/` files when token export is useful and values are stable enough
- `04.35-high-fidelity-screen.md` plus optional single-screen specimen only when one screen needs an extra pixel pass
- `04.36-clickable-demo.md` + `prototypes/<product>-demo.html`
- `04.4-prototype-test.md`
- `04.45-design-critique.md`
- `04.55-risk-register.md` when the domain makes it mandatory
- `04.5-feasibility-review.md`
- `05-engineering-handoff.md`
- `screenshots/` when references are researched

Lite mode creates only: `00-brief.md`, `00-decision-log.md`, `00-review-dashboard.html`, `01-*(research|ideation).md`, `02-prd.md`, `02.5-screen-contracts.md`, `03-storyboard.html` (init with `--lite`).

To initialize the artifact structure, run:

```bash
python3 <plugin-root>/scripts/init_prd_project.py "<product name>" --root docs/product-planning   # add --lite for Lite mode
```

If `python3` is unavailable, do not stall: create the folder and the stub files directly with your file tools (same names as above; the script is a convenience, not a dependency).

## Completion

Use `references/quality-bar.md` to judge whether the output is industry-usable. Report which gates are complete, which flows are unverified, which mechanisms still need feasibility review, and whether the project is ready for engineering handoff or still needs product/design work.

## Next Step

- If starting a new planning project, initialize the folder with `scripts/init_prd_project.py`, then run `product-blueprint:research` or `product-blueprint:ideation`.
- If all required artifacts are complete, stop at `product-blueprint:engineering-handoff` unless the user explicitly asks for `product-blueprint:tech-plan`.
