## ADDED Requirements

### Requirement: Validate the reviewed identity resolution set
Fixture ingestion SHALL validate the reviewed exact-ISIN mappings, explicit liquidity-fund exclusions, and provider-versus-security-master venue provenance when regenerating snapshots.

#### Scenario: Reviewed mappings survive fixture regeneration
- **WHEN** fixture ingestion processes the reviewed holdings with the configured override document
- **THEN** each mapped holding SHALL contain its expected ISIN and canonical identity while retaining raw provider fields

#### Scenario: Explicit exclusions survive fixture regeneration
- **WHEN** fixture ingestion processes `ICSEAGD` or `ICSSAGD`
- **THEN** the rows SHALL remain in the snapshot without contributing to company identity aggregation

#### Scenario: Venue discrepancy is included in provenance
- **WHEN** fixture ingestion resolves `QIA` to `NL0015002SN0`
- **THEN** the snapshot SHALL retain Deutsche Börse Xetra / Germany as provider context and the LSE security-master label as a documented discrepancy

### Requirement: Do not publish guessed identity resolutions
Fixture ingestion SHALL retain explicit diagnostics for reviewed holdings that remain ambiguous or unresolved and SHALL NOT publish a guessed company identity from ticker-only matching.

#### Scenario: Remaining ambiguous holding remains diagnosable
- **WHEN** a fixture contains one of the unresolved name-only or ticker/context conflicts
- **THEN** the snapshot SHALL retain the source row and its ambiguity diagnostic for external review
