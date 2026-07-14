## ADDED Requirements

### Requirement: One stacked bar per company
The aggregated holdings view SHALL render exactly one stacked bar for each company row.

#### Scenario: Company row uses a single bar
- **WHEN** the aggregated holdings view renders a company with one or more ETF contributors
- **THEN** the company row SHALL contain one bar composed of stacked ETF-colored segments
- **AND** the view SHALL NOT render separate bars for each contributing ETF

### Requirement: Bar width reflects ranking exposure
The aggregated holdings view SHALL size the full width of each stacked bar according to the company's total exposure value used for ranking.

#### Scenario: Largest company gets the widest bar
- **WHEN** multiple companies are displayed in the aggregated list
- **THEN** the company with the highest total exposure SHALL render the widest bar
- **AND** each lower-ranked company SHALL render a bar width proportional to its total exposure relative to that maximum
- **AND** the ranking order SHALL remain based on the same total exposure value

### Requirement: Stacked segments preserve ETF composition
The aggregated holdings view SHALL preserve ETF-colored segments within each company bar so the segment widths represent each ETF's contribution to that company's total exposure.

#### Scenario: Bar segments show ETF shares
- **WHEN** a company bar contains contributions from multiple ETFs
- **THEN** each stacked segment SHALL use the ETF-specific color
- **AND** each segment width SHALL represent that ETF's share of the company total exposure
- **AND** the company label and exact company exposure SHALL remain visible alongside the bar
