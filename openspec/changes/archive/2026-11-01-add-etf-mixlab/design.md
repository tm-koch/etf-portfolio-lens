# Design

## Context

See `proposal.md` for motivation and the spec deltas for externally visible behavior. The app already has a destination registry, local portfolio state, published ETF snapshots, company-level look-through aggregation, an inverse-HHI effective-company metric, and static catalog loading. The registry model and catalog builder currently whitelist metadata fields, so new registry values must be propagated explicitly. Existing snapshots are retained as historical artifacts.

The published candidate catalog is small enough for a bounded browser-side search. Holdings coverage and country classification vary by ETF, so a country match cannot be presented without its classified-coverage figure. The current diversification calculation already normalizes disclosed company weights and reports holdings coverage; MixLab should reuse the same semantics rather than create a second HHI definition.

## Goals / Non-Goals

**Goals:**
- Keep portfolio data and all optimizer calculations local to the browser.
- Separate current-portfolio look-through targets from custom fund-sleeve allocations.
- Make the data basis, constraints, ranking, and estimates inspectable.
- Add metadata additively without rewriting historical snapshots; include verified weighted portfolio TER in PDF summary metrics without exposing MixLab controls or modeled results.

**Non-Goals:**
- Execute trades, mutate the saved portfolio, or provide tax-aware advice.
- Support bonds, cash, commodities, or other non-equity asset classes in this iteration.
- Claim that the result is optimal across the whole ETF market; it is limited to the published catalog.
- Add MixLab data to PDF export or shared-portfolio URLs.

## Decisions

### Keep the two target models distinct

Consolidation mode derives a target vector from the current portfolio's underlying holdings. Use exclusive country buckets: Switzerland, developed Europe ex-Switzerland, North America, developed Asia-Pacific, emerging markets, other classified markets, and unclassified. Each normalized country identifier maps to at most one bucket. Keep the mapping versioned and include its reference source and effective date in the methodology disclosure.

Custom mode treats entered percentages as fund-sleeve capital allocations, not look-through exposures. Classify products explicitly as developed World, all-country World, emerging markets, Europe, or Switzerland. World plus regional sleeves may overlap by design; always calculate and display the resulting country exposures separately. Do not infer a product's sleeve from its name or ticker.

### Use additive, stable optimizer metadata

Add TER as a numeric percentage-point value (`0.06` means 0.06%), a controlled distribution policy (`accumulating` or `distributing`), and explicit investment-universe classifications to registry entries and published catalog entries. Extend the typed registry model and the catalog serializer together. Preserve source/as-of provenance where available; missing metadata remains unavailable and cannot be treated as zero cost.

Add a normalized ISO 3166-1 alpha-2 `country_code` to newly generated holding classifications when it is supported by an exact security-master match or verified override. Preserve the existing country label and provenance. Do not rewrite older snapshots; MixLab treats missing identifiers or unmapped codes as unclassified exposure.

### Keep the optimizer bounded and deterministic

Precompute each eligible ETF's country vector, sparse company weights, coverage, TER, distribution policy, sleeve classification, and snapshot date after catalog and snapshots load. Consolidation searches product sets from one to five ETFs, then solves non-negative allocations that sum to 100% for each set. Use a deterministic constrained optimizer over the small candidate space; reject sets that cannot meet the exposure threshold. Custom mode holds user-entered sleeve totals fixed and selects eligible products within each active sleeve.

For consolidation, define proportional overlap as `sum(min(targetBucket, candidateBucket))` over the exclusive country buckets after normalizing the classified exposure vectors. Do not label a candidate as meeting the exposure requirement unless both target and candidate have at least 95% classified country exposure and overlap meets the selected threshold. Preserve unclassified weights for display rather than silently redistributing them.

Calculate effective companies with the existing company aggregation semantics: combine exposures by canonical company identity, normalize positive disclosed weights, calculate HHI, and report its inverse. The slider maps to normalized weighted TER versus normalized HHI penalty; display the unnormalized TER and effective-company values beside the score. Enforce enabled TER and effective-company bounds, distribution filtering, and exposure conditions before ranking. Break otherwise equivalent ranks by fewer ETFs, then lower TER. If no result qualifies, return the nearest candidates with each failed condition identified.

### Add a read-only Lab view

Register `Lab` as a primary destination with a flask-style Lucide icon and a dedicated panel. Use a segmented mode selector, sleeve percentage inputs or current-portfolio summary, distribution-policy segmented control defaulting to Both, a TER-versus-breadth slider, independently enabled numeric limits, and the CHF 10,000 portfolio-value input for percentage mode. The value input and results are Lab-only state; they do not alter portfolio shares or allocation units.

Show a ranked result summary with fund mix, weights, TER, annual cost estimate, effective companies, exposure overlap or sleeve fit, actual look-through country exposures, classified coverage, and unclassified exposure. Keep source snapshot dates as data provenance, not as metrics in result cards. Include a methodology disclosure covering country mapping, unknown exposure, TER-estimate basis, taxes/trading costs, and catalog scope. Use localized strings in the app's supported locales. Keep report generation and report analytics unchanged.

Show annual TER change as candidate cost minus the current baseline, so a cost improvement is negative. Label maximum weighted TER with its percent unit and limit it to three decimal places; limit minimum effective companies to one decimal place. Place the Mix type selector inside the shared Lab controls card and omit the divider above Distribution policy. Keep a clear gap between both fieldset legends and their segmented selectors. Render the custom sleeve allocation title inside its card and use it as the accessible group label. In consolidation mode, show either the empty-portfolio message or the current-portfolio summary, ensure the hidden state does not occupy layout space, and separate visible state cards by the same 18px gap used between Explore cards. Seed the independently disabled maximum-TER and minimum-effective-company inputs from available current-portfolio metrics, refreshing them on portfolio changes until each value is manually edited. Add a Home summary card with weighted TER and annual CHF cost, reusing current portfolio weights and TER metadata. For an empty portfolio, show 0% TER and CHF 0.00 annual cost; for non-empty percentage-only portfolios, show weighted TER but leave the absolute CHF cost unavailable because the Lab-only value input is not a Home valuation.

### Add weighted portfolio TER to PDF summaries

Add the same weighted portfolio TER metric shown on Home to the PDF summary metrics, with estimated annual CHF cost as detail in the same card when CHF valuations are complete. Derive both from portfolio weights and verified TER metadata, show zero for an empty portfolio, and show unavailable when the required TER or valuation data is incomplete. Percentage-only portfolios show weighted TER but no absolute CHF cost. Keep detailed metric cards at 22 mm with their text baselines compacted so later analytics content clears the page footer. Do not include MixLab inputs or modeled alternatives.

### Preserve fractional limit editing

Do not normalize numeric limit values on each keystroke. Preserve the active edit buffer, then round to the configured maximum precision when the value is committed so decimal values can be entered naturally.

### Keep the feature advisory-neutral

Use `MixLab` as the page title and `Lab` as the tab label. Describe outputs as modeled or illustrative mixes, never as trade instructions or personalized financial advice. Keep provider order neutral and avoid sponsored ranking. Naming and disclosures do not establish regulatory compliance; obtain review before launch.

## Risks / Trade-offs

- [Incomplete or stale holdings data can distort exposure similarity] → Preserve source snapshot dates in the underlying data, show classified coverage in results, and require at least 95% country coverage to claim a qualifying match.
- [Country market classification can change or vary by provider] → Maintain a versioned project mapping, disclose its reference and date, and test that each country maps to no more than one bucket.
- [Catalog metadata can be stale or missing] → Preserve TER and distribution provenance, exclude missing values from affected ranking/filter paths, and identify unavailable values rather than defaulting to zero.
- [A bounded search can miss a better mix outside its product-count cap] → Disclose the five-ETF search limit and catalog date; keep the bound explicit and tested.
- [Cost and diversification normalization can make slider scores difficult to interpret] → Use fixed documented normalization rules, show raw metrics, and test slider endpoints and tie-breaking behavior.
- [Personalized product comparisons may have regulatory implications] → Use neutral educational language and obtain Swiss compliance review before release.

## Migration Plan

1. Add validated optimizer metadata to registry models and source entries; publish it through the catalog builder.
2. Extend newly generated snapshots with country identifiers where verified, without modifying historical data.
3. Implement and unit-test the data normalization and bounded optimizer before connecting the UI.
4. Add the Lab destination, localized controls, disclosures, and result states; verify responsive behavior and report exclusion.
5. Regenerate the current fixture-backed catalog/snapshots and validate the metadata and snapshot provenance before publishing.

Rollback removes the Lab destination and panel and reverts optimizer-specific metadata fields. Existing snapshots and older catalog consumers remain usable because additions are optional and historical files are unchanged.

## Open Questions

None. The country mapping source and effective date are recorded as versioned data during implementation; changing the bucket semantics later would require a spec update.
