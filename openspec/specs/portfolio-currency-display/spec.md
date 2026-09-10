# portfolio-currency-display Specification

## Purpose
TBD - created by archiving change format-portfolio-currency-values. Update Purpose after archive.
## Requirements
### Requirement: Format displayed Portfolio currency values
The Portfolio workflow SHALL display finite monetary values in supported CHF and EUR currencies with the currency code, exactly two decimal places, and apostrophe-separated thousands. This formatting SHALL apply to the summary total, selected position prices, and selected position CHF values without changing the underlying numeric values.

#### Scenario: Large CHF and EUR values are grouped
- **WHEN** the Portfolio view renders finite values such as `12345.67` in CHF or EUR
- **THEN** the displayed values use `CHF 12'345.67` or `EUR 12'345.67`

#### Scenario: Display formatting does not change editable data
- **WHEN** a user edits a share count or another numeric Portfolio input
- **THEN** the input value, persisted numeric data, and calculations remain numeric and are not replaced with apostrophe-formatted text

#### Scenario: Private portfolio lacks absolute values
- **WHEN** a private portfolio contains no absolute price or value data
- **THEN** the existing unavailable presentation remains visible instead of inventing or formatting an absolute amount

### Requirement: Display supported live valuation currencies
The Portfolio workflow SHALL support CHF, EUR, and USD source currencies and SHALL display the effective valuation source and live-data timestamp or fallback status when available.

#### Scenario: USD price is displayed
- **WHEN** a selected position has a finite USD price
- **THEN** the position displays the USD currency code with exactly two decimal places and apostrophe-separated thousands

#### Scenario: Imported fallback is displayed
- **WHEN** a live valuation is unavailable and the imported CHF value is used
- **THEN** the position identifies the value as an imported fallback rather than presenting it as current live data

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

