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

### Requirement: Register the Amundi Prime All Country World identity
The ETF registry SHALL contain canonical metadata for ISIN `IE0009HF1MK9`, including its Amundi product name, product URL, provider, ticker, full-holdings fetch strategy, parser, and supplied fixture path.

#### Scenario: New Amundi identity is represented
- **WHEN** the registry is loaded for `IE0009HF1MK9`
- **THEN** it returns the canonical product identity and the supplied Amundi workbook fixture metadata

#### Scenario: Existing registry entries remain stable
- **WHEN** the new registry entry is added
- **THEN** all existing ETF entries remain selectable with their existing source and parser fields

### Requirement: Represent fund and listing metadata independently
The registry SHALL represent the USD share-class currency and the intended SIX CHF listing metadata independently, including the exchange, listing ticker, and listing quote currency.

#### Scenario: CHF SIX listing metadata is available
- **WHEN** metadata for `IE0009HF1MK9` is read
- **THEN** it identifies SIX Swiss Exchange, listing ticker `WEBGCHF`, listing currency CHF, and share-class currency USD

#### Scenario: Listing currency does not rewrite source currency
- **WHEN** a live quote or imported position is loaded for the ETF
- **THEN** registry listing metadata remains descriptive and the source record's currency remains authoritative for valuation

### Requirement: Synchronize catalog identity
The generated web catalog SHALL include the new ETF with the same ISIN, ticker, name, and provider as the registry after successful ingestion.

#### Scenario: Successful ingestion updates catalog selection
- **WHEN** catalog generation runs with a successful `IE0009HF1MK9` snapshot
- **THEN** the catalog contains a selectable entry pointing to that snapshot

### Requirement: Register the three requested ETF identities
The registry SHALL include canonical identities and supplied fixture metadata for all three requested ETFs.

#### Scenario: iShares Europe identity is available
- **WHEN** registry metadata is read for `IE00B4K48X80`
- **THEN** it identifies iShares Core MSCI Europe UCITS ETF EUR (Acc), provider iShares, and the supplied IMEA holdings fixture

#### Scenario: iShares Emerging Markets IMI identity is available
- **WHEN** registry metadata is read for `IE00BKM4GZ66`
- **THEN** it identifies iShares Core MSCI EM IMI UCITS ETF, provider iShares, and the supplied EIMI holdings fixture

#### Scenario: UBS Core MSCI World identity is available
- **WHEN** registry metadata is read for `IE00BD4TXV59`
- **THEN** it identifies UBS Core MSCI World UCITS ETF USD acc, provider UBS, the supplied UBS holdings fixture, and fixture-only processing

### Requirement: Represent fund and quote currencies independently
The registry SHALL retain each ETF's share-class currency independently from its intended listing quote currency and ticker.

#### Scenario: iShares Europe currency metadata is distinct
- **WHEN** metadata for `IE00B4K48X80` is read
- **THEN** its share-class currency is EUR and its intended quote ticker and currency are IMEA and CHF

#### Scenario: iShares Emerging Markets IMI quote metadata is available
- **WHEN** metadata for `IE00BKM4GZ66` is read
- **THEN** its share-class currency and intended quote currency are both USD and its intended quote ticker is EIMI

#### Scenario: UBS Core MSCI World currency metadata is distinct
- **WHEN** metadata for `IE00BD4TXV59` is read
- **THEN** its share-class currency is USD and its intended quote ticker and currency are WRDUSW and CHF

### Requirement: Synchronize new identities to the generated catalog
After successful ingestion, the generated web catalog SHALL expose each new ETF with the same ISIN, ticker, name, and provider as its registry entry.

#### Scenario: Each new ETF is selectable after catalog generation
- **WHEN** catalog generation runs with successful snapshots for the three new ISINs
- **THEN** the catalog contains selectable entries matching their registry identity metadata

### Requirement: Preserve historical snapshots when adding ETF identities
Adding the three registry and catalog entries SHALL NOT rewrite existing historical snapshots.

#### Scenario: Existing raw snapshots remain unchanged
- **WHEN** the new ETF registry entries and catalog data are generated
- **THEN** files for existing snapshots under `data/raw/` remain unchanged
