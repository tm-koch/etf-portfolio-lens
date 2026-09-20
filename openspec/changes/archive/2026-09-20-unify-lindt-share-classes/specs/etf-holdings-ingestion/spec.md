## MODIFIED Requirements

### Requirement: Support controlled identity overrides
The ETF holdings ingestion pipeline SHALL load a version-controlled override document and SHALL record the override source and applied selector in snapshot provenance. Complete overrides SHALL resolve an exact instrument even when the security master has no matching record. Overrides for context-bearing holdings SHALL be scoped by the provider's instrument context and SHALL NOT rely on a ticker-only selector. Multiple distinct instruments SHALL be permitted to resolve to the same verified canonical `company_id` and `canonical_name` so company-level aggregation can unify share classes without merging their instrument identities.

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

#### Scenario: Distinct Lindt share classes share company aggregation identity
- **WHEN** holdings with ISINs `CH0010570759` and `CH0010570767` are normalized using verified exact-ISIN overrides
- **THEN** both holdings SHALL retain their own ISIN and ticker while using company ID `chocoladefabriken-lindt-spruengli-ag` and canonical name `Chocoladefabriken Lindt & Spruengli AG`
