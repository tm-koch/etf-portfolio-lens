# Spec Delta

## MODIFIED Requirements

### Requirement: Control full-portfolio valuation mode
The Portfolio workflow SHALL provide a control for full portfolios that selects latest published valuation, and SHALL offer imported broker valuation only when the portfolio contains at least one position and every position has a usable persisted imported CHF valuation. The selected mode SHALL immediately affect all monetary displays and portfolio calculations.

#### Scenario: User selects latest valuation
- **WHEN** a user selects latest published valuation for a full portfolio
- **THEN** selected positions use available live quotes and supported FX conversion, falling back to persisted imported CHF values when live valuation is unavailable

#### Scenario: User selects imported valuation
- **WHEN** a user selects imported valuation for a full portfolio where every position has a usable persisted imported CHF valuation
- **THEN** selected positions use their persisted imported broker values and do not use live quote prices for effective valuation

#### Scenario: Mode changes are reflected immediately
- **WHEN** the user changes the full-portfolio valuation mode
- **THEN** position prices, CHF values, weights, totals, and source labels rerender without re-importing the PDF

#### Scenario: Empty portfolio has no imported valuation option
- **WHEN** a full portfolio contains no positions
- **THEN** the valuation control does not offer imported broker valuation

#### Scenario: Mixed portfolio has no imported valuation option
- **WHEN** at least one position in a full portfolio lacks a usable persisted imported CHF valuation
- **THEN** the valuation control does not offer imported broker valuation

#### Scenario: Complete imported valuations make the option available
- **WHEN** a full portfolio contains at least one position and every position has a usable persisted imported CHF valuation
- **THEN** the valuation control offers imported broker valuation

#### Scenario: Adding an unvalued position removes imported availability
- **WHEN** a position without a usable persisted imported CHF valuation is added to a full portfolio using imported valuation
- **THEN** the portfolio switches to latest published valuation and the control no longer offers imported broker valuation

### Requirement: Persist full-portfolio valuation mode
The application SHALL persist the selected full-portfolio valuation mode across reloads and SHALL default legacy portfolios without a stored mode to latest published valuation. When a restored portfolio does not have a usable imported CHF valuation for every position, the application SHALL use and persist latest published valuation without discarding imported position fields.

#### Scenario: Mode survives reload
- **WHEN** a user reloads after selecting imported valuation and every position still has a usable persisted imported CHF valuation, or after selecting latest published valuation
- **THEN** the same valuation mode is restored and applied to the portfolio

#### Scenario: Imported mode falls back after reload when values are incomplete
- **WHEN** a saved portfolio is restored in imported mode and any position lacks a usable persisted imported CHF valuation
- **THEN** the application switches to and persists latest published valuation while retaining all imported position fields

#### Scenario: Legacy portfolio loads
- **WHEN** a portfolio saved before portfolio-level valuation mode exists is loaded
- **THEN** the application uses latest published valuation as the default without discarding imported position fields
