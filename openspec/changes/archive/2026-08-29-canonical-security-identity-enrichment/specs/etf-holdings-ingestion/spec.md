## ADDED Requirements

### Requirement: Support controlled identity overrides
The ETF holdings ingestion pipeline SHALL load a version-controlled override document and SHALL record the override source and applied selector in snapshot provenance.

#### Scenario: Override document is loaded
- **WHEN** ingestion starts with the configured override document
- **THEN** the pipeline SHALL validate and load it before normalizing ETF holdings

#### Scenario: Override provenance is stored
- **WHEN** an override contributes to a resolved holding
- **THEN** the snapshot SHALL record that the override was applied and which matching strategy selected it

### Requirement: Provide strict enrichment validation
The ingestion CLI SHALL provide an opt-in strict mode that terminates with an error when selected holdings are unresolved, ambiguous, or missing required identity data.

#### Scenario: Strict mode rejects unresolved holdings
- **WHEN** strict ingestion encounters an unresolved or ambiguous holding
- **THEN** the command SHALL report the holding and terminate unsuccessfully

#### Scenario: Strict mode does not publish partial output
- **WHEN** strict validation fails for any selected ETF
- **THEN** ingestion SHALL NOT publish successful partial snapshots or update the catalog

#### Scenario: Default mode retains diagnostics
- **WHEN** ingestion runs without strict mode and a holding cannot be completed
- **THEN** the command SHALL retain the holding with an explicit diagnostic and continue according to existing warning behavior

### Requirement: Persist canonical identities in snapshots
Future snapshots SHALL store canonical company identity and canonical display name for every resolved holding while retaining raw source fields and exact instrument data.

#### Scenario: Snapshot contains canonical identity
- **WHEN** a holding is successfully enriched
- **THEN** its serialized security data SHALL include `company_id` and canonical name

#### Scenario: Raw source data remains available
- **WHEN** canonical fields differ from provider values
- **THEN** the snapshot SHALL preserve the original provider values in provenance
