## ADDED Requirements

### Requirement: Preconfigure supported ETF source entries
The system MUST include registry entries for the five supported ETF sources with their ISINs and download links.

#### Scenario: Supported ETF sources are registered
- **WHEN** the ingestion registry is loaded
- **THEN** it MUST include entries for the following ETF sources:
	- IE00B44Z5B48: https://www.ssga.com/ch/en_gb/intermediary/library-content/products/fund-data/etfs/emea/holdings-daily-emea-en-spyy-gy.xlsx
	- LU0908500753: https://www.amundietf.ch/8961ee57-3a33-46f3-8111-02a70fd7493d
	- IE00BCLWRD08: https://www.ishares.com/ch/individual/en/products/257270/ishares-msci-emu-mid-cap-ucits-etf/1495092304805.ajax?fileType=csv&fileName=EMUM_holdings&dataType=fund
	- CH0237935652: https://www.ishares.com/ch/individual/en/products/264107/ishares-spi-ch-fund/1495092304805.ajax?fileType=csv&fileName=CHSPI_holdings&dataType=fund
	- CH0130595124: https://www.ubs.com/9780d2d6-3ef1-4069-8ce9-69c94f32a317

#### Scenario: Registry entry keeps source identity stable
- **WHEN** a supported ETF source is processed
- **THEN** the system MUST associate the snapshot with the ETF's configured ISIN and source URL

### Requirement: Registry-driven ETF source configuration
The system MUST load ETF source definitions from a registry that includes the ETF identifier, source URL, expected source format, and parser identifier.

#### Scenario: Registry entry selects parser
- **WHEN** a registry entry declares a source format and parser identifier
- **THEN** the system MUST use the matching adapter to fetch and parse that ETF source

#### Scenario: New ETF can be added without changing the website contract
- **WHEN** a new ETF is added to the registry with a supported source definition
- **THEN** the system MUST ingest it without requiring any changes to the normalized JSON schema consumed by the website

### Requirement: Normalize ETF holdings into a canonical snapshot
The system MUST convert provider-specific holdings into a canonical JSON snapshot containing ETF metadata, holdings, aggregates, and provenance.

#### Scenario: Snapshots are generated on demand
- **WHEN** the ingestion process is invoked for one or more ETFs
- **THEN** the system MUST generate snapshots only for the requested run

#### Scenario: Snapshots are written to date-stamped folders
- **WHEN** a snapshot is generated
- **THEN** the system MUST write the snapshot to a folder named with the script execution date, such as `data/raw/2026-07-11/`

#### Scenario: Snapshot contains normalized holdings
- **WHEN** a provider holdings file is processed successfully
- **THEN** the system MUST write a snapshot whose holdings use the canonical field structure required by the website

#### Scenario: Snapshot includes provenance metadata
- **WHEN** a snapshot is written
- **THEN** the system MUST include source format, source URL, parser identifier, and raw source fields used during normalization

### Requirement: Enrich missing security attributes from the security master
The system MUST enrich missing sector, country, exchange, asset class, ticker, and name fields using `data/tickers.csv` as the security master.

#### Scenario: Match by ISIN first
- **WHEN** a holding record includes an ISIN that exists in the security master
- **THEN** the system MUST use that record as the primary enrichment match

#### Scenario: Match by ticker and exchange when ISIN is absent
- **WHEN** a holding record does not include a usable ISIN but includes a ticker and exchange
- **THEN** the system MUST attempt enrichment using the ticker plus exchange combination

#### Scenario: Match by aliases as a fallback
- **WHEN** a holding record cannot be matched by ISIN or ticker plus exchange
- **THEN** the system MUST attempt enrichment using aliases from the security master

### Requirement: Generate comparison-ready aggregates
The system MUST derive sector, region, currency exposure, and top-holdings aggregates from the normalized holdings data.

#### Scenario: Sector exposure is derived from holdings weights
- **WHEN** a snapshot is generated
- **THEN** the system MUST include a sector weight breakdown computed from the normalized holdings

#### Scenario: Currency exposure is derived from holdings weights
- **WHEN** a snapshot is generated
- **THEN** the system MUST include a currency weight breakdown computed from the normalized holdings

#### Scenario: Top holdings are included
- **WHEN** a snapshot is generated
- **THEN** the system MUST include a ranked top-holdings summary derived from the holdings weights

### Requirement: Preserve raw source details for traceability
The system MUST preserve raw source fields and parsing warnings alongside normalized holdings so provider differences can be audited.

#### Scenario: Downloaded source files are retained
- **WHEN** a provider file is downloaded for ingestion
- **THEN** the system MUST keep the downloaded file in the date-stamped output folder

#### Scenario: Raw fields remain available after normalization
- **WHEN** a holding is normalized
- **THEN** the system MUST retain the original provider fields in provenance metadata

#### Scenario: Warnings are captured on partial enrichment
- **WHEN** a holding cannot be fully enriched from the security master
- **THEN** the system MUST record a warning in the snapshot provenance

### Requirement: Warn on incomplete unmatched records
The system MUST emit a console warning when a holding record cannot be fully matched or enriched.

#### Scenario: Warning is shown for incomplete matches
- **WHEN** a holding record is missing enough information to complete enrichment
- **THEN** the system MUST print a warning to the console while continuing the ingestion run
