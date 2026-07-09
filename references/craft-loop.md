# Craft Loop — layered passes, not one-shot

Production-grade screens are not generated in one pass. The first render is the training-average draft. Quality comes from **discrete layered passes, each an edit + a fresh browser screenshot**. This reference defines the loop the hi-fi-screen and workbench skills run.

## Establish the ceiling on ONE screen first

Do not render all P0 screens at mediocre quality simultaneously. Pick the single most decisive screen — the one carrying the highest product/design risk for *your* product (e.g. discovery/home or the `detail → persona gate → chat` entry for character-chat; the transaction/checkout for commerce; the primary dashboard for a data product) — craft it to the bar, pass the adversarial gate, and **only then** propagate the passing system to the other screens. One screen at the ceiling beats eight screens at the average.

## The passes

Run these in order. Each pass = one focused change set, then re-screenshot and look. Delegate the craft to the named Claude Code design skills when available; they are engineered against the slop signatures.

1. **Structure** — content and hierarchy only, no styling. What is the one focal element? What is the information order? Get the wireframe-level hierarchy right (readable as structure with zero color/imagery). Skill: `impeccable`/`craft` (shape step).
2. **Layout & grid** — real columns, gutters, alignment, deliberate asymmetry, negative space. Kill center-everything (S12). Skill: `layout`.
3. **Typography** — apply the measured type ramp; establish ≥3 distinct roles; weight/size/line-height/tracking per spec. Skill: `typeset`.
4. **Color & material** — apply OKLCH tokens; mostly-neutral surface, accent used sparingly, semantic colors for state only; hairlines over shadows; no gradient hero (S1/S8). Skill: `colorize`.
5. **Imagery** — apply the image treatment spec (aspect, crop, overlay/duotone/grain) so art reads as one editorial world, never placeholder (S7). Use real/generated assets, not gray wells.
6. **Density & polish** — spacing on the 4px grid, optical alignment, consistent radius-by-role, remove clutter. Skills: `distill`, `polish`.
7. **Distinctiveness push** — if it still reads as a template, push it: strengthen the signature element, add one memorable-but-functional move. Skill (if available): `bolder`. Then re-check it did not reintroduce slop.

## States are part of craft, not an afterthought

Before a screen is "done", render its non-happy states as part of the same specimen: loading/skeleton, empty (real first-run copy), locked/safety, error+retry, paid confirmation, success, correction/recovery, long-content overflow, image-load-failure. A happy-path-only screen is incomplete.

## Fidelity rules (so good design isn't destroyed by bad rendering)

- Render each screen **full-size at real viewport** — mobile 390×844, desktop 1440-wide — one screen per view. Never tile P0 screens into tiny phone frames inside a grid; that destroys fidelity and hides slop.
- Screenshot at 2x. Verify text is legible in the delivered screenshot (unreadable text is itself a gate failure).
- Planning labels, arrows, and critique notes live **outside** the product frame. The mocked screen contains only plausible user-facing UI.

## Loop exit

Exit a screen only when it passes the adversarial visual gate (`adversarial-visual-gate.md`), not on the first "looks fine". Conditional-pass is not pass. If the gate finds a slop signature or a measured-spec violation, fix and re-screenshot. Expect 2–4 loops on the ceiling screen.

## Division of labor

- This plugin's skills own: product logic, IA, screen contracts, states, the measured spec, and the gate.
- The Claude design skills own: the pixel craft in passes 1–7.
- Do not let the design skills change product IA (e.g. promote persona to a home tab) for visual convenience — the screen contract wins.
