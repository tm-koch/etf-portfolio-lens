# Proposal

## Why

The numeric fields for selected-position Shares and Allocation values are narrow, while Shares mode currently permits manual fractional quantities despite presenting whole-share increments. Improving field width and enforcing whole-number shares will make entry clearer and prevent fractional share edits without changing allocation precision or existing portfolio data.

## What Changes

- Increase the shared position-entry field width by approximately 15%, from 84px to about 97px, on desktop and mobile while preserving responsive layout.
- In Shares mode, accept only finite, non-negative integer values for manual edits; reject fractional edits and restore the previous committed value rather than rounding.
- Keep decimal relative Allocation values supported.
- Do not migrate or coerce already saved or imported values unless the user edits them.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-allocation-mode`: Specify the wider position-entry field and whole-number Shares edits while retaining fractional relative Allocation entry.

## Impact

- `web/app.js` for Shares-mode edit validation and preserving allocation-mode precision.
- `web/styles.css` for the shared position-entry width at desktop and mobile breakpoints.
- `tests/test_web_runtime.py` and `tests/test_web_contract.py` for edit validation and responsive field sizing.
- `openspec/specs/portfolio-allocation-mode/spec.md` for the position-entry behavior contract.
