# Figma-informed design and prototyping model

This workflow borrows Figma's useful organizational model without requiring Figma, Storybook, or Code Connect.

Official research basis:

- Pages organize milestones, components, explorations, and development-ready designs; sections group and label review/handoff regions: https://help.figma.com/hc/en-us/articles/15297425105303-Explore-design-files
- Prototype flows have named starting points and connected frames, and one page can hold multiple user journeys: https://help.figma.com/hc/en-us/articles/360039823894-Create-and-manage-prototype-flows
- Components expose intentional boolean, text, instance-swap, slot, and variant properties instead of arbitrary layer overrides: https://help.figma.com/hc/en-us/articles/39636407507735-Components-collection-Component-property-fundamentals
- Variants organize state, size, and visual roles and are intended to move design components closer to frontend code: https://help.figma.com/hc/en-us/articles/360056440594-Create-and-use-variants
- Variables and modes switch themes, locales, device spacing, and prototype state from reusable values: https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma
- Code Connect maps design properties to real component props. It is optional inspiration, not a dependency of Product Blueprint: https://developers.figma.com/docs/code-connect/react/
- Figma AI uses First Draft for editable early exploration, can replace placeholder content, add interactions, and rename layers: https://help.figma.com/hc/en-us/articles/23870272542231-Use-AI-tools-in-Figma-Design
- Figma Make generates functional code prototypes from designs and context, but its downloaded-code edits do not automatically round-trip back into Make: https://help.figma.com/hc/en-us/articles/35710574222487-Beyond-the-basics-Using-Figma-Make
- Figma's 2026 code-to-canvas workflow recommends a real-code prototype playground, visual review on canvas, and token synchronization rather than leaving AI code disconnected from the design system: https://help.figma.com/hc/en-us/articles/40219873508247-Release-notes-roundup-May-2026

## React equivalent

| Figma concept | Product Blueprint React artifact |
| --- | --- |
| Page | board group or exported route: Foundations, Components, Patterns, Depth 1, Depth 2, Overlays, Flows, Archive |
| Section | labeled review section with purpose, status, owner, and evidence outside product UI |
| Main component | one reusable React component source with a stable component ID |
| Instance | that component imported by boards and product screens |
| Variant/property | explicit typed props and documented allowed values; avoid one component per boolean combination |
| Variables/modes | CSS variable collections and fixture modes for theme, viewport, locale, density, and state |
| Prototype flow | named React flow starting point plus reachable screen/action/state graph |
| Dev Mode handoff | source refs, prop mapping, token refs, screenshots, and acceptance hashes |

## Board order

1. `00 Cover / review status`
2. `01 Reference evidence / explorations`
3. `02 Foundations / brand / tokens / modes`
4. `03 Components / variants / properties / states`
5. `04 Patterns`
6. `10 Global shell + Depth 1`
7. `20 Depth 2`
8. `30 Overlays / sheets / modals`
9. `40 Named prototype flows and exception paths`
10. `90 Archive / rejected directions`

Do not collapse the board into a gallery of unrelated pretty screens. Every screen imports component instances, every flow has a named start, and every accepted mode/state is reproducible.

## AI-assisted design policy

Use AI to widen and accelerate the design process, not to self-approve its first output.

1. **First-draft exploration**: generate 2–3 materially different directions from the same screen contract. Treat them as editable exploration, never the baseline.
2. **Context before generation**: provide reference evidence, brand rules, screen contract, existing components/tokens, real copy, and negative constraints. A prompt without this context is expected to collapse to generic UI.
3. **System-constrained assembly**: once direction is locked, AI may assemble only from accepted React components, props, tokens, patterns, and fixtures. A missing component returns to the component board; it is not improvised inside one screen.
4. **Realistic content**: use AI to replace duplicate placeholders with long, short, empty, error, and localized content before layout approval.
5. **Interaction assistance**: AI may wire named flow starts and transitions, but deterministic reachability and exception-path audits still decide pass/fail.
6. **Organization assistance**: AI may name sources, layers, component IDs, and evidence, but stable user-approved names are not silently rewritten.
7. **Point-and-revise loop**: feedback targets a component, section, screen, or flow ID; revise the earliest owner and regenerate downstream evidence.
8. **Anti-simplification gate**: AI-generated flows often omit validation, permissions, recovery, long copy, and edge cases. The service manifest and all-P0 state matrix must catch every omission before approval.
9. **Single-source rule**: do not maintain separate AI mockup markup and app markup. React boards and previews import the same sources; the HTML behavior demo remains non-visual.

Record the prompt/context bundle and rejected direction IDs in the decision log so later reruns do not reset taste or scope.

## Design acceptance implication

- A user can review foundations, components, Depth screens, and flows separately without losing traceability.
- Changing a token or component invalidates every affected screen evidence row.
- Changing a screen contract invalidates the affected flow and Depth evidence.
- Standalone HTML may validate flow wiring, but only the React board/preview can prove design-to-implementation reuse.
