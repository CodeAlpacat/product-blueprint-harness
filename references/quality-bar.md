# Quality Bar — Is This Output Industry-Usable?

The completion judge for the whole harness. Run this at the end of `orchestrate` (and any time the user asks "is this done?"). Every check is a yes/no you can verify by opening a file — never grade with adjectives.

## How to use

For the current run mode, walk the applicable table. Report each row as **pass / fail / n.a. (scoped out)** with the file that proves it. A row you cannot prove with an artifact is a fail. "Conditional pass" does not exist at this bar — a known limitation is either fixed or explicitly recorded as ACCEPT-FLAG (see Retry Cap below).

## Bar 1 — Planning core (all modes, including Lite)

| # | Check | Proof artifact |
|---|---|---|
| 1 | Target user + core job + core loop stated in one screen of text | `00-brief.md` |
| 2 | Every user decision made so far is recorded with date; open decisions listed | `00-decision-log.md` |
| 3 | At least 2 direction alternatives were considered before lock (or user explicitly chose speed) | `01.6-parallel-concepts.md` |
| 4 | P0 scope enumerated; every P0 item classified (Core P0 / P0 support); non-goals listed | `02-prd.md` |
| 5 | Claims are labeled 관찰/사용자 확정/제안/가정/미확인 — no unlabeled reference claims | any research artifact |
| 6 | `00-review-dashboard.html` reflects the CURRENT state (not the init stub, not a stale phase) | dashboard |

## Bar 2 — Screens & flows (Standard/Deep)

| # | Check | Proof artifact |
|---|---|---|
| 7 | Every P0 screen has a contract: purpose, allowed/forbidden actions, entry/exit, states | `02.5-screen-contracts.md` |
| 7.5 | Service manifest contract-stage validator passes: stable IDs, bidirectional wiring, operation ownership, journeys/lifecycle, explicit exclusions | `02.6-service-manifest.json` + validator output |
| 8 | Entry/exit map connects every P0 screen with no dead ends; forbidden shortcuts enumerated | same |
| 9 | State matrix covers empty/loading/locked/error/success per screen where relevant | same |
| 10 | Storyboard shows every P0 screen as a legible frame with wiring annotations outside the mock UI | `03-storyboard.html` |
| 11 | Positioning + name direction + voice decided (or explicitly deferred by the user with a note) | `01.8-positioning-brand.md` |
| 12 | Feasibility checkpoint ran BEFORE visual design: every mechanism a P0 screen depends on has a verdict (feasible / conditional / infeasible), none silently dropped | `02.7-feasibility-checkpoint.md` |

## Bar 3 — Visual & design system (Standard/Deep)

| # | Check | Proof artifact |
|---|---|---|
| 13 | Art direction is numeric: OKLCH color roles + contrast targets, type ramp (size/lh/weight), spacing grid, radius roles, imagery treatment. Zero adjective-only rules | `03.5-art-direction-brief.md` |
| 14 | Tokens exist as machine files and are USED by the rendered artifacts (grep a token var in the html) | `tokens/` |
| 15 | **All-P0 coverage matrix**: every P0 surface/state from the service manifest appears in the workbench/demo AND passed the visual gate. A missing row = fail, not "propagated" | `04.32-design-system-workbench.md` §coverage |
| 15.5 | Prototype-stage validator passes: DOM surface/action/state IDs, transitions/effects, reachability, responsive evidence, no uncontracted/dead controls | validator output |
| 16 | Adversarial gate ran with fresh context; measurable checks (WCAG ratios, grid sampling, palette count, ≥3 type roles) recorded with numbers | `04.1-visual-quality-gate.md` |
| 17 | Non-happy states are RENDERED somewhere reviewable (states screen / state lab), not just listed in prose | workbench or demo |
| 18 | Screenshot evidence exists for every rendered artifact claim ("rendered and verified" without a screenshot = fail) | `screenshots/` |
| 19 | Survival tests pass: "is this a shadcn/SaaS starter?" and "could this screenshot be any product?" — both answered no, with the distinguishing elements named | gate artifact |

## Bar 4 — Handoff (Standard/Deep, before declaring done)

| # | Check | Proof artifact |
|---|---|---|
| 20 | Entity & State Contract present: entities + relationships (descriptive), per-screen state machines, invariants as testable assertions. No storage schema (that stays out of scope) | `05-engineering-handoff.md` |
| 21 | Handoff-stage validator generated a current manifest-hash-bound readiness report; dashboard/handoff consume it and do not self-declare readiness | `05-readiness-report.{json,md}` |
| 21 | Forbidden shortcuts restated as routing/model invariants a developer can enforce structurally | same |
| 22 | Risk register exists for policy/age/PII/moderation exposure with P0 mitigations (mandatory when the domain touches adult content, payments, minors, or UGC) | `04.55-risk-register.md` |
| 23 | Open questions and approved compromises are explicit — the developer knows what was decided vs deferred | handoff |
| 24 | A `Known Missing / Not Yet Explored` section exists. An output that claims nothing is missing fails this row | handoff or dashboard |

## Retry cap and ACCEPT-FLAG

Gates loop at most **3 fix cycles** per artifact. If a check still fails after 3, do not loop forever and do not silently pass: record **ACCEPT-FLAG** in the decision log — what failed, why it is being accepted, what would fix it later. ACCEPT-FLAG rows must be surfaced in the dashboard and the handoff. An unrecorded limitation is a lie; a recorded one is a decision.

## Verdict format

End with exactly one of:

- **READY** — all applicable rows pass (ACCEPT-FLAG rows listed).
- **NOT READY — N rows failing** — list the failing rows and the single next skill that fixes the most of them.

## Coverage additions (2026-07-10 dogfood — gaps the founder had to ask about)

- [ ] Responsive grammar rendered: desktop = mobile extended with an app max-width cap (the mobile-first cap pattern common in consumer apps), ≥3 screens drawn, derivation rule for the rest. No desktop-only grammar.
- [ ] Form controls enumerated Storybook-style (rendered states, not a legend) + written form validation policy.
- [ ] Wiring matrix (screen × action → destination; click-verified vs state-sample rows distinguished).
- [ ] Global fallbacks drawn: 404 · connection-lost/server-error (progress-preserved copy) · maintenance.
- [ ] Cross-cutting sheets drawn: guest lazy-auth · report · payment in-progress/done.
- [ ] `02.8-undefined-surfaces.md` registry exists with zero unclassified rows ("이 목록에 없는 화면 임의 생성 금지").
