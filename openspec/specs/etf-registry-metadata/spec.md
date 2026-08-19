# etf-registry-metadata Specification

## Purpose
TBD - created by archiving change correct-amundi-fund-metadata. Update Purpose after archive.
## Requirements
### Requirement: Canonical Amundi ETF identity
The registry SHALL identify ISIN `LU0908500753` with the current Amundi product name `Amundi Core Stoxx Europe 600 UCITS ETF Acc`, canonical product URL `https://www.amundietf.ch/en/professional/products/equity/amundi-core-stoxx-europe-600-ucits-etf-acc/lu0908500753`, and an explicit Amundi full-holdings fetch strategy separate from its parser ID.

#### Scenario: Registry contains current Amundi identity
- **WHEN** the ETF registry entry for `LU0908500753` is read
- **THEN** its name and source URL match the current Amundi product identity

#### Scenario: Registry selects the Amundi fetcher
- **WHEN** live ingestion selects the entry for `LU0908500753`
- **THEN** the entry identifies the Amundi full-holdings fetch strategy independently from `parser_id`

#### Scenario: Existing identity fields remain stable
- **WHEN** the corrected registry entry is compared with the previous entry
- **THEN** its ISIN, ticker `MEUD`, provider `Amundi`, expected format `xlsx`, parser ID `amundi_landing_xlsx_v1`, and fixture path remain unchanged

### Requirement: Synchronized web catalog metadata
The static web catalog SHALL expose the same corrected name for ISIN `LU0908500753` as the ETF registry.

#### Scenario: Catalog displays current Amundi name
- **WHEN** the web catalog entry for `LU0908500753` is loaded
- **THEN** its displayed name is `Amundi Core Stoxx Europe 600 UCITS ETF Acc`

#### Scenario: Registry and catalog names agree
- **WHEN** registry and catalog entries are compared by ISIN
- **THEN** the name for `LU0908500753` is identical in both sources

### Requirement: Historical snapshot preservation
The metadata correction SHALL apply to future generated data without rewriting existing historical snapshots.

#### Scenario: Existing snapshots remain unchanged
- **WHEN** the registry and catalog metadata are corrected
- **THEN** existing files under `data/raw/` are not modified as part of the change

#### Scenario: Future snapshot uses corrected identity
- **WHEN** a new ingestion run creates a snapshot for `LU0908500753`
- **THEN** the snapshot metadata uses the corrected registry name and canonical source URL

### Requirement: UBS SPI Extra registry metadata
The ETF registry SHALL include the canonical identity and fixture metadata for UBS SPI® Extra ETF in addition to its existing ETF entries.

#### Scenario: New UBS identity is represented
- **WHEN** registry metadata is read for ISIN `CH1553162921`
- **THEN** the entry uses ticker `SPIEXT`, name `UBS SPI® Extra ETF`, provider `UBS`, and the English UBS product page as `source_url`

#### Scenario: Existing registry entries remain available
- **WHEN** the registry is loaded after the new entry is added
- **THEN** all existing ETF entries remain present and unchanged

