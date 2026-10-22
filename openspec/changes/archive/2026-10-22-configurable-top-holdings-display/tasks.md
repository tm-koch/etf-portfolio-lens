# Tasks

## 1. Developer Holdings Maximum

- [x] 1.1 Add a persisted developer-mode integer setting with a default of zero, validation for non-negative values, and localized UI labels; verify stored-value defaults, invalid-value fallback, and reload persistence with focused tests.
- [x] 1.2 Apply the positive maximum to unfiltered rendering in both standard and compact Explore views while leaving search over the full ranking; verify limits below, equal to, and above the available count, plus matching a holding below the limit and restoring the capped list after clearing search.

## 2. Page-Sticky Preview Header

- [x] 2.1 Separate the visual header from the horizontal-overflow body while preserving accessible table headers, shared column sizing, and synchronized horizontal position; verify header/body alignment at narrow and wide viewport widths.
- [x] 2.2 Keep the visual header sticky during page scrolling and bounded by the table section; verify it sticks at the viewport top, stops at the table bottom, and does not cover following content in browser tests.
- [x] 2.3 Run the focused frontend contract and runtime test suites and verify both Explore presentations retain existing rendering, search, and responsive table behavior.
- [x] 2.4 Constrain the compact table and search control to the Explore card while preserving horizontal scrolling; verify the search stays within the card and the table scroller can scroll on narrow viewports.
- [x] 2.5 Keep the compact preview's first visual header cell pinned to the left edge during horizontal scrolling while the remaining columns stay aligned; verify at narrow and wide viewports.
- [x] 2.6 Give Portfolio and fund headings enough column width to fit without overflow, right-align them, and keep the holding heading left-aligned; verify header text bounds and header/body column alignment.
