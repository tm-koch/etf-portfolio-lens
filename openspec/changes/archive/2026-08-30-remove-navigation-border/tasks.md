## 1. Navigation Styling

- [x] 1.1 Set the desktop `.primary-navigation` border to `0` so the shared `.card` border is not visible on the navigation.
- [x] 1.2 Remove the mobile `.primary-navigation` top-border declaration while preserving its background, shadow, gradient, safe-area spacing, and geometry.

## 2. Contract Coverage

- [x] 2.1 Update `tests/test_web_contract.py` to assert the navigation is borderless in the base and mobile styling while retaining existing navigation treatments.
- [x] 2.2 Run the focused web contract tests and confirm the borderless navigation behavior at desktop and mobile breakpoints.

## 3. Specification Validation

- [x] 3.1 Validate the completed OpenSpec change and confirm the delta matches the `bottom-navigation` requirement.