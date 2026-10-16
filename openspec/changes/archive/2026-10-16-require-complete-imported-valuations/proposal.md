# Proposal

## Why

The portfolio currently offers imported broker valuation even when no imported values exist for the current holdings, or when only some positions have usable imported values. This exposes a mode that cannot consistently value the portfolio and can leave positions unavailable.

## What Changes

- Offer imported broker valuation only for a non-empty shares-based portfolio where every position has a usable persisted imported CHF valuation.
- Automatically switch the portfolio to latest published valuation when imported valuation is no longer available for every position, including when loading a saved portfolio.
- Preserve imported position data so the imported option can become available again when all current positions have usable values.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-valuation-mode`: Make imported-mode availability conditional on complete imported valuation coverage and define automatic fallback to latest mode.

## Impact

The portfolio valuation selector and mode state in `web/app.js`, imported-value resolution in `web/valuation.js`, portfolio persistence and share loading, and the existing `portfolio-valuation-mode` specification and related tests may be affected. No API or dependency changes are expected.
