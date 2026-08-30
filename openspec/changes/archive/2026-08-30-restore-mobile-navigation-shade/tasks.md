## 1. Restore Theme-Specific Mobile Surfaces

- [x] 1.1 Add a mobile Bright-mode override so the fixed navigation uses the historical solid `#ffffff` background.
- [x] 1.2 Add a mobile Dark-mode override so the fixed navigation uses `var(--card-strong)` while preserving the existing border and shadow.
- [x] 1.3 Add a Dark-mode-only mobile `::after` edge gradient using dark-surface colors while leaving Bright mode flat.
- [x] 1.4 Tune the Dark mobile edge gradient from the lighter dark-slate border tone to the dark frame background.
- [x] 1.5 Change the Dark mobile gradient endpoint to transparency so the frame background shows through.
- [x] 1.6 Reduce the Dark mobile gradient edge height from 18px to 9px without changing its colors or direction.

## 2. Update Contract Coverage

- [x] 2.1 Update `tests/test_web_contract.py` to assert the Bright and Dark mobile surface declarations, the Dark-only edge gradient, and the absence of a Bright edge selector.
- [x] 2.2 Run the focused web contract test and confirm the theme-specific mobile navigation requirements pass.
- [x] 2.3 Update the contract assertion for the tuned Dark gradient endpoints.
- [x] 2.4 Update the contract assertion for the transparent Dark gradient endpoint.
- [x] 2.5 Update the contract assertion for the 9px Dark gradient height.

## 3. Validate Regression Scope

- [x] 3.1 Run the full available test suite and confirm no unrelated web, ingestion, or catalog behavior regresses.
- [x] 3.2 Review the final diff to confirm desktop navigation, mobile geometry, active-tab styling, safe-area handling, and color-mode persistence are unchanged.
