# security-identity-enrichment Specification

## Purpose
TBD - created by archiving change canonical-security-identity-enrichment. Update Purpose after archive.
## Requirements
### Requirement: Normalize exchange identifiers
The resolver SHALL normalize provider-specific exchange labels into stable internal exchange codes before applying ticker-based matching, while retaining the original exchange value in holding provenance.

#### Scenario: SIX aliases resolve consistently
- **WHEN** holdings use `SIX`, `SIX Swiss Exchange`, or another configured SIX alias
- **THEN** the resolver SHALL use the same internal exchange code for all of them

#### Scenario: Unknown exchange remains auditable
- **WHEN** a holding contains an exchange label with no configured alias
- **THEN** the resolver SHALL retain the raw label and SHALL NOT silently map it to an unrelated exchange

### Requirement: Resolve holdings with override-first precedence
The resolver SHALL consult version-controlled overrides before the security master and SHALL support selectors based on ISIN, ticker plus normalized exchange or country, and holding name. It SHALL use the security master only to fill fields that remain missing after the override is applied.

#### Scenario: Explicit override corrects a source identifier
- **WHEN** a holding matches an override by source context and holding name
- **THEN** the resolver SHALL apply the override identity and canonical data before consulting the security master

#### Scenario: ISIN resolution fills missing fields
- **WHEN** a holding has an ISIN that uniquely matches the security master
- **THEN** the resolver SHALL use that record to fill missing identity and classification fields

#### Scenario: Ticker resolution uses exchange or country
- **WHEN** an ISIN is unavailable and a ticker matches a security-master record by normalized exchange or country
- **THEN** the resolver SHALL use that unique record and SHALL NOT rely on ticker globally

#### Scenario: Holding-name resolution is unique
- **WHEN** an unresolved holding name uniquely matches an override or security-master record
- **THEN** the resolver SHALL use that record to complete the holding

### Requirement: Assign canonical company identity
Every successfully resolved holding SHALL contain a stable `company_id` and canonical company name in addition to its exact instrument identity. Multiple instruments or share classes may reference the same company ID, and no company ID SHALL be inferred from ticker alone.

#### Scenario: Unambiguous holding receives identity
- **WHEN** a holding is uniquely resolved through the override or security master
- **THEN** the normalized holding SHALL contain `company_id` and canonical company name

#### Scenario: Share classes consolidate by company
- **WHEN** two resolved instruments represent the same company
- **THEN** they SHALL retain distinct instrument fields while sharing the same `company_id`

#### Scenario: Roper and Roche remain separate
- **WHEN** `ROP` is observed on Nasdaq for Roper and on SIX for Roche
- **THEN** the resolver SHALL assign different company IDs and SHALL preserve the exchange-specific identities

### Requirement: Detect unresolved and ambiguous holdings
The resolver SHALL distinguish resolved, overridden, ambiguous, incomplete, and unresolved outcomes and SHALL retain attempted strategies and missing fields in diagnostics.

#### Scenario: Ambiguous ticker is not guessed
- **WHEN** a ticker matches multiple records and exchange or country cannot disambiguate it
- **THEN** the resolver SHALL mark the holding ambiguous and SHALL NOT select an arbitrary record

#### Scenario: Missing identity remains unresolved
- **WHEN** no override or security-master strategy uniquely resolves a holding
- **THEN** the resolver SHALL mark it unresolved and retain the source holding data

### Requirement: Keep canonical aggregation independent of ETF insertion order
The published canonical holding result SHALL be determined by resolved holding identity and exposure, not by the order in which ETFs are added to a portfolio.

#### Scenario: ACWD and CHSPI produce the same result in either order
- **WHEN** ACWD and CHSPI are added with the same share quantities first as ACWD then CHSPI and then as CHSPI then ACWD
- **THEN** the aggregated holding set, canonical names, company IDs, total exposures, and ranking order SHALL be identical in both cases, including Roche as Roche rather than Roper

#### Scenario: Conflicting source names do not determine display identity
- **WHEN** two holdings with the same resolved company ID provide different source names
- **THEN** aggregation SHALL display the persisted canonical name and SHALL NOT use the first ETF's source name

