## ADDED Requirements

### Requirement: Portfolio-weighted comparison reference ring
The comparison view SHALL render a portfolio reference ring for the sector, region, and currency doughnut charts.

The reference ring SHALL summarize the entire portfolio using portfolio share-count weighting.
The reference ring SHALL be the outermost ring in each comparison donut.
The reference ring SHALL use the same category labels as the existing ETF rings for the corresponding metric.

#### Scenario: Reference ring appears for each comparison donut
- **WHEN** the user selects two or more ETFs with non-zero share counts
- **THEN** the sector, region, and currency comparison charts each include an outer portfolio reference ring
- **AND** the outer ring reflects the full portfolio composition weighted by share counts
- **AND** the inner rings continue to represent the selected ETFs

#### Scenario: Reference ring updates with portfolio weights
- **WHEN** the user changes the share count of one selected ETF
- **THEN** the portfolio reference ring updates to reflect the new share-count weighting
- **AND** the per-ETF rings remain unchanged except for their existing ETF-specific data

#### Scenario: No reference ring without a selectable portfolio
- **WHEN** there are no selected ETFs or all selected ETFs have zero share counts
- **THEN** the comparison charts SHALL not render a portfolio reference ring
- **AND** the charts SHALL continue to handle the empty state without errors
