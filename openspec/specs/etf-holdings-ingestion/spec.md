# etf-holdings-ingestion Specification

## Purpose

Define reliable provider download resolution and completeness safeguards for ETF holdings ingestion, including the iShares EUMD full-fund export.
## Requirements
### Requirement: Resolve the complete EUMD holdings export

The ingestion backend SHALL use the iShares EUMD full holdings export for ISIN `IE00BF20LF40`, rather than the product landing page or a top-ten holdings endpoint.

#### Scenario: Direct EUMD export is configured

- **WHEN** the registry entry for `IE00BF20LF40` is loaded
- **THEN** its source URL requests the iShares holdings file with `fileType=csv`, `fileName=EUMD_holdings`, and `dataType=fund`

#### Scenario: EUMD live ingestion receives the full export

- **WHEN** live ingestion processes `IE00BF20LF40`
- **THEN** it passes the complete holdings CSV to the existing `ishares_csv_v1` parser

### Requirement: Resolve provider links that declare format in query parameters

The generic URL fetcher SHALL recognize HTML links as downloadable sources when their query parameters explicitly request `fileType=csv`, `fileType=xls`, or `fileType=xlsx`, including when the link is relative to the source page.

#### Scenario: iShares CSV link is discovered from HTML

- **WHEN** an HTML page contains a relative link with `fileType=csv`
- **THEN** the fetcher resolves it against the page URL and downloads that linked resource instead of returning the HTML page

#### Scenario: Non-download page response is rejected before parsing

- **WHEN** a configured holdings source returns HTML and no valid download link can be resolved
- **THEN** ingestion fails with an explicit source-format validation error before invoking a holdings table parser

### Requirement: Preserve complete holdings and reject partial data

The ingestion backend SHALL reject top-ten or otherwise incomplete EUMD holdings data and SHALL NOT generate a successful partial snapshot.

#### Scenario: Full holdings are retained

- **WHEN** the EUMD export contains the complete holdings table
- **THEN** ingestion retains every valid holdings row and generates a snapshot whose holdings count is greater than ten

#### Scenario: Top-ten response is rejected

- **WHEN** the selected EUMD response contains only ten holdings rows or a top-ten breakdown
- **THEN** ingestion fails with an incomplete-holdings error and does not generate a partial snapshot

#### Scenario: Required CSV structure is missing

- **WHEN** the downloaded response cannot be parsed as the expected iShares holdings CSV
- **THEN** ingestion fails before normalization with an explicit format-validation error

### Requirement: Preserve offline fixture behavior

The EUMD download fix SHALL preserve deterministic fixture-based ingestion and the existing parser contract.

#### Scenario: Fixture mode remains offline

- **WHEN** EUMD ingestion runs with `--fixtures`
- **THEN** it uses `data/example/EUMD_holdings.csv` without contacting the iShares source URL

#### Scenario: Parser identity remains stable

- **WHEN** the EUMD registry entry is updated
- **THEN** its `expected_format` remains `csv` and its `parser_id` remains `ishares_csv_v1`

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

### Requirement: Persist canonical identities in snapshots
Future snapshots SHALL store canonical company identity and canonical display name for every resolved holding while retaining raw source fields and exact instrument data.

#### Scenario: Snapshot contains canonical identity
- **WHEN** a holding is successfully enriched
- **THEN** its serialized security data SHALL include `company_id` and canonical name

#### Scenario: Raw source data remains available
- **WHEN** canonical fields differ from provider values
- **THEN** the snapshot SHALL preserve the original provider values in provenance

### Requirement: Provide accurate visualization match diagnostics
The website SHALL report only holdings with genuinely incomplete identity enrichment as unmatched or partially matched. Holdings with match status `matched` or `overridden` SHALL NOT contribute to that warning count, while holdings with status `ambiguous` or `unmatched` SHALL remain visible in the diagnostics.

#### Scenario: Successful override is not reported as incomplete

- **WHEN** a selected ETF contains a holding with match status `overridden`
- **THEN** the website SHALL exclude that holding from the unmatched or partially matched warning count

#### Scenario: Genuine incomplete matches remain reported

- **WHEN** a selected ETF contains holdings with match status `ambiguous` or `unmatched`
- **THEN** the website SHALL report their count in the selection warnings

#### Scenario: Normal matches remain warning-free

- **WHEN** all holdings in a selected ETF have match status `matched` or `overridden`
- **THEN** the website SHALL report no unmatched or partially matched warning for that ETF

#### Scenario: Visualization data is unchanged

- **WHEN** a holding is excluded from the warning count because its status is `overridden`
- **THEN** the holding SHALL remain available to sector, region, currency, and company exposure visualizations

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

### Requirement: Support verified canonical display aliases
The ingestion backend SHALL support an exact-ISIN identity override that supplies a verified canonical display name and stable company ID for a matched holding while preserving the original provider and security-master values in provenance.

#### Scenario: TSMC uses the verified English alias
- **WHEN** a holding has ISIN `TW0002330008` and the identity override is loaded
- **THEN** the normalized holding uses company ID `taiwan-semiconductor-manufacturing-co` and canonical name `Taiwan Semiconductor Manufacturing Co.`

#### Scenario: Alias override takes precedence over the security master
- **WHEN** the security master matches `TW0002330008` with a different name
- **THEN** the normalized holding retains the override canonical name and is marked as overridden rather than displaying the security-master name

#### Scenario: Original source identity remains auditable
- **WHEN** the TSMC alias is applied
- **THEN** the raw provider fields and security-master provenance remain present and the override does not alter unrelated classification or exposure fields

#### Scenario: Unrelated instruments are unchanged
- **WHEN** a holding has an ISIN other than `TW0002330008`
- **THEN** the TSMC alias is not applied and the holding follows existing identity-enrichment behavior

### Requirement: Validate the reviewed identity resolution set
Fixture ingestion SHALL validate the reviewed exact-ISIN mappings, explicit liquidity-fund exclusions, and provider-versus-security-master venue provenance when regenerating snapshots.

#### Scenario: Reviewed mappings survive fixture regeneration
- **WHEN** fixture ingestion processes the reviewed holdings with the configured override document
- **THEN** each mapped holding SHALL contain its expected ISIN and canonical identity while retaining raw provider fields

#### Scenario: Explicit exclusions survive fixture regeneration
- **WHEN** fixture ingestion processes `ICSEAGD` or `ICSSAGD`
- **THEN** the rows SHALL remain in the snapshot without contributing to company identity aggregation

#### Scenario: Venue discrepancy is included in provenance
- **WHEN** fixture ingestion resolves `QIA` to `NL0015002SN0`
- **THEN** the snapshot SHALL retain Deutsche Börse Xetra / Germany as provider context and the LSE security-master label as a documented discrepancy

### Requirement: Do not publish guessed identity resolutions
Fixture ingestion SHALL retain explicit diagnostics for reviewed holdings that remain ambiguous or unresolved and SHALL NOT publish a guessed company identity from ticker-only matching.

#### Scenario: Remaining ambiguous holding remains diagnosable
- **WHEN** a fixture contains one of the unresolved name-only or ticker/context conflicts
- **THEN** the snapshot SHALL retain the source row and its ambiguity diagnostic for external review
