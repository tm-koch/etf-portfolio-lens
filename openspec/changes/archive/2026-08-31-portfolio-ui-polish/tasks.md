## 1. About Dialog And Provenance

- [x] 1.1 Add a Data section to the About this build dialog for the ETF data timestamp and selected snapshot paths.
- [x] 1.2 Render current selected ETF snapshot provenance whenever build information or portfolio selection changes.
- [x] 1.3 Remove visible snapshot-path rows from Portfolio catalog items while preserving catalog identity and controls.

## 2. Portfolio Presentation Polish

- [x] 2.1 Update selected-position identity markup to render ticker and ETF name on one line with a middle-dot separator.
- [x] 2.2 Add responsive styles for the compact selected-position identity without changing catalog item presentation.
- [x] 2.3 Increase spacing between the Share portfolio button and feedback text while preserving fallback-link behavior.
- [x] 2.4 Correct the Share units summary to sum actual share counts independently from monetary weighting.
- [x] 2.5 Add a Total value CHF summary card using valid imported CHF-normalized values and an unavailable state when none exist.

## 3. Import Debug Preference

- [x] 3.1 Add a persisted Portfolio import debug preference with a default-off loader and saver.
- [x] 3.2 Add the debug switch to the About this build Developer mode settings and restore its stored state.
- [x] 3.3 Gate extracted PDF text download visibility on both the debug preference and available extracted pages.
- [x] 3.4 Keep debug download state synchronized when imports succeed, fail, or the preference changes.

## 4. Verification

- [x] 4.1 Add web contract coverage for provenance relocation, compact selected positions, sharing spacing, the debug switch, and summary metrics.
- [x] 4.2 Run the focused web tests and the full existing test suite.
- [x] 4.3 Verify desktop and mobile rendering and the debug download interaction in a browser.
