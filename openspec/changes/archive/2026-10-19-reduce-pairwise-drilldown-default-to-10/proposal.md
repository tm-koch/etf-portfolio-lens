# Proposal

## Why

The pairwise holdings drill-down currently defaults to showing 20 companies, which can make the comparison unnecessarily long. Reducing the default to 10 makes the initial view more concise while leaving users able to choose a larger maximum.

## What Changes

- Change the default maximum displayed company count for the pairwise holdings drill-down from 20 to 10.
- Keep valid saved user preferences unchanged; use 10 when no valid preference exists.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `pairwise-product-overlap`: Change the default maximum displayed company count for the pairwise holdings drill-down from 20 to 10.

## Impact

- `web/redundancy.js`: default and fallback behavior for the saved display maximum.
- `tests/test_pairwise_frontend.py`: regression coverage for default and fallback values.
- `openspec/specs/pairwise-product-overlap/spec.md`: update the display-maximum requirement and its default scenario.