# Proposal

## Why

ETF Portfolio Lens already helps users inspect look-through holdings, but it does not help them compare simpler, lower-cost ETF mixes while retaining a chosen exposure profile. MixLab adds a private, client-side comparison workflow using the published catalog, giving users transparent estimates without sending portfolio data to a backend.

## What Changes

- Add a primary-navigation destination labelled **Lab**, with a **MixLab** page for interactive portfolio-mix comparisons.
- Provide two modes: consolidate a current portfolio while preserving its country-bucket exposure, or build a custom allocation across explicitly classified fund sleeves. Sleeve allocations are not represented as look-through exposure targets, and the sleeve allocation title appears inside its card.
- Rank candidate mixes using weighted TER and effective number of underlying companies, controlled by a user-facing balance slider. Preserve exposure within a default 97% proportional-overlap threshold in consolidation mode, and prefer fewer ETFs as a tie-breaker.
- Provide independently enabled maximum-TER and minimum-effective-company constraints, with TER expressed as a percentage, fractional values accepted during editing, and limit precision capped at three and one decimal places respectively. When no mix satisfies all active constraints, show the closest alternatives and identify each unmet constraint.
- Prefill the maximum-TER and minimum-effective-company limits with the current portfolio's weighted TER and effective-company breadth when available, while leaving each constraint disabled until enabled by the user.
- Add an editable CHF portfolio-value input defaulting to CHF 10,000 for percentage-only portfolios, and a distribution-policy filter defaulting to Both.
- Add a Home summary card showing the portfolio's weighted TER and estimated annual CHF cost when the required metadata and valuations are available, with zero TER and cost for an empty portfolio.
- Include weighted portfolio TER and estimated annual CHF cost in the PDF summary using the same availability rules as Home, without adding MixLab inputs or modeled alternatives.
- Keep PDF summary metric cards compact enough that subsequent analytics content remains clear of the page footer.
- Show modeled mix allocations, look-through country exposures, estimated annual TER costs and signed cost changes where a baseline is available (negative means the candidate costs less), classified and unclassified exposure, and explicit exclusions for taxes and trading costs. Keep source snapshot dates as data provenance, not as metrics in result cards.
- Publish TER, distribution policy, sleeve/universe classifications, and normalized country identifiers needed by the browser-side comparison.
- Keep MixLab interactive-only; do not add its inputs or results to PDF reports. Use educational comparison language rather than presenting outputs as financial advice; legal compliance remains subject to review.

## Capabilities

### New Capabilities
- `portfolio-mixlab`: Client-side portfolio consolidation and custom fund-sleeve mix comparison, including constraints, ranking, results, and data-quality disclosures.

### Modified Capabilities
- `etf-registry-metadata`: Store TER, distribution policy, and explicit fund-universe classifications for registered ETFs.
- `web-catalog-generation`: Publish the new optimizer metadata with each catalog ETF entry.
- `etf-holdings-ingestion`: Persist normalized country identifiers in generated holdings snapshots for deterministic geographic grouping.
- `security-identity-enrichment`: Populate a holding's country identifier from verified identity data when available, while retaining missing or conflicting data as explicit unknowns.

## Impact

- Backend metadata model, registry loading, snapshot serialization, and catalog generation; existing historical snapshots remain unchanged.
- Browser navigation, Lab panel, localization, optimizer, catalog data loading, and focused UI/runtime tests.
- No new server or optimization dependency; calculations remain local to the browser and operate on published snapshots.
- PDF reports gain the verified weighted portfolio TER summary metric and annual CHF cost detail; existing portfolio valuation and entry-mode behavior remains unchanged.
