# Proposal

## Why

Several PDF presentation details make reports harder to scan and navigate: score cards include an unwanted coverage item, unavailable table values use verbose labels, and multi-page footers lack page numbers. Consolidating these refinements also gives the cover a more balanced layout by centering its separator and moving the title group down.

## What Changes

- Rename the PDF analytics score heading to localized `Portfolio scores`; show redundancy and diversification verdict badges using the website's bright-mode colors, regardless of app theme.
- Remove the Holdings coverage card and any coverage caveat from the PDF score section, while preserving existing score calculations and classifications.
- Display `—` for unavailable value cells in the PDF `1 · Portfolio` table, preserving genuine zeroes and localized unavailable labels elsewhere.
- Add a right-aligned localized current-page-of-total label to every footer while preserving the generated text and brand-only website link.
- Center the cover separator vertically and shift the icon, title, and provenance layout down while preserving their spacing.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-pdf-export`: Update score presentation, missing-value placeholders, footer numbering, and cover layout.

## Impact

PDF rendering in `web/pdf-report-renderer.js` and footer stamping in `web/pdf-export.js`, localized PDF heading resources, and focused PDF contract/runtime tests. Score calculations, app color-mode preference, stored portfolio data, APIs, and dependencies remain unchanged.
