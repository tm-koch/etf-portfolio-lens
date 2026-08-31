## 1. CSS Visibility Fix

- [x] 1.1 Add a component-scoped `.share-portfolio-url-label[hidden] { display: none; }` rule so the hidden share-link label is removed from layout.
- [x] 1.2 Preserve the existing visible layout when the label is revealed after a generated share URL is available.

## 2. Regression Coverage

- [x] 2.1 Extend `tests/test_web_contract.py` to assert the scoped hidden-state selector and existing conditional visibility contract.
- [x] 2.2 Run focused and full test suites, then smoke-test the deployed empty and populated sharing states.
