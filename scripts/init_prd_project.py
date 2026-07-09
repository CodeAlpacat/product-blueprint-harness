#!/usr/bin/env python3
"""Create a Product Blueprint planning artifact folder."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "product-plan"


FILES = {
    "00-brief.md": """# Product Brief

## Idea

## Target User

## Core Job

## Reference Services

## Constraints

## Unknowns

## Assumptions

## User Decisions Needed

## Next Step

- Use product-blueprint:research when references exist.
- Use product-blueprint:ideation when references do not exist.
""",
    "00-decision-log.md": """# Decision Log

Use this file to keep user decisions, assumptions, and gate status from getting lost across a long planning run.

## Intake Answers

## User Decisions

## Assumptions Carried Forward

## Gate Status

| Phase | Status | User decision needed | Next recommended skill |
| --- | --- | --- | --- |

## Open Questions
""",
    "00-review-dashboard.html": """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Product Blueprint Review Dashboard</title>
</head>
<body>
  <main>
    <h1>Review Dashboard</h1>
    <p>Use this as the fast visual review surface. Markdown files remain the detailed source of truth.</p>
    <section>
      <h2>Current Status</h2>
      <p>Update with the current phase, gate status, and next decision.</p>
    </section>
    <section>
      <h2>Decision Queue</h2>
      <p>List approve/change/hold decisions here.</p>
    </section>
    <section>
      <h2>Next Step</h2>
      <p>Use the next recommended Product Blueprint skill.</p>
    </section>
  </main>
</body>
</html>
""",
    "01-reference-research.md": """# Reference Research

## Scope

## Screenshot Inventory

## Feature Map

## Core Loops

## Verified Flows

## Unverified Flows

## Opportunities

## Next Step

- Use product-blueprint:reference-deconstruction when references exist.
""",
    "01-ideation.md": """# Ideation

## Product Theses

## Core Loop Candidates

## Differentiation

## Recommended MVP

## Assumptions To Validate

## Next Step

- Use product-blueprint:parallel-concepts.
""",
    "01.5-reference-deconstruction.md": """# Reference Deconstruction

## Evidence Map

## Feature-To-Mental-Model Table

## Screen Role And Entry-Gate Map

## Mechanism And Trust-Surface Map

## Product Principles To Reuse

## Anti-Copy List

## Open Research Gaps

## Next Step

- Use product-blueprint:parallel-concepts.
""",
    "01.6-parallel-concepts.md": """# Parallel Concepts

## Concept A

## Concept B

## Concept C

## Comparison

## Recommended Direction

## Validation Needed

## Next Step

- Use product-blueprint:screen-contract and product-blueprint:experience-mechanisms.
""",
    "02-prd.md": """# PRD

## Product Thesis

## Users

## Core Loop

## MVP Scope

## User Stories

## Requirements

## States

## Risks

## Acceptance Criteria

## Next Step

- Use product-blueprint:screen-contract.
""",
    "02-mechanisms.md": """# Product Experience Mechanisms

## Mechanism Inventory

## Long-Term Memory

### User Promise

### Inputs And Outputs

### User Controls

### Transparency And Recovery

### Acceptance Examples

### Feasibility Questions

## Judging / Scoring / Ranking

### User Promise

### Inputs And Outputs

### User Controls

### Transparency And Recovery

### Acceptance Examples

### Feasibility Questions

## Next Step

- Use product-blueprint:prd or product-blueprint:screen-contract.
""",
    "02.5-screen-contracts.md": """# Screen Contracts

## Screen Inventory

## Contract Per Screen

## Entry And Exit Map

## State Matrix

## Forbidden Shortcuts

## Acceptance Checks

## Next Step

- Use product-blueprint:storyboard.
""",
    "03-storyboard.html": """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Product Storyboard</title>
</head>
<body>
  <main>
    <h1>Product Storyboard</h1>
    <p>Replace this with the evidence-backed storyboard.</p>
    <h2>Next Step</h2>
    <p>Use product-blueprint:art-direction-brief.</p>
  </main>
</body>
</html>
""",
    "03.5-art-direction-brief.md": """# Art Direction Brief

## Design Thesis

## Product World

## Reference Translation

## Palette And Typography Rationale

## Imagery And Motion Rules

## Signature Element

## Anti-Slop Checklist

## Open Design Risks

## Next Step

- Use product-blueprint:visual-quality-gate.
""",
    "04.1-visual-quality-gate.md": """# Visual Quality Gate

## Verdict

## AI-Slop Findings

## Reference Fidelity Issues

## Product-Specific Art Direction

## State And Mechanism Gaps

## Required Revisions Before Production Design

## Next Step

- Use product-blueprint:backend-systems-brief and product-blueprint:design-system.
""",
    "04.2-backend-systems-brief.md": """# Backend Systems Brief

## Product-Level System Responsibilities

## Trust-Critical Mechanisms

## Data Categories

## Permission And Boundary Map

## Lifecycle Map

## High-Risk Invariants

## Failure And Dispute Handling

## Later Engineering Decisions

## Next Step

- Use product-blueprint:design-system or product-blueprint:feasibility-review.
""",
    "04.3-design-system.md": """# Design System

## Brand Position

## Named Art Direction

## Design Principles

## Tokens

## Components

## Screen Application

## Mechanism And State Coverage

## Accessibility

## Next Step

- Use product-blueprint:design-system-workbench.
""",
    "04.32-design-system-workbench.md": """# Design System Workbench

## Purpose

Render the product's visual system as a React/Tailwind workbench before technical design.

## Required Workbench Artifact

- prototypes/<product>-design-system-workbench.html

## Foundation Tokens

## Component Catalog

## State Lab

## Production Screen Set

## Flow Wiring Notes

## Implementation Handoff Map

## Browser Verification

## Open Design Decisions

## Next Step

- Use product-blueprint:prototype-test.
""",
    "04.4-prototype-test.md": """# Prototype Test

## Test Tasks

## Pass / Fail Table

## Confusion Log

## Required Revisions

## Prototype Evidence

## Decision

## Next Step

- Use product-blueprint:design-critique.
""",
    "04.45-design-critique.md": """# Design Critique

## Findings By Severity

## Open Questions

## Required Revisions

## Optional Improvements

## Handoff Readiness

## Next Step

- Use product-blueprint:feasibility-review when P0/P1 issues are resolved.
""",
    "04.5-feasibility-review.md": """# Feasibility Review

## Product Non-Negotiables

## Mechanism Risk Table

## Tradeoff Options

## Scope-Out Candidates

## Questions For Engineering

## Decision Log

## Next Step

- Use product-blueprint:engineering-handoff.
""",
    "05-engineering-handoff.md": """# Engineering Handoff

## Product Thesis

## MVP Loop

## User Journeys And Screen Map

## Product Non-Negotiables

## Mechanism Contracts For Engineering Review

## Backend/System Responsibilities And Invariants

## Approved Compromises

## Scope-Out Candidates

## Open Questions

## Evidence Links

## Technical Design Readiness Checklist

## Next Step

- Stop here by default. Use product-blueprint:tech-plan only if the user explicitly asks for technical architecture.
""",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Product or planning project name")
    parser.add_argument("--root", default="docs/product-planning", help="Output root directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    target = Path(args.root).expanduser() / slugify(args.name)
    target.mkdir(parents=True, exist_ok=True)
    (target / "screenshots").mkdir(exist_ok=True)
    (target / "prototypes").mkdir(exist_ok=True)
    (target / "tokens").mkdir(exist_ok=True)

    for filename, content in FILES.items():
        path = target / filename
        if path.exists() and not args.force:
            continue
        path.write_text(content, encoding="utf-8")

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
