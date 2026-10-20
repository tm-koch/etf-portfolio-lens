# Spec Delta

## ADDED Requirements

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