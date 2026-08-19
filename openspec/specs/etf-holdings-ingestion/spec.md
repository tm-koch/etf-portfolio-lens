# etf-holdings-ingestion Specification

## Purpose

Define reliable provider download resolution and completeness safeguards for ETF holdings ingestion, including the iShares EUMD full-fund export.

## Requirements

### Requirement: Resolve the complete EUMD holdings export

The ingestion backend SHALL use the iShares EUMD full holdings export for ISIN `IE00BF20LF40`, rather than the product landing page or a top-ten holdings endpoint.

#### Scenario: Direct EUMD export is configured

- **WHEN** the registry entry for `IE00BF20LF40` is loaded
- **THEN** its source URL requests the iShares holdings file with `fileType=csv`, `fileName=EUMD_holdings`, and `dataType=fund`

#### Scenario: EUMD live ingestion receives the full export

- **WHEN** live ingestion processes `IE00BF20LF40`
- **THEN** it passes the complete holdings CSV to the existing `ishares_csv_v1` parser

### Requirement: Resolve provider links that declare format in query parameters

The generic URL fetcher SHALL recognize HTML links as downloadable sources when their query parameters explicitly request `fileType=csv`, `fileType=xls`, or `fileType=xlsx`, including when the link is relative to the source page.

#### Scenario: iShares CSV link is discovered from HTML

- **WHEN** an HTML page contains a relative link with `fileType=csv`
- **THEN** the fetcher resolves it against the page URL and downloads that linked resource instead of returning the HTML page

#### Scenario: Non-download page response is rejected before parsing

- **WHEN** a configured holdings source returns HTML and no valid download link can be resolved
- **THEN** ingestion fails with an explicit source-format validation error before invoking a holdings table parser

### Requirement: Preserve complete holdings and reject partial data

The ingestion backend SHALL reject top-ten or otherwise incomplete EUMD holdings data and SHALL NOT generate a successful partial snapshot.

#### Scenario: Full holdings are retained

- **WHEN** the EUMD export contains the complete holdings table
- **THEN** ingestion retains every valid holdings row and generates a snapshot whose holdings count is greater than ten

#### Scenario: Top-ten response is rejected

- **WHEN** the selected EUMD response contains only ten holdings rows or a top-ten breakdown
- **THEN** ingestion fails with an incomplete-holdings error and does not generate a partial snapshot

#### Scenario: Required CSV structure is missing

- **WHEN** the downloaded response cannot be parsed as the expected iShares holdings CSV
- **THEN** ingestion fails before normalization with an explicit format-validation error

### Requirement: Preserve offline fixture behavior

The EUMD download fix SHALL preserve deterministic fixture-based ingestion and the existing parser contract.

#### Scenario: Fixture mode remains offline

- **WHEN** EUMD ingestion runs with `--fixtures`
- **THEN** it uses `data/example/EUMD_holdings.csv` without contacting the iShares source URL

#### Scenario: Parser identity remains stable

- **WHEN** the EUMD registry entry is updated
- **THEN** its `expected_format` remains `csv` and its `parser_id` remains `ishares_csv_v1`
