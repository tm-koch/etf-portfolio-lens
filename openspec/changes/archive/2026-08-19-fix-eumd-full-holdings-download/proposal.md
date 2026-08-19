## Why

Live ingestion for iShares EUMD (`IE00BF20LF40`) currently downloads the product landing page instead of the holdings CSV. The pipeline then attempts to parse the HTML as a table and fails with `Unsupported source format: .html`; the fix is needed so the CLI can perform a complete live download rather than relying only on the committed fixture.

The change must preserve full-fund holdings. The provider exposes both a complete holdings CSV and other product data endpoints that may contain only top-ten holdings, so accepting a partial response would produce an apparently successful but incorrect snapshot.

## What Changes

- Point the EUMD registry entry at the provider's direct full holdings CSV endpoint.
- Make generic HTML download-link resolution recognize provider links whose CSV format is expressed in query parameters such as `fileType=csv`.
- Validate downloaded source format before table parsing so an HTML landing page cannot reach a CSV/XLS/XLSX parser with a misleading failure.
- Add regression coverage for EUMD's direct export, HTML-to-download resolution, and complete holdings ingestion.
- Keep fixture mode and the existing `ishares_csv_v1` parser unchanged.
- Reject top-ten or otherwise incomplete holdings responses instead of generating a partial snapshot.

## Capabilities

### New Capabilities

- `etf-holdings-ingestion`: Require live iShares EUMD ingestion to resolve the complete holdings export and reject HTML, top-ten, or incomplete source data before normalization.

### Modified Capabilities

None.

## Impact

- `data/etf_registry.json`: update the EUMD source URL while preserving its identity and parser metadata.
- `etf_ingestion_backend/fetching.py`: improve download-link resolution and source validation.
- `etf_ingestion_backend/pipeline.py`: fail early when the downloaded format is incompatible with the registry entry.
- `tests/test_ingestion.py`: add focused live-shaped and completeness regression tests.
- No new dependencies or public CLI flags are required.
