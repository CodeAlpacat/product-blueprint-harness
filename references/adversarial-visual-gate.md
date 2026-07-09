# Adversarial Visual Gate

The old gate failed because the model that produced the screen also graded it, against an adjective checklist, and passed its own slop. This reference replaces that with a gate that is (1) run by a fresh critic that did not generate the screen, (2) measurable, and (3) a loop that does not exit on "conditional pass".

## Principle

A generator is biased toward passing its own output. So the gate must be **adversarial** — its job is to *find reasons to reject*, defaulting to fail on doubt — and **externally anchored** — it judges against numbers and named signatures, not taste.

## Who runs it

Run the gate as a **fresh-context critic subagent** that receives only:
- the rendered screenshot(s) (desktop + mobile),
- the measured design spec + tokens,
- the screen contract (allowed/forbidden actions, states),

and **not** the generation conversation. Inside Claude Code, use a Task/subagent (or the `critique` + `audit` skills) with those inputs. The critic never sees the rationalizations that produced the screen.

## Check A — slop signature scan (from anti-slop-doctrine §2)

Scan the screenshot for each named signature S1–S14. For every one found, the critic must cite *where* it appears. Any confirmed signature = fail (or conditional only with an explicit, spec-justified reason).

Also run the two template tests:
- "Could this be any shadcn/Vercel/Linear/SaaS starter with content swapped?" → yes = fail (S3/§3).
- "Would a senior designer put this in a portfolio?" → no = fail.

## Check B — measurable conformance (compute, don't eyeball)

The critic verifies numbers against the spec:

- **Contrast**: compute WCAG ratios for `ink/surface`, `ink-muted/surface`, `accent-ink/accent`, and every text-on-color pair. Below target = fail. State each as `X on Y = N:1`.
- **Type scale**: heading steps follow the spec ratio and are consistent; ≥3 distinct roles present; no "two sizes of one weight" (S10).
- **Spacing grid**: sampled gaps/paddings are on the 4px scale; flag off-grid values (S11).
- **Radius**: a scale-by-role is used, not one radius everywhere (S3).
- **Palette count**: distinct base hues ≤ 3 + semantic (S14).
- **Legibility**: smallest text is readable in the delivered screenshot at 1x.

## Check C — completeness (product, not just pretty)

- **Focal point**: one clear focal element resolvable in <1s.
- **States**: required non-happy states rendered (loading, empty, locked, error+retry, paid, success, correction, overflow, image-fail). Missing state = fail for that surface.
- **Flow fidelity**: screen preserves the contract's allowed/forbidden actions and entry/exit; no mechanism promoted to a surface it shouldn't own (e.g. persona → home tab).
- **Imagery**: art-directed treatment applied; no placeholder wells (S7).
- **Copy**: real product vocabulary in every string; no lorem/"Card Title" (S13).

## Verdict format

The critic outputs, per screen:

```
Verdict: PASS | CONDITIONAL | FAIL
Slop signatures found: [S#: location, ...]  (empty on pass)
Measured violations: [check: expected vs actual, ...]
Missing states / completeness gaps: [...]
Template test: pass/fail + why
Required fixes (ranked): [...]
```

## Loop protocol (the part that was missing)

- **CONDITIONAL is not PASS.** Do not advance to workbench/propagation on conditional. Return the ranked fixes to the craft loop, fix, re-screenshot, re-gate.
- **Loop until clean**, up to a sane cap (≈4 rounds on the ceiling screen). If still failing after the cap, stop and surface to the user with the specific unresolved signatures — do not quietly pass it.
- **Anchor future screens.** Once the ceiling screen passes, it becomes the reference specimen. Every propagated screen is gated against the same checks; a screen that regresses below the anchor fails.
- **Never let polish hide uncertainty.** If a product/flow decision is unresolved, the gate says so; it does not accept a prettier screen as a substitute for the decision.

## Honesty rules

- Report what was actually rendered and screenshotted. "Looks good" without a browser screenshot is not a gate result.
- If a signature is present but intentionally chosen (e.g. one gradient as a justified art-direction device), it must be named in the spec as an exception, not silently allowed.
- Do not downgrade a required state or surface to make the gate pass.
