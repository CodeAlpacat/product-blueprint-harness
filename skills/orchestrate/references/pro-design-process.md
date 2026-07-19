# Professional Design Process Notes

Use these notes to keep Product Blueprint aligned with common senior product-design practice.

## Source Models

- Design Council Double Diamond: discover/define/develop/deliver. Use divergent exploration before converging on one direction.
- IDEO design thinking: balance human desirability, technical feasibility, and organizational viability.
- Nielsen Norman Group design thinking: empathize, define, ideate, prototype, test, implement. Do not skip prototype testing.
- Figma guidance: pages/sections organize review, component properties/variants expose intended change, variables/modes express context, and named flows connect frames. Product Blueprint maps these to reusable React sources; see `${CLAUDE_PLUGIN_ROOT}/references/figma-design-process.md`.

## Product Blueprint Translation

1. **Discover**: `research`, `reference-deconstruction`, or `ideation`.
2. **Define**: `experience-mechanisms`, `prd`, `screen-contract`.
3. **Develop**: `parallel-concepts`, `storyboard`, `art-direction-brief`, `visual-quality-gate`, `design-system`, `design-system-workbench`, optional `high-fidelity-screen`.
4. **Deliver preparation**: `backend-systems-brief`, `prototype-test`, `design-critique`, `feasibility-review`, `engineering-handoff`.

## Senior Designer Behaviors To Enforce

- Define the screen's job before drawing the screen.
- Explore multiple concepts before polishing one.
- Convert reference screenshots into principles and gates, not copied styling.
- Use art direction to reject generic visual output.
- Design states and recovery paths, not just happy paths.
- Use HTML boards only for cheap flow/IA review. Final visual approval uses React ComponentBoard, DepthBoard, and FlowPreview importing the same sources.
- Use AI for divergent first drafts, realistic content, organization, and interaction assistance; lock direction before system-constrained assembly and audit the edge cases AI tends to simplify.
- Use single-screen high-fidelity specimens only as an extra pixel pass after the workbench, not as the whole design-system deliverable.
- Test prototypes with concrete tasks.
- Critique against product intent, not personal taste.

## Source Links

- https://www.designcouncil.org.uk/resources/the-double-diamond/
- https://designthinking.ideo.com/
- https://www.nngroup.com/articles/design-thinking/
- https://help.figma.com/hc/en-us/articles/14552802134807-Lesson-1-Welcome-to-design-systems
- https://help.figma.com/hc/en-us/articles/15297425105303-Explore-design-files
- https://help.figma.com/hc/en-us/articles/23870272542231-Use-AI-tools-in-Figma-Design
