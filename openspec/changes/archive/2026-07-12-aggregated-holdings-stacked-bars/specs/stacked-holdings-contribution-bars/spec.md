## ADDED Requirements

### Requirement: Horizontal stacked holdings bars
The system MUST present the aggregated company exposure view as horizontal stacked bars, where each row represents one company ranked by total portfolio exposure.

#### Scenario: Render ranked company rows as bars
- **WHEN** the user opens the aggregated holdings view
- **THEN** the system SHALL show each company as a horizontal bar row
- **AND THEN** the rows SHALL be ordered from highest total exposure to lowest total exposure

### Requirement: ETF contribution segments
The system MUST split each company bar into ETF-specific segments that represent how much each ETF contributes to that company’s total portfolio exposure.

#### Scenario: Show segment contribution by ETF
- **WHEN** a company appears in more than one ETF in the portfolio
- **THEN** the system SHALL divide the company’s bar into one segment per contributing ETF
- **AND THEN** each segment SHALL represent that ETF’s share of the company’s total exposure

#### Scenario: Single-ETF company exposure
- **WHEN** a company appears in only one ETF in the portfolio
- **THEN** the system SHALL render the bar as a single segment for that ETF

### Requirement: Contribution percentages must be visible
The system MUST display percentage values for the individual ETF contributions within each company bar so the user can read the split without relying only on color.

#### Scenario: Label the contribution segments
- **WHEN** a company bar contains multiple ETF segments
- **THEN** the system SHALL display the ETF contribution percentage for each visible segment
- **AND THEN** the labels SHALL identify which ETF contributed the segment

#### Scenario: Handle narrow segments
- **WHEN** a segment is too small to fit an inline label safely
- **THEN** the system SHALL preserve the percentage in hover or detail text for that segment
- **AND THEN** the segment SHALL remain part of the stacked bar

### Requirement: Company total exposure remains visible
The system MUST continue to show the total company exposure as a percentage of the whole portfolio alongside each stacked bar.

#### Scenario: Preserve total ranking semantics
- **WHEN** a company row is rendered in the aggregated holdings view
- **THEN** the row SHALL show the company’s total exposure as a whole-portfolio percentage
- **AND THEN** the total SHALL equal the sum of the ETF contribution segments for that company

### Requirement: Responsive stacked bar layout
The system MUST render the stacked holdings bars in a layout that remains readable on narrow screens without introducing horizontal scrolling in the main content area.

#### Scenario: View stacked bars on a narrow viewport
- **WHEN** the user opens the aggregated holdings view on a smartphone-sized screen
- **THEN** the company bars SHALL remain legible
- **AND THEN** the view SHALL remain usable without horizontal overflow in the main content area
