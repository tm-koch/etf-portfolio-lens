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
The Home destination SHALL display live summary boxes for Positions, Share units, Total value, Underlying holdings, and Shared companies using the current selected portfolio state. Total value SHALL use the sum of finite non-negative effective CHF valuations from the hybrid valuation policy, including live values and explicitly marked imported fallbacks, with exactly two decimal places and apostrophe-separated thousands. When no portfolio positions are selected, or no finite effective CHF valuations are available, Total value SHALL display `CHF 0.00`.

#### Scenario: Summary reflects selected positions
- **WHEN** a user adds, removes, changes shares, or changes valuation mode for a portfolio position
- **THEN** the five Home summary boxes update to reflect the current effective portfolio state

#### Scenario: Live and fallback values are combined
- **WHEN** selected positions contain a mixture of live effective values and imported fallback values
- **THEN** Total value displays the sum of both finite effective values and the interface exposes that fallback data is present

#### Scenario: No effective valuation is available
- **WHEN** selected positions exist but none has a finite effective CHF valuation
- **THEN** Home displays `CHF 0.00` for Total value without inventing a value

