## ADDED Requirements

### Requirement: Aggregated company bars scale to the largest holding
The aggregated holdings view SHALL normalize the visible width of each company bar against the company with the highest total exposure.

#### Scenario: Largest holding spans the full row width
- **WHEN** the aggregated holdings view renders multiple companies
- **THEN** the company with the highest total exposure SHALL render at the maximum available bar width
- **AND** every other company bar SHALL render proportionally smaller based on its total exposure

### Requirement: Aggregated bar segments preserve contributor shares
The aggregated holdings view SHALL continue to show each ETF's contribution within a company bar using stacked segments that reflect that ETF's share of the company total.

#### Scenario: Internal splits remain proportional
- **WHEN** a company bar is rendered with multiple contributing ETFs
- **THEN** each stacked segment SHALL represent that ETF's share of the company total exposure
- **AND** the full bar width SHALL still be governed by the company total relative to the largest holding
