## MODIFIED Requirements

### Requirement: Resolve holdings with override-first precedence
The resolver SHALL consult version-controlled overrides before the security master and SHALL support selectors based on ISIN, ticker plus normalized exchange or country, and holding name. It SHALL use the security master only to fill fields that remain missing after the override is applied. A ticker-only match SHALL NOT override explicit exchange or country context supplied by the holding.

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

#### Scenario: Conflicting context blocks global ticker fallback
- **WHEN** an ISIN is unavailable, a holding supplies an exchange or country, and the only global ticker candidate conflicts with that context
- **THEN** the resolver SHALL NOT select the global ticker candidate and SHALL continue to name or alias matching before returning an unresolved or ambiguous diagnostic

### Requirement: Detect unresolved and ambiguous holdings
The resolver SHALL distinguish resolved, overridden, ambiguous, incomplete, and unresolved outcomes and SHALL retain attempted strategies and missing fields in diagnostics. A holding rejected because its contextual exchange or country conflicts with a unique ticker candidate SHALL produce an explicit warning in non-strict mode and SHALL fail strict validation unless another strategy resolves it.

#### Scenario: Ambiguous ticker is not guessed
- **WHEN** a ticker matches multiple records and exchange or country cannot disambiguate it
- **THEN** the resolver SHALL mark the holding ambiguous and SHALL NOT select an arbitrary record

#### Scenario: Missing identity remains unresolved
- **WHEN** no override or security-master strategy uniquely resolves a holding
- **THEN** the resolver SHALL mark it unresolved and retain the source holding data

#### Scenario: Context-conflicting ticker is warned
- **WHEN** a holding has ticker `CFR` on normalized exchange `SIX` and the only security-master `CFR` candidate is on `NYSE`
- **THEN** non-strict normalization SHALL retain the source holding, mark it unresolved or ambiguous, and emit a diagnostic warning rather than assigning Cullen/Frost Bankers

#### Scenario: Strict mode rejects the unresolved context conflict
- **WHEN** strict ingestion encounters the context-conflicting `CFR` holding without a valid Richemont override
- **THEN** the command SHALL report the holding and terminate without publishing a partial snapshot

## ADDED Requirements

### Requirement: Correct the Swiss Richemont CFR listing
The version-controlled identity override document SHALL contain a selector specific to the CHSPI Richemont listing and SHALL map it to the verified Swiss instrument identity and canonical Richemont company identity.

#### Scenario: CHSPI Richemont override resolves safely
- **WHEN** a holding has ticker `CFR`, normalized exchange `SIX`, and source name `COMPAGNIE FINANCIERE RICHEMONT SA`
- **THEN** the resolver SHALL apply the verified Richemont ISIN, canonical company ID, and canonical name before security-master matching

#### Scenario: Richemont override does not affect Cullen/Frost
- **WHEN** a holding has ticker `CFR` on `NYSE` or a Cullen/Frost source name
- **THEN** the Richemont override SHALL NOT match it and the Cullen/Frost identity SHALL remain distinct

### Requirement: Preserve corrected identity in published data
Regenerated snapshots and the web catalog SHALL use the corrected canonical Richemont identity after the override is added, while preserving the original provider fields for auditability.

#### Scenario: CHSPI snapshot contains Richemont identity
- **WHEN** the corrected CHSPI fixture is ingested
- **THEN** the CFR holding SHALL contain the verified Richemont instrument identity, canonical company ID, and canonical name, and SHALL retain the original source name and ticker in provenance

#### Scenario: Catalog points to corrected snapshots
- **WHEN** the corrected fixture run succeeds with catalog update enabled
- **THEN** the web catalog SHALL reference the regenerated snapshot date containing the corrected CHSPI identity
