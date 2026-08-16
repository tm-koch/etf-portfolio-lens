## ADDED Requirements

### Requirement: Compact mobile navigation geometry
At viewport widths up to 760px, the mobile navigation SHALL use a stable 64px icon-and-label row, 18px navigation icons, a 3px icon-to-label gap, and a 2px gap between destination items. Each destination button SHALL retain a target height of at least 44px.

#### Scenario: Compact navigation dimensions
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation row and destination buttons use a 64px height, each icon is 18px square, and the icon-to-label gap is 3px

#### Scenario: Compact navigation item spacing
- **WHEN** the viewport width is 760px or less
- **THEN** adjacent destination items use a 2px gap and all three destinations remain visible without horizontal scrolling

#### Scenario: Compact geometry remains stable
- **WHEN** the browser visual viewport changes during mobile scrolling
- **THEN** the navigation row height and destination button height remain 64px and do not resize based on content

### Requirement: Mobile navigation typography distinguishes state
At viewport widths up to 760px, inactive navigation labels SHALL use a 0.75rem font size, regular font weight, and the muted navigation color. The active navigation label SHALL use the same font size with bold font weight and accent blue, and its icon SHALL use accent blue with bold stroke emphasis.

#### Scenario: Inactive destination typography
- **WHEN** a destination is inactive and the viewport width is 760px or less
- **THEN** its label uses a 0.75rem font size, regular font weight, and the muted color

#### Scenario: Active destination typography
- **WHEN** a destination is active and the viewport width is 760px or less
- **THEN** its label uses a 0.75rem font size, bold font weight, and accent blue, and its icon is accent blue

#### Scenario: Desktop typography remains unchanged
- **WHEN** the viewport width is greater than 760px
- **THEN** the compact mobile font sizes, weights, icon sizes, and spacing do not alter desktop navigation styling
