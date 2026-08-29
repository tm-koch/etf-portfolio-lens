## MODIFIED Requirements

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
