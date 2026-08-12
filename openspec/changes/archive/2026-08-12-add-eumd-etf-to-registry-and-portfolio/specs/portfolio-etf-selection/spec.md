## ADDED Requirements

### Requirement: Registry-backed ETFs are published to the catalog
The system MUST publish any ETF source entry that has been ingested into a snapshot into the portfolio catalog consumed by the web app.

#### Scenario: Newly added ETF becomes available in the catalog
- **WHEN** a new ETF source entry is added to the registry and its snapshot is generated
- **THEN** the published catalog SHALL include that ETF with its ISIN, ticker, name, provider, and snapshot path
- **AND** the portfolio UI SHALL be able to load it without manual code changes to the selector

### Requirement: Users can add newly published ETFs to a portfolio
The system MUST allow users to search for, add, and persist any ETF that appears in the published catalog.

#### Scenario: User adds the new iShares ETF
- **WHEN** the user searches for the newly published ETF in the portfolio tab
- **THEN** the ETF SHALL appear in search results
- **AND** the user SHALL be able to add it to the portfolio
- **AND** the added position SHALL persist across reloads
