# Design

## Context

The Redundancy score box uses 20px top padding and a zero-margin title at all widths. Compare chart cards, the Rollups section above 760px, and the Portfolio Selected positions box use 18px top padding with default heading margins; the Rollups section uses 20px top padding at compact widths. See proposal.md for motivation and the spec deltas for the behavior contract.

## Goals / Non-Goals

**Goals:**
- Match Compare metric-card titles, the Rollups section heading, and the Selected positions heading to the Redundancy score title at every viewport width.
- Preserve subtitle clearance and existing card, chart, and legend spacing.
- Preserve inner rollup card alignment and responsive structure.

**Non-Goals:**
- Change markup, localized copy, card padding, chart sizing, or Explore heading styles.

## Decisions

- Set the top margin to 2px for Compare, Rollups, and Selected positions headings in the base styles. This offsets the 2px difference between their 18px card padding and the Redundancy score box's 20px padding. Retain the existing compact Rollups heading reset, where its card already has 20px padding.
- Validate rendered title-to-card top offsets for Compare, Rollups, and Selected positions against the Redundancy score title at 390px, 760px, 761px, and 1440px. Check subtitle/chart spacing and inner rollup cards alongside the title offsets.

## Risks / Trade-offs

- Changing base heading margins can affect subtitle spacing on wider layouts. Verify the title/subtitle gap remains readable and chart/rollup content does not shift unexpectedly.