## ADDED Requirements

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
