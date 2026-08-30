## Context

The global color-mode control is absolutely positioned by `web/app.js` against the active panel's primary title area. On wide desktop viewports, Home's `.hero-meta` and the side content in the Portfolio, Compare, and Explore panel headings occupy the same upper-right region, so they can render beneath the control. The existing mobile breakpoint is 760px and must retain its current compact selector and navigation geometry.

## Goals / Non-Goals

**Goals:**

- Provide enough vertical clearance for the Home hero metadata and the Portfolio, Compare, and Explore heading-side content to remain readable and unobstructed by the selector.
- Apply the spacing only at widths greater than 760px.
- Keep the selector's current alignment, persistence, accessibility, and menu behavior unchanged.
- Add focused contract coverage and perform wide-desktop and mobile browser checks.

**Non-Goals:**

- Do not redesign or relocate the global color-mode control.
- Do not change the mobile layout, bottom navigation, typography, colors, or content.
- Do not reserve a new horizontal column or alter the app's data and rendering model.

## Decisions

1. **Use desktop-only top spacing on affected secondary regions.** Add a media-query rule for Home's `.hero-meta` and the side content in the Portfolio, Compare, and Explore headings. This directly clears the existing absolutely positioned utility while preserving the established title alignment. A horizontal reservation was considered, but it would reduce the usable width of the Home metadata column and could introduce new wrapping at intermediate desktop widths.

2. **Target existing semantic layout hooks.** Use the existing Home and Portfolio classes or narrowly scoped selectors rather than changing markup or adding a new layout abstraction. This keeps the change local to `web/styles.css` and avoids changing `web/app.js`'s positioning contract.

3. **Keep the mobile breakpoint as the boundary.** Place the new rules inside the existing `min-width: 761px` desktop styling boundary or equivalent desktop-only block. This avoids accidental changes to the compact mobile trigger, fixed navigation, and mobile content flow across all destinations.

4. **Validate geometry rather than relying only on snapshots.** Extend `tests/test_web_contract.py` for the desktop-only selectors and use browser measurements at a wide desktop viewport to confirm the secondary regions start below the utility control. Repeat a compact mobile check to confirm the rules do not apply there.

## Risks / Trade-offs

- [Risk] A fixed spacing value may be insufficient if the utility control's height or title geometry changes later. -> Mitigation: derive the value from the current control footprint with a small buffer and keep a browser geometry check at 1600px.
- [Risk] The added vertical gap may make the desktop hero or heading feel less compact. -> Mitigation: apply spacing only to the two overlapping secondary regions, not the whole panel or global shell.
- [Risk] A selector may match unrelated panel content. -> Mitigation: use the existing Home class and explicit Portfolio, Compare, and Explore panel IDs, then inspect all affected destinations in the focused test.

## Migration Plan

No data or deployment migration is required. Apply the CSS and contract-test changes, run the focused Python tests, then verify Home and Portfolio at wide desktop and compact mobile widths. Rollback consists of removing the new desktop-only spacing rules and their tests.

## Open Questions

- The final spacing value should be confirmed against the rendered control height and the repository's existing desktop spacing scale during implementation.
