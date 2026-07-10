# Visual Quality Checklist — detailed gate checks

The itemized companion to `visual-quality-gate`. Every row is checkable by looking at a rendered screenshot or grepping the artifact — no adjective rows. Record pass/fail per row with where you saw it.

## A. Measurable (compute, don't eyeball)

- [ ] WCAG contrast per text pair: body ≥ 4.5:1, large display ≥ 3:1, on-accent text ≥ 4.5:1 (compute from the actual token values)
- [ ] Type: ≥ 3 distinct roles visible per screen; adjacent heading steps ratio ≈ consistent; body line-height fits the script (KR ≈ 1.6–1.7)
- [ ] Spacing: sample 10 gaps — all on the declared grid (e.g. 4px); off-grid values named or fixed
- [ ] Palette: ≤ 1 accent hue + neutrals + semantic states; count actual hues in the render
- [ ] Radius: role-consistent (thumb/card/sheet); no mixed-radius siblings
- [ ] Tokens actually used: grep the rendered file for token vars; hardcoded colors that bypass tokens = fail

## B. Slop signatures (from anti-slop-doctrine S1–S14 — scan each)

- [ ] No 2-stop gradient hero / glow / glassmorphism on content surfaces
- [ ] No oversized border-radius everywhere; no stadium pills as tabs/tags
- [ ] No in-app mega-hero with centered marketing copy
- [ ] No gray-box / placeholder art where the product depends on visual appeal
- [ ] No lorem/dummy strings ("Item 1", "홍길동님 안녕하세요")
- [ ] No rainbow accents; no default-shadcn look (the "any SaaS starter?" test)
- [ ] Imagery treatment uniform across all images (one filter recipe, stated)

## C. Contract fidelity

- [ ] Every P0 screen from `02.5-screen-contracts.md` appears (all-P0 coverage matrix — enumerate, don't sample)
- [ ] Transitions/entry/exit visible in wiring annotations OUTSIDE the mock UI
- [ ] No invented screens/features that aren't in the contract; no dropped contracted ones
- [ ] Forbidden shortcuts not violated by any CTA (e.g. no "start chat" on a card that must route through a gate)
- [ ] Non-happy states RENDERED: empty, loading (skeleton same shape as loaded screen), error/retry, locked, image-fallback
- [ ] Copy matches the microcopy sheet (`03.7-ux-writing.md`) verbatim where it exists; zero jargon-ban violations

## D. Craft

- [ ] One coherent content storyline threads the screens (not disconnected sample data)
- [ ] Focal hierarchy: each screen has one primary action; CTA count per screen ≤ 1 primary
- [ ] Alignment: edges align across sections (overlay a grid mentally on the screenshot)
- [ ] Density appropriate to the product (editorial vs dashboard); whitespace is doing hierarchy work
- [ ] The signature element (from art direction) appears and is doing narrative work, not decoration

## E. Evidence

- [ ] Every "rendered/verified" claim has a screenshot in `screenshots/`
- [ ] Full-viewport render (not a cropped corner); board/all-screens shot for coverage scans
- [ ] Verdict recorded with per-row results, not a summary adjective
