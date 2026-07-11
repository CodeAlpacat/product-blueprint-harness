---
name: positioning-brand
description: Positioning statement, product naming with user taste-first iteration and availability signals, brand voice and tone, and mascot/wordmark direction. Use after direction lock and before art direction, or when the user asks to name the product, define the brand, pick a mascot, or write the tagline.
---

# Positioning & Brand

Turn the locked direction into a positioning statement, a name, a voice, and a visual identity direction — BEFORE art direction, because the name/mascot/voice constrain the visual world (wordmark typography, mascot palette, copy tone in every mockup).

## Inputs

- `00-decision-log.md` (direction lock), `01.6-parallel-concepts.md`, `01.5-reference-deconstruction.md` (competitor names/voices)

## Output

`01.8-positioning-brand.md` with the sections below. Update `00-decision-log.md` with a `BRAND-LOCK` entry when the user confirms.

## 1. Positioning

- One-sentence positioning: for WHOM, the product does WHAT, unlike WHOM/WHAT.
- Contrast position vs the 2–3 nearest references (from deconstruction) — what we deliberately do differently.
- Tagline candidates (2–3, mark as 후보 until user confirms).

## 2. Naming — taste first, availability second

Naming fails when run in the wrong order. The proven order:

1. **Ask the user's taste constraints first**: syllable count, language feel (KR/EN/coined/compound), reference names they like, sounds to avoid. Do not generate 20 names before this.
2. **Generate 3–5 candidates per round, judged on 어감 (sound/feel) with the user** — present with pronunciation, association, and a one-line rationale each. Iterate rounds until the user reacts positively to 1–2. Expect multiple rounds; a rejected round is signal, not failure — record WHY each was rejected (it narrows the space).
3. **Only then research availability signals** for the survivors: app-store search collision, dominant IP/brand collision (mascots too — an animal can be "taken" by a famous character), domain/social handle, phonetic neighbors that cause confusion. Use a fresh research agent when available.
4. Present the shortlist as a table: name | 어감/연상 | availability signals | risk notes. User picks.
5. **Always flag**: signal research ≠ trademark clearance. Before spending money (domain, filing, store listing) the user needs a real KIPRIS/USPTO + store search. Write this warning into the artifact.

Anti-patterns: generating names by availability first (survivors have bad 어감); locking a generic dictionary word without noting SEO/ownership weakness; picking a mascot animal without checking dominant IP.

## 3. Voice & Tone (one-pager)

- 2–3 voice rules with a do/don't example each (e.g., "plain UI labels in user language; evocative copy only where content lives").
- Jargon ban list: internal planning terms that must never reach UI copy, with the user-facing word for each (e.g., persona → 나의 설정).
- Tone for sensitive surfaces if relevant (adult gates, payments, errors): calm, safety-framed, never coy.

## 4. Mascot / Wordmark direction (when the product wants one)

- Mascot: which animal/figure, why (meme energy, audience fit, IP whitespace), and the palette rule — **the mascot lives inside the existing token palette, zero new colors**.
- Wordmark: typography family (inherits art-direction display face), casing, accent usage.
- Usage boundaries: where the mascot appears (onboarding, empty states, long loading) and where it never appears (core content surfaces, chat/detail) — mascots that appear everywhere cheapen the product.
- Motion signature if any (one loop, duration, easing) — motion only in waiting states.

## Gate (before art direction consumes this)

- [ ] Positioning sentence approved or explicitly deferred by the user
- [ ] Name: locked, or shortlist + availability signals recorded with the trademark warning
- [ ] Voice one-pager exists with do/don't examples
- [ ] Decision log updated

## Next Step

- 다음 추천: `product-blueprint:experience-mechanisms` (Standard order) — 또는 이름이 이미 확정돼 시각으로 직행할 때는 `product-blueprint:art-direction-brief`.
- 사용자가 결정할 것: 이름 확정 여부 / 태그라인 / 마스코트 채택.
