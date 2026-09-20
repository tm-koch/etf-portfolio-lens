## MODIFIED Requirements

### Requirement: Provide accurate visualization match diagnostics
The website SHALL report only holdings with genuinely unresolved identity enrichment as unmatched or partially matched. Holdings with match status `matched`, `overridden`, or `isin_only` SHALL NOT contribute to that warning count, while holdings with status `ambiguous` or `unmatched` SHALL remain visible in the diagnostics.

#### Scenario: Successful override is not reported as incomplete

- **WHEN** a selected ETF contains a holding with match status `overridden`
- **THEN** the website SHALL exclude that holding from the unmatched or partially matched warning count

#### Scenario: ISIN-only enrichment is not reported as incomplete

- **WHEN** a selected ETF contains a holding with match status `isin_only`
- **THEN** the website SHALL exclude that holding from the unmatched or partially matched warning count

#### Scenario: Genuine incomplete matches remain reported

- **WHEN** a selected ETF contains holdings with match status `ambiguous` or `unmatched`
- **THEN** the website SHALL report their count in the selection warnings

#### Scenario: Normal matches remain warning-free

- **WHEN** all holdings in a selected ETF have match status `matched`, `overridden`, or `isin_only`
- **THEN** the website SHALL report no unmatched or partially matched warning for that ETF

#### Scenario: Visualization data is unchanged

- **WHEN** a holding is excluded from the warning count because its status is `overridden` or `isin_only`
- **THEN** the holding SHALL remain available to sector, region, currency, and company exposure visualizations

## ADDED Requirements

### Requirement: Identify backend holding warnings by ETF ticker
The ingestion backend SHALL prefix each emitted unresolved holding warning with the ticker of the ETF whose source data produced the warning.

#### Scenario: Unmatched warning includes ETF ticker

- **WHEN** ingestion emits a warning for an unmatched holding in an ETF
- **THEN** the warning SHALL begin with the ETF ticker followed by the holding diagnostic

#### Scenario: Warning context uses the ETF ticker rather than constituent ticker

- **WHEN** a source row has a constituent ticker that differs from the ETF registry ticker
- **THEN** the warning prefix SHALL use the ETF registry ticker

#### Scenario: Existing diagnostic detail is preserved

- **WHEN** an ETF-prefixed warning is emitted
- **THEN** it SHALL retain the existing holding identifier and missing-element or match-conflict detail
