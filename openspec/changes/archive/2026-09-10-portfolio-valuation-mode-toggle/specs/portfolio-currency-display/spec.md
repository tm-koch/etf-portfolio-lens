## ADDED Requirements

### Requirement: Display the selected valuation source
The Portfolio workflow SHALL identify whether displayed position prices and CHF values come from latest live valuation, imported valuation, or imported fallback according to the active portfolio valuation mode and available data.

#### Scenario: Latest mode has a live quote
- **WHEN** latest mode is active and a valid live quote with required FX data exists
- **THEN** the position displays the live source and the live price and CHF value

#### Scenario: Imported mode is active
- **WHEN** imported mode is active and an imported value exists
- **THEN** the position displays the imported source and imported price and CHF value

#### Scenario: Latest mode falls back
- **WHEN** latest mode is active but live quote or required FX data is unavailable and an imported CHF value exists
- **THEN** the position displays the imported fallback source and imported CHF value

### Requirement: Recalculate portfolio weights from selected valuation
Portfolio weights and monetary totals SHALL use the effective CHF values produced by the active valuation mode whenever absolute values are available.

#### Scenario: Mode changes weights
- **WHEN** switching between latest and imported mode changes effective CHF values
- **THEN** the displayed weights and total value update to match the selected mode
