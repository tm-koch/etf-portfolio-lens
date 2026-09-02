## ADDED Requirements

### Requirement: Register iShares SMIM ETF (CH)

The ETF registry SHALL include iShares SMIM® ETF (CH) with ISIN `CH0019852802`, ticker `CSSMIM`, provider `iShares`, the verified iShares holdings CSV endpoint, expected format `csv`, parser `ishares_csv_v1`, and the supplied offline fixture.

#### Scenario: CSSMIM registry metadata is loaded

- **WHEN** the registry is loaded
- **THEN** it SHALL expose one CSSMIM entry with the specified identity, source URL, format, parser, and fixture metadata

### Requirement: Ingest the complete CSSMIM holdings export

The ingestion backend SHALL parse and retain all valid rows from the CSSMIM iShares CSV export, including equity, cash, collateral, foreign-currency cash, and futures rows.

#### Scenario: CSSMIM fixture ingestion succeeds

- **WHEN** CSSMIM is ingested in fixture mode
- **THEN** the resulting snapshot SHALL contain 34 holdings and preserve the provider source fields

#### Scenario: CSSMIM weights are retained

- **WHEN** the CSSMIM fixture is normalized
- **THEN** the holdings' provider weights SHALL sum to `100.0%` within the established fixture tolerance

### Requirement: Publish CSSMIM catalog data

A successful CSSMIM ingestion SHALL produce a normalized dated snapshot and a catalog entry that exposes CSSMIM using the registry identity.

#### Scenario: CSSMIM snapshot preserves ETF identity

- **WHEN** the CSSMIM fixture pipeline completes
- **THEN** the snapshot SHALL contain ISIN `CH0019852802`, ticker `CSSMIM`, and name `iShares SMIM® ETF (CH)`

#### Scenario: CSSMIM is available in the web catalog

- **WHEN** the catalog is regenerated from successful ingestion results
- **THEN** the catalog SHALL include CSSMIM and reference its generated snapshot
