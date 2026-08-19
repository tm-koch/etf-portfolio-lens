## Context

The ingestion pipeline selects registry entries, downloads each `source_url` through `fetch_url()`, and passes the resulting file to the parser selected by `parser_id`. The EUMD registry entry currently points to an iShares product landing page. That page contains a generated full-holdings link, but the generic resolver only recognizes links containing a file extension or the word `download`; the iShares link identifies its format through `fileType=csv`. As a result, the landing page is saved as HTML and parsing fails.

The current iShares export contract is a direct AJAX URL with `fileType=csv`, `fileName=EUMD_holdings`, and `dataType=fund`. The full export is distinct from the page's other AJAX data, including endpoints that can represent top-ten holdings. The existing `ishares_csv_v1` parser and committed EUMD fixture already cover the CSV shape.

## Goals / Non-Goals

**Goals:**

- Resolve the EUMD full holdings CSV during live CLI ingestion.
- Preserve all holdings rows and reject partial or top-ten data.
- Make HTML download-link resolution recognize query-parameter file formats used by iShares.
- Fail early and clearly when a downloaded source format does not match the registry expectation.
- Preserve fixture-mode behavior and existing parser selection.

**Non-Goals:**

- Introduce a new iShares parser.
- Rework portfolio aggregation or frontend catalog behavior.
- Add provider authentication, retries, or a generalized browser automation layer.
- Treat the top-ten endpoint as a valid fallback.

## Decisions

### Use the direct full-holdings URL in the EUMD registry

Set EUMD's `source_url` to the current direct endpoint:

`https://www.ishares.com/ch/professionals/en/products/287746/fund/1495092304805.ajax?fileType=csv&fileName=EUMD_holdings&dataType=fund`

This keeps the registry declarative and avoids depending on page markup for the normal EUMD path. The identity, expected format, parser ID, and fixture path remain unchanged.

Alternative considered: retain the landing page and rely only on HTML link discovery. Rejected as the primary path because page markup is more volatile than the explicit export URL.

### Recognize query-parameter download links generically

Extend the existing HTML link selection logic to treat links with `fileType=csv`, `fileType=xls`, or `fileType=xlsx` as downloadable sources. Continue resolving links relative to the page URL and preserve the existing extension/content-type naming behavior.

Alternative considered: add an EUMD-specific fetcher. Rejected because the link convention is a reusable property of provider download links and does not require a new fetcher abstraction.

### Validate source format before parsing

Add a pipeline-level validation step that compares the downloaded source to the registry's `expected_format` before invoking `parse_table()`. HTML responses and unsupported extensions must produce an explicit source-format error. CSV content should also be recognized by content or URL query when the provider response does not include a `.csv` path suffix.

Alternative considered: allow `parse_table()` to infer CSV from arbitrary HTML-named files. Rejected because it would hide bad downloads and weaken the parser's format boundary.

### Verify completeness through row-level ingestion

The EUMD live regression must assert that the resulting holdings contain more than ten rows and preserve the complete CSV row set, using the known full export or a representative mocked response. The implementation must not select the top-ten AJAX endpoint or silently truncate rows.

Alternative considered: assert only that the command exits successfully. Rejected because a top-ten response could satisfy that check while producing incorrect portfolio exposures.

## Risks / Trade-offs

- [iShares changes the AJAX export identifier or query contract] -> Keep the direct URL in registry metadata, retain fixture coverage, and make the failure identify the received format or missing holdings rows.
- [The landing page exposes multiple CSV-like links] -> Prefer the configured direct registry URL; use HTML discovery only as a generic fallback and select links whose query explicitly requests a file format.
- [A provider returns a CSV payload with an unexpected filename or content type] -> Validate recognizable CSV content and expected headers before table parsing rather than trusting only the path suffix.
- [The full export contains explanatory rows or a changed header layout] -> Reuse the existing parser contract and add a focused regression fixture/test before accepting upstream changes.

## Migration Plan

1. Update the EUMD registry URL and implement the download-resolution and format-validation changes.
2. Add mocked/live-shaped tests proving the full export is selected and more than ten holdings are ingested.
3. Run the focused EUMD tests, the complete backend test suite, and the CLI command against the current provider endpoint.
4. Regenerate snapshots or catalog data only if the implementation workflow requires published data changes.

Rollback removes the direct URL and new validation behavior, restoring the previous registry and fetch path. The committed fixture remains available for offline ingestion throughout.

## Open Questions

None. The current page response identifies the full-holdings endpoint and distinguishes it from the top-ten data path.
