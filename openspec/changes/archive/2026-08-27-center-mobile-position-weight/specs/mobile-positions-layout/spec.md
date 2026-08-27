## MODIFIED Requirements

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
