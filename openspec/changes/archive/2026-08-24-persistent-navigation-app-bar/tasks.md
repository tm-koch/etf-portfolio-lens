## 1. Reorganize Application Structure

- [x] 1.1 Move the primary navigation before the destination panels in `web/index.html`.
- [x] 1.2 Remove the `.page-frame` wrapper and introduce a constrained destination-content container without changing panel IDs or destination keys.

## 2. Implement Responsive App Chrome

- [x] 2.1 Style the desktop navigation as a full-width sticky app bar above the constrained content column.
- [x] 2.2 Remove smartphone body gutters and outer panel framing while preserving internal panel padding and nested grouping surfaces.
- [x] 2.3 Preserve the existing smartphone fixed bottom-navigation height, safe-area handling, full-width geometry, active state, and content clearance.
- [x] 2.4 Verify the app-bar stacking and focus behavior when switching between desktop and smartphone breakpoints.

## 3. Validate Navigation And Layout

- [x] 3.1 Verify all four destinations render and switch correctly with keyboard and pointer interaction, including `aria-current="page"`.
- [x] 3.2 Verify desktop navigation appears above content, remains visible while scrolling, and does not reduce the content column's readable width unexpectedly.
- [x] 3.3 Verify smartphone layouts are full-bleed across Home, Portfolio, Compare, and Explore without horizontal overflow or content hidden behind the bottom bar.
- [x] 3.4 Verify comparison charts, legends, tables, dialogs, and empty states at representative desktop and smartphone viewport sizes.
