## Why

On wide desktop viewports, the globally positioned color-mode switcher shares the title-row area with Home's hero metadata and Portfolio's persistence note. Those secondary content boxes can sit underneath the switcher, making ordinary page content harder to read and interact with. The desktop layout needs explicit vertical clearance while preserving the compact mobile arrangement.

## What Changes

- Add wide-desktop spacing so Home's hero metadata begins below the color-mode switcher.
- Add wide-desktop spacing so Portfolio's heading-side persistence note clears the switcher.
- Add the same wide-desktop spacing so Compare and Explore heading-side explanatory text clears the switcher.
- Preserve the existing color-mode alignment, control behavior, and compact mobile layout.
- Validate that the affected content remains visible and non-overlapping at representative desktop widths.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `global-color-mode-selector`: The selector's desktop title-row placement SHALL provide enough vertical clearance for adjacent Home, Portfolio, Compare, and Explore secondary content without changing mobile behavior.

## Impact

- `web/styles.css`: desktop-only spacing rules for Home hero metadata and the side content of Portfolio, Compare, and Explore panel headings.
- `web/app.js`: likely unchanged; existing selector positioning remains the source of truth.
- `tests/test_web_contract.py`: contract coverage for the desktop clearance rules and mobile boundary.
- Browser-level visual verification at wide desktop and compact mobile widths.
