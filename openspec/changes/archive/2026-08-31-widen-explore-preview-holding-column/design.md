## Context

The compact Explore preview is rendered as a semantic table in `web/app.js` and styled by dedicated selectors in `web/styles.css`. Its sticky Holding column and holding-name span are currently limited to 220px on widescreen layouts, which clips longer names earlier than necessary. A mobile media query already assigns both dimensions to `36vw`.

The change is a presentation-only adjustment. The table structure, ranked data, incremental loading, horizontal scrolling, sticky behavior, numeric column widths, and mobile sizing must remain unchanged.

## Goals / Non-Goals

**Goals:**

- Give the widescreen sticky Holding column a `300px` minimum width.
- Allow the holding-name content to use up to `300px` on widescreen layouts.
- Keep the existing responsive mobile width, which overrides the desktop values at the current breakpoint.
- Update the focused web contract test to assert the new desktop dimensions.

**Non-Goals:**

- Change table markup, row order, data values, or incremental loading.
- Change ETF numeric column widths or table overflow behavior.
- Change mobile sizing or introduce a new breakpoint.
- Modify the standard Explore presentation, backend, catalog, or data model.

## Decisions

### Change the existing desktop limits in place

Update the two existing desktop `220px` declarations to `300px`: the sticky Holding column's `min-width` and the holding-name span's `max-width`. This keeps the current cascade and lets the existing mobile rule continue to override the desktop sizing at `max-width: 760px`.

An alternative is to add a new widescreen media query. That would duplicate the existing base declarations without improving behavior, and it would create another breakpoint-specific rule to maintain.

### Preserve the current mobile override

Leave the mobile `width`, `min-width`, `max-width`, and name `max-width` declarations at `36vw`. The request targets widescreen visibility; mobile needs viewport-relative sizing to keep the sticky column usable on narrow screens.

An alternative is to use `300px` at every viewport size, which would consume too much of a mobile viewport and conflict with the existing responsive table contract.

### Update contract coverage with the CSS change

Change the focused assertions in `tests/test_web_contract.py` to expect the new `300px` desktop declarations while retaining checks for the mobile override and existing sticky behavior.

An alternative is to omit the test update, but that would leave the repository's contract suite asserting an intentionally obsolete layout value.

## Risks / Trade-offs

- [The wider sticky column reduces the visible space for ETF columns] -> Retain horizontal scrolling and stable numeric widths; only the requested desktop holding column expands.
- [The desktop value could affect tablet-sized layouts before the mobile breakpoint] -> Keep the established `760px` breakpoint and verify representative wide and narrow viewports.
- [Future CSS changes could override the new dimensions] -> Keep the values in the existing dedicated selectors and retain focused contract assertions.

## Migration Plan

No data or runtime migration is required. Update the two desktop CSS limits and their contract-test expectations, then run the focused web contract tests and the broader available test suite. Rollback consists of restoring the two values and corresponding test expectations to `220px`.

## Open Questions

None. The requested widescreen width is defined as `300px` and the existing mobile behavior remains in force.
