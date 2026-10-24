# Proposal

## Why

The PDF Portfolio Analytics score cards currently occupy half of the printable content width each, making them wider than the three-column exposure rollup cards above. Giving each score card one rollup-column width will create a more compact, consistent layout while keeping both portfolio scores easy to compare.

## What Changes

- Size each PDF portfolio score card to match one exposure-rollup column.
- Keep the redundancy and diversification cards adjacent, preserving their current order, content, verdict badges, and spacing.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-pdf-export`: Define the score cards as one exposure-rollup column wide while retaining their side-by-side arrangement and contents.

## Impact

Affects score-card geometry in `web/pdf-report-renderer.js`, its PDF runtime tests, and the `portfolio-pdf-export` specification. No score calculations, report data, public APIs, or dependencies change.
