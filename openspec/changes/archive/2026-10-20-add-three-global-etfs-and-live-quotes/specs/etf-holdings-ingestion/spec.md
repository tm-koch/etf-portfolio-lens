# Spec Delta

## ADDED Requirements

### Requirement: Ingest complete supplied holdings fixtures
Fixture ingestion for the three registered ISINs SHALL retain every valid row in the supplied holdings files and SHALL NOT publish a top-ten or otherwise partial snapshot.

#### Scenario: EIMI fixture is complete
- **WHEN** fixture ingestion processes `IE00BKM4GZ66`
- **THEN** its snapshot contains all 3,094 valid rows from the supplied fixture

#### Scenario: IMEA fixture is complete
- **WHEN** fixture ingestion processes `IE00B4K48X80`
- **THEN** its snapshot contains all 398 valid rows from the supplied fixture

#### Scenario: UBS Core MSCI World fixture is complete
- **WHEN** fixture ingestion processes `IE00BD4TXV59`
- **THEN** its snapshot contains all 1,181 valid rows from the supplied fixture

### Requirement: Preserve non-equity rows in new ETF snapshots
The holdings pipeline SHALL retain valid non-equity rows present in the supplied EIMI and IMEA fixtures without requiring fabricated company identities.

#### Scenario: EIMI cash and market-instrument rows remain available
- **WHEN** fixture ingestion processes EIMI rows classified as cash, collateral, FX, or futures
- **THEN** those rows remain in the snapshot and are not required to resolve to a company

#### Scenario: IMEA cash and market-instrument rows remain available
- **WHEN** fixture ingestion processes IMEA rows classified as cash, money market, collateral, or futures
- **THEN** those rows remain in the snapshot and are not required to resolve to a company

### Requirement: Keep fixture ingestion offline for new ETFs
Fixture ingestion for the three new ETF entries SHALL use their supplied local holdings files without making network requests.

#### Scenario: New ETF fixture run is offline
- **WHEN** fixture ingestion selects any of the three new ISINs
- **THEN** it reads the corresponding supplied fixture and completes without contacting the configured holdings URL

### Requirement: Keep UBS Core MSCI World fixture-only
The ingestion pipeline SHALL always use the supplied local fixture for `IE00BD4TXV59` and SHALL NOT attempt an automated download for that ETF.

#### Scenario: Normal ingestion uses the UBS fixture
- **WHEN** an ingestion run selects `IE00BD4TXV59` without global fixture mode
- **THEN** it processes the supplied UBS fixture without making a network request

#### Scenario: Missing UBS fixture fails clearly
- **WHEN** an ingestion run selects `IE00BD4TXV59` and its fixture is unavailable
- **THEN** ingestion fails before publishing a snapshot and identifies the missing fixture