## ADDED Requirements

### Requirement: Apply canonical company identity by exact ISIN
The normalization pipeline SHALL support a verified exact-ISIN mapping that assigns one canonical company name and stable company ID to every occurrence of the same instrument, while preserving each occurrence's original provider name and instrument ISIN.

#### Scenario: ACWD canonical name is applied
- **WHEN** a holding matches one of the audited same-ISIN mappings with one unambiguous ACWD name
- **THEN** normalization SHALL use the ACWD name as `canonical_name` and assign the mapped stable `company_id`
- **AND** the holding SHALL retain its source ISIN and raw provider name

#### Scenario: Multiple ETFs share one canonical company identity
- **WHEN** the same mapped ISIN occurs in multiple ETF snapshots with different provider names
- **THEN** all occurrences SHALL expose the same canonical name and company ID
- **AND** no source occurrence SHALL be discarded

#### Scenario: Non-ACWD conflict uses a documented preferred source
- **WHEN** an audited same-ISIN conflict has no ACWD occurrence
- **THEN** normalization SHALL use only a separately verified preferred name mapping
- **AND** the system SHALL NOT apply the ACWD rule by default

### Requirement: Support ISIN-only identity outcomes
When a provider supplies a valid ISIN but the bundled security master has no matching record, normalization SHALL retain the source identity and expose an explicit ISIN-only outcome without fabricating ticker or exchange data.

#### Scenario: Source ISIN is absent from the security master
- **WHEN** a source row contains an ISIN and name but no exact security-master record
- **THEN** the normalized holding SHALL retain the ISIN and source name
- **AND** it SHALL receive a stable fallback identity and ISIN-only status

#### Scenario: ISIN-only metadata remains incomplete explicitly
- **WHEN** an ISIN-only holding has no trusted ticker or exchange enrichment
- **THEN** ticker and exchange SHALL remain empty
- **AND** diagnostics SHALL identify the missing enrichment rather than inventing values

#### Scenario: Exact override completes an ISIN-only holding
- **WHEN** an ISIN-only holding matches a complete verified exact-ISIN override
- **THEN** the override SHALL supply the canonical identity and the holding SHALL be marked overridden
- **AND** the holding SHALL no longer be reported as unresolved

### Requirement: Preserve identity provenance
Canonicalization SHALL preserve enough provenance to audit the source identity, security-master lookup, and applied override independently.

#### Scenario: Provider and canonical names coexist
- **WHEN** a canonical name differs from the provider name
- **THEN** the snapshot SHALL retain the provider name in source fields
- **AND** the serialized security SHALL expose the canonical name

#### Scenario: Override source is recorded
- **WHEN** an identity override contributes to normalization
- **THEN** snapshot provenance SHALL record that the override was applied and the selector strategy used

### Requirement: Exclude non-company instruments from company identity cleanup
Cash, collateral, liquidity funds, and futures SHALL remain representable holdings but SHALL NOT require company IDs, fabricated ISINs, or company-name overrides.

#### Scenario: Cash or derivative row is classified as non-company
- **WHEN** a holding is classified as cash, collateral, liquidity-fund, or futures
- **THEN** it SHALL remain in the snapshot with its provider classification
- **AND** it SHALL not produce a company identity warning requiring an override

#### Scenario: Placeholder ISIN is not treated as a company identity
- **WHEN** multiple non-company rows share a placeholder such as `Unassigned`
- **THEN** the rows SHALL not be counted as same-ISIN company conflicts
- **AND** they SHALL not be merged into a company identity
