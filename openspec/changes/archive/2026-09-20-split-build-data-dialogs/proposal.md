## Why

The current `About this build` popup combines build provenance, developer preview controls, ETF/live-data provenance, and portfolio selection warnings. Separating these concerns will make each surface easier to scan and give users a clearer distinction between how the application was built and what data it is currently using.

## What Changes

- Replace the single About dialog entry point with separate `Build & preview` and `Data details` actions in the Home development/status area.
- Move source, commit, publish, optional build metadata, and developer preview/debug controls into the Build & preview dialog.
- Move ETF data timestamps, live-data status, selected ETF snapshot paths, and current selection warnings into the Data details dialog.
- Preserve in-page dialog behavior, keyboard dismissal, focus restoration, fault-tolerant metadata handling, and unchanged portfolio/navigation behavior.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `build-provenance`: Replace the single About build-details surface with separate Build & preview and Data details surfaces while preserving provenance display and accessibility behavior.
- `developer-selection-warnings`: Relocate current-selection warnings from the combined build dialog to the Data details dialog.

## Impact

- Affected Home markup and dialog controls in `web/index.html`.
- Affected dialog state, focus management, metadata rendering, and event wiring in `web/app.js`.
- Affected shared dialog styles and responsive behavior in `web/styles.css`.
- Affected static web contract tests and existing build/warning specifications.
- No backend, data artifact, persistence, API, or navigation destination changes.