## Context

This change defines the backend ingestion layer for ETF holdings data. The repository already contains a security master in `data/tickers.csv` and sample provider outputs in mixed formats, including CSV, XML spreadsheet `.xls`, and `.xlsx`. The website depends on a single normalized data contract, but the sources are heterogeneous and provider-specific.
The user has also defined operational constraints for the backend: snapshots are generated on demand, raw downloads are retained, incomplete unmatched records must emit console warnings, and generated artifacts should live under a date-stamped folder such as `data/raw/<run-date>/`.

## Goals / Non-Goals

**Goals:**
- Build a Python-based ingestion pipeline that can fetch ETF holdings from multiple providers.
- Normalize holdings into a stable JSON snapshot format that the static website can consume directly.
- Enrich incomplete provider data using `data/tickers.csv` as the canonical fallback reference.
- Support the five current ETFs without hardcoding the website to any single provider format.
- Keep the ingestion architecture extensible for future ETFs and new source formats.
- Generate snapshots on demand into a date-stamped directory and retain the downloaded raw files for each run.
- Emit console warnings when holdings cannot be fully matched or enriched.

**Non-Goals:**
- Building the frontend visualization layer.
- Designing the portfolio-selection UI.
- Creating an opinionated investment model or ranking algorithm.
- Solving all upstream data-quality issues beyond deterministic enrichment and validation.

## Decisions

1. **Use a registry-driven adapter architecture**
   - Each ETF source is defined in a registry entry with source URL, expected format, and parser identifier.
   - Provider-specific adapters encapsulate download and parsing quirks.
   - Alternative considered: one generic parser with a large rules table. Rejected because the providers vary enough that it would become brittle and difficult to extend.

2. **Normalize to a single JSON snapshot contract**
   - The ingestion layer will emit one canonical JSON file per ETF per snapshot date.
   - Each snapshot will include ETF metadata, holdings, aggregates, and provenance.
   - Alternative considered: writing provider-native artifacts and letting the frontend adapt. Rejected because it would leak source complexity into the website and comparison logic.

3. **Store run outputs under a date-stamped folder**
   - Each execution should write snapshots and retained raw downloads into a folder named for the execution date, such as `data/raw/2026-07-11/`.
   - This keeps reruns isolated and preserves the exact inputs used for each snapshot.
   - Alternative considered: a shared latest-output directory. Rejected because it makes auditability and reruns harder.

4. **Treat `data/tickers.csv` as the enrichment source of truth**
   - The security master will fill missing sector, country, asset class, exchange, and alias data when source files omit them.
   - Matching priority should be deterministic: ISIN first, then ticker plus exchange, then aliases.
   - Alternative considered: provider-derived enrichment only. Rejected because the providers are inconsistent and incomplete across formats.

5. **Separate raw source provenance from normalized fields**
   - Normalized holdings will store the fields needed by the website.
   - Raw source fields and parser metadata will be preserved in provenance for traceability and debugging.
   - Alternative considered: flattening everything into the normalized row. Rejected because debugging provider differences would become difficult.

6. **Compute comparison-ready aggregates during ingestion**
   - Sector, region, and currency exposure should be derived once in the backend rather than recalculated in the frontend for every render.
   - Alternative considered: deferring all aggregation to the UI. Rejected because it duplicates logic and makes cross-ETF comparison harder to keep consistent.

7. **Warn on partial matches instead of failing silently**
   - If a record cannot be fully matched to the security master, the backend should continue processing but must emit a console warning.
   - Alternative considered: silently preserve the incomplete record. Rejected because operational visibility is required for data quality review.

## Risks / Trade-offs

- [Provider formats change unexpectedly] -> Keep adapters isolated, add source-specific tests, and fail with descriptive parser errors.
- [Security master mismatches create incorrect enrichment] -> Use deterministic lookup order, preserve raw fields, and surface enrichment warnings in provenance.
- [Some source data is missing critical fields] -> Allow partial normalization where safe, but require clear validation failures for required identifiers.
- [Backend schema drift breaks the website] -> Version the JSON snapshot schema and keep the output contract small and explicit.
- [Retained raw downloads increase storage usage] -> Use date-stamped directories and document cleanup/retention policy later if needed.

## Migration Plan

1. Introduce the source registry and canonical JSON schema.
2. Implement adapter(s) for the five known ETF sources.
3. Validate enrichment against `data/tickers.csv` and generate one snapshot per ETF on demand.
4. Wire the static website to read the normalized JSON snapshots from the date-stamped output folder.
5. Add a process for registering new ETFs without changing the frontend contract.

Rollback strategy: keep the raw source files and registry entries intact so a failed ingestion run can be reprocessed after adapter fixes without changing the website contract.

## Open Questions

- How strict should validation be for incomplete provider records that cannot be matched in the security master?
- What cleanup policy, if any, should apply to the retained date-stamped raw download folders?
