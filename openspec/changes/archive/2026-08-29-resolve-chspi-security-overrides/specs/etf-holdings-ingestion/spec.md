## MODIFIED Requirements

### Requirement: Support controlled identity overrides
The ETF holdings ingestion pipeline SHALL load a version-controlled override document and SHALL record the override source and applied selector in snapshot provenance. Complete overrides SHALL resolve an exact instrument even when the security master has no matching record. Overrides for context-bearing holdings SHALL be scoped by the provider's instrument context and SHALL NOT rely on a ticker-only selector.

#### Scenario: Override document is loaded

- **WHEN** ingestion starts with the configured override document
- **THEN** the pipeline SHALL validate and load it before normalizing ETF holdings

#### Scenario: Complete override resolves a missing security-master record

- **WHEN** a holding matches a complete, verified override and no security-master record matches the exact instrument
- **THEN** normalization SHALL resolve the holding using the override without requiring a security-master match

#### Scenario: Context-scoped override prevents ticker collision

- **WHEN** a holding has ticker, exchange, and name context and an unrelated security-master record shares only its ticker
- **THEN** the pipeline SHALL select the scoped override and SHALL NOT select the unrelated ticker-only record

#### Scenario: Override provenance is stored

- **WHEN** an override contributes to a resolved holding
- **THEN** the snapshot SHALL record that the override was applied and which matching strategy selected it

### Requirement: Provide strict enrichment validation
The ingestion CLI SHALL provide an opt-in strict mode that terminates with an error when selected holdings are unresolved, ambiguous, or missing required identity data. For the CHSPI fixture, strict validation SHALL require all non-excluded equity holdings to resolve to verified exact instruments; the explicitly excluded cash and market-instrument rows SHALL NOT require security overrides.

#### Scenario: Strict mode rejects unresolved holdings

- **WHEN** strict ingestion encounters an unresolved or ambiguous holding
- **THEN** the command SHALL report the holding and terminate unsuccessfully

#### Scenario: Strict mode does not publish partial output

- **WHEN** strict validation fails for any selected ETF
- **THEN** ingestion SHALL NOT publish successful partial snapshots or update the catalog

#### Scenario: CHSPI strict mode resolves non-excluded equities

- **WHEN** strict fixture ingestion processes CHSPI with verified overrides for its non-excluded equity rows
- **THEN** every such equity holding SHALL contain an exact ISIN and canonical company identity, and the command SHALL not report an identity failure for those rows

#### Scenario: CHSPI exclusions remain outside override scope

- **WHEN** strict fixture ingestion processes `EUR CASH`, `CHF CASH`, `CASH COLLATERAL CHF F-GSI`, `GBP CASH`, or `SWISS MKT IX SEP 26`
- **THEN** those rows SHALL not require a company security override or fabricated ISIN

#### Scenario: Default mode retains diagnostics

- **WHEN** ingestion runs without strict mode and a holding cannot be completed
- **THEN** the command SHALL retain the holding with an explicit diagnostic and continue according to existing warning behavior
