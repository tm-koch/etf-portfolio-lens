## MODIFIED Requirements

### Requirement: Support controlled identity overrides
The ETF holdings ingestion pipeline SHALL load a version-controlled override document and SHALL record the override source and applied selector in snapshot provenance. Complete overrides SHALL resolve an exact instrument even when the security master has no matching record. Overrides for context-bearing holdings SHALL be scoped by the provider's instrument context and SHALL NOT rely on a ticker-only selector. Multiple distinct instruments SHALL be permitted to resolve to the same verified canonical `company_id` and `canonical_name` so company-level aggregation can unify share classes without merging their instrument identities. Exact-ISIN canonical-name overrides SHALL be supported for cross-provider same-ISIN naming conflicts, with ACWD as the preferred naming source when it supplies one unambiguous occurrence.

#### Scenario: Override document is loaded
- **WHEN** ingestion starts with the configured override document
- **THEN** the pipeline SHALL validate and load it before normalizing ETF holdings

#### Scenario: Complete override resolves a missing security-master record
- **WHEN** a holding matches a complete, verified override and no security-master record matches the exact instrument
- **THEN** normalization SHALL resolve the holding using the override without requiring a security-master match

#### Scenario: Context-scoped override prevents ticker collision
- **WHEN** a holding has ticker, exchange, and name context and an unrelated security-master record shares only its ticker
- **THEN** the pipeline SHALL select the scoped override and SHALL NOT select the unrelated ticker-only record

#### Scenario: Exact ISIN override canonicalizes a provider name
- **WHEN** a holding matches a verified exact-ISIN override generated from the preferred naming source
- **THEN** normalization SHALL apply the override canonical name and company ID regardless of whether the source provider uses a different name
- **AND** the original provider name SHALL remain in provenance

#### Scenario: Override provenance is stored
- **WHEN** an override contributes to a resolved holding
- **THEN** the snapshot SHALL record that the override was applied and which matching strategy selected it

#### Scenario: Distinct Lindt share classes share company aggregation identity
- **WHEN** holdings with ISINs `CH0010570759` and `CH0010570767` are normalized using verified exact-ISIN overrides
- **THEN** both holdings SHALL retain their own ISIN and ticker while using company ID `chocoladefabriken-lindt-spruengli-ag` and canonical name `Chocoladefabriken Lindt & Spruengli AG`

### Requirement: Provide controlled diagnostics for incomplete identity enrichment
The ingestion pipeline SHALL classify valid source ISINs absent from the security master as explicit ISIN-only outcomes and SHALL retain warnings for ambiguous or unverifiable company identities. Non-company holdings SHALL remain excluded from company identity validation.

#### Scenario: ISIN-only outcome is diagnostic but non-fatal
- **WHEN** a valid source ISIN has no security-master record and no complete override
- **THEN** ingestion SHALL retain the holding with ISIN-only status and continue in default mode
- **AND** the diagnostic SHALL identify missing trusted enrichment fields

#### Scenario: Ambiguous identity remains visible
- **WHEN** ticker, name, or contextual matching produces multiple plausible securities
- **THEN** ingestion SHALL retain an ambiguous diagnostic and SHALL NOT choose an arbitrary company identity

#### Scenario: Non-company holding is not an identity failure
- **WHEN** a row is classified as cash, collateral, liquidity fund, or futures
- **THEN** it SHALL remain in the snapshot without requiring a company override or fabricated identity
