# amundi-full-holdings-download Specification

## Purpose
TBD - created by archiving change integrate-amundi-full-holdings-download. Update Purpose after archive.
## Requirements
### Requirement: Resolve the complete Amundi holdings composition
The ingestion backend SHALL resolve the full-fund holdings composition for Amundi ISIN `LU0908500753` through the Amundi product API used by its canonical product page, without relying on a static HTML anchor or the top-ten breakdown.

#### Scenario: Full holdings export is resolved
- **WHEN** live ingestion processes `LU0908500753` with its Amundi fetch strategy
- **THEN** it obtains the complete `composition.compositionData` collection and its `totalNumberOfInstruments` value

#### Scenario: Provider context is supplied
- **WHEN** the Amundi resolver requests product data or an export
- **THEN** it supplies the configured country, language, and investor-profile context required by the product page

### Requirement: Validate resolved holdings before normalization
The ingestion backend SHALL validate that the resolved result is a complete Amundi composition before passing its rows through the existing Amundi normalization semantics.

#### Scenario: Valid complete composition
- **WHEN** the response contains `compositionData`, `totalNumberOfInstruments`, required identity/weight fields, and matching counts
- **THEN** the composition is accepted for normalization

#### Scenario: HTML response is returned
- **WHEN** the resolver receives HTML instead of an API JSON response
- **THEN** ingestion fails with an explicit download-validation error

#### Scenario: Top-ten data is returned
- **WHEN** the response contains only top-ten `breakDowns` data or ten composition rows
- **THEN** ingestion fails with an explicit incomplete-holdings error and does not generate a partial snapshot

#### Scenario: API structure is incompatible
- **WHEN** the API response is missing required composition or holdings identity/weight fields
- **THEN** ingestion fails before normalization with an explicit format-validation error

### Requirement: Preserve and validate Amundi weight semantics
The integration SHALL retain the `amundi_landing_xlsx_v1` fractional-weight semantics only when API composition weights match the attached full XLSX fixture and normalized totals are valid.

#### Scenario: Fractional weights remain compatible
- **WHEN** representative API weights are fractions and normalized holdings aggregate to a valid portfolio total
- **THEN** `amundi_landing_xlsx_v1` remains the selected parser

#### Scenario: Weight semantics change
- **WHEN** representative API weights are already percentages or produce invalid totals under the Amundi semantics
- **THEN** ingestion fails validation and does not silently reuse the parser

### Requirement: Preserve fixture and provenance behavior
The integration SHALL retain deterministic fixture ingestion and record both canonical and resolved source locations for generated snapshots.

#### Scenario: Fixture mode remains offline
- **WHEN** ingestion runs with `--fixtures`
- **THEN** the configured Amundi fixture is used without contacting the live provider resolver

#### Scenario: Snapshot records resolved source
- **WHEN** a live Amundi composition is accepted and normalized
- **THEN** the snapshot records the canonical product URL as `source_url` and the API endpoint as `resolved_download_url`

