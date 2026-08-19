## Why

The registry and published web catalog do not currently include UBS SPI® Extra ETF (`CH1553162921`), so users cannot ingest, select, compare, or include this Swiss equity ETF in portfolio analysis. The supplied UBS holdings workbook matches the existing UBS OOXML spreadsheet parser, making this a focused registry and end-to-end data integration.

## What Changes

- Add UBS SPI® Extra ETF to the registry with ticker `SPIEXT`, ISIN `CH1553162921`, canonical English product URL, UBS provider metadata, and the supplied holdings fixture.
- Reuse the existing `ubs_xml_xls_v1` parser and UBS empty-row table termination behavior.
- Generate and validate a normalized snapshot with holdings and aggregate data for the new ETF.
- Regenerate the static web catalog so the frontend discovers the ETF through its existing catalog and snapshot loading paths.
- Add regression coverage for the new fixture, snapshot identity, holdings boundary, and catalog entry.
- Keep the current generic UBS product-page download approach; improving handling for dynamic pages or HTTP 403 responses is explicitly deferred to a future release.

## Capabilities

### New Capabilities

- `ubs-spi-extra-etf`: Registry, ingestion, snapshot, and published catalog support for UBS SPI® Extra ETF.

### Modified Capabilities

- `etf-registry-metadata`: Extend registry identity and fixture coverage to include the new UBS ETF.
- `web-catalog-generation`: Require the generated catalog to expose the newly registered ETF when its ingestion succeeds.

## Impact

- Affected data: `data/etf_registry.json`, the new example workbook, generated `data/raw/<run-date>/` snapshot data, and `web/data/catalog.json`.
- Affected backend surfaces: registry loading, existing UBS parsing/normalization path, ingestion tests, and catalog generation tests.
- Affected frontend behavior: existing catalog-driven Portfolio, Compare, and Explore workflows will gain the new ETF without ETF-specific UI code.
- No public API or snapshot schema change is expected.
- Live UBS retrieval remains subject to the current product-page behavior and is not expanded by this change.
