## MODIFIED Requirements

### Requirement: Provide strict enrichment validation

The ingestion CLI SHALL provide an opt-in strict mode that terminates with an error when selected company holdings are unresolved, ambiguous, or missing required identity data. For CHSPI and CSSMI fixtures, strict validation SHALL require all non-excluded equity holdings to resolve to verified exact instruments. Cash, collateral, foreign-currency cash, and market-instrument rows SHALL remain in the snapshot but SHALL NOT require company security overrides or fabricated ISINs, and SHALL NOT resolve to unrelated security-master records through ticker-only matching.

#### Scenario: Strict mode rejects unresolved equity holdings

- **WHEN** strict ingestion encounters an unresolved or ambiguous equity holding
- **THEN** the command SHALL report the holding and terminate unsuccessfully

#### Scenario: Strict mode does not publish partial output

- **WHEN** strict validation fails for any selected ETF
- **THEN** ingestion SHALL NOT publish successful partial snapshots or update the catalog

#### Scenario: CHSPI strict mode resolves non-excluded equities

- **WHEN** strict fixture ingestion processes CHSPI with verified overrides for its non-excluded equity rows
- **THEN** every such equity holding SHALL contain an exact ISIN and canonical company identity, and the command SHALL not report an identity failure for those rows

#### Scenario: CSSMI strict mode resolves non-excluded equities

- **WHEN** strict fixture ingestion processes CSSMI
- **THEN** all 20 equity holdings, including the `LOGN` provider-name variant, SHALL contain an exact ISIN and canonical company identity

#### Scenario: Cash and derivative exclusions remain outside override scope

- **WHEN** strict fixture ingestion processes `EUR CASH`, `CHF CASH`, `USD CASH`, `CASH COLLATERAL CHF F-GSI`, `GBP CASH`, or `SWISS MKT IX SEP 26`
- **THEN** those rows SHALL remain available as holdings without requiring a company security override, fabricated ISIN, or unrelated company match

#### Scenario: Default mode retains diagnostics

- **WHEN** ingestion runs without strict mode and a company holding cannot be completed
- **THEN** the command SHALL retain the holding with an explicit diagnostic and continue according to existing warning behavior
