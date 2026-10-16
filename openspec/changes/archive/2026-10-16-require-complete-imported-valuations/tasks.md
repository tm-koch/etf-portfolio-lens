# Tasks

## 1. Imported Valuation Validity

- [x] 1.1 Ensure imported valuation resolution and portfolio/share normalization treat explicit null values as missing while retaining genuine numeric zero values; verify with focused valuation tests for null, zero, and source-currency conversion.

## 2. Availability and Portfolio State

- [x] 2.1 Add a single eligibility check requiring a non-empty shares portfolio and a usable imported CHF valuation for every position; verify cases for empty, complete, and mixed portfolios.
- [x] 2.2 Hide the imported option when eligibility is false and reconcile an active Imported mode to Latest after position changes, persisting the mode without dropping imported fields; verify add/remove and mode-transition behavior.

## 3. Portfolio Restoration

- [x] 3.1 Reconcile restored local and full-share portfolios against imported valuation eligibility before rendering; verify incomplete imported-mode portfolios load in Latest mode and complete portfolios preserve their selected mode.
- [x] 3.2 Run the focused web runtime and contract test suites and verify all valuation availability, persistence, and existing percentage-portfolio scenarios pass.
