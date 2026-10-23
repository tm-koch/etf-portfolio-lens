# Tasks

## 1. Shared Wide Metric Columns

- [x] 1.1 Define consistent wide-layout grid tracks for Price, Value CHF, and Weight across share-based position boxes while preserving the separate percentage-only and mobile layouts; verify the CSS contract with `python -m unittest discover -s tests -p test_web_runtime.py`.
- [x] 1.2 Add regression coverage that guards shared metric-column starts and unchanged mobile/percentage-only behavior; verify the focused runtime and contract tests pass.

## 2. Rendered Layout Verification

- [x] 2.1 Render multiple positions with different ticker names, currencies, value widths, and unavailable values at wide viewport widths; verify the left edges of Price, Value CHF, and Weight labels and values match across all rows, and verify mobile reflow remains unchanged.
- [x] 2.2 Run `python -m unittest discover -s tests` and confirm the full suite passes.
