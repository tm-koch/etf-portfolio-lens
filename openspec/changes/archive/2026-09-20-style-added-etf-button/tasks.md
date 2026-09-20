## 1. Catalog State Markup

- [x] 1.1 Add an explicit added-state marker to catalog buttons rendered for ETFs already present in the active portfolio.
- [x] 1.2 Preserve the existing `Added` label, disabled attribute, and duplicate-add guard for selected ETFs.

## 2. Added-State Styling

- [x] 2.1 Add the outlined status treatment for the added-state marker: accent-blue border and text, white background, and full opacity.
- [x] 2.2 Verify the status treatment overrides the existing filled catalog button rule in bright and dark color modes without affecting unrelated disabled buttons.

## 3. Contract Coverage

- [x] 3.1 Add focused web contract assertions for the added-state marker, status label, disabled behavior, and required style declarations.
- [x] 3.2 Run the focused web tests and the full available test suite, then review the rendered catalog state for regressions.