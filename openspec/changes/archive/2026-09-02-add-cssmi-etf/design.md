## Context

The backend is registry-driven: each ETF points to a provider source, expected format, parser identifier, and offline fixture. iShares CSV exports are already handled by `ishares_csv_v1`, and CSSMI's supplied endpoint returns CSV with the same holdings columns as the existing iShares fixtures. The CSSMI export contains 20 Swiss equities plus cash, collateral, foreign-currency cash, and a futures row. The security master and existing override registry resolve most equities, but the provider uses a `LOGN` name variant and includes a `USD CASH` row whose ticker can collide with an unrelated security-master record.

The change crosses registry metadata, enrichment, strict validation, snapshot generation, catalog generation, and tests, but does not require a new parser or external dependency.

## Goals / Non-Goals

**Goals:**

- Register CSSMI with its verified ISIN, ticker, name, provider, live CSV URL, parser, and fixture.
- Ingest the complete supplied CSSMI export through the existing iShares CSV path.
- Preserve deterministic fixture ingestion and publish a normalized snapshot and catalog entry.
- Resolve the CSSMI `LOGN` equity through a scoped override.
- Classify CSSMI cash and derivative rows as non-company instruments so ticker collisions cannot create false company identities.
- Make CSSMI pass strict fixture validation for all equity holdings.

**Non-Goals:**

- Adding a new provider adapter or changing the iShares CSV schema.
- Replacing the security master or redesigning general identity matching.
- Adding historical NAV, performance, or benchmark data.
- Changing unrelated ETF integrations or frontend portfolio behavior.

## Decisions

1. **Use the supplied CSV endpoint and existing parser.** The endpoint responds with `text/csv` and 25 parseable rows, while the product page also exposes an alternate XLS link. The direct CSV source matches the fixture and existing iShares registry pattern, so no format-specific downloader work is needed. The XLS link is retained only as provider context, not as the configured source.

2. **Keep the supplied fixture as the offline contract.** The fixture is copied unchanged and used for tests and reproducible snapshot generation. Tests will assert its header shape, row count, weight total tolerance, and CSSMI metadata.

3. **Use a scoped identity override for LOGN.** The override will match ticker, SIX exchange, and the exact provider name variant, then supply the verified Logitech ISIN and canonical company identity. This avoids broad ticker-only matching and remains compatible with future provider naming variants.

4. **Recognize cash and derivatives before company matching for strict identity purposes.** CSSMI rows such as `USD CASH`, collateral, and futures must remain in holdings and aggregates, but must not be treated as companies merely because their ticker resembles a security-master ticker. Existing explicit exemptions will be extended or generalized narrowly for provider cash/derivative classifications, preserving diagnostics and raw provider fields.

5. **Generate snapshots and catalog through existing CLI workflows.** The implementation will run fixture ingestion with the repository security master and overrides, then update the catalog from successful results. No new publication mechanism is introduced.

## Risks / Trade-offs

- [Provider CSV format changes] -> Keep the fixture and assert required headers before normalization; live ingestion continues to fail explicitly on format mismatch.
- [Security-master ticker collisions] -> Use instrument classification and scoped overrides instead of accepting ticker-only matches for cash/derivative rows.
- [Snapshot date churn] -> Generate only the repository's normal dated output and avoid rewriting unrelated historical snapshots.
- [Catalog omission] -> Add a catalog assertion for CSSMI and regenerate the catalog as part of the implementation task.
- [Strict behavior affects existing cash rows] -> Preserve the existing CHSPI exclusions and add tests for both CHSPI and CSSMI before changing shared validation logic.

## Migration Plan

1. Add registry, override, enrichment, and test changes.
2. Run focused CSSMI fixture tests and the full Python test suite.
3. Generate the CSSMI snapshot and update `web/data/catalog.json`.
4. Run catalog and contract validation.
5. Roll back by removing the CSSMI registry/fixture output and reverting the scoped enrichment changes; existing ETF entries remain unchanged.

## Open Questions

- Whether the provider will continue serving the CSV endpoint indefinitely while the product page advertises an XLS download; live ingestion should retain the direct CSV URL until it becomes unavailable.
- Whether future CSSMI exports will use `LOGITECH INTERNATIONAL SA` or another legal-name variant; the implementation should keep the selector narrow and add another explicit selector only when observed.
