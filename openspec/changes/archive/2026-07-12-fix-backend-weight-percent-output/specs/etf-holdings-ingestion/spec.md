## MODIFIED Requirements

### Requirement: Normalize ETF holdings into a canonical snapshot
The system MUST convert provider-specific holdings into a canonical JSON snapshot containing ETF metadata, holdings, aggregates, and provenance.
The system MUST write `weight_pct` values in the holdings array and in derived aggregate summaries, including `sector_weights`, `region_weights`, and `currency_weights`, as percentage numbers in the 0-100 range.

#### Scenario: Snapshots are generated on demand
- **WHEN** the ingestion process is invoked for one or more ETFs
- **THEN** the system MUST generate snapshots only for the requested run

#### Scenario: Snapshot contains normalized holdings
- **WHEN** a provider holdings file is processed successfully
- **THEN** the system MUST write a snapshot whose holdings use the canonical field structure required by the website
- **AND** the holding `weight_pct` values MUST be written as percentage numbers rather than fractions

#### Scenario: Snapshot includes percentage-based aggregates
- **WHEN** a snapshot is written
- **THEN** the sector, region, and currency summary weights MUST use the same percentage unit as the holdings array
- **AND** consumers of the snapshot MUST be able to read those values directly as percentages without applying an additional scaling factor

### Requirement: Generate comparison-ready aggregates
The system MUST derive sector, region, currency exposure, and top-holdings aggregates from the normalized holdings data.
The derived aggregate values MUST remain aligned with the percentage-based `weight_pct` convention used in the holdings array.

#### Scenario: Sector exposure is derived from holdings weights
- **WHEN** a snapshot is generated
- **THEN** the system MUST include a sector weight breakdown computed from the normalized holdings
- **AND** each sector weight MUST be expressed as a percentage number in the 0-100 range

#### Scenario: Currency exposure is derived from holdings weights
- **WHEN** a snapshot is generated
- **THEN** the system MUST include a currency weight breakdown computed from the normalized holdings
- **AND** each currency weight MUST be expressed as a percentage number in the 0-100 range

#### Scenario: Top holdings are included
- **WHEN** a snapshot is generated
- **THEN** the system MUST include a ranked top-holdings summary derived from the holdings weights
- **AND** each top-holding weight MUST be expressed as a percentage number in the 0-100 range
