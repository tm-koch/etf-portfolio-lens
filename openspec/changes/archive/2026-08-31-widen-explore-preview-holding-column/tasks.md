## 1. Widescreen Layout

- [x] 1.1 Update the compact Explore sticky Holding column minimum width from `220px` to `300px` in `web/styles.css`.
- [x] 1.2 Update the compact Explore holding-name maximum width from `220px` to `300px` while preserving the mobile `36vw` override.

## 2. Contract Coverage

- [x] 2.1 Update `tests/test_web_contract.py` to assert the `300px` desktop dimensions and retain the existing sticky, overflow, and mobile behavior checks.

## 3. Verification

- [x] 3.1 Run the focused web contract test suite and confirm it passes.
- [x] 3.2 Verify the compact Explore preview at widescreen and mobile viewport sizes, including horizontal scrolling and long holding-name visibility.
