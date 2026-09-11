## 1. Hidden-State Styling

- [x] 1.1 Add scoped `[hidden]` display rules for `.portfolio-valuation-control` and `.portfolio-valuation-status` in `web/styles.css`.
- [x] 1.2 Verify full portfolios retain the existing valuation selector and Live/Imported status presentation.

## 2. Regression Coverage

- [x] 2.1 Extend `tests/test_web_contract.py` to require the two component-specific hidden display rules.
- [x] 2.2 Run the focused web contract and runtime tests and confirm private valuation elements remain absent while full-mode behavior remains covered.
- [x] 2.3 Run the complete test suite and verify the OpenSpec scenarios before marking the change complete.
