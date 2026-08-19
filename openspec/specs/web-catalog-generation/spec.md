# web-catalog-generation Specification

## Purpose
TBD - created by archiving change generate-web-catalog. Update Purpose after archive.
## Requirements
### Requirement: Opt-in catalog generation
The ingestion CLI SHALL support an `--update-catalog` option that generates `web/data/catalog.json` after successful ingestion, while ingestion without the option SHALL not modify the catalog.

#### Scenario: Combined ingestion and catalog update
- **WHEN** the user runs `python -m etf_ingestion_backend --all --fixtures --update-catalog`
- **THEN** the CLI generates snapshots and updates `web/data/catalog.json` from that run

#### Scenario: Ordinary ingestion leaves catalog unchanged
- **WHEN** the user runs ingestion without `--update-catalog`
- **THEN** snapshots may be generated but `web/data/catalog.json` is not modified

### Requirement: Catalog manifest schema
Generated catalog output SHALL preserve the frontend manifest schema with `generatedAt`, `basis`, and ETF entries containing ISIN, ticker, name, provider, and snapshot path.

#### Scenario: Catalog contains current run metadata
- **WHEN** catalog generation completes for a run date
- **THEN** `generatedAt` equals the run date and `basis` equals `share_weighted`

#### Scenario: Catalog entry references generated snapshot
- **WHEN** an ETF is successfully ingested
- **THEN** its catalog entry contains the registry identity fields and a root-absolute path to `/data/raw/<run-date>/snapshots/<isin>.json`

### Requirement: Catalog selection and ordering
Catalog generation SHALL include successfully generated snapshots for the selected registry entries in registry order.

#### Scenario: Full catalog generation
- **WHEN** the command selects all registry entries and all ingest successfully
- **THEN** the catalog contains one entry for each selected ETF in registry order

#### Scenario: Partial selection
- **WHEN** the command selects a subset of registry entries
- **THEN** the generated catalog contains only that subset and does not claim to represent unselected ETFs

### Requirement: Failure-safe catalog replacement
The CLI SHALL not replace the existing catalog when ingestion or manifest generation fails.

#### Scenario: Ingestion failure
- **WHEN** any selected ingestion fails before catalog generation completes
- **THEN** the command reports failure and the previous `web/data/catalog.json` remains unchanged

#### Scenario: Atomic catalog write
- **WHEN** the complete manifest has been serialized successfully
- **THEN** the target catalog is replaced as one completed file operation and is never left partially written

### Requirement: Catalog command documentation
The root README SHALL document the combined ingestion and catalog-refresh command.

#### Scenario: User finds the update command
- **WHEN** a user reads the repository ingestion instructions
- **THEN** the README shows `python -m etf_ingestion_backend --all --fixtures --update-catalog` and explains that it refreshes the web catalog

### Requirement: Catalog publishes the new UBS ETF
The web catalog generation flow SHALL include UBS SPI® Extra when its registry entry is successfully ingested in the selected run.

#### Scenario: Successful full catalog update
- **WHEN** fixture ingestion for all registry entries succeeds with `--update-catalog`
- **THEN** `web/data/catalog.json` contains one UBS SPI® Extra entry in registry order with its generated snapshot path

#### Scenario: Failed UBS ingestion does not publish a dangling entry
- **WHEN** UBS SPI® Extra ingestion fails before catalog generation completes
- **THEN** the existing catalog remains unchanged and does not reference a missing UBS SPI® Extra snapshot

