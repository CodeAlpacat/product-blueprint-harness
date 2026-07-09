# Anti-Slop Craft Doctrine

This is the master reference for producing production-grade UI instead of AI slop. Every visual-craft skill in this plugin points here. Read it before art direction, token work, screen craft, or the visual quality gate.

The old failure mode of this plugin: quality was described in adjectives ("senior handoff", "not generic") and the same model that produced slop self-graded against that adjective list. This doctrine replaces adjectives with **named slop signatures, measurable checks, positive craft moves, and an adversarial gate**.

## 1. Why AI produces slop

An LLM asked to "design a nice UI" samples the center of its training distribution. The center is the most-repeated tutorial/starter/Dribbble output on the internet. So "nice UI" collapses to a small set of recognizable defaults. Slop is not ugliness — it is **mode collapse to the average**. The fix is never "try harder to be pretty"; it is to (a) remove the defaults, (b) inject product-specific constraints with numbers, and (c) push past the first sample with iteration and an adversarial critic.

Corollary: **taste does not transfer through adjectives.** "Elegant, modern, premium" produce slop because the model already thinks its average output is elegant/modern/premium. Taste transfers through *constraints and references with numbers*: this exact type ramp, this exact grid, this reference's exact spacing, this forbidden pattern.

## 2. Slop signature taxonomy — detect and kill

Each signature below is a concrete visual pattern, why it reads as AI, and the craft move that replaces it. The visual quality gate scans for these by name.

| # | Slop signature | Why it reads as AI | Craft replacement |
|---|---|---|---|
| S1 | Gradient hero band / mesh gradient / aurora blur behind text | Default "make it look designed" move; appears in 90% of AI landing pages | Flat, intentional surface. If depth is needed, use one real material (paper grain, hairline, a single elevation step), not a glow. |
| S2 | Glassmorphism (blurred translucent cards) everywhere | 2021 iOS-tutorial default | Opaque surfaces with a defined elevation token. Reserve blur for one deliberate overlay, never for content cards. |
| S3 | Everything rounded (radius ≥ 12–16px on every element) | "Friendly SaaS" default | A radius *scale* (e.g. 0 / 4 / 8 / full) applied by role. Data tables and dense lists often want 4px or square. |
| S4 | Pill overload — tags, filters, tabs, chips all identical stadium shapes | The model reuses one shape for every taxonomy | Differentiate by role: tabs = underline/segment, filters = square token, tags = text with a leading dot or hairline, status = colored dot. |
| S5 | Oversized centered hero text inside an app workflow | Landing-page grammar leaking into product UI | App headers are left-aligned, ~20–28px, functional. Big editorial type is for marketing surfaces only. |
| S6 | Identical repeated cards (icon + heading + one paragraph) in a 3-col grid | "Features section" template | Vary the module. Real products mix list rows, hero item, dense grid, and editorial cards by information priority. |
| S7 | Blank gradient image wells / obvious placeholder art / stocky AI portraits dumped raw | Model can't source real imagery so it fakes it | Art-directed image treatment: fixed aspect + crop rule + overlay/duotone/grain so imagery reads as *intentional editorial art*, not a placeholder. For image-heavy products the art IS the product — treat it. |
| S8 | Purple→blue / teal→indigo tech gradient palette | The single most-sampled "AI palette" | A product-derived palette with named roles and measured contrast. Never a two-stop tech gradient as the brand. |
| S9 | Emoji as iconography / emoji section headers | Chat-model default for "friendly" | A real icon set (Lucide/Radix icons) used consistently, or no icon. Emoji only if the product itself is emoji-native. |
| S10 | Weak type: one family (Inter/Geist), 2 sizes, everything 400–600 weight, tight default line-height | Model uses the framework default font untouched | A real type system: named ramp with distinct display/body/data roles, deliberate weight contrast, measured line-height per role, optical tracking on large sizes. |
| S11 | Uniform 16/24px padding everywhere, no rhythm | No spacing system, just a default | A spacing scale on a 4px grid, applied so density communicates hierarchy (tight in data, generous around focal content). |
| S12 | Center-everything layout, symmetric, no tension | Safe default composition | Deliberate asymmetry, a dominant focal element, alignment to a real column grid, intentional negative space. |
| S13 | Fake precision: lorem-ish copy, "Lorem", "Card Title", "12,345", stock numbers | Placeholder content never replaced | Real product vocabulary and plausible domain content in every string, number, and state. |
| S14 | Rainbow of accent colors / every card a different hue | No color discipline | One accent with a defined use, semantic colors reserved for state (success/warn/danger/locked/paid). |

## 3. The shadcn / component-library sameness trap (and the defense)

Adopting shadcn/ui + Radix is correct for behavior and accessibility, but shadcn has its **own** slop signature: the New-York/zinc/neutral default skin with Geist, `rounded-md`, `border-border`, muted-foreground everywhere. A shadcn app left on defaults is instantly recognizable — "slop v2." The substrate must never ship its defaults.

Defense — three separations, enforced:

1. **Behavior ≠ skin.** Take Radix primitives (focus management, keyboard nav, ARIA, portal/overlay logic) and shadcn's component *structure*. Then **strip the default theme entirely**: replace the token layer, the font, the radius scale, the border treatment, and the spacing. shadcn is the skeleton; your measured design spec is the skin. If a reviewer can name "this is a shadcn starter" from the look, the skin was not replaced.
2. **Tokens are the differentiator, and they come from art direction, not defaults.** Your OKLCH palette is derived from the product's art direction (see `token-substrate.md`), not `zinc`. Your type is a chosen family with a real ramp, not Geist untouched. Your radius/density/elevation/motion are product decisions. The default gray ramp and default radius are banned starting values.
3. **The signature element breaks the template read.** Art direction defines one recurring product-specific visual device (a route line, a ledger rule, a spine/tab motif, a stamp). It must appear across surfaces so the UI reads as *this product*, not *a component kit*. Generic kit + one strong signature + product content = not-a-template.

Gate test for this trap: **"Could this exact screen be any shadcn/Vercel/Linear starter with the content swapped?"** If yes, fail — the skin/tokens/signature did not do their job.

## 4. Positive craft — what senior work actually does

Slop-avoidance is necessary but not sufficient. Production-grade work also does these, and the gate checks for their presence, not just slop's absence:

- **One clear focal point per screen**, established by size/contrast/position — the eye knows where to land in <1s.
- **Type hierarchy you can read as a wireframe** — remove color and imagery and the structure is still obvious from type and space alone.
- **A real grid.** Columns, consistent gutters, aligned edges. Nothing floats.
- **Density that matches the job.** Discovery scans dense; a reading/chat surface breathes; a data surface is compact and aligned. One density for everything is slop.
- **Color earns its place.** Mostly neutral surface; accent and semantic colors used sparingly and meaningfully so they actually signal.
- **Every state designed**, not just the happy path: loading/skeleton, empty (with a real first-run message), locked/safety, error+retry, paid confirmation, success, correction/recovery, long-content overflow, image-load-failure.
- **Motion explains**, it doesn't decorate: state changes, spatial transitions, and feedback on action — never gratuitous parallax/float.
- **Copy is product-specific and does work** — labels, empty states, and errors are written, not lorem.

## 5. Iteration beats one-shot

The first render is a draft, never the deliverable. Real quality is layered passes, each a discrete edit + screenshot: **structure → layout/grid → typography → color → density/polish → distinctiveness push**. See `craft-loop.md`. A screen that was generated once and never re-critiqued is, by definition, the training-average sample.

## 6. Delegate craft to the proven design skills

When running inside Claude Code, do not hand-improvise the craft. Delegate to the environment's design skills, which are engineered against exactly these signatures:

- `impeccable` (a.k.a. `craft`) — shape-then-build distinctive, non-generic UI; the primary craft engine.
- `layout`, `typeset`, `colorize`, `distill` — the per-pass craft moves in section 5.
- `bolder` / `ui-redesign` — push a safe/flat result past the template read.
- `critique`, `audit`, `polish` — the review + final pass.

The blueprint skills own **product logic, IA discipline, states, and the measured spec/gate**; the design skills own **pixel craft**. Keep that division.

## 7. The two survival questions

Before any visual artifact is called "pass":

1. **Would a senior product designer put their name on this in a portfolio?** Not "is it fine" — is it *intentional and distinctive*.
2. **Strip the content: could this be any starter template or SaaS dashboard?** If yes, the design has no product point of view yet.

If either fails, it is a draft, not a deliverable. Loop.
