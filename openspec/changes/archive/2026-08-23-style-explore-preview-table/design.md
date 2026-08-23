## Context

The compact Explore preview is rendered as a semantic table in `web/app.js` and styled by dedicated `.compact-explore-table` selectors in `web/styles.css`. The table can be wider than the viewport, uses a sticky holding-name column, and already provides hover feedback for rows. Its current header and sticky-column backgrounds use the general card palette, while body rows do not have explicit alternating colors.

This is a presentation-only change. The table structure, ranked data, responsive overflow, sticky positioning, and interaction behavior must remain unchanged.

## Goals / Non-Goals

**Goals:**

- Set the compact table header background to `rgb(232, 236, 244)`.
- Alternate body rows between `rgb(244, 246, 251)` and white.
- Keep the sticky holding-name cells visually synchronized with their rows.
- Preserve hover feedback and existing borders, typography, sizing, and overflow behavior.

**Non-Goals:**

- Change table markup, row order, data values, or incremental loading.
- Change the existing Explore preview toggle or persistence.
- Restyle other tables, cards, navigation, or general application surfaces.
- Remove the existing hover state.

## Decisions

### Scope colors to compact Explore selectors

Apply the palette only to `.compact-explore-table` header, body rows, and sticky holding cells. This keeps the visual contract isolated from other tables and avoids changing the broader card system.

An alternative is to define global table row colors. That would unintentionally affect unrelated surfaces and make the compact preview less independently maintainable.

### Use structural row selectors

Use `tbody tr:nth-child(odd)` and `tbody tr:nth-child(even)` so the alternating pattern remains correct as batches append rows during infinite scrolling. Apply corresponding backgrounds to the sticky holding cells because those cells have their own background and otherwise would obscure the row color while scrolling horizontally.

An alternative is to add row classes from JavaScript. That would add presentation logic to a data renderer for a concern CSS can express directly.

### Preserve hover as a temporary interaction state

Keep the current hover background and sticky-cell hover background. The requested alternating colors define the resting state; hover remains a useful pointer cue and does not change the underlying row parity.

An alternative is to remove hover styling to enforce exact colors at all times. That would reduce discoverability and is unnecessary because hover is an intentional transient state.

## Risks / Trade-offs

- [Sticky cells can visually diverge from their row] -> Set odd/even backgrounds on `.compact-explore-holding` and retain its hover override.
- [Future rows may reset the pattern if styling depends on insertion order] -> Use `nth-child` selectors, which naturally account for all rows in the table body.
- [Hover can temporarily obscure the alternating palette] -> Document hover as an intentional interaction state and verify resting colors after pointer exit.
- [Color values can drift through theme variables] -> Use the requested RGB literals in the compact-table selectors.

## Migration Plan

No migration is required. Update the compact-table CSS, verify the table at desktop and mobile widths, and deploy the static stylesheet with the existing frontend bundle. Rollback consists of reverting the compact-table background declarations.

## Open Questions

No open product questions remain. Hover feedback is intentionally preserved as a transient state over the requested resting row colors.
