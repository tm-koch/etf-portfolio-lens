## Context

The ETF identity is defined in `data/etf_registry.json` and copied into the static web catalog at `web/data/catalog.json`. The entry for ISIN `LU0908500753` currently uses an obsolete share-class name and legacy Amundi landing URL. The current Amundi product page identifies the fund as `Amundi Core Stoxx Europe 600 UCITS ETF Acc`.

The ingestion pipeline records registry metadata into newly generated snapshots, while historical snapshots under `data/raw/` are retained as immutable data. This change must therefore correct future metadata without rewriting historical outputs.

## Goals / Non-Goals

**Goals:**

- Use the current Amundi product name and canonical product URL for `LU0908500753`.
- Keep the registry and web catalog consistent.
- Preserve the existing ticker, ISIN, provider, expected format, parser ID, and fixture path.
- Make the next generated snapshot carry the corrected metadata.

**Non-Goals:**

- Resolve the current page's dynamically generated holdings-download endpoint.
- Change XLSX parsing, weight normalization, or parser selection.
- Rewrite historical snapshots or their provenance metadata.
- Change web application behavior beyond the displayed catalog name.

## Decisions

### Keep the current parser and format metadata

The Amundi page still presents full fund holdings as an XLS/XLSX download, and the existing parser handles the established Amundi workbook structure. Preserve `expected_format: "xlsx"` and `parser_id: "amundi_landing_xlsx_v1"` until a separate download-format validation change confirms otherwise.

Changing the parser speculatively would mix identity correction with ingestion behavior and could invalidate existing fixtures.

### Use the canonical product page as source metadata

Set `source_url` to the current product page URL supplied by Amundi. The page is the stable canonical identity reference even though its holdings download is generated dynamically. Resolving that download remains a separate concern because the current fetcher may require provider-specific API handling.

### Synchronize the static catalog explicitly

Update the matching `web/data/catalog.json` entry to the same current name. The catalog is a generated/static projection rather than a runtime read of the registry, so leaving it unchanged would expose stale identity data after the registry correction.

### Preserve historical snapshots

Do not rewrite existing files under `data/raw/`. Their metadata describes the source and registry state used when those snapshots were generated. Future ingestion runs will naturally use the corrected registry entry.

## Risks / Trade-offs

- [The current product page may not be directly downloadable by the existing fetcher] -> Keep download resolution out of this change and track it separately.
- [Static catalog and registry can drift again] -> Add a focused validation or update workflow that checks the matching ISIN metadata during implementation.
- [Existing historical snapshots retain the old name] -> Treat this as intentional historical immutability and document that only future snapshots change.

## Migration Plan

1. Update the registry name and canonical Amundi product URL.
2. Update the matching static web catalog name.
3. Validate JSON structure and exact field preservation.
4. Run focused ingestion/catalog tests without requiring a live Amundi download.

Rollback is a targeted revert of the registry and catalog metadata changes; no historical data migration is required.

## Open Questions

No questions remain for this metadata-only change. The dynamic holdings download endpoint should be handled in a separate proposal.
