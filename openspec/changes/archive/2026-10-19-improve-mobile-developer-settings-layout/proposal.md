# Proposal

## Why

The developer threshold controls in Build & preview become unnecessarily tall on smartphone screens, and the near-identical threshold is visually misaligned with the paired redundancy controls. A consistent responsive layout will make the settings easier to scan and keep related numeric inputs visually comparable.

## What Changes

- Keep the low/moderate and moderate/high redundancy threshold fields side by side at smartphone widths.
- Make the near-identical threshold section separator span the full settings content width.
- Size the near-identical threshold input to match one redundancy threshold input across viewport modes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-redundancy-score`: Specify the responsive layout of the paired developer threshold fields.
- `pairwise-product-overlap`: Specify the full-width separator and matching input width for the near-identical threshold control.

## Impact

- Affects developer-settings layout in `web/styles.css` and its existing markup in `web/index.html`.
- No application behavior, threshold values, APIs, or dependencies change.
