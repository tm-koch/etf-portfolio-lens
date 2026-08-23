# home-tab Specification

## Purpose
TBD - created by archiving change add-home-tab. Update Purpose after archive.
## Requirements
### Requirement: Home destination overview
The web app SHALL provide a Home destination as the first item in the primary navigation. The Home destination SHALL contain the ETF Portfolio Lens introduction currently shown at the beginning of the application and SHALL be independently selectable from Portfolio, Compare, and Explore.

#### Scenario: Home is the first navigation destination
- **WHEN** the application renders its primary navigation
- **THEN** Home appears before Portfolio, Compare, and Explore and displays a house icon above its label

#### Scenario: Home displays the product overview
- **WHEN** Home is the active destination
- **THEN** the ETF Portfolio Lens introduction and its build-information action are visible in the Home panel

#### Scenario: Selecting Home changes the active panel
- **WHEN** a user activates Home
- **THEN** the Home panel becomes active and the Portfolio, Compare, and Explore panels become inactive

### Requirement: Home portfolio summary
The Home destination SHALL display live summary boxes for Positions, Share units, Underlying holdings, and Shared companies using the current selected portfolio state.

#### Scenario: Summary reflects selected positions
- **WHEN** the user adds, removes, or changes shares for a portfolio position
- **THEN** the four Home summary boxes update to reflect the current portfolio state

#### Scenario: Empty portfolio summary
- **WHEN** no portfolio positions are selected
- **THEN** Home displays zero values for the four summary boxes without failing to render
