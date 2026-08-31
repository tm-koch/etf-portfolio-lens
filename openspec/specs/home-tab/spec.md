# home-tab Specification

## Purpose
TBD - created by archiving change add-home-tab. Update Purpose after archive.
## Requirements
### Requirement: Home destination overview
The web app SHALL provide a Home destination as the first item in the primary navigation. The Home destination SHALL contain the ETF Portfolio Lens introduction currently shown at the beginning of the application and SHALL be independently selectable from Portfolio, Compare, and Explore. The Home panel SHALL retain its build-information action, while color-mode selection SHALL be provided by the global app-level control rather than the build-information dialog.

#### Scenario: Home is the first navigation destination
- **WHEN** the application renders its primary navigation
- **THEN** Home appears before Portfolio, Compare, and Explore and displays a house icon above its label

#### Scenario: Home displays the product overview
- **WHEN** Home is the active destination
- **THEN** the ETF Portfolio Lens introduction and its build-information action are visible in the Home panel

#### Scenario: Home does not own color-mode selection
- **WHEN** the user opens About this build from Home
- **THEN** build details remain available and color-mode selection is not embedded in that dialog because the global control provides it

#### Scenario: Selecting Home changes the active panel
- **WHEN** a user activates Home
- **THEN** the Home panel becomes active and the Portfolio, Compare, and Explore panels become inactive

### Requirement: Home portfolio summary
The Home destination SHALL display live summary boxes for Positions, Share units, Total value, Underlying holdings, and Shared companies using the current selected portfolio state. Total value SHALL use the existing CHF currency format for finite non-negative imported valuation totals. When no portfolio positions are selected, or no finite non-negative imported valuation values are available, Total value SHALL display `CHF 0.00` rather than an unavailable-data label.

#### Scenario: Summary reflects selected positions
- **WHEN** the user adds, removes, or changes shares for a portfolio position
- **THEN** the five Home summary boxes update to reflect the current portfolio state

#### Scenario: Empty portfolio summary
- **WHEN** no portfolio positions are selected
- **THEN** Home displays `0` for Positions, Share units, Underlying holdings, and Shared companies, displays `CHF 0.00` for Total value, and does not fail to render

#### Scenario: Portfolio has no imported valuation data
- **WHEN** selected positions exist but none has a finite non-negative imported valuation value
- **THEN** Home displays `CHF 0.00` for Total value without changing the other summary values

#### Scenario: Portfolio has imported valuation data
- **WHEN** selected positions include finite non-negative imported valuation values
- **THEN** Total value displays their sum using the existing CHF formatting with two decimal places and apostrophe-separated thousands

