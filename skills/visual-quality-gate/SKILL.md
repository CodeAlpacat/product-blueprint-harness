---
name: visual-quality-gate
description: Reviews and hardens visual direction before production design, preventing AI-slop storyboards, generic mockups, weak design systems, and fake high-fidelity UI. Use after storyboard and before design-system approval when the user cares about production-grade design quality, reference fidelity, art direction, or avoiding generic AI aesthetics.
---

# Product Blueprint Visual Quality Gate

Use this as a gate, not as decoration. It decides whether the current visual direction is strong enough to become a production design brief.

## Run It Adversarially — Not As Self-Grading

The gate is worthless if the model that produced the screen also grades it against an adjective list; it will pass its own slop (this is a common failure — weak output slips through as "conditional pass"). Follow `${CLAUDE_PLUGIN_ROOT}/references/adversarial-visual-gate.md`:

- **Fresh critic.** Run the gate as a fresh-context subagent (or the `critique` + `audit` skills) that receives only the rendered screenshots, the measured spec/tokens, and the screen contract — **not** the generation conversation. Its job is to find reasons to reject; default to fail on doubt.
- **Measurable, not vibes.** Compute WCAG contrast for each text pair, check the type-scale ratio, sample spacing for off-grid values, count palette hues, and scan for each named slop signature S1–S14 in `${CLAUDE_PLUGIN_ROOT}/references/anti-slop-doctrine.md`. Cite where each finding appears.
- **Two template tests.** "Could this be any shadcn/SaaS starter with content swapped?" and "Would a senior designer put this in a portfolio?" A wrong answer to either = fail.
- **Loop until clean, capped.** CONDITIONAL is not PASS — return ranked fixes to the craft loop, fix, re-screenshot, re-gate. Cap at **3 fix cycles** per artifact; still failing → record **ACCEPT-FLAG** in the decision log (what failed, why accepted, later fix) and surface it in the dashboard — never quietly pass, never loop forever (`references/quality-bar.md`).
- **Browser proof required.** "Looks good" without a real screenshot is not a gate result.

## Two scan modes

- **Ceiling scan** (one screen, deep): full pass list below on the single decisive screen — run during the craft loop.
- **All-P0 board scan** (breadth): after the workbench/clickable-demo exists, screenshot the board/all-screens view and check EVERY P0 surface/state from `02.6-service-manifest.json` against the rendered coverage matrix. A P0 surface with no rendered artifact = fail; "propagated from the ceiling" without a render is not coverage. Also scan cross-screen coherence: same tokens, same imagery treatment, one storyline.

## Output Language And Stage Exit

- Default to the user's conversation language.
- If the user is Korean, write the verdict, findings, risks, and next-step guidance in Korean.
- End with:
  1. `지금 확인할 산출물`
  2. `사용자가 결정할 것`
  3. `수정이 필요하면 어디를 바꿀지`
  4. `다음 추천 스킬`

## Inputs

- Product thesis and audience
- Reference screenshots and benchmark notes
- PRD and mechanism contracts
- Storyboard
- Any visual mockups, style tiles, or design-system draft

## Review Passes

1. **Reference fidelity**: Does the visual plan preserve the reference product's real flow and interaction model, or did it invent a prettier but wrong flow?
2. **Audience fit**: Does the tone match the actual user context and emotional job?
3. **Product specificity**: Could this design be reused for a random SaaS dashboard? If yes, fail.
4. **AI-slop scan**: Check generic gradients, glassmorphism, identical cards, ungrounded illustrations, fake data, weak typography, one-note palettes, decorative blobs, and unreadable screenshots.
5. **Mechanism surfacing**: Are memory, judging, scoring, paid actions, ranking, or recommendations surfaced only where needed, and recoverable when they fail?
6. **State coverage**: Check empty, loading, locked, paid, error, unsafe, result, retry, and correction states.
7. **Handoff usefulness**: Can a human designer or frontend team understand what to design next without guessing?
8. **Entry-gate fidelity**: For character-chat products, does the design preserve `character detail -> persona/setup -> chat room`, and avoid turning persona into home/nav?
9. **Flow wiring**: Does every priority frame have entry, user decision, primary exit, and next frame as annotations outside the mocked product UI?
10. **Scope discipline**: Are P1/P2 ideas kept out of the P0 main flow unless the user approved them?
11. **Core surface completeness**: Are obvious category basics such as search, detail tabs, states, and recovery surfaces present or explicitly scoped out?
12. **Artifact fidelity choice**: Is the artifact using the right medium for the stage: HTML for storyboards/flow boards, React workbench for tokens/components/states/P0 screens, and optional React specimens for pixel-level screen passes?

## Pass / Fail

Pass only if:

- Reference-based screens are not flow-inaccurate.
- Screenshots are readable and uncropped when used as evidence.
- The design has a named art direction tied to product behavior.
- Major components and states are accounted for.
- Trust-critical mechanisms are visible, inspectable, or recoverable at the right moment, without taking over screens where they are only background behavior.
- A critique pass lists remaining weaknesses honestly.
- The user can tell which artifact to review next and what decision is needed.

Fail if:

- It looks like a generic AI-generated mockup.
- It hides product uncertainty behind polish.
- It has screens without states or state transitions.
- It omits a category-baseline surface without explicitly scoping it out.
- It turns an unconfirmed feature interpretation into a P0 screen.
- It invents or drops a surface/action/state relative to the service manifest, even when the invented design looks better.
- It uses reference screenshots but misses scroll/tab content that affects product structure.
- It uses abstract placeholders where the product's core appeal depends on visual assets.
- It does not show entry/decision/next wiring for priority frames, or puts those planning labels inside the mocked product UI instead of outside frame annotations.
- It has design tokens without actual product usage.
- It claims production quality without browser screenshot verification.
- It treats a convenience HTML storyboard as final production UI.
- It claims production design with only one polished screen while the component catalog, state lab, and P0 screen set are missing.

## Output

Create `04.1-visual-quality-gate.md` with:

- Verdict: pass or fail (plus any ACCEPT-FLAG rows — "conditional pass" is not a verdict)
- All-P0 coverage matrix result (board scan)
- AI-slop findings
- Reference fidelity issues
- Product-specific art direction
- State and mechanism gaps
- Required revisions before production design

Use `references/visual-quality-checklist.md` for detailed checks.

## Next Step

- If the verdict is fail, revise `product-blueprint:art-direction-brief`, `product-blueprint:screen-contract`, or the prototype before continuing.
- If the verdict is pass (including pass with recorded ACCEPT-FLAG rows), use `product-blueprint:backend-systems-brief` and `product-blueprint:design-system`.
- If design quality is the main risk, follow the design-system brief with `product-blueprint:design-system-workbench` before engineering handoff.
