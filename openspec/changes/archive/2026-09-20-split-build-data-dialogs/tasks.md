## 1. Home Dialog Structure

- [x] 1.1 Replace the single `About this build` trigger with accessible `Build & preview` and `Data details` actions in the Home development/status area.
- [x] 1.2 Add two labelled native dialogs with distinct headings, descriptions, close controls, and content ownership.

## 2. Dialog Rendering and Behavior

- [x] 2.1 Split build provenance, optional build details, and developer preview/debug controls into the Build & preview dialog.
- [x] 2.2 Split ETF/live-data provenance, selected ETF snapshot paths, and current-selection warnings into the Data details dialog.
- [x] 2.3 Add independent open, close, cancel, Escape, and return-focus handling for both dialogs while preserving local metadata fallback behavior.

## 3. Styling and Responsive Layout

- [x] 3.1 Reuse and adjust shared dialog styles for the two surfaces, their triggers, section separators, and responsive content without changing unrelated dialogs.
- [x] 3.2 Verify both dialogs remain readable and non-overlapping at desktop and mobile widths, including long metadata and selected ETF warning lists.

## 4. Contract Coverage

- [x] 4.1 Update web contract tests for the two triggers, dialog labels, content placement, independent controls, and keyboard-accessible close behavior.
- [x] 4.2 Run focused and full test suites and review the Home dialog flows for regressions.