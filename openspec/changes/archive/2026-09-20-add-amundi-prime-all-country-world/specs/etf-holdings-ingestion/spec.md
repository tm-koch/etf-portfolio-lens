## ADDED Requirements

### Requirement: Ingest the Amundi Prime All Country World full composition
The ingestion backend SHALL support ISIN `IE0009HF1MK9` through the existing Amundi full-composition fetch strategy and `amundi_landing_xlsx_v1` parser, retaining all valid holding records rather than a top-ten subset.

#### Scenario: Registry selects the reusable Amundi importer
- **WHEN** live ingestion selects `IE0009HF1MK9`
- **THEN** it uses `amundi_product_page_v1` for retrieval and `amundi_landing_xlsx_v1` for the downloaded workbook

#### Scenario: Complete composition is retained
- **WHEN** a valid Amundi response contains the full composition for `IE0009HF1MK9`
- **THEN** the resulting snapshot contains every valid holding row and more than ten holdings

### Requirement: Exclude Amundi workbook metadata rows
The Amundi workbook parser SHALL exclude rows that lack a valid holding ISIN or numeric weight from normalized holdings while preserving valid rows that have very small positive weights.

#### Scenario: Provider footer is ignored
- **WHEN** the workbook contains disclaimer, legal, or source-note rows after the holdings table
- **THEN** those rows are excluded before normalization and do not affect the holdings count

#### Scenario: Fractional holding is retained
- **WHEN** a valid holding has an ISIN and a numeric weight below one basis point
- **THEN** it remains in the normalized holdings rather than being discarded as metadata

### Requirement: Validate new Amundi fixture completeness
Fixture-based ingestion SHALL validate that the supplied `IE0009HF1MK9` workbook has a non-empty complete holding set and an accepted aggregate weight total before publishing a snapshot.

#### Scenario: Valid fixture is accepted
- **WHEN** the supplied workbook contains the expected holding columns, valid identities, and an aggregate weight within the documented tolerance
- **THEN** fixture ingestion succeeds and publishes a snapshot

#### Scenario: Invalid or partial fixture is rejected
- **WHEN** the workbook has missing required columns, no valid holdings, or an aggregate weight outside the accepted tolerance
- **THEN** ingestion fails without publishing a successful partial snapshot
