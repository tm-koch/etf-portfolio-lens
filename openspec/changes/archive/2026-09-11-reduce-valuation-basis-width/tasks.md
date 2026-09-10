## 1. Compact Valuation Controls

- [x] 1.1 Change the shared `.portfolio-valuation-control` width cap from `min(100%, 320px)` to `min(100%, 224px)` in `web/styles.css`.
- [x] 1.2 Remove the redundant portfolio-row width override while preserving existing margins, mobile stacking, and status alignment.

## 2. Regression Coverage

- [x] 2.1 Update the relevant web contract test to assert the shared 224px rule and both controls' markup coverage.
- [x] 2.2 Run focused web tests and verify both controls remain usable at desktop and mobile viewport widths.

## 3. Validation

- [x] 3.1 Run the complete test suite and inspect diagnostics for changed files.
- [x] 3.2 Review the final diff to confirm only valuation-basis presentation width and its contract coverage changed.
