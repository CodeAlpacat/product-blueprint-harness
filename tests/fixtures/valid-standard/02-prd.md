# Fixture Service PRD

## Inspect item

As a guest arriving at the public home, I can choose an item and open its detail without signing in. The home establishes what can be inspected, provides a clear primary action, and preserves a predictable route back from detail. Acceptance evidence must show the home surface, the open-detail action, the selected item context, and the resulting detail surface on narrow and wide viewports.

## Recover item load

When detail loading fails, the guest sees a contextual error on the detail surface rather than a dead end. Retrying keeps the same item selected, changes to a content-shaped loading state, and then restores the detail. The backend item service owns the load result; the interface owns progress, error explanation, retry, and focus feedback.

## First-version boundaries

Accounts, private items, favorites, notifications, payments, editing, and cross-device persistence are excluded. Existing or future entry points for those capabilities must not appear as working controls. The release is accepted only when the public-home journey, refresh and back behavior, loading and error states, operation ownership, and prototype evidence remain mutually traceable.
