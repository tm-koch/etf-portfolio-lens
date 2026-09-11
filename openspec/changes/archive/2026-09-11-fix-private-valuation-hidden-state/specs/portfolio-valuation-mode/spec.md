## MODIFIED Requirements

### Requirement: Keep percentage portfolios valuation-independent

The valuation mode control and portfolio-level valuation-status box SHALL be hidden or disabled for percentage-only private portfolios, including before asynchronous portfolio loading completes, and changing or loading such a portfolio SHALL not invent, resolve, or render absolute prices or CHF totals. When hidden, the valuation mode control and valuation-status box SHALL be visually absent from layout. Percentage-only position tables SHALL contain ETF, relative Shares, normalized Weight, and Remove columns.

#### Scenario: Percentage portfolio is active

- **WHEN** the active portfolio is percentage-only
- **THEN** the valuation mode control and valuation-status box are unavailable and visually absent, the Price and Value CHF headers and cells are absent, the relative Weight header and cells remain visible, the Remove control remains available, and absolute monetary values remain unavailable

#### Scenario: Percentage portfolio is edited

- **WHEN** a user changes a relative Shares unit in a percentage-only portfolio
- **THEN** weights and dependent exposure views update from relative units without resolving position prices, CHF values, or valuation provenance

#### Scenario: Full portfolio remains valuation-capable

- **WHEN** the active portfolio is a normal full portfolio
- **THEN** the valuation mode control, valuation-status box, and valuation columns remain available and the selected latest or imported valuation behavior is unchanged

### Requirement: Show valuation provenance at portfolio level

The full portfolio presentation SHALL show one `Live` or `Imported` provenance note beside and horizontally aligned with the valuation mode control, right-aligned within the valuation row, with its top aligned to the select box rather than the selector label, instead of appending the source in parentheses to each Value CHF cell. The blue status dot SHALL be visible and slowly animated only for live mode. Percentage-only private portfolios SHALL not display this provenance note or status box.

#### Scenario: Live valuation is selected

- **WHEN** the active full portfolio uses the latest valuation mode
- **THEN** the portfolio-level note says `Live`, includes the blue status dot, and the Value CHF cells contain numeric values without a parenthesized source label

#### Scenario: Imported valuation is selected

- **WHEN** the active full portfolio uses imported valuation mode
- **THEN** the portfolio-level note says `Imported`, omits the blue status dot, and the Value CHF cells contain numeric values without a parenthesized source label

#### Scenario: Private valuation provenance is hidden

- **WHEN** a valid private percentage-only share portfolio is active
- **THEN** the valuation-status box is absent after startup and subsequent portfolio rerenders, including in the browser layout
