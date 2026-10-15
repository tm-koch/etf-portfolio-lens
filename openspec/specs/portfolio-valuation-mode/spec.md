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

The valuation mode control and portfolio-level valuation-status box SHALL be hidden or disabled for percentage-only portfolios, whether entered locally or loaded from a private share, including before asynchronous portfolio loading completes. Changing or loading such a portfolio SHALL NOT invent, resolve, or render absolute prices or CHF totals. When hidden, the valuation mode control and valuation-status box SHALL be visually absent from layout. Percentage-only position tables SHALL contain ETF, relative allocation input, normalized Weight, and Remove columns.

#### Scenario: Percentage portfolio is active

- **WHEN** the active portfolio is in relative allocation mode
- **THEN** the valuation mode control and valuation-status box are unavailable and visually absent, the Price and Value CHF headers and cells are absent, the relative Weight header and cells remain visible, the Remove control remains available, and absolute monetary values remain unavailable

#### Scenario: Percentage portfolio is edited

- **WHEN** a user changes a relative allocation unit in a locally entered or privately shared percentage portfolio
- **THEN** weights and dependent exposure views update from relative units without resolving position prices, CHF values, or valuation provenance

#### Scenario: Full portfolio remains valuation-capable

- **WHEN** the active portfolio is a shares-based portfolio
- **THEN** the valuation mode control, valuation-status box, and valuation columns remain available and the selected latest or imported valuation behavior is unchanged

### Requirement: Show valuation provenance at portfolio level

The full portfolio presentation SHALL show one `Live` or `Imported` provenance note beside and horizontally aligned with the valuation mode control, right-aligned within the valuation row, with its top aligned to the select box rather than the selector label, instead of appending the source in parentheses to each Value CHF cell. The blue status dot SHALL be visible and slowly animated only for live mode. Percentage-only portfolios, whether entered locally or loaded from a private share, SHALL not display this provenance note or status box.

#### Scenario: Live valuation is selected

- **WHEN** the active shares-based portfolio uses the latest valuation mode
- **THEN** the portfolio-level note says `Live`, includes the blue status dot, and the Value CHF cells contain numeric values without a parenthesized source label

#### Scenario: Imported valuation is selected

- **WHEN** the active shares-based portfolio uses imported valuation mode
- **THEN** the portfolio-level note says `Imported`, omits the blue status dot, and the Value CHF cells contain numeric values without a parenthesized source label

#### Scenario: Percentage valuation provenance is hidden

- **WHEN** a local or privately shared percentage-only portfolio is active
- **THEN** the valuation-status box is absent after startup and subsequent portfolio rerenders, including in the browser layout
