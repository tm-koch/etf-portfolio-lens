## ADDED Requirements

### Requirement: Sector labels are normalized to GIC-style names
The system MUST normalize sector labels from source holdings and security-master enrichment to a consistent GIC-style sector taxonomy before snapshot aggregates are written.

#### Scenario: Communication is normalized
- **WHEN** a holding or enriched security record contains the sector label `Communication`
- **THEN** the normalized sector SHALL be written as `Communication Services`
- **AND** the normalized value SHALL be used in sector aggregates

#### Scenario: Localized aliases are normalized
- **WHEN** a holding or enriched security record contains a localized or provider-specific sector label that maps to a known GIC sector
- **THEN** the system SHALL translate it to the configured normalized sector name before writing the snapshot
- **AND** the sector aggregate SHALL use the translated label

#### Scenario: Canonical GIC labels remain stable
- **WHEN** a holding or enriched security record already contains a canonical GIC sector label
- **THEN** the system SHALL preserve that canonical label unchanged
- **AND** the sector aggregate SHALL use the same label

### Requirement: Raw sector provenance is preserved
The system MUST preserve the original source sector text in snapshot provenance so source-specific labels remain inspectable.

#### Scenario: Source sector remains traceable
- **WHEN** a sector label is normalized during ingestion
- **THEN** the original source sector text SHALL remain available in the snapshot provenance or source fields
- **AND** the normalized sector value SHALL be stored separately from the raw source text

