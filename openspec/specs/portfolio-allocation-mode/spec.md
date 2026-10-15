# portfolio-allocation-mode Specification

## Purpose
TBD - created by archiving change portfolio-percentage-entry. Update Purpose after archive.
## Requirements
### Requirement: Select and persist portfolio entry mode

The Portfolio tab SHALL provide an accessible control for selecting shares-based entry or relative allocation entry. The selected mode SHALL be persisted and restored across reloads. Existing saved portfolios without a mode SHALL continue to load in shares mode, and valid private percentage share links SHALL continue to load in relative allocation mode.

#### Scenario: Select relative allocation mode
- **WHEN** a user selects Allocation (%) for a shares-based portfolio
- **THEN** the application changes the portfolio to relative allocation mode, converts each selected position to its current derived normalized weight, persists the mode, and updates the portfolio presentation

#### Scenario: Select relative allocation mode for an empty portfolio
- **WHEN** a user selects Allocation (%) with no selected positions
- **THEN** the application enters relative allocation mode with an empty portfolio and persists the selection

#### Scenario: Restore selected mode
- **WHEN** a user reloads after selecting a portfolio entry mode
- **THEN** the application restores that mode and its portfolio values, while a legacy saved portfolio with no mode remains in shares mode

### Requirement: Edit relative allocation weights

In relative allocation mode, the Portfolio tab SHALL allow users to add, edit, and remove positions using finite non-negative relative weight units. Entered values SHALL NOT be required to total 100. The application SHALL normalize each position's displayed weight and all dependent portfolio analysis by the sum of the selected positions' relative units. The interface SHALL identify the values as relative allocation inputs and SHALL NOT imply they are absolute share counts.

#### Scenario: Edit a relative allocation
- **WHEN** a user changes a position's relative allocation value
- **THEN** the application persists the value and updates normalized weights and dependent exposure views without resolving absolute valuations

#### Scenario: Relative allocation values do not total 100
- **WHEN** relative allocation values have a positive sum other than 100
- **THEN** the application accepts the values and displays and analyzes each position using its value divided by the total relative units

#### Scenario: Add a position in relative allocation mode
- **WHEN** a user adds an ETF while relative allocation mode is active
- **THEN** the new position receives a relative allocation unit and appears in the existing allocation presentation

### Requirement: Retain positions when leaving relative allocation mode

The application SHALL NOT convert relative allocation units into absolute share counts without an explicit investment amount and valuation basis. When a user switches from relative allocation mode to shares mode, the application SHALL immediately retain every selected ETF, set each position's share count to zero, persist the shares-based mode, and SHALL NOT show a confirmation prompt.

#### Scenario: Switch to shares mode without a prompt
- **WHEN** a user selects Shares while relative allocation mode is active
- **THEN** the application immediately enters shares mode, retains every selected ETF with a share count of zero, persists the portfolio, and displays the shares-based presentation without showing a confirmation prompt

#### Scenario: Switch an empty allocation portfolio to shares mode
- **WHEN** a user selects Shares while the relative allocation portfolio is empty
- **THEN** the application immediately enters shares mode with an empty portfolio and persists the mode without showing a confirmation prompt
