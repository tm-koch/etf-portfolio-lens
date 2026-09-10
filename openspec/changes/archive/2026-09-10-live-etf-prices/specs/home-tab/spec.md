## MODIFIED Requirements

### Requirement: Home portfolio summary
The Home destination SHALL display live summary boxes for Positions, Share units, Total value, Underlying holdings, and Shared companies using the current selected portfolio state. Total value SHALL use the sum of finite non-negative effective CHF valuations from the hybrid valuation policy, including live values and explicitly marked imported fallbacks, with exactly two decimal places and apostrophe-separated thousands. When no portfolio positions are selected, or no finite effective CHF valuations are available, Total value SHALL display `CHF 0.00`.

#### Scenario: Summary reflects selected positions
- **WHEN** a user adds, removes, changes shares, or changes valuation mode for a portfolio position
- **THEN** the five Home summary boxes update to reflect the current effective portfolio state

#### Scenario: Live and fallback values are combined
- **WHEN** selected positions contain a mixture of live effective values and imported fallback values
- **THEN** Total value displays the sum of both finite effective values and the interface exposes that fallback data is present

#### Scenario: No effective valuation is available
- **WHEN** selected positions exist but none has a finite effective CHF valuation
- **THEN** Home displays `CHF 0.00` for Total value without inventing a value
