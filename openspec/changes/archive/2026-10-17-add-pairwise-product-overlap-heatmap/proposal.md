# Proposal

## Why

The portfolio redundancy score describes aggregate duplicated exposure, but it does not show which selected ETFs overlap. A pairwise heatmap will make product-to-product overlap visible, identify near-identical pairs, and explain how disclosed holdings coverage bounds the comparison.

## What Changes

- Add a responsive lower-triangle pairwise product-overlap heatmap to Explore, using the existing application font, restrained rounded cells, and the selected ETFs in portfolio order.
- Compute pairwise overlap offline from normalized ETF holdings and publish the matrix with the generated catalog JSON so both share one version and new catalog products are included on rebuild.
- Match holdings by ISIN, falling back to canonical company identity when ISIN is unavailable; calculate overlap as the sum of the smaller disclosed weight for each shared holding without renormalizing incomplete holdings to 100%.
- Add a persisted developer setting for the near-identical threshold, defaulting to 90%. Mark pairs at or above the threshold in the heatmap and show a localized warning with a warning icon and affected product names at the bottom of the redundancy-score box.
- Keep the matrix usable for large selections with bounded two-axis scrolling, a sticky column header row, and a sticky first product column.
- Revise the redundancy-score requirement that currently prohibits near-identical pair warnings.

## Capabilities

### New Capabilities
- `pairwise-product-overlap`: Generate, publish, configure, and display pairwise product-overlap data for selected ETFs, including near-identical classification.

### Modified Capabilities
- `portfolio-redundancy-score`: Allow a near-identical-pair warning at the bottom of the score box while preserving the score's independent calculation and presentation.
- `web-catalog-generation`: Include the offline pairwise matrix in the generated catalog JSON and rebuild it from the same successful ETF snapshot set.

## Impact

- Backend catalog generation and tests under `etf_ingestion_backend/` and `tests/`.
- Catalog JSON schema in `web/data/catalog.json` and its loading, selection, and rendering in `web/data.js` and `web/app.js`.
- Explore markup, responsive matrix styles, developer settings, translations, and offline data behavior in `web/index.html`, `web/styles.css`, `web/locales/`, and `web/sw.js`.
- OpenSpec behavior contracts for pairwise overlap, catalog generation, and redundancy-score warnings.
