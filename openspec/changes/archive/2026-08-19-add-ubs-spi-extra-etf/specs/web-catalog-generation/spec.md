## ADDED Requirements

### Requirement: Catalog publishes the new UBS ETF
The web catalog generation flow SHALL include UBS SPI® Extra when its registry entry is successfully ingested in the selected run.

#### Scenario: Successful full catalog update
- **WHEN** fixture ingestion for all registry entries succeeds with `--update-catalog`
- **THEN** `web/data/catalog.json` contains one UBS SPI® Extra entry in registry order with its generated snapshot path

#### Scenario: Failed UBS ingestion does not publish a dangling entry
- **WHEN** UBS SPI® Extra ingestion fails before catalog generation completes
- **THEN** the existing catalog remains unchanged and does not reference a missing UBS SPI® Extra snapshot
