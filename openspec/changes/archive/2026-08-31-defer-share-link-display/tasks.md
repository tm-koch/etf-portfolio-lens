## 1. Conditional Share-Link Display

- [x] 1.1 Add a stable reference for the share-link label and keep the label and URL input hidden when no generated fallback URL exists.
- [x] 1.2 Update `renderShareFeedback()` to reveal the label and URL input together when `state.shareFallbackUrl` is populated, while preserving status feedback for empty and clipboard-unavailable outcomes.
- [x] 1.3 Extend `tests/test_web_contract.py` with assertions covering the initial hidden state and conditional reveal contract.

## 2. Verification

- [x] 2.1 Run the focused web contract tests and the full existing test suite.
- [x] 2.2 Smoke-test populated, empty-portfolio, and clipboard-unavailable sharing states in the browser.
