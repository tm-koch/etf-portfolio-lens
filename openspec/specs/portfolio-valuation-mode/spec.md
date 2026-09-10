# portfolio-valuation-mode Specification

## Purpose
TBD - created by archiving change portfolio-valuation-mode-toggle. Update Purpose after archive.
## Requirements
### Requirement: Control full-portfolio valuation mode
The Portfolio workflow SHALL provide a control for full portfolios that selects either latest published valuation or imported broker valuation. The selected mode SHALL immediately affect all monetary displays and portfolio calculations.

#### Scenario: User selects latest valuation
- **WHEN** a user selects latest published valuation for a full portfolio
- **THEN** selected positions use available live quotes and supported FX conversion, falling back to persisted imported CHF values when live valuation is unavailable

#### Scenario: User selects imported valuation
- **WHEN** a user selects imported valuation for a full portfolio
- **THEN** selected positions use their persisted imported broker values and do not use live quote prices for effective valuation

#### Scenario: Mode changes are reflected immediately
- **WHEN** the user changes the full-portfolio valuation mode
- **THEN** position prices, CHF values, weights, totals, and source labels rerender without re-importing the PDF

### Requirement: Persist full-portfolio valuation mode
The application SHALL persist the selected full-portfolio valuation mode across reloads and SHALL default legacy portfolios without a stored mode to latest published valuation.

#### Scenario: Mode survives reload
- **WHEN** a user reloads after selecting imported or latest valuation
- **THEN** the same valuation mode is restored and applied to the portfolio

#### Scenario: Legacy portfolio loads
- **WHEN** a portfolio saved before portfolio-level valuation mode exists is loaded
- **THEN** the application uses latest published valuation as the default without discarding imported position fields

### Requirement: Keep percentage portfolios valuation-independent
The valuation mode control SHALL be hidden or disabled for percentage-only private portfolios, and changing or loading such a portfolio SHALL not invent absolute prices or CHF totals.

#### Scenario: Percentage portfolio is active
- **WHEN** the active portfolio is percentage-only
- **THEN** the valuation mode control is unavailable and absolute monetary values remain unavailable
