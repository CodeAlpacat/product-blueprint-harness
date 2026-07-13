# Product Blueprint Harness

Cross-agent plugin for pre-development product planning and production-grade visual design. Runs in **both Codex and Claude Code**.

## Quickstart (60 seconds)

1. Install (see Install below).
2. In a new or empty project folder, just **describe your idea and name the plugin** — there is no slash command; skills auto-trigger:

   > "product-blueprint로 내 아이디어 기획해줘: 러닝 기록·공유 모바일 웹앱을 만들고 싶어. 레퍼런스는 Strava."

   or explicitly: "`product-blueprint:orchestrate`부터 시작해줘".
3. Answer the short intake (max 5 questions). Pick a **mode**:

   | Mode | You get | Rough effort |
   |---|---|---|
   | **Lite** | brief → research/ideation → PRD → screen contracts + compact service manifest → storyboard + dashboard | one short session |
   | **Standard** (default) | full pipeline: research → mechanisms/screens → service contract → design system → all-P0 clickable prototype → deterministic readiness → handoff | several sessions |
   | **Deep** | Standard + richer evidence, risk register, stronger boundary/role coverage | multi-day |

4. Want it hands-off? Say **"쭉 진행해"** — the orchestrator chains phases and only stops at the decisions that are genuinely yours (direction, brand, MVP scope, design acceptance, handoff). Every response ends with a `다음 단계` block: the recommended next skill, what you must decide, and where you are in the pipeline.
5. Review visually, not by reading markdown: open `00-review-dashboard.html` (always current), the storyboard, and the clickable demo. The `.md` files are the detail source of truth.

Notes: artifact scaffolding uses `python3` if available (falls back to direct file creation if not). Interrupted sessions resume from `00-decision-log.md` — say "이어서 진행해" in the same folder; say "아트디렉션만 다시" to redo one phase and its downstream only.

This repository contains only the reusable plugin:

- `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` (Claude Code)
- `.codex-plugin/plugin.json` (Codex)
- `skills/*/SKILL.md` (shared — same SKILL.md format on both hosts)
- `references/*.md` (anti-slop craft doctrine — the visual quality spine)
- `scripts/init_prd_project.py` + `scripts/validate_service_blueprint.py`
- `assets/templates/storyboard-section.html`

It intentionally does not include any project-specific planning outputs, benchmark captures, or screenshots from dogfood runs.

## Anti-Slop Visual Craft Spine

The planning/IA discipline was always strong; the weak point was visual output collapsing to AI slop that a self-graded gate passed. The `references/` doctrine fixes this structurally:

- `anti-slop-doctrine.md` — why slop happens (mode collapse to the training average), a named S1–S14 slop-signature taxonomy with fixes, the shadcn/component-library sameness defense, and the two survival tests.
- `measured-design-spec.md` — art direction must resolve to numbers (type ramp, OKLCH color roles + contrast, grid, spacing), never adjectives.
- `token-substrate.md` — build on shadcn/ui + Radix with the default skin stripped and product OKLCH tokens applied; never raw divs, never default shadcn.
- `craft-loop.md` — layered craft passes, ceiling-on-one-screen-first, full-viewport rendering + screenshots.
- `adversarial-visual-gate.md` — a fresh-context critic runs measurable checks and loops until clean; conditional is not pass.

On Claude Code, the visual phases can additionally delegate pixel craft to an **external design-skill suite if you have it installed** — `impeccable` (Apache 2.0, based on Anthropic's `frontend-design` skill) and its companion skills (`craft`, `layout`, `typeset`, `colorize`, `distill`, `polish`, `bolder`, `critique`). **These are third-party skills, not authored by or bundled with this plugin** — install them separately if you want them. When they are absent, the `references/` doctrine above is self-sufficient: apply the craft passes by hand. Either way, this plugin owns product logic, IA, states, the measured spec, and the adversarial gate; the craft layer only owns pixels.

## Purpose

Product Blueprint guides an idea or reference product through:

- research and reference deconstruction
- ideation and parallel concepts
- positioning, naming (taste-first rounds + availability signals), brand voice, mascot direction
- PRD, experience mechanisms, and screen contracts
- a machine-readable service contract connecting stories, surfaces, actions, states, frontend feedback, backend/data ownership, and journeys
- feasibility checkpoint BEFORE visual design (so mockups never promise the impossible)
- storyboard visualization
- art direction and adversarial visual quality gates (with an all-P0 coverage matrix)
- UX writing / microcopy sheets
- design-system planning, tokens, portable DESIGN.md, and workbench generation
- high-fidelity screen specimens and a single-file clickable demo (phone-frame flow + Figma-like board mode + rendered non-happy states)
- prototype testing (heuristic + real-user protocol) and design critique
- backend systems briefing and risk register
- feasibility review
- engineering handoff with an Entity & State Contract developers can architect from
- deterministic contract/prototype/handoff gates and a manifest-hash-bound readiness report, so documents cannot self-declare completion

The plugin is for planning before implementation. Frontend/backend technical architecture is a later handoff step, not the default starting point.

## Install

### Claude Code

Add the repo as a plugin marketplace, then install the plugin:

```text
/plugin marketplace add CodeAlpacat/product-blueprint-harness
/plugin install product-blueprint@product-blueprint-harness
```

Skills are auto-discovered from `skills/` and invoked as `product-blueprint:orchestrate`, `product-blueprint:art-direction-brief`, etc.

### Codex

Clone and link it using your Codex plugin workflow:

```bash
git clone https://github.com/CodeAlpacat/product-blueprint-harness.git
```

## How the skills fit together

`orchestrate` is the **router, not a gatekeeper**: it sequences phases, enforces gates, and writes the decision log — but every skill below is standalone-callable. You do not need a full orchestrate run to use one piece.

Start a full run with:

```text
product-blueprint:orchestrate
```

### Skill map (pipeline order)

| Stage | Skill | Owns (artifact) |
|---|---|---|
| Control | `orchestrate` | phase routing, gates, `00-decision-log.md` |
| Control | `decision-dashboard` | `00-review-dashboard.html` (the visual review surface — refresh after every phase) |
| Research | `research` / `ideation` | `01-reference-research.md` / `01-ideation.md` |
| Research | `reference-deconstruction` | `01.5-reference-deconstruction.md` |
| Concept | `parallel-concepts` | `01.6-parallel-concepts.md` (direction lock input) |
| Brand | `positioning-brand` | `01.8-positioning-brand.md` (name, voice, mascot direction) |
| Definition | `experience-mechanisms` | `02-mechanisms.md` (invisible behavior: memory, scoring, safety, paid) |
| Definition | `prd` | `02-prd.md` (MVP lock input) |
| Definition | `product-definition` | `02.1-product-definition.json` (confirmed personas, mental models, P0 requirements, entry points) |
| Definition | `screen-contract` | `02.5-screen-contracts.md` (per-screen actions/states/wiring) |
| Definition | `service-contract` | `02.6-service-manifest.json` (stable IDs, operations, journeys, evidence maturity) |
| Gate | `design-readiness` | contract/prototype/design/handoff validation + `05-readiness-report.*` |
| Definition | `feasibility-review` (checkpoint mode) | `02.7-feasibility-checkpoint.md` — BEFORE any visual design |
| Existing assets | `feature-adoption` (optional) | adoption map when you already own a mature codebase |
| Visual | `storyboard` | `03-storyboard.html` (flow board) |
| Visual | `art-direction-brief` | `03.5-art-direction-brief.md` (measured spec, not adjectives) |
| Visual | `visual-quality-gate` | `04.1-visual-quality-gate.md` (adversarial anti-slop gate) |
| Visual | `ux-writing` | `03.7-ux-writing.md` (microcopy used verbatim downstream) |
| Visual | `design-system` → `design-system-workbench` | `04.3-*` + workbench HTML (tokens, component states, all-P0 mockups) |
| Visual | `high-fidelity-screen` | single ceiling-screen pixel pass |
| Visual | `clickable-demo` | `prototypes/<product>-demo.html` (primary founder review artifact) |
| Assets | `art-production` (optional) | character/scene asset pipeline (prompt recipes, batch, curation board) |
| Validation | `prototype-test`, `design-critique` | `04.4-*`, `04.45-*` |
| Validation | `risk-register` | `04.55-risk-register.md` (mandatory for adult/minors/payments/UGC/PII/AI content) |
| Validation | `feasibility-review` (full) | `04.5-feasibility-review.md` |
| Acceptance | `design-acceptance` | `05-design-acceptance.json` (absorbed constraints + explicit current user approval) |
| Handoff | `backend-systems-brief` | `04.2-backend-systems-brief.md` |
| Handoff | `engineering-handoff` | compatibility-named `05-engineering-handoff.md` (accepted product/design contract, not implementation readiness) |
| Post-handoff | `tech-plan` (opt-in only) | technical architecture — only when explicitly requested |

### Improving one part mid-stream (partial use)

Skills communicate through the numbered artifacts, with `00-decision-log.md` as shared state — so partial reruns are a first-class flow, not a hack:

1. **Call the one skill you need** (in the planning folder). It reads its upstream artifacts and rewrites only its own.
2. **Cascade downstream only**: after the rerun, update the artifacts that consume the changed one, farthest-upstream first, and leave the rest untouched. Saying "아트디렉션만 다시" to `orchestrate` does exactly this (its Phase 0 redo mode).
3. **Refresh the dashboard** (`decision-dashboard`) so the review surface matches.

Common partial asks:

| You want to… | Call | Then cascades to |
|---|---|---|
| Rename / rebrand | `positioning-brand` | art-direction → design-system → workbench → demo |
| Add or change one screen | `screen-contract` | storyboard → workbench (if new components) → demo |
| Add or change a flow/state/data responsibility | `service-contract` | storyboard → demo → prototype test → readiness report |
| Rebuild just the demo | `clickable-demo` | — (reads existing contracts) |
| Strengthen form/component states | `design-system-workbench` | demo (if shared components changed) |
| Redo the visual direction | `art-direction-brief` | visual-quality-gate → design-system → workbench → demo |
| Generate/curate art assets | `art-production` | demo (asset wiring) |
| Audit what's still undefined | run the coverage self-audit (`references/coverage-self-audit.md`) | `02.8-undefined-surfaces.md` + dashboard |
| Check risk/compliance only | `risk-register` | handoff |
| Mine an existing codebase | `feature-adoption` | screen-contract deltas → demo → feasibility consultation |

If you're unsure which skill owns what you want to change, ask `orchestrate` to route it ("X만 다시") — it will identify the owning skill and the downstream update list instead of restarting the pipeline.

## Service contract and readiness gates

Standard/Deep runs use `02.6-service-manifest.json` as the stable identity and wiring source. Markdown explains decisions; the manifest makes them checkable. A P0 surface is not simply “complete”: it moves through `defined → prototyped → wired → contracted → verified` with concrete evidence.

Run the same validator at four product/design boundaries:

```bash
python3 scripts/validate_service_blueprint.py docs/product-planning/<slug> --stage contract --no-write
python3 scripts/validate_service_blueprint.py docs/product-planning/<slug> --stage prototype --no-write
python3 scripts/validate_service_blueprint.py docs/product-planning/<slug> --stage design --no-write
python3 scripts/validate_service_blueprint.py docs/product-planning/<slug> --stage handoff
```

The final command writes `05-readiness-report.json` and `.md`. Dashboard and handoff readiness must be derived from that report. A pass means the accepted product/design contract is ready to begin a separate technical-design process; it never means implementation-ready. Lite keeps all accepted-design dimensions false.

Prototype validation also requires `04.37-runtime-verification.json`, produced from a real browser walkthrough. It records every transition/effect/required-state result and the current manifest/demo SHA-256 values. Changing either source makes the report stale and blocks readiness until the browser scenario is rerun.

The architecture follows the useful parts of [Matt Pocock's skills](https://github.com/mattpocock/skills): small composable skills, test seams fixed in the spec, prototypes that answer concrete questions, and separate standards-vs-spec review. Product Blueprint extends that pattern with a mandatory whole-service prototype contract and a developer-lens consultation that feeds constraints back into design; neither is treated as implementation readiness.
