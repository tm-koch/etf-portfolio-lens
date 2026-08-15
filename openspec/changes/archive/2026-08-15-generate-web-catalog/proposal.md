## Why

Ingestion writes date-stamped snapshots but does not refresh the static catalog consumed by the web app, so the frontend can continue showing stale names and snapshot paths after a successful ingestion run. The workflow needs an explicit opt-in catalog update that publishes the latest selected snapshot set without making every backend run mutate frontend assets unexpectedly.

## What Changes

- Add an `--update-catalog` CLI option to `python -m etf_ingestion_backend`.
- When combined with ingestion, generate `web/data/catalog.json` from the latest successful snapshot set.
- Preserve the existing catalog schema: `generatedAt`, `basis`, and ETF entries with ISIN, ticker, name, provider, and snapshot path.
- Select the catalog snapshot date from the current ingestion output rather than hardcoding a date.
- Include only ETFs with successfully generated snapshots and preserve registry ordering.
- Add root README documentation for the explicit command:
  `python -m etf_ingestion_backend --all --fixtures --update-catalog`.
- Keep catalog updates opt-in; ingestion without `--update-catalog` continues to write snapshots only.

## Capabilities

### New Capabilities

- `web-catalog-generation`: Generate the frontend ETF catalog from a dated ingestion snapshot set.

### Modified Capabilities

## Impact

- `etf_ingestion_backend/cli.py`: Add the opt-in catalog update flag and invoke catalog generation after successful ingestion.
- New backend catalog-generation module: Build and validate the frontend manifest.
- `web/data/catalog.json`: Become an explicit generated output of the opt-in workflow.
- `README.md`: Document the combined ingestion and catalog-refresh command.
- Tests: Cover date selection, registry ordering, missing/failed snapshots, schema output, and opt-in behavior.
- No changes to snapshot format, frontend runtime loading, or ingestion parser behavior.
