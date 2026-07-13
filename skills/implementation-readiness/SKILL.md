---
name: implementation-readiness
description: Compatibility router for older Product Blueprint calls. The harness no longer claims implementation readiness; route contract, prototype, design, and handoff checks to design-readiness, and keep technical/implementation readiness outside this plugin's acceptance boundary.
---

# Compatibility: use Design Readiness

This name remains only so existing projects do not silently lose their gate.

Use `product-blueprint:design-readiness` for all current work. It verifies the continuous product/design contract and can prove that the accepted design is ready to hand to a later technical-design process. It must never claim that implementation can start unchanged.

If an old artifact or command asks for `engineering_ready`, `technical_design_ready`, or `implementation_ready`, keep those compatibility fields false and explain that the Product Blueprint harness does not own them.

## Next step

Run the same stage through `design-readiness`, repair the earliest product/design owner, and request user reapproval after any feasibility-driven design change.
