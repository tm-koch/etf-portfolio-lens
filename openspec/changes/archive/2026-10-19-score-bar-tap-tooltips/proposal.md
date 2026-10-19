# Proposal

## Why

Score-band labels are currently exposed through hover tooltips, which are not reliably available on touch screens. Showing the localized label for the band a user taps will make the redundancy and diversification bars understandable on smartphones while preserving the existing desktop interaction.

## What Changes

- Show the tapped band's localized rating label directly below the finger for both score bars.
- Preserve the existing hover tooltip behavior and use the existing rating translations.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-diversification-score`: Extend the shared score-bar band tooltip behavior to touch, with the label positioned below the tapped band.

## Impact

- Affects score-bar interaction and presentation in `web/app.js`, `web/index.html`, and `web/styles.css`, with focused web regression coverage.
- No score calculations, rating thresholds, APIs, or dependencies change.
