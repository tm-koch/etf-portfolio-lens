# portfolio-valuation-mode Specification

## Purpose
TBD - created by archiving change portfolio-valuation-mode-toggle. Update Purpose after archive.

## Requirements

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

### Requirement: Keep valuation controls compact on smartphones

On smartphone-width viewports in shares-based mode, the valuation selector and provenance status SHALL appear directly beneath Entry mode on the same horizontal row. The status SHALL be vertically centered with the selector, and the row SHALL fit the available viewport without a fixed empty vertical spacer or horizontal overflow.

#### Scenario: Valuation selector and status share a row on a phone
- **WHEN** the Portfolio tab displays a shares-based portfolio on a smartphone-width viewport
- **THEN** the valuation selector and provenance status appear directly beneath Entry mode on the same row, with their control surfaces vertically centered and no oversized blank region

#### Scenario: Selector and status fit on a narrow phone
- **WHEN** the selected-positions panel is displayed at a 320px viewport width
- **THEN** the selector uses the available row width beside the provenance status, both remain visible and operable, and the page has no horizontal overflow
