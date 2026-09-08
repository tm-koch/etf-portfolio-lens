## Context

The backend represents supported ETFs as registry entries in `data/etf_registry.json`. The ingestion pipeline uses the registry to select a source URL, expected format, parser ID, and optional offline fixture. Existing UBS entries use the generic downloader, the `xls` format, and `ubs_xml_xls_v1`.

The two supplied workbooks have the same XML-in-XLS structure and headers as the existing UBS fixtures. With `stop_at_empty_row=True`, they produce 30 SMIM holdings totaling 100.0% and 20 SMI holdings totaling approximately 100.0%. The parser and normalization code already recognize the UBS `ISIN`, `Securities`, `Currency`, and `Weight %` fields.

## Goals / Non-Goals

**Goals:**

- Add both UBS ETFs as selectable registry entries with stable identity and source metadata.
- Reuse `ubs_xml_xls_v1`, the generic downloader, normalization, and snapshot generation.
- Preserve deterministic fixture ingestion and verify that legal footer text is excluded.
- Validate live source behavior without adding a browser automation dependency.

**Non-Goals:**

- Add a new parser or alter the existing UBS parser contract.
- Add a UBS-specific API client or scraper in this change.
- Change security-master enrichment or add manual overrides unless fixture validation identifies a concrete unresolved holding that blocks the requested default behavior.
- Change frontend presentation beyond catalog regeneration through the existing workflow.

## Decisions

### Use registry metadata as the integration surface

Add one entry per ISIN with provider `UBS`, expected format `xls`, parser ID `ubs_xml_xls_v1`, the supplied fixture path, and the canonical fund-page URL. This matches the existing UBS SPI and SPI Extra entries and keeps transport selection separate from table interpretation.

### Reuse the existing UBS parser unchanged

The workbooks use the same header row and XML spreadsheet structure already handled by `parse_xlsx_bytes`. The pipeline already enables `stop_at_empty_row` for `ubs_xml_xls_v1`, which removes provider legal text after the holdings table. A parser change would increase risk without addressing a demonstrated format difference.

### Use fixture tests as the deterministic contract

Tests will assert registry metadata, workbook row counts, complete ISIN/weight rows, approximate 100% weight totals, and successful fixture snapshots. This protects the offline workflow independently of UBS page availability.

### Treat live download resolution as a smoke check

The product-page URLs remain the canonical `source_url` values. The generic downloader may resolve a linked workbook when UBS exposes one, but cookie-gated or dynamically rendered pages can prevent deterministic discovery. The implementation must document or test the observed live behavior rather than introduce a speculative provider-specific fetcher.

## Risks / Trade-offs

- [UBS changes the product-page markup or blocks automated requests] -> Keep fixture mode as the deterministic path and report live retrieval failure explicitly; isolate any future UBS fetcher in a separate change.
- [Security-master coverage differs for the new constituents] -> Preserve default diagnostic behavior, inspect fixture snapshots, and add narrowly scoped overrides only when required by strict validation.
- [Ticker naming differs from exchange conventions] -> Use the fund's registry ticker only for ETF identity; constituent identity continues to use provider ISINs and existing security-master matching.
- [Small rounding differences make exact weight assertions brittle] -> Assert approximate totals with a narrow tolerance while requiring every retained holding row to have a numeric weight.

## Migration Plan

1. Add the two registry entries and fixture-focused tests.
2. Run fixture ingestion for both ISINs and inspect generated snapshots.
3. Run the backend test suite and a live smoke check against both product pages.
4. Regenerate the catalog only through the existing explicit catalog-update workflow if the application should publish the new ETFs.

Rollback removes the two registry entries and any generated catalog/snapshot outputs created for them. Existing UBS entries and historical snapshots remain unchanged.

## Open Questions

- Whether UBS exposes a stable direct workbook link to automated clients on the current product pages; this should be resolved by the live smoke check.
- Whether strict mode can resolve every new constituent from the current security master without additional verified overrides.