## ADDED Requirements

### Requirement: Primary destination navigation
The web app SHALL provide a primary navigation containing the destinations Portfolio, Compare, and Explore.

#### Scenario: Navigation displays the initial destinations
- **WHEN** the application loads successfully
- **THEN** one navigation control contains exactly the Portfolio, Compare, and Explore destinations

#### Scenario: Selecting a destination shows its content
- **WHEN** a user activates a destination navigation item
- **THEN** the corresponding content panel becomes active and the other destination panels become inactive

#### Scenario: Explore maps to the aggregated panel
- **WHEN** a user activates Explore
- **THEN** the panel using the internal `aggregated` destination key becomes active

### Requirement: Icon and label presentation
Each destination navigation item SHALL display a consistent Lucide icon and its visible text label, with the icon positioned above the label.

#### Scenario: Destination has an understandable visual identity
- **WHEN** the navigation is rendered
- **THEN** Portfolio, Compare, and Explore each display a distinct suitable icon above its label

#### Scenario: Icon rendering is unavailable
- **WHEN** the icon asset cannot be loaded or initialized
- **THEN** the destination labels remain visible and the navigation remains operable

### Requirement: Responsive navigation placement
The navigation SHALL remain in normal document flow on desktop widths and SHALL be fixed to the viewport bottom at widths up to 760px.

#### Scenario: Desktop navigation placement
- **WHEN** the viewport width is greater than 760px
- **THEN** the navigation occupies its document-flow position below the summary cards and does not overlay the viewport edge

#### Scenario: Mobile navigation placement
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation remains visible at the bottom of the viewport while the user scrolls

#### Scenario: Mobile content clearance
- **WHEN** the mobile navigation is fixed
- **THEN** page content has enough bottom clearance for the navigation and its safe-area inset so the navigation does not obscure reachable content

### Requirement: Safe-area and visual treatment
The mobile navigation SHALL use a solid background and SHALL account for devices with a bottom safe-area inset.

#### Scenario: Device has a bottom safe area
- **WHEN** the browser reports a non-zero `env(safe-area-inset-bottom)` value
- **THEN** the navigation includes that inset in its bottom spacing without moving or clipping the destination labels

#### Scenario: Navigation remains visually distinct
- **WHEN** destination content is scrolled behind the fixed mobile navigation
- **THEN** the solid navigation background keeps labels and icons legible and visually separates the navigation from content

### Requirement: Active destination accessibility
The navigation SHALL expose the active destination to keyboard and assistive-technology users.

#### Scenario: Active destination is announced
- **WHEN** a destination is active
- **THEN** its navigation button exposes the active state through `aria-current="page"` and a visible selected style

#### Scenario: Navigation is keyboard operable
- **WHEN** a keyboard user focuses a destination item and activates it
- **THEN** the same destination switching behavior occurs as for pointer activation

### Requirement: Destination persistence
The app SHALL persist the selected destination locally and SHALL restore it after a page reload without changing the browser URL or history.

#### Scenario: Selected destination survives reload
- **WHEN** a user selects Compare or Explore and reloads the page
- **THEN** the selected destination is restored after initialization

#### Scenario: No destination has been stored
- **WHEN** the app loads without a stored destination
- **THEN** Portfolio is selected by default

#### Scenario: Stored destination is invalid
- **WHEN** the app loads with a stored key that is not present in the current navigation registry
- **THEN** Portfolio is selected and the invalid key is not activated

#### Scenario: Navigation does not create browser history
- **WHEN** a user switches between destinations
- **THEN** the browser URL and history remain unchanged

### Requirement: Empty destinations remain available
The navigation SHALL keep Compare and Explore available when the portfolio contains no positions.

#### Scenario: Empty portfolio navigation
- **WHEN** the portfolio contains no positions and the user selects Compare or Explore
- **THEN** the selected panel is displayed with its existing empty state instead of being disabled or removed

### Requirement: Extensible destination model
The navigation SHALL support adding future destinations through the same destination definition and rendering path without changing the navigation interaction contract.

#### Scenario: Future destination is registered
- **WHEN** a valid future destination is added to the navigation registry and a matching panel is provided
- **THEN** it is rendered with the same icon, label, active-state, accessibility, and switching behavior as the initial destinations

#### Scenario: Badges remain optional
- **WHEN** a future destination definition does not provide a badge
- **THEN** the navigation renders the destination without reserving or displaying a badge
