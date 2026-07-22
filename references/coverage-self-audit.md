# Coverage Self-Audit — the developer-lens gap scan (run it BEFORE the user has to ask)

Dogfood evidence (2026-07-10): three separate founder questions — "where are the desktop layouts and side panels?", "desktop should extend mobile with a max-width cap", "where is the Storybook-style state enumeration?" — each hit a real P0 gap the harness had not caught. The pattern to kill: **gaps surface only when the founder asks**. This audit makes the harness ask first.

## When

Mandatory once per run, after the clickable demo exists and BEFORE `engineering-handoff` declares readiness. Re-run after any screen-set change.

`02.6-service-manifest.json` is the enumerated set. This audit may discover and classify missing surfaces, but every closure must update the manifest; the registry is not a second wiring SoT.

## The scan (all six, yes/no + evidence path)

1. **Responsive grammar rendered?** Desktop views exist for at least discovery, detail, and the core-action screen — drawn as *the mobile experience extended* (app max-width cap, single breakpoint, nav promotion, content column keeps the mobile layout; a persistent side panel is allowed only as the opened form of an existing mobile sheet). Screens not drawn must be covered by an explicit derivation rule. "Desktop-only grammar" (new grids, split layouts) fails.
2. **Component/form states enumerated Storybook-style?** Every form control × every state (default/focus/filled/error+message/disabled; counters; locked-not-disabled choice cards; toggle/checkbox incl. required-unchecked; button pending; toast success/error; destructive confirm dialog) is RENDERED, not listed as a legend. A form validation policy (when to validate, submit-with-missing-required behavior, save model per surface, destructive confirmation) is written.
3. **Wiring matrix complete?** A screen × action → destination table exists, distinguishing click-verified transitions from state-sample-contracted ones. Script-verify the demo against it.
4. **Global fallbacks + cross-cutting sheets drawn?** 404, connection-lost/server-error (with progress-preserved copy), maintenance; lazy-auth sheet for guests; report sheet; payment in-progress/done. Rendered in the states sample or as screens.
5. **Form policy honored by every drawn form?** Required-missing, over-limit, and error copy follow the written policy (plain-language cause + next action).
6. **Undefined-surface registry written?** See below — the single most important output.

## Output: `02.8-undefined-surfaces.md` (the anti-improvisation registry)

Developers improvise screens that were referenced but never defined. Enumerate every surface any artifact points to (an action, a "보기/관리" link, a contract exit path) and classify each:

- **정의됨** — contract + demo/state-sample exists (evidence path).
- **규칙 파생** — not drawn, but derivable from a stated rule (name the rule; e.g., "document viewer = plain text page, style §X").
- **미정의 → 지금 계약** — add a 3-line mini-contract (목적/허용/금지) on the spot. Most gaps close in 3 lines.
- **P1 명시 이연** — deferred on purpose, with the note "P0에서 이 진입점은 어떻게 보이는가" answered.

Registry header must say: **"이 목록에 없는 화면을 개발 중 임의 생성하지 말 것 — 발견 시 목록에 추가하고 확인 요청."**

## Gate

Handoff readiness fails while any scan item is "no" without an ACCEPT-FLAG, or while the registry has an unclassified row. Surface the registry in the decision dashboard ("남은 갭" section).

After closing the registry, run the prototype-stage validator. A prose audit cannot self-upgrade missing DOM/transition evidence:

```bash
python3 <plugin-root>/scripts/validate_service_blueprint.py <planning-dir> --stage prototype
```
