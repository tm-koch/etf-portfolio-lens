## 1. Portfolio Mutation Feedback

- [x] 1.1 Add a shared helper in `web/app.js` that clears `state.shareFeedback` and any associated generated-link fallback state, then rerenders the share feedback area.
- [x] 1.2 Invoke the helper after confirmed PDF import, new ETF addition, share-count update, and ETF removal while leaving the share URL fragment unchanged.

## 2. Contract Coverage

- [x] 2.1 Extend `tests/test_web_contract.py` to verify feedback invalidation is wired to every portfolio mutation boundary and that startup share loading remains intact.
- [x] 2.2 Add assertions that non-mutating import review actions do not clear feedback and that the URL is not rewritten by the mutation flow.

## 3. Verification

- [x] 3.1 Run the focused web contract tests and confirm all existing and new cases pass.
- [x] 3.2 Run the full Python test suite and manually verify edit-then-refresh behavior with a private share link in desktop and mobile layouts.
