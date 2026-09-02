## MODIFIED Requirements

### Requirement: Home portfolio summary
The Home destination SHALL display live summary boxes for Positions, Share units, Total value, Underlying holdings, and Shared companies using the current selected portfolio state. Total value SHALL use the existing CHF currency format with exactly two decimal places and apostrophe-separated thousands for finite non-negative imported valuation totals. When no portfolio positions are selected, or no finite non-negative imported valuation values are available, Total value SHALL display `CHF 0.00` rather than an unavailable-data label.

#### Scenario: Summary reflects selected positions
- **WHEN** a user adds, removes, or changes shares for a portfolio position
- **THEN** the five Home summary boxes update to reflect the current portfolio state

#### Scenario: Empty portfolio summary
- **WHEN** no portfolio positions are selected
- **THEN** Home displays `0` for Positions, Share units, Underlying holdings, and Shared companies, displays `CHF 0.00` for Total value, and does not fail to render

#### Scenario: Portfolio has no imported valuation data
- **WHEN** selected positions exist but none has a finite non-negative imported valuation value
- **THEN** Home displays `CHF 0.00` for Total value without changing the other summary values

#### Scenario: Portfolio has imported valuation data
- **WHEN** selected positions include finite non-negative imported valuation values
- **THEN** Total value displays their sum with exactly two decimal places and apostrophe-separated thousands
