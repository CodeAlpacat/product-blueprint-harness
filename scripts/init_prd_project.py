#!/usr/bin/env python3
"""Create a Product Blueprint planning artifact folder."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def slugify(value: str) -> str:
    # Preserve unicode word chars (Korean/Japanese/etc.) so non-Latin project
    # names do not collapse to the fallback. ASCII-only stripping used to turn
    # every Korean name into "product-plan".
    slug = re.sub(r"[^\w]+", "-", value.strip().lower(), flags=re.UNICODE).strip("-_")
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
  <title>Product Blueprint — Review Dashboard</title>
  <style>
    :root{--surface:#faf7f2;--raised:#fff;--ink:#2a2622;--muted:#6b6259;--hair:#e7e0d6;--accent:#7c2d3a}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#f2ede5;color:var(--ink);font-family:-apple-system,"Apple SD Gothic Neo","Pretendard",sans-serif;line-height:1.55}
    .wrap{max-width:1040px;margin:0 auto;padding:36px 24px 64px}
    h1{font-size:24px;font-weight:600}
    .sub{color:var(--muted);font-size:13px;margin-top:4px}
    .todo{margin:18px 0;padding:12px 16px;border-left:3px solid var(--accent);background:#fbeef0;font-size:13px}
    .hero{background:var(--raised);border:1px solid var(--hair);border-left:3px solid var(--accent);border-radius:4px;padding:20px 22px;margin:14px 0}
    .eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:700}
    section{background:var(--raised);border:1px solid var(--hair);border-radius:4px;padding:16px 20px;margin-top:14px}
    section h2{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:700;margin-bottom:10px}
    .row{display:flex;justify-content:space-between;gap:12px;padding:7px 0;border-bottom:1px solid var(--hair);font-size:13.5px}
    .row:last-child{border-bottom:0}
    code{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--accent)}
  </style>
</head>
<body data-readiness-status="not-evaluated">
  <div class="wrap">
    <h1>Review Dashboard</h1>
    <div class="sub">검증을 실행하면 현재 결정, 필요한 파일과 누락 사항이 이 화면에 자동으로 정리됩니다.</div>
    <div class="todo">아직 검증 전입니다. 먼저 제품 방향을 정리한 뒤 현재 단계의 검증을 실행하세요.</div>

    <div class="hero">
      <div class="eyebrow">여기만 보세요</div>
      <h2 style="font-weight:600;margin:6px 0 8px">리뷰가 필요한 핵심 (2~4개)</h2>
      <p style="font-size:13px;color:var(--muted)">지금 유저가 실제로 봐야 할 산출물 2~4개만. 각 항목 = 무엇을 확인/결정할지 1줄. 나머지는 근거.</p>
    </div>

    <section><h2>1. 현재 상태</h2><p style="font-size:13px;color:var(--muted)">현재 단계와 아직 해결하지 않은 내용을 보여줍니다.</p></section>
    <section><h2>2. 지금 필요한 결정</h2><p style="font-size:13px;color:var(--muted)">확정, 수정 또는 보류할 내용과 영향을 보여줍니다.</p></section>
    <section><h2>3. 유저플로우 스냅샷</h2><p style="font-size:13px;color:var(--muted)">진입→게이트→커밋→결과→복구 압축 맵 (텍스트 아닌 시각 우선).</p></section>
    <section><h2>4. 경험 설계 스냅샷</h2><p style="font-size:13px;color:var(--muted)">주요 화면 · 흐름 · 상태 · 아직 정하지 않은 시각 디자인.</p></section>
    <section><h2>5. 첫 버전 범위</h2><p style="font-size:13px;color:var(--muted)">지금 포함할 것, 다음으로 미룰 것, 하지 않을 것을 보여줍니다.</p></section>
    <section><h2>6. 산출물 지도</h2><p style="font-size:13px;color:var(--muted)">각 md = 1줄 목적 + 상태 + 핵심(★) 표시. 링크로 상세 연결.</p></section>
    <section><h2>7. 근거와 빈틈</h2><p style="font-size:13px;color:var(--muted)">직접 확인한 내용, 사용자가 확인한 내용, 제안, 가정과 미확인 내용을 구분합니다.</p></section>
    <section><h2>8. 다음 단계</h2><p style="font-size:13px;color:var(--muted)">추천 스킬 1개 · 이유 · 산출물.</p></section>
  </div>
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
    "01-lite-direction.md": """# Lite Direction

## Evidence Or Ideation Basis

## Compared Product Directions

## Confirmed Product Direction

## Positioning And Working Brand

## Known Assumptions And Risks

## Decision References
""",
    "02-lite-plan.md": """# Lite Product Plan

## Target User And Core Job

## Core Loop

## First-Version Scope And Non-Goals

## Essential Mechanisms And Trust Behavior

## User Stories And Acceptance Outcomes

## Entry Points, Screens, And Critical States

## Feasibility Limits

## Confirmed Product Definition

## Open Questions
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

- Ask the user to confirm one direction, then use product-blueprint:positioning-brand.
""",
    "01.8-positioning-brand.md": """# Positioning & Brand

## Positioning Statement

## Naming (taste-first rounds -> availability signals)

## Voice & Tone One-Pager

## Jargon Ban List

## Mascot / Wordmark Direction

## Trademark Warning

- Signal research only. Real KIPRIS/USPTO + store search required before spending money.

## Next Step

- Use product-blueprint:experience-mechanisms.
""",
    "02.7-feasibility-checkpoint.md": """# Product Feasibility Checkpoint

| Mechanism | Depending P0 screens | Verdict (feasible/conditional/infeasible) | Condition / closest alternative | User decision needed |
| --- | --- | --- | --- | --- |

## Next Step

- Resolve infeasible rows with the user BEFORE storyboarding those screens.
- Then use product-blueprint:storyboard.
""",
    "03.7-ux-writing.md": """# UX Writing — Microcopy Sheet

Downstream mockups use these strings verbatim.

## Voice Rules (from positioning-brand)

## Per-Screen Copy Tables

## Empty States

## Errors & Recovery

## Confirmations & Costs

## CTA Verb List

## Next Step

- Use product-blueprint:design-system-workbench or product-blueprint:clickable-demo.
""",
    "04.36-clickable-demo.md": """# Clickable Demo Notes

Demo file: prototypes/<product>-demo.html (single file, no build, opens from disk)

## What Is Wired

## Transition-Map Verification (from -> to => landed)

## States Sample Coverage

## Known Gaps / Mocked Parts

## Next Step

- Use product-blueprint:prototype-test.
""",
    "04.55-risk-register.md": """# Risk Register

Not legal advice — real counsel reviews before launch.

| Risk | Trigger surface | Jurisdiction note | P0 mitigation (structural) | Owner decision | Status |
| --- | --- | --- | --- | --- | --- |

## Categories Swept (mark n.a. explicitly)

- Age & content rating / Personal data / Payments & virtual currency / UGC & moderation / AI-generated content / Platform policy / Accessibility & consumer law

## Next Step

- Engineering handoff is NOT ready while any P0 row lacks a mitigation.
""",
    "02.8-undefined-surfaces.md": """# Undefined Surfaces Registry (coverage self-audit)

> 이 목록에 없는 화면을 개발 중 임의 생성하지 말 것 — 발견 시 목록에 추가하고 확인 요청.

| Surface (referenced by) | 분류 | 처리 (mini-contract 3줄 / 파생 규칙 / P1 사유) |
| --- | --- | --- |

분류: 정의됨(증거 경로) / 규칙 파생 / 지금 계약 / P1 명시 이연

## Next Step

- 미분류 행이 남아 있으면 흐름과 화면 계약을 먼저 보완합니다.
""",
    "02-prd.md": """# PRD

## Product Thesis

## Target Users, Situations, And Anti-Users

## Core Loop And Activation Moment

## MVP Scope And Non-Goals

## Baseline Surface Classification

| Surface | P0 / P1 / P2 / excluded | Decision ref | Current-release entry behavior |
| --- | --- | --- | --- |

## Feature Table

| Feature | User job | Evidence | Scope | Required screens | Explicit non-goals |
| --- | --- | --- | --- | --- | --- |

## User Stories

Use stable IDs: `us-<job>-<nn>`.

## Functional Requirements

## Product-Experience Mechanisms And Trust

## Screen And State Inventory

## Monetization And Cost Moments

## Safety, Policy, Age, Privacy, And Abuse Risks

## Metrics And Qualitative Success Signals

## Open Questions And Unverified Flows

## Entry-Point Inventory

Cover first use, returning, route/deep link, auth gate, external/notification, refresh, back, cross-device, and offline. Mark `n/a` with a reason.

## Acceptance Criteria

## Feature Checklist

## Product Definition Seed

| Requirement candidate | Kind | Persona / mental model | Entry point | Required result | Exception / boundary | Decision evidence |
| --- | --- | --- | --- | --- | --- | --- |

## Next Step

- Use product-blueprint:planning-quality-gate before confirming the first-version scope.
""",
    "02.05-planning-quality-review.md": """# Planning Quality Review

## Executive Verdict

## Lens Summaries

### Product Strategy

### User Evidence

### Brand

### PRD

### Service Feasibility

### Growth And Risk

## Findings

| ID | Lens | Severity | Status | Owner | Problem | Evidence | Required change |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Changes Applied

## Recommended First-Version Scope

## Known Limits

- This review is not target-user validation or trademark clearance.

## User Decision Needed

## Next Step

- After explicit first-version scope confirmation, use product-blueprint:product-definition.
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

## Stable ID Registry

## Action Feedback & Accessibility Matrix

## Operation References

## Next Step

- Use product-blueprint:service-contract, then product-blueprint:storyboard.
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
    <p>Use product-blueprint:design-brief. This board defines behavior, not visual design.</p>
  </main>
</body>
</html>
""",
    "03-design-brief.md": """# Design Brief

## Product In One Minute

## Brand Direction

## Experience Priorities

## Screen And Flow Map

## State And Recovery Requirements

## Interaction Invariants

## Responsive And Accessibility Requirements

## System-Visible Constraints

## Reference Status

## Open Design Questions

## Acceptance Criteria For Visual Exploration

## Optional Next Step

- Stop after planning approval by default.
- If the user explicitly requests visual UI or a prototype, use product-blueprint:design-production.
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
    "03.4-visual-directions.md": """# Visual Directions

## User Taste Evidence And Gaps

## Shared Comparison Setup

## Direction A

## Direction B

## Direction C (optional)

## Comparable Evidence

## Comparison

## Recommendation And Tradeoffs

## User Decision Status

## Chosen Direction

## Next Step

- After explicit user choice, use product-blueprint:art-direction-brief to codify the selected direction.
""",
    "03.8-key-screen-review.md": """# Key Screen Review

## Representative Surface And Why

## Narrow Viewport Evidence

## Wide Viewport Evidence

## Critical State Evidence

## Product And Visual Critique

## Revisions Applied

## User Decision

## Expansion Boundary

- Do not expand to the full design system until the key-screen validator passes.
""",
    "04.1-visual-quality-gate.md": """# Visual Quality Gate

## Verdict

## AI-Slop Findings

## Reference Fidelity Issues

## Product-Specific Art Direction

## State And Mechanism Gaps

## Required Revisions Before Production Design

## Next Step

- If the all-P0 visual gate passes, continue to clickable-demo or final design critique. Route failures to the named screen or design-system owner.
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

- Use product-blueprint:design-brief. Visual design begins later only through the optional design-production workflow.
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

Render the product's visual system as dependency-light React sources before technical design.

## Required Workbench Artifact

- visual-workbench/ with tokens, components, fixtures, ComponentBoard, DepthBoard, and FlowPreview

## Foundation Tokens

## Component Catalog

## State Lab

## Depth And P0 Screen Set

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

## Stable-ID Feasibility Matrix

| Check ID | Subject kind / ID | Lens | Verdict | Product-visible constraint | Design owner | Regenerated evidence |
| --- | --- | --- | --- | --- | --- | --- |

## Next Step

- Use product-blueprint:design-acceptance. Conditional constraints must be absorbed before user approval.
""",
    "05-engineering-handoff.md": """---
planning-readiness: pending
---

# Product/Design Handoff

## Product Thesis

## MVP Loop

## User Journeys And Screen Map

## Product Non-Negotiables

## Mechanism Contracts For Engineering Review

## Backend/System Responsibilities And Invariants

## Approved Compromises

## Scope-Out Candidates

## Open Questions

## Journey Continuity Matrix

| Journey ID | Entry points | Surfaces | Actions | States | Operations | Recovery | Feasibility constraints |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Evidence Links

## Design Handoff Completeness Checklist

## Next Step

- Run product-blueprint:design-readiness at handoff stage. Stop after an approved pass by default; technical design is a separate, explicit workflow.
""",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Product or planning project name")
    parser.add_argument("--root", default="docs/product-planning", help="Output root directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--lite", action="store_true", help="Scaffold only the Lite-mode artifact set")
    mode.add_argument("--deep", action="store_true", help="Scaffold the full artifact set with Deep profile markers")
    parser.add_argument(
        "--with-design",
        action="store_true",
        help="Also add optional visual-design, prototype, acceptance, and handoff scaffolds",
    )
    args = parser.parse_args()
    if args.lite and args.with_design:
        parser.error("Lite stops at compact planning. Re-initialize or upgrade to Standard before --with-design.")

    target = Path(args.root).expanduser() / slugify(args.name)
    target.mkdir(parents=True, exist_ok=True)
    if args.with_design:
        (target / "screenshots").mkdir(exist_ok=True)
        (target / "prototypes").mkdir(exist_ok=True)
        (target / "tokens").mkdir(exist_ok=True)

    template_path = Path(__file__).resolve().parent.parent / "assets" / "templates" / "service-manifest.json"
    manifest = json.loads(template_path.read_text(encoding="utf-8"))
    manifest["project"]["name"] = args.name
    profile = "lite" if args.lite else "deep" if args.deep else "standard"
    manifest["project"]["mode"] = profile
    manifest["evidence"]["demo_file"] = f"prototypes/{slugify(args.name)}-demo.html"
    files = dict(FILES)
    workflow_state_path = Path(__file__).resolve().parent.parent / "assets" / "templates" / "workflow-state.json"
    workflow_state = json.loads(workflow_state_path.read_text(encoding="utf-8"))
    workflow_state["profile"] = profile
    workflow_state["locale"] = "ko" if re.search(r"[가-힣]", args.name) else "en"
    files["00-workflow-state.json"] = json.dumps(workflow_state, ensure_ascii=False, indent=2) + "\n"
    files["02.6-service-manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    product_definition_path = Path(__file__).resolve().parent.parent / "assets" / "templates" / "product-definition.json"
    files["02.1-product-definition.json"] = product_definition_path.read_text(encoding="utf-8")
    planning_review_path = Path(__file__).resolve().parent.parent / "assets" / "templates" / "planning-review.json"
    planning_review = json.loads(planning_review_path.read_text(encoding="utf-8"))
    planning_review["profile"] = profile
    files["02.05-planning-quality-review.json"] = json.dumps(planning_review, ensure_ascii=False, indent=2) + "\n"
    design_acceptance_path = Path(__file__).resolve().parent.parent / "assets" / "templates" / "design-acceptance.json"
    files["05-design-acceptance.json"] = design_acceptance_path.read_text(encoding="utf-8")
    visual_direction_path = Path(__file__).resolve().parent.parent / "assets" / "templates" / "visual-direction-review.json"
    files["03.4-visual-directions.json"] = visual_direction_path.read_text(encoding="utf-8")
    key_screen_path = Path(__file__).resolve().parent.parent / "assets" / "templates" / "key-screen-review.json"
    files["03.8-key-screen-review.json"] = key_screen_path.read_text(encoding="utf-8")

    PLANNING_FILES = {
        "00-brief.md",
        "00-decision-log.md",
        "00-workflow-state.json",
        "00-review-dashboard.html",
        "01.6-parallel-concepts.md",
        "01.8-positioning-brand.md",
        "02-mechanisms.md",
        "02-prd.md",
        "02.05-planning-quality-review.md",
        "02.05-planning-quality-review.json",
        "02.1-product-definition.json",
        "02.5-screen-contracts.md",
        "02.6-service-manifest.json",
        "02.7-feasibility-checkpoint.md",
        "02.8-undefined-surfaces.md",
        "03-storyboard.html",
        "03-design-brief.md",
        "04.2-backend-systems-brief.md",
    }

    LITE_FILES = {
        "00-brief.md",
        "00-workflow-state.json",
        "00-review-dashboard.html",
        "01-lite-direction.md",
        "02-lite-plan.md",
        "02.6-service-manifest.json",
        "03-design-brief.md",
    }

    DESIGN_FILES = {
        "03.5-art-direction-brief.md",
        "03.4-visual-directions.md",
        "03.4-visual-directions.json",
        "03.8-key-screen-review.md",
        "03.8-key-screen-review.json",
        "03.7-ux-writing.md",
        "04.1-visual-quality-gate.md",
        "04.3-design-system.md",
        "04.32-design-system-workbench.md",
        "04.36-clickable-demo.md",
        "04.4-prototype-test.md",
        "04.45-design-critique.md",
        "04.5-feasibility-review.md",
        "05-design-acceptance.json",
        "05-engineering-handoff.md",
    }

    selected_files = set(LITE_FILES if args.lite else PLANNING_FILES)
    if args.deep:
        selected_files.add("04.55-risk-register.md")
    if args.with_design:
        selected_files.update(DESIGN_FILES)

    for filename, content in files.items():
        if filename not in selected_files:
            continue
        path = target / filename
        if path.exists() and not args.force:
            continue
        path.write_text(content, encoding="utf-8")

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
