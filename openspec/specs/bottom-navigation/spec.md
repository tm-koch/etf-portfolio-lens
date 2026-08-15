# bottom-navigation Specification

## Purpose
TBD - created by archiving change mobile-bottom-navigation. Update Purpose after archive.
## Requirements
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
The navigation SHALL remain in normal document flow on desktop widths and SHALL be fixed to the viewport bottom at widths up to 760px. At mobile widths, the navigation SHALL span the full viewport width, SHALL have no rounded corners, and SHALL maintain stable total geometry while the browser visual viewport changes during scrolling. Firefox Android SHALL render the navigation as a simple opaque fixed element without special compositor or containment hints.

#### Scenario: Desktop navigation placement
- **WHEN** the viewport width is greater than 760px
- **THEN** the navigation occupies its document-flow position below the summary cards and does not overlay the viewport edge

#### Scenario: Mobile navigation placement
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation remains visible at the bottom of the viewport while the user scrolls

#### Scenario: Mobile navigation spans the viewport
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation reaches the viewport's left and right edges without a horizontal inset

#### Scenario: Mobile navigation has rectangular geometry
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation has no rounded corners

#### Scenario: Mobile navigation geometry remains stable
- **WHEN** the browser visual viewport height changes during mobile scrolling
- **THEN** the navigation's internal icon-and-label row height and total navigation height do not change because of content-driven sizing

#### Scenario: Mobile content clearance
- **WHEN** the mobile navigation is fixed
- **THEN** page content has enough bottom clearance for the stable navigation footprint and its safe-area inset so the navigation does not obscure reachable content

### Requirement: Safe-area and visual treatment
The mobile navigation SHALL use a solid background, SHALL use a restrained visual boundary without a heavy shadow, SHALL reserve a stable safe-area region without changing the icon-and-label row geometry, and SHALL display a small static shadow above the navigation on mobile widths. Firefox Android SHALL not include a dynamically changing `env(safe-area-inset-bottom)` value in the navigation footprint.

#### Scenario: WebKit mobile device has a bottom safe area
- **WHEN** a WebKit mobile browser reports a non-zero `env(safe-area-inset-bottom)` value
- **THEN** the navigation includes that stable inset in its bottom spacing without moving or clipping the destination labels

#### Scenario: Navigation remains visually distinct
- **WHEN** destination content is scrolled behind the fixed mobile navigation
- **THEN** the solid navigation background, subtle top border, and small static top shadow keep labels and icons legible and visually separate the navigation from content

#### Scenario: Mobile shadow is restrained
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation uses a static upward shadow equivalent to `0 -2px 8px rgba(22, 34, 58, 0.10)` and does not use the former heavy drop shadow

#### Scenario: Desktop shadow remains unchanged
- **WHEN** the viewport width is greater than 760px
- **THEN** the mobile-specific top shadow does not alter the desktop navigation styling

#### Scenario: Shadow does not affect geometry
- **WHEN** the mobile navigation is rendered or the browser toolbar changes state
- **THEN** the shadow does not change the navigation height, safe-area spacing, icon row height, or page content clearance

#### Scenario: Shadow is not animated
- **WHEN** the user scrolls or switches navigation destinations
- **THEN** the shadow remains static and no shadow transition or animation runs

### Requirement: Active destination accessibility
The navigation SHALL expose the active destination to keyboard and assistive-technology users. On mobile widths, the active destination SHALL use a transparent background with both its icon and label rendered in the accent blue.

#### Scenario: Active destination is announced
- **WHEN** a destination is active
- **THEN** its navigation button exposes the active state through `aria-current="page"` and a visible selected style

#### Scenario: Active mobile destination uses blue content
- **WHEN** a destination is active and the viewport width is 760px or less
- **THEN** its icon and label use the accent blue and its button does not use a blue filled background

#### Scenario: Inactive mobile destinations remain muted
- **WHEN** a destination is inactive and the viewport width is 760px or less
- **THEN** its icon and label retain the muted navigation color

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

