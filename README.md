# Product Blueprint Harness

Cross-agent plugin for pre-development product planning and production-grade visual design. Runs in **both Codex and Claude Code**.

This repository contains only the reusable plugin:

- `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` (Claude Code)
- `.codex-plugin/plugin.json` (Codex)
- `skills/*/SKILL.md` (shared — same SKILL.md format on both hosts)
- `references/*.md` (anti-slop craft doctrine — the visual quality spine)
- `scripts/init_prd_project.py`
- `assets/templates/storyboard-section.html`

It intentionally does not include project-specific benchmark outputs, screenshots, WHIF captures, or Boylog planning artifacts.

## Anti-Slop Visual Craft Spine

The planning/IA discipline was always strong; the weak point was visual output collapsing to AI slop that a self-graded gate passed. The `references/` doctrine fixes this structurally:

- `anti-slop-doctrine.md` — why slop happens (mode collapse to the training average), a named S1–S14 slop-signature taxonomy with fixes, the shadcn/component-library sameness defense, and the two survival tests.
- `measured-design-spec.md` — art direction must resolve to numbers (type ramp, OKLCH color roles + contrast, grid, spacing), never adjectives.
- `token-substrate.md` — build on shadcn/ui + Radix with the default skin stripped and product OKLCH tokens applied; never raw divs, never default shadcn.
- `craft-loop.md` — layered craft passes, ceiling-on-one-screen-first, full-viewport rendering + screenshots.
- `adversarial-visual-gate.md` — a fresh-context critic runs measurable checks and loops until clean; conditional is not pass.

On Claude Code, the visual phases delegate pixel craft to the built-in design skills (`impeccable`/`craft`, `layout`, `typeset`, `colorize`, `distill`, `polish`, `bolder`/`ui-redesign`, `critique`/`audit`) while the plugin owns product logic, IA, states, the measured spec, and the gate.

## Purpose

Product Blueprint guides an idea or reference product through:

- research and reference deconstruction
- ideation and parallel concepts
- PRD and screen contracts
- storyboard visualization
- art direction and visual quality gates
- design-system planning and workbench generation
- high-fidelity screen specimens
- prototype testing and design critique
- backend systems briefing
- feasibility review
- engineering handoff

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

## Main Skill

Start with:

```text
product-blueprint:orchestrate
```

The orchestrator should ask for missing decisions, write decision logs, and recommend the next skill at each stage. For production-grade visual output, it routes through the anti-slop visual craft spine described above.
