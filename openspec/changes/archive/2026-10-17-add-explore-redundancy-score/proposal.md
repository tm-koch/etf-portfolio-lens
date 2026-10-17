# Proposal

## Why

Portfolio owners can see their largest look-through company exposures in Explore, but have no concise measure of how much capital is duplicated across selected ETFs. A separate redundancy score makes this overlap visible and comparable against clear, configurable risk bands.

## What Changes

- Add a standalone redundancy-score box to Explore, separate from the Top companies section and styled consistently with the provided bullet-bar reference and existing application font.
- Calculate aggregate duplicated exposure from current ETF allocations and per-security holdings, and dynamically scale the bar maximum according to the number of selected ETFs using `1 - 1/n` (zero for one ETF).
- Add developer settings for the low/moderate and moderate/high score thresholds, defaulting to 10% and 25%.
- Localize the score labels, explanatory text, and settings in the supported interface languages.
- Exclude near-identical ETF-pair detection from this change.

## Capabilities

### New Capabilities
- `portfolio-redundancy-score`: Calculate and present aggregate look-through overlap in a separate Explore score box with a count-dependent scale and configurable classification thresholds.

### Modified Capabilities

## Impact

- Web Explore markup, rendering, styles, and developer settings in `web/index.html`, `web/app.js`, and `web/styles.css`.
- English, German, and Polish interface resources under `web/locales/`.
- OpenSpec behavior contract and focused web tests for score calculation, scale, threshold settings, and rendering states.
