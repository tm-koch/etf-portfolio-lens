## Context

The backend is registry-driven. Each ETF entry identifies its source, format, parser, and optional fixture; the ingestion pipeline downloads or copies the source, parses holdings, normalizes them through the security master, aggregates exposure, and writes a dated snapshot. The existing UBS entry uses `ubs_xml_xls_v1`, and the updated UBS SPI® Extra fixture has the same OOXML workbook structure, English headers, and blank-row table terminator.

The frontend is catalog-driven. Successful ingestion results can be published through `web/data/catalog.json`, and the existing Portfolio, Compare, and Explore views load ETF snapshots from the catalog without ETF-specific code.

## Goals / Non-Goals

**Goals:**

- Register UBS SPI® Extra ETF (`CH1553162921`, ticker `SPIEXT`) with its canonical English product identity.
- Reuse the current UBS parser and table termination behavior.
- Validate complete fixture ingestion, normalized snapshot output, aggregates, and catalog publication.
- Make the ETF available end-to-end through existing frontend workflows.

**Non-Goals:**

- Do not add a new parser for the updated workbook.
- Do not introduce German header localization.
- Do not redesign UBS download retrieval or work around dynamic-page/HTTP 403 behavior in this change.
- Do not change the snapshot schema or add ETF-specific frontend components.
- Do not rewrite existing historical snapshots.

## Decisions

1. **Use the existing `ubs_xml_xls_v1` parser.** The updated fixture is recognized as OOXML by its ZIP signature and parses with headers `Securities`, `ISIN`, `Sedol Code`, `Currency`, `Price`, and `Weight %`. A new parser would duplicate working behavior.

2. **Keep the registry source URL as the canonical English UBS product page.** The registry distinguishes product identity from the resolved download path recorded in snapshots. The current generic fetch approach remains in place; live retrieval improvements are deferred.

3. **Use the supplied fixture for deterministic regression coverage.** Fixture ingestion must confirm 179 holdings, preserve the blank-row boundary, exclude UBS disclaimer rows, and produce a weight total within the existing aggregation tolerance.

4. **Publish through the existing catalog command.** Running ingestion with `--update-catalog` adds the ETF metadata and dated snapshot path to the static catalog. No frontend logic changes are required.

5. **Use `SPIEXT` and `UBS SPI® Extra ETF` as registry identity values.** These values are supplied as the authoritative ticker and canonical display name for this change.

## Risks / Trade-offs

- [The UBS product page may return a dynamic shell or HTTP 403 instead of a directly discoverable workbook] -> Keep the current generic approach as requested, retain the fixture for offline and release validation, and defer a provider-specific fetcher to a future change.
- [The source workbook may change its layout or row boundary] -> Keep the raw download, add fixture assertions for header shape, holding count, and disclaimer exclusion, and let parser failures surface during ingestion.
- [Security-master enrichment may not match every Swiss holding] -> Preserve source names and identifiers using existing normalization fallback behavior; do not block the ETF from publication solely on enrichment gaps.
- [Catalog and snapshots can become out of sync] -> Generate the catalog only from successful results of the same ingestion run and validate the new catalog entry references its snapshot.

## Migration Plan

1. Add the new fixture and registry entry.
2. Add or update backend tests for parser compatibility, snapshot identity, holdings completeness, and catalog inclusion.
3. Run fixture ingestion and generate the catalog.
4. Verify the new ETF appears in all existing frontend selection and analysis flows.
5. Roll back by removing the registry entry, fixture, generated catalog entry, and generated snapshot if the integration is rejected; no historical data migration is required.

## Open Questions

- What stable UBS download endpoint, if any, should replace the generic product-page retrieval in a future release?
- How should future source-date extraction be handled if the product workbook date needs to differ from the ingestion run date?
