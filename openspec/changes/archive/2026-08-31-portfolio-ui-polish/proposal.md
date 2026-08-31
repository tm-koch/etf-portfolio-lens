## Why

The Portfolio tab currently exposes implementation-oriented snapshot paths beside every catalog item, while useful data provenance is split between the Portfolio view and the About dialog. The selected-position layout and share feedback also consume more vertical space than necessary, and PDF import diagnostics are available without an explicit developer opt-in.

## What Changes

- Remove visible snapshot paths from Portfolio catalog items.
- Add a Data section to the About this build dialog showing the ETF data timestamp and each selected ETF's snapshot path.
- Render each selected position's ticker and ETF name on one line, separated by a middle dot.
- Increase the visual spacing between the Share portfolio button and its feedback text.
- Add a Portfolio import debug switch to the About dialog, defaulting to off and persisting locally.
- Show the Download extracted PDF text button only when the debug switch is enabled and extracted PDF pages are available.
- Correct the Share units summary card to use the actual number of shares rather than the monetary weighting base.
- Add a summary card showing the total portfolio value in CHF from valid imported CHF-normalized values.

## Capabilities

### New Capabilities

- `portfolio-ui-polish`: Organizes ETF data provenance, compactly presents selected positions, improves portfolio sharing spacing, gates PDF import diagnostics behind an opt-in developer setting, and clarifies portfolio summary metrics.

### Modified Capabilities

## Impact

- Updates the static frontend markup, rendering logic, styles, and local-storage preferences in `web/index.html`, `web/app.js`, and `web/styles.css`.
- Adds web contract coverage for snapshot relocation, selected-position presentation, sharing spacing, debug-switch visibility and persistence, and summary metric calculations.
- No external dependencies, backend APIs, persisted portfolio schema, or import parsing behavior change.
