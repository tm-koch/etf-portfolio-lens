## ADDED Requirements

### Requirement: Aggregate weights are derived from finalized holdings
The system SHALL derive `sector_weights`, `region_weights`, and `currency_weights` from the finalized holdings records that are written to the snapshot.

#### Scenario: Finalized holdings drive summary weights
- **WHEN** the ingestion pipeline has completed normalization and enrichment for all holdings in a snapshot
- **THEN** the aggregate weights SHALL be computed from those finalized holdings
- **AND** the aggregate values SHALL reflect the data present in the written holdings output

### Requirement: Aggregate summaries stay aligned with enriched data
The system SHALL ensure the aggregate summaries reflect any missing-field fallback or enrichment applied before snapshot generation.

#### Scenario: Missing data filled before aggregation
- **WHEN** a holding receives additional classification or security data during normalization
- **THEN** the holding’s final values SHALL be used when calculating sector, region, and currency summaries
- **AND** the summary output SHALL not depend on stale pre-enrichment values
