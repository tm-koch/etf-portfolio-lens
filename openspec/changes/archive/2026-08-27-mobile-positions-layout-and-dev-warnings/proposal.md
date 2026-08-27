## Why

The Selected positions table becomes wider than the available viewport on mobile because the ETF identity, Shares, Weight, and Remove controls remain in a single desktop-style row. This makes position editing require horizontal scrolling and hides important actions; the developer build dialog also lacks a consolidated view of the warnings already shown in Explore.

## What Changes

- Reflow each Selected positions entry into a mobile-friendly two-row layout with ETF identity above.
- Keep Shares, Weight, and Remove together on the lower mobile row, with no horizontal scrolling at supported mobile widths.
- Preserve the existing four-column table presentation for desktop and tablet-sized viewports where it remains usable.
- Add a clearly labeled current-selection warning summary to the developer build dialog.
- Reuse the existing warning conditions and messages so the developer dialog and Explore warnings do not diverge.
- Keep the Selected positions Weight column focused on portfolio percentages; warning details belong in the dedicated warning views.
- Preserve position editing, weight display, remove behavior, and empty-state behavior.

## Capabilities

### New Capabilities

- `mobile-positions-layout`: Responsive presentation of editable Selected positions without mobile horizontal scrolling.
- `developer-selection-warnings`: Consolidated display of current selection warnings in the developer build dialog.

### Modified Capabilities

<!-- No existing capability requirements are changed. -->

## Impact

- `web/app.js`: position rendering and shared warning data/presentation logic.
- `web/styles.css`: mobile position-row layout, control alignment, and responsive overflow behavior.
- `web/index.html`: developer-dialog warning summary container and any accessible labeling needed for the responsive controls.
- Existing browser and Python tests may need focused coverage for mobile layout structure and warning visibility; no external dependencies or backend APIs are required.
