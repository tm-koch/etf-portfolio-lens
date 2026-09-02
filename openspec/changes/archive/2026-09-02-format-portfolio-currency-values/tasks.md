## 1. Currency Display Formatter

- [x] 1.1 Generalize the existing CHF display formatting into one currency-aware formatter for finite CHF and EUR values, preserving exactly two decimal places and apostrophe-separated thousands.
- [x] 1.2 Keep non-finite, unavailable, input, persistence, parsing, and calculation paths on their existing behavior.

## 2. Portfolio Displays

- [x] 2.1 Update Portfolio summary and selected-position price/value render paths to use the shared formatter for supported currencies.
- [x] 2.2 Verify private portfolios without absolute valuation data continue to display their established unavailable values.

## 3. PDF Import Review Displays

- [x] 3.1 Update import review row values, CHF-normalized values, and live recalculated totals to use the shared formatter.
- [x] 3.2 Preserve editable raw numeric fields and the existing fixed EUR-to-CHF conversion.

## 4. Verification

- [x] 4.1 Add web contract tests covering CHF and EUR grouping, two decimal places, zero values, and the affected Portfolio and import review display paths.
- [x] 4.2 Run the focused web contract tests and the full `python -m unittest discover -s tests` suite.
