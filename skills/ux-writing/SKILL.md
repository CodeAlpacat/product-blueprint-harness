---
name: ux-writing
description: Voice-and-tone application and microcopy sheet covering labels, empty states, errors, loading, confirmations, and CTA verbs for every P0 screen. Use after art direction and before or during the workbench/demo, or whenever UI copy reads like internal jargon, placeholder text, or inconsistent tone.
---

# UX Writing — microcopy as a deliverable, not an afterthought

Copy is UI. A screen with placeholder copy is an unfinished screen; a label that leaks internal jargon breaks trust. This skill turns the brand voice (from `01.8-positioning-brand.md`) into the actual words on every P0 screen.

## Inputs

- `01.8-positioning-brand.md` (voice rules + jargon ban list), `02.5-screen-contracts.md` (human explanation), `02.6-service-manifest.json` (P0 surface/action/state IDs), `02-mechanisms.md` (what the product promises)

## Output

`03.7-ux-writing.md` — the microcopy sheet. Downstream (workbench, clickable-demo) must use these strings verbatim; if a mockup needs a string that isn't here, add it here first.

## The sheet

Per P0 surface ID, a table: action/state ID | element | copy (user language) | tone note. Must cover:

1. **Labels & navigation**: every tab, button, and section header. User language only — apply the jargon ban list (internal concept names never surface).
2. **Empty states**: a real sentence + a next action for every empty in the state matrix. Never "No data". Good empties acknowledge the moment ("아직 시작한 이야기가 없어요") and offer one door.
3. **Errors & recovery**: what happened, what it cost the user (be explicit when it cost nothing: "별은 차감되지 않았어요"), and the retry action. Never blame the user.
4. **Loading & waiting**: what is happening; when to say nothing (short waits = skeleton only, no copy).
5. **Confirmations & destructive actions**: what will happen, what is reversible, the honest cost (paid actions always show price BEFORE the tap).
6. **Gates & sensitive surfaces** (age verification, payments, permissions): calm, factual, safety-framed. State what is stored and what is discarded.
7. **CTA verb list**: the canonical verbs (start, continue, save…) in the product's voice — one verb per meaning, reused everywhere.

## Rules

- Evocative/branded copy lives only where content lives (content titles, story text); interface copy is plain.
- Consistency beats cleverness: the same action uses the same verb on every screen.
- Write in the product's shipping language; do not draft in English and translate.
- Every mechanism promise in `02-mechanisms.md` that reaches the UI needs its user-facing phrasing decided here.

## Gate

- [ ] Every manifest P0 surface has its rows; every required state/action that shows text has copy keyed by the same ID
- [ ] Zero jargon-ban violations (grep the ban list against the sheet)
- [ ] Paid/destructive/verification moments disclose cost/consequence in the copy itself

## Next Step

- 다음 추천: `product-blueprint:design-system-workbench` 또는 `product-blueprint:clickable-demo` — 이 시트의 문자열을 그대로 사용.
- 사용자가 결정할 것: 톤 방향 승인, 브랜드 카피 후보 선택.
