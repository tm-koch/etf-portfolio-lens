## ADDED Requirements

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
