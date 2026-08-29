## ADDED Requirements

### Requirement: Complete SPMCHA classification through verified overrides
The ingestion pipeline SHALL support exact-ISIN overrides that provide complete, manually verified identity and classification data for SPMCHA equity holdings absent from the security master. Each completed override SHALL provide `company_id`, `canonical_name`, `sector`, `asset_class`, `country`, and `exchange`; region SHALL be derived from country using the existing taxonomy, and provider currency SHALL remain authoritative when present.

#### Scenario: SPMCHA override supplies missing classification

- **WHEN** an SPMCHA holding matches one of the 11 supplied ISINs and its completed override provides the required identity and classification fields
- **THEN** normalization SHALL populate the holding with those fields and derive its region from country

#### Scenario: Overrides use exact provider ISINs

- **WHEN** the UBS fixture contains an affected holding with an exact ISIN
- **THEN** the pipeline SHALL select the corresponding ISIN-scoped override without requiring ticker or exchange fields from the provider row

#### Scenario: Manual completion is required

- **WHEN** an affected ISIN override lacks any required identity or classification field
- **THEN** strict ingestion SHALL fail rather than publish a holding with incomplete classification

#### Scenario: Currency and source provenance are preserved

- **WHEN** a completed SPMCHA override is applied to a holding whose UBS row contains currency and source fields
- **THEN** normalization SHALL retain the provider currency and raw source fields while recording that the override supplied the resolved identity/classification

#### Scenario: SPMCHA aggregates use completed classifications

- **WHEN** strict fixture ingestion processes SPMCHA after all 11 overrides are completed
- **THEN** the affected equity weights SHALL contribute to their supplied sectors and derived region, and SHALL NOT be grouped under `Unknown` for those fields
