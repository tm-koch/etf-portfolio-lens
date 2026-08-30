## MODIFIED Requirements

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
