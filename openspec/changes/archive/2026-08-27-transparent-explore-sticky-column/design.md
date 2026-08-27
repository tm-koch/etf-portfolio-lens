## Context

The compact Explore preview renders a semantic holdings matrix inside `.compact-explore-table-wrap`, which provides horizontal overflow. The first holding column is `position: sticky` and currently receives opaque backgrounds for the header, alternating body rows, and hover state. This preserves readability but hides the horizontally scrolling ETF cells beneath the fixed column.

The change is limited to presentation. The existing table structure, semantic cells, ranked data, incremental loading, and scroll container remain the source of truth.

## Goals / Non-Goals

**Goals:**

- Make the sticky body holding column slightly translucent so horizontally moving cells can be perceived beneath it.
- Keep holding names readable against both alternating row colors and the hover state.
- Keep the sticky header opaque and legible.
- Preserve the current desktop and mobile overflow behavior without layout shifts.
- Verify the visual effect and existing interaction behavior in representative wide and narrow viewports.

**Non-Goals:**

- No changes to holding data, table markup, column order, ranking, or loading batches.
- No JavaScript scroll listener or scroll-position state.
- No changes to the existing long-name fade or hover tooltip.
- No new dependency or persistent user preference.

## Decisions

1. **Use CSS translucency on sticky body cells.** The moving ETF cells already pass behind the sticky holding cells because of the existing table stacking order. Replacing the body holding backgrounds with carefully chosen `rgba(...)` colors exposes that motion without changing the scroll model.

   Alternatives considered: a JavaScript scroll listener would add state and event handling for a purely visual effect; a gradient mask or shadow would signal the boundary but would not reveal the underlying cell content.

2. **Keep the table header opaque.** The header is independently sticky and has a higher stacking level. Its opaque background keeps the `Holding` label and column headings crisp while the body demonstrates the transparency effect.

   Alternatives considered: making the header translucent would provide visual consistency but risks reducing contrast against both body rows and moving content.

3. **Retain explicit row-state backgrounds using alpha colors.** Odd/even rows and hover state will continue to assign backgrounds to the sticky cells, but with enough opacity to distinguish the row while allowing a subtle view-through effect.

   Alternatives considered: removing sticky-cell backgrounds entirely would maximize visibility but allow unrelated content and borders to interfere with holding-name readability.

4. **Validate with browser interaction checks.** The focused check should enable compact preview, select enough ETFs to cause horizontal overflow, scroll the table wrapper, and confirm the holding column remains fixed while underlying content becomes visible through it. The same check should cover narrow viewport sizing and hover/readability states where practical.

## Risks / Trade-offs

- [Reduced contrast] → Use a high-opacity light background and confirm text remains readable over moving numeric cells.
- [Zebra-striping becomes less distinct] → Keep separate odd/even translucent values and verify both row types.
- [Browser compositing differences] → Prefer standard CSS `rgba(...)` backgrounds and test Chromium desktop and mobile-sized viewports.
- [Visual regression in hover state] → Define a translucent hover background explicitly rather than inheriting the row background.

## Migration Plan

Update the compact Explore sticky-cell CSS, then run the focused browser/UI verification. Rollback consists of restoring the existing opaque sticky-cell background declarations; no stored data or migration is involved.

## Open Questions

None. The agreed behavior is permanent light translucency for the sticky body column, with an opaque header.
