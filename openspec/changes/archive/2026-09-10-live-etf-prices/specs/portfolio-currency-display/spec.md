## ADDED Requirements

### Requirement: Display supported live valuation currencies
The Portfolio workflow SHALL support CHF, EUR, and USD source currencies and SHALL display the effective valuation source and live-data timestamp or fallback status when available.

#### Scenario: USD price is displayed
- **WHEN** a selected position has a finite USD price
- **THEN** the position displays the USD currency code with exactly two decimal places and apostrophe-separated thousands

#### Scenario: Imported fallback is displayed
- **WHEN** a live valuation is unavailable and the imported CHF value is used
- **THEN** the position identifies the value as an imported fallback rather than presenting it as current live data
