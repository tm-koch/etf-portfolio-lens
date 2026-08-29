## MODIFIED Requirements

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
