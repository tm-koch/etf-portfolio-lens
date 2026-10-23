# Proposal

## Why

The text block above each comparison donut is separated from its chart frame by excess vertical space, making the cards feel disconnected. Reducing that gap consistently will bring the chart closer to its title and description across Sectors, Regions, and Currencies.

## What Changes

- Reduce the vertical separation between each comparison card's heading/description block and donut chart frame.
- Apply the same spacing behavior to all three comparison metrics at supported viewport widths.
- Preserve heading text, chart sizing, donut-to-legend spacing, and responsive behavior outside this gap.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `comparison-donut-spacing`: Require a reduced, consistent gap between the text block and chart frame in each comparison metric card.

## Impact

- `web/styles.css`: spacing between `.chart-card-head` and `.chart-frame`.
- `tests/test_web_runtime.py` and/or `tests/test_web_contract.py`: regression coverage for consistent spacing across all three cards and responsive layouts.
- `openspec/specs/comparison-donut-spacing/spec.md`: add the text-to-chart gap requirement.
