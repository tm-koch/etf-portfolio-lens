# mobile-positions-layout Specification

## Purpose
TBD - created by archiving change mobile-positions-layout-and-dev-warnings. Update Purpose after archive.
## Requirements
### Requirement: Mobile selected-position reflow

The application SHALL render each selected ETF position without requiring horizontal scrolling at supported mobile viewport widths. On mobile, the ETF ticker and name SHALL occupy the upper area of the position entry, while Shares, Weight, and Remove SHALL occupy the same lower row. Each position entry SHALL render as a complete enclosed card with visible top, right, bottom, and left boundaries.

#### Scenario: Position fits within a phone viewport
- **WHEN** the Selected positions view is displayed at a supported mobile viewport width
- **THEN** each position entry SHALL fit within the available content width without horizontal scrolling

#### Scenario: ETF identity is above controls
- **WHEN** a mobile position entry is rendered
- **THEN** its ETF ticker and name SHALL appear in the upper area before the Shares, Weight, and Remove controls

#### Scenario: Remove shares the lower row
- **WHEN** a mobile position entry displays its controls
- **THEN** Shares, Weight, and Remove SHALL be presented together on one lower row

#### Scenario: Position card has a complete boundary
- **WHEN** a mobile position entry is rendered
- **THEN** its visible card border SHALL include continuous top, right, bottom, and left edges without the lower edge being omitted or clipped

### Requirement: Mobile position controls remain usable

The mobile position layout SHALL preserve editing of Shares, display of the existing Weight value without duplicated inline warning text, and removal of the selected ETF. The Weight value SHALL be vertically centered within the lower control row alongside the Shares input and Remove control. Each control SHALL retain an accessible name and SHALL remain usable by keyboard and pointer input.

#### Scenario: Shares are edited on mobile
- **WHEN** the user changes a Shares input in a mobile position entry
- **THEN** the application SHALL preserve the existing position-editing behavior and update the displayed portfolio state

#### Scenario: Position is removed on mobile
- **WHEN** the user activates Remove in a mobile position entry
- **THEN** the application SHALL remove that selected ETF using the existing removal behavior

#### Scenario: Position weight remains concise
- **WHEN** a selected ETF has an existing position warning
- **THEN** the mobile Weight area SHALL display the portfolio percentage without appending a warning count, while the warning remains available in the dedicated warning views

#### Scenario: Mobile control strip avoids repeated labels
- **WHEN** a selected ETF position is displayed at a mobile viewport width
- **THEN** Shares, Weight, and Remove SHALL remain accessible without requiring repeated visible field titles, and Remove SHALL expose an accessible name and pointer tooltip

#### Scenario: Position weight is vertically centered
- **WHEN** a mobile position entry displays its Shares input, Weight percentage, and Remove control
- **THEN** the Weight percentage SHALL be vertically centered relative to the neighboring Shares and Remove controls

### Requirement: Larger viewport compatibility

The application SHALL present selected ETF positions as rounded enclosed boxes above the mobile reflow breakpoint. In the wide catalog-and-portfolio side-by-side layout, each position box SHALL place the ETF ticker and name on the first line, place labeled Shares and available pricing/value and Weight metrics on the second line, and place the Remove control in a right-aligned area centered vertically across the box. The application SHALL preserve the existing position editing, valuation, weight, and removal behavior. At the mobile reflow breakpoint, the existing mobile card layout SHALL remain in effect.

#### Scenario: Wide positions use rounded boxes

WHEN the Selected positions view is displayed in the wide catalog-and-portfolio side-by-side layout

THEN each selected ETF SHALL appear in an enclosed rounded position box with visible boundaries and spacing from adjacent boxes.

#### Scenario: Wide identity occupies the first line

WHEN a wide selected position is rendered

THEN its ticker and ETF name SHALL appear together on the first line before the position metrics.

#### Scenario: Wide metrics occupy the second line

WHEN a wide selected position is rendered

THEN Shares, available Price and Value CHF fields, and Weight SHALL appear as labeled metrics on the second line, with absolute valuation fields omitted for percentage-only portfolios.

#### Scenario: Wide Remove control is centered and right-aligned

WHEN a wide selected position displays its Remove control

THEN the control SHALL be right-aligned in a dedicated area and vertically centered against the complete position box.

#### Scenario: Wide position behavior is preserved

WHEN a user edits Shares, changes valuation mode, or activates Remove in a wide position box

THEN the existing state update, valuation, weight recalculation, and removal behavior SHALL continue to work.

#### Scenario: Mobile reflow remains unchanged

WHEN the Selected positions view is displayed at a supported mobile viewport width

THEN the existing mobile arrangement SHALL keep identity above the Shares, Weight, and Remove control row without horizontal scrolling.
