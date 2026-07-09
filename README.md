# Product Blueprint Harness

Codex plugin for pre-development product planning.

This repository contains only the reusable plugin:

- `.codex-plugin/plugin.json`
- `skills/*/SKILL.md`
- `scripts/init_prd_project.py`
- `assets/templates/storyboard-section.html`

It intentionally does not include project-specific benchmark outputs, screenshots, WHIF captures, or Boylog planning artifacts.

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

## Install Locally

Clone this repository and add it as a Codex plugin from the local path.

```bash
git clone https://github.com/CodeAlpacat/product-blueprint-harness.git
```

Then install or link it using your Codex plugin workflow.

## Main Skill

Start with:

```text
product-blueprint:orchestrate
```

The orchestrator should ask for missing decisions, write decision logs, and recommend the next skill at each stage.
