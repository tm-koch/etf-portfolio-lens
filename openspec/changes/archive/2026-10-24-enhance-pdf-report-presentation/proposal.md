# Proposal

## Why

The PDF report lacks a branded cover, repeats a raw website URL in its footer, and gives subordinate report pages more visual weight than their parent sections. In addition, exposure roll-ups are empty in exported reports because positions with precomputed weights are skipped by the aggregation path.

## What Changes

- Add a standalone cover page with the PWA launcher icon, ETF Portfolio Lens title, and report provenance; count it in the existing page numbering so `1 · Portfolio` may begin on page 2.
- Include a clickable portfolio share link under the Portfolio section, preserving the current share-count or relative-allocation semantics.
- Fix exposure roll-ups for report positions that already contain portfolio weights.
- Show parent section titles as running headers on Top Companies and Pairwise ETF Overlap pages, and render those category titles at subordinate heading size.
- Add decorative accent bars below the sector, region, and currency chart titles. Align each title and bar at the same left edge, span the chart column, and leave 10 mm between columns.
- Group generation/build/snapshot/live-price provenance on the cover without individual cards. Keep each footer to `ETF Portfolio Lens | Generated: <timestamp>` with only the brand label hyperlinked, cap each rollup at 20 named values plus a combined remainder, and use thin gray exposure separators with a four-column currency legend.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-pdf-export`: Define the cover, provenance placement and footer link presentation, embedded portfolio share link, roll-up availability, section/category heading hierarchy, and decorative exposure-chart title bars.

## Impact

- `web/pdf-report-renderer.js` and `web/pdf-export.js`: Cover layout, section headers, title accents, portfolio link annotation, and footer presentation.
- `web/app.js`: Supply the report roll-ups and the existing mode-appropriate portfolio share URL.
- `tests/test_web_contract.py` and `tests/test_web_runtime.py`: Report content, analytics, link, pagination, and layout contracts.
- `openspec/specs/portfolio-pdf-export/spec.md`: Update the report behavior contract.