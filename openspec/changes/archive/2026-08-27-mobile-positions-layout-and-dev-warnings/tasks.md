## 1. Position Rendering Contract

- [x] 1.1 Update the Selected positions markup in `web/index.html` with any mobile layout hooks and accessible labels needed for the existing position cells.
- [x] 1.2 Preserve the existing `renderPositions()` editing, weight, warning-count, and remove behavior while exposing the cells for responsive reflow.

## 2. Shared Selection Warnings

- [x] 2.1 Refactor current-selection warning construction in `web/app.js` into a reusable warning-record collection consumed by both rendering surfaces.
- [x] 2.2 Add the labeled current-selection warning section to the developer build dialog and render the shared warning records, including the no-warnings state without stale content.
- [x] 2.3 Keep the Explore warning panel output consistent with the shared warning records and preserve existing warning conditions and messages.

## 3. Responsive Styling

- [x] 3.1 Add the mobile position-row reflow in `web/styles.css`, placing ETF identity above a lower Shares, Weight, and Remove row.
- [x] 3.2 Ensure mobile position controls wrap or flex within the available width, retain readable names, and do not create horizontal scrolling while preserving the desktop/tablet table layout.
- [x] 3.3 Preserve accessible focus, pointer, and keyboard states for the mobile Shares input and Remove control.

## 4. Validation

- [x] 4.1 Add or update focused tests for shared warning records, developer-dialog warning output, and mobile position markup behavior.
- [x] 4.2 Run the existing Python test suite and any available frontend checks.
- [x] 4.3 Verify the Selected positions view at narrow mobile and desktop widths in the browser, including editing, removal, warning display, and absence of horizontal overflow.

## 5. Warning Presentation Refinement

- [x] 5.1 Remove duplicated warning counts from Selected positions Weight cells and verify warning details remain available in the developer dialog and Explore warning panel.
- [x] 5.2 Make the mobile control strip visually compact by hiding repeated labels and using an accessible icon-only Remove action, while retaining desktop labels.
