## ADDED Requirements

### Requirement: Respect an explicit user valuation mode
The valuation layer SHALL accept an explicit full-portfolio valuation mode. In latest mode it SHALL use a valid live quote and supported FX conversion when available, with imported CHF fallback; in imported mode it SHALL use persisted imported CHF values and SHALL NOT use a live quote for effective valuation.

#### Scenario: Latest mode uses live data
- **WHEN** latest mode is selected and a valid quote, supported FX rate, shares, and imported fallback fields exist
- **THEN** effective valuation uses the live quote and FX rate and is marked live

#### Scenario: Imported mode bypasses live data
- **WHEN** imported mode is selected and a live quote exists alongside a persisted imported CHF value
- **THEN** effective valuation uses the imported CHF value and is marked imported rather than live

#### Scenario: Latest mode retains fallback behavior
- **WHEN** latest mode is selected but a quote or required FX rate is unavailable
- **THEN** effective valuation uses the persisted imported CHF value and is marked imported fallback
