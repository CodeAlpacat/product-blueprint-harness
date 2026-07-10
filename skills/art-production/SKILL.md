---
name: art-production
description: Runs a character/mood art production loop against a local or remote image-generation backend (ComfyUI/SDXL-class) — fixed-appearance prompt packs, a pilot round with board comparison, style-seed lock, batch generation, tag-corrected re-rolls, and demo wiring. Use when the planning package needs real launch art to replace placeholder imagery.
---

# Art Production — pilot → lock → batch → re-roll → wire

Art is generated, but taste is curated. The loop below produced a locked 24-shot roster in 3 pilot cycles during dogfood; codify it instead of improvising.

## Prerequisites

- Art direction brief + design system (image treatment rule — e.g., neutral originals, warm duotone applied in CSS).
- A roster list: character slug, age, 2–4 line fixed appearance, hero-scene one-liner, rating notes.
- A reachable generation backend (ask the user which; verify reachability before promising).

## 1. Prompt pack (`06.1-art-prompt-pack.md`)

- **One shared style prefix** (quality tags + rendering style + palette mood + product genre tag) — the style seed is this prefix + a fixed seed family, not luck.
- **Per-character fixed appearance block** — identical across that character's shots (identity consistency).
- **Shot templates**: card (3:4 bust, paper background) and hero (4:5, scene + narrative props). Fixed sampler/steps/cfg/sizes recorded in the pack.
- **Calibration rules learned the hard way (apply from round 1)**:
  - Age via explicit numbers ("29 years old adult male"), never adjectives — "young/bishounen" collapses to teenagers.
  - Uncorrected models drift toward the training mean (stubble/bulk/armor/neon). Write concept-negating negatives per character (clean shaven, no armor…) and relax them only where the drift IS the concept.
  - Ratings: art stays at suggestion/mood level unless the user explicitly decides otherwise; record the decision.

## 2. Pilot (2 characters × card+hero × 2 seeds)

Render a **duotone contact sheet** (apply the product's CSS treatment in the sheet) including any existing placeholder art for comparison. Judge per shot against the target audience persona — not "is it pretty" but "is it the contracted character". Verdict per shot: adopt / reject with the failure mode named.

## 3. Style-seed lock

Adopted pilot prefix+seed becomes the pack's confirmed §0. Failures get ONE calibrated re-roll round each (change the named failure tag only). **Cap: 3 cycles per character**, then ACCEPT-FLAG the best remaining (quality-bar rule).

## 4. Batch + re-roll

Queue the full roster with per-character age tokens. Curate on a contact sheet; re-roll only FAILs with corrected tags. Record PASS/FAIL verdicts and reasons in the decision log — reasons become new §0 calibration rules.

## 5. Promote + wire + gate

- Promote curated files to stable names `prototypes/assets/<slug>-{card|hero}.png` (raw candidates stay in `_pilot/`/`_batch/`).
- Rewire the demo/workbench to the final assets — grep to zero remaining placeholder references, keep character↔art mapping true to adjacent copy.
- Re-run the board render + visual gate. The demo's "temporary art" compromise note in the handoff flips to "final art wired".

## Next Step

- 다음 추천: `product-blueprint:visual-quality-gate` (배선 후 보드 스캔) → 핸드오프 갱신.
- 사용자가 결정할 것: 채택 컷 승인(특히 수위·연령 인상), 리롤 예산, 백엔드 선택.
