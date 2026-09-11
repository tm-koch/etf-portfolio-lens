## MODIFIED Requirements

### Requirement: Keep the existing portfolio GUI for private mode

The application SHALL use the existing selected-position table and Shares inputs for private portfolios and SHALL communicate that the values are relative weighting units through the portfolio hint or share feedback. It SHALL hide the valuation basis control and the portfolio-level valuation-status box for percentage-only portfolios, and those elements SHALL be visually absent whenever their hidden state is active. It SHALL omit Price and Value CHF headers and cells entirely, SHALL display each position's normalized relative Weight, and SHALL retain the Remove control. It SHALL NOT resolve absolute position valuations while rendering percentage-only rows.

#### Scenario: Private portfolio is displayed

- **WHEN** a recipient opens a valid private link
- **THEN** the existing relative-allocation portfolio presentation remains available with editable Shares inputs, normalized Weight values, and Remove controls, while the valuation basis control, valuation-status box, Price, and Value CHF headers and cells are absent

#### Scenario: Private valuation elements are hidden by the presentation layer

- **WHEN** a percentage-only portfolio marks the valuation basis control and valuation-status box as hidden
- **THEN** CSS removes both elements from layout so neither valuation control nor valuation provenance is visible

#### Scenario: Private portfolio does not resolve valuations

- **WHEN** a percentage-only portfolio is rendered or a relative Shares unit is edited
- **THEN** the application calculates displayed weights from relative units without invoking position valuation resolution or creating absolute price or CHF values

#### Scenario: Private portfolio supports scenario exploration

- **WHEN** a recipient edits a relative Shares unit and the change is valid
- **THEN** the edited portfolio is persisted and all existing portfolio weights, charts, and look-through exposure update from the normalized relative units

#### Scenario: Full portfolio valuation presentation remains available

- **WHEN** a normal full portfolio is rendered
- **THEN** the existing valuation basis control, valuation-status box, Price, Value CHF, and Weight columns remain available according to the selected valuation mode

#### Scenario: Private table stays compact on mobile

- **WHEN** a percentage-only portfolio is displayed on a mobile viewport
- **THEN** each row contains the ETF identity, Shares input, normalized Weight, and Remove control, without an empty valuation grid area

#### Scenario: Private table has mobile separation

- **WHEN** a percentage-only portfolio is displayed on a mobile viewport
- **THEN** the first ETF row is separated from the selected-position heading and valuation area by visible top spacing
