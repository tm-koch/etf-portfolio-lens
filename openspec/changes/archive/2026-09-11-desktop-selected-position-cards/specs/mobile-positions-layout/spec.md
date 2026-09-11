## MODIFIED Requirements

### Requirement: Larger viewport compatibility

The application SHALL present selected ETF positions as rounded enclosed boxes above the mobile reflow breakpoint. In the wide catalog-and-portfolio side-by-side layout, each position box SHALL place the ETF ticker and name on the first line, place labeled Shares and available pricing/value and Weight metrics on the second line, and place the Remove control in a right-aligned area centered vertically across the box. The application SHALL preserve the existing position editing, valuation, weight, and removal behavior. At the mobile reflow breakpoint, the existing mobile card layout SHALL remain in effect.

#### Scenario: Wide positions use rounded boxes

- **WHEN** the Selected positions view is displayed in the wide catalog-and-portfolio side-by-side layout
- **THEN** each selected ETF SHALL appear in an enclosed rounded position box with visible boundaries and spacing from adjacent boxes

#### Scenario: Wide identity occupies the first line

- **WHEN** a wide selected position is rendered
- **THEN** its ticker and ETF name SHALL appear together on the first line before the position metrics

#### Scenario: Wide metrics occupy the second line

- **WHEN** a wide selected position is rendered
- **THEN** Shares, available Price and Value CHF fields, and Weight SHALL appear as labeled metrics on the second line, with absolute valuation fields omitted for percentage-only portfolios

#### Scenario: Wide Remove control is centered and right-aligned

- **WHEN** a wide selected position displays its Remove control
- **THEN** the control SHALL be right-aligned in a dedicated area and vertically centered against the complete position box

#### Scenario: Wide position behavior is preserved

- **WHEN** a user edits Shares, changes valuation mode, or activates Remove in a wide position box
- **THEN** the existing state update, valuation, weight recalculation, and removal behavior SHALL continue to work

#### Scenario: Mobile reflow remains unchanged

- **WHEN** the Selected positions view is displayed at a supported mobile viewport width
- **THEN** the existing mobile arrangement SHALL keep identity above the Shares, Weight, and Remove control row without horizontal scrolling
