## 1. Empty Summary Value

- [x] 1.1 Replace the empty or unavailable Total value fallback in `web/app.js` with the existing CHF formatter applied to zero.
- [x] 1.2 Extend `tests/test_web_contract.py` with a regression assertion for the currency-formatted zero fallback while preserving populated-value formatting coverage.

## 2. Verification

- [x] 2.1 Run the focused web contract tests and the full existing test suite.
- [x] 2.2 Smoke-test the Home tab with an empty portfolio and confirm Total value displays `CHF 0.00` alongside the other zero summary cards.
