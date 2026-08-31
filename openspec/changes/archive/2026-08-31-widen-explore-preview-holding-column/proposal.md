## Why

Long holding names in the widescreen Explore preview are clipped too early because the sticky Holding column is limited to 220px. Increasing the available desktop width will make the matrix easier to scan without changing its data or interaction model.

## What Changes

- Increase the widescreen compact Explore preview Holding column width from 220px to 300px.
- Increase the matching desktop holding-name visibility limit to 300px.
- Preserve the existing mobile `36vw` sizing, sticky behavior, overflow scrolling, and numeric column widths.
- Update the web contract coverage for the revised desktop dimensions.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `compact-explore-preview`: Widescreen holding names must have up to 300px of visible sticky-column space while mobile sizing remains responsive.

## Impact

- `web/styles.css`: desktop holding-column and holding-name width limits.
- `tests/test_web_contract.py`: expected compact Explore dimensions.
- `openspec/specs/compact-explore-preview/`: responsive table requirement delta.
- No backend, data, API, or dependency changes.
