## ADDED Requirements

### Requirement: Register iShares SMI ETF (CH)

The ETF registry SHALL include iShares SMI® ETF (CH) with ISIN `CH0008899764`, ticker `CSSMI`, provider `iShares`, the verified product holdings CSV endpoint, expected format `csv`, parser `ishares_csv_v1`, and the supplied offline fixture.

#### Scenario: CSSMI registry metadata is loaded

- **WHEN** the registry is loaded
- **THEN** it SHALL expose one CSSMI entry with the specified identity, source, format, parser, and fixture metadata

### Requirement: Ingest the complete CSSMI holdings export

The ingestion backend SHALL parse and retain all valid rows from the CSSMI iShares CSV export, including equity, cash, collateral, foreign-currency cash, and futures rows.

#### Scenario: CSSMI fixture ingestion succeeds

- **WHEN** CSSMI is ingested in fixture mode
- **THEN** the resulting snapshot SHALL contain 25 holdings and preserve the provider's source fields

#### Scenario: CSSMI weights are retained

- **WHEN** the CSSMI fixture is normalized
- **THEN** the holdings' provider weights SHALL sum to approximately `99.99%` within the established fixture tolerance

### Requirement: Publish CSSMI catalog data

A successful CSSMI ingestion SHALL produce a normalized dated snapshot and a catalog entry that exposes CSSMI using the registry identity.

#### Scenario: CSSMI snapshot preserves ETF identity

- **WHEN** the CSSMI fixture pipeline completes
- **THEN** the snapshot SHALL contain ISIN `CH0008899764`, ticker `CSSMI`, and name `iShares SMI® ETF (CH)`

#### Scenario: CSSMI is available in the web catalog

- **WHEN** the catalog is regenerated from successful ingestion results
- **THEN** the catalog SHALL include CSSMI and reference its generated snapshot
