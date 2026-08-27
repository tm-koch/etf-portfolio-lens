## 1. Shell Density Implementation

- [x] 1.1 Reduce the desktop/tablet `.app-shell` top-level gap from `18px` to `12px`.
- [x] 1.2 Reduce the desktop/tablet `.content-column` outer padding from `24px` to `16px` while preserving the existing maximum width and centering.
- [x] 1.3 Align the desktop primary-navigation outer inset with the reduced content gutter without changing its internal padding, control sizes, or mobile override.
- [x] 1.4 Reduce mobile tab-panel outer padding from `24px` to `16px` so the visible panel inset matches the requested density.

## 2. Responsive Verification

- [x] 2.1 Verify desktop and tablet viewports expose more active content area without clipping or overlapping panels, tables, charts, or controls.
- [x] 2.2 Verify mobile content remains full width and bottom-navigation height, safe-area clearance, and hit areas remain unchanged.
- [x] 2.3 Confirm internal card, table, chart, and control spacing is unchanged and run the repository's available tests or validation commands.
