# bottom-navigation Specification

## Purpose
TBD - created by archiving change mobile-bottom-navigation. Update Purpose after archive.
## Requirements
### Requirement: Primary destination navigation
The web app SHALL provide a primary navigation containing the destinations Home, Portfolio, Compare, and Explore in that order.

#### Scenario: Navigation displays the initial destinations
- **WHEN** the application loads successfully
- **THEN** one navigation control contains exactly the Home, Portfolio, Compare, and Explore destinations in that order

#### Scenario: Selecting a destination shows its content
- **WHEN** a user activates a destination navigation item
- **THEN** the corresponding content panel becomes active and the other destination panels become inactive

#### Scenario: Explore maps to the aggregated panel
- **WHEN** a user activates Explore
- **THEN** the panel using the internal `aggregated` destination key becomes active

### Requirement: Icon and label presentation
Each destination navigation item SHALL display a consistent Lucide icon and its visible text label, with the icon positioned above the label. Home SHALL use a distinct house icon suitable for an overview destination.

#### Scenario: Destination has an understandable visual identity
- **WHEN** the navigation is rendered
- **THEN** Home, Portfolio, Compare, and Explore each display a distinct suitable icon above its label

#### Scenario: Icon rendering is unavailable
- **WHEN** the icon asset cannot be loaded or initialized
- **THEN** the destination labels remain visible and the navigation remains operable

### Requirement: Responsive navigation placement
The navigation SHALL be presented before destination content in the document order. At viewport widths greater than 760px, it SHALL occupy a persistent app-bar position above the active destination content, remaining available at the top while the user scrolls. At viewport widths up to 760px, it SHALL be fixed to the viewport bottom. At mobile widths, the navigation SHALL span the full viewport width, SHALL have no rounded corners, and SHALL maintain stable total geometry while the browser visual viewport changes during scrolling. Firefox Android SHALL render the navigation as a simple opaque fixed element without special compositor or containment hints.

#### Scenario: Desktop navigation appears before content
- **WHEN** the application loads at a viewport width greater than 760px
- **THEN** the primary navigation appears before the active destination panel in document and visual order

#### Scenario: Desktop navigation remains available while scrolling
- **WHEN** a user scrolls the active destination at a viewport width greater than 760px
- **THEN** the primary navigation remains available at the top as a persistent app bar

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
- **THEN** the solid navigation background, subtle top border, and small static top shadow keep labels and icons legible and visually separate from content

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
The app SHALL persist the selected destination locally and SHALL restore it after a page reload without changing the browser URL or history. When no valid destination is stored, Home SHALL be selected by default.

#### Scenario: Selected destination survives reload
- **WHEN** a user selects Home, Portfolio, Compare, or Explore and reloads the page
- **THEN** the selected destination is restored after initialization

#### Scenario: No destination has been stored
- **WHEN** the app loads without a stored destination
- **THEN** Home is selected by default

#### Scenario: Stored destination is invalid
- **WHEN** the app loads with a stored key that is not present in the current navigation registry
- **THEN** Home is selected and the invalid key is not activated

#### Scenario: Navigation does not create browser history
- **WHEN** a user switches between Home, Portfolio, Compare, and Explore
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

### Requirement: Enlarged mobile navigation geometry
At viewport widths up to 760px, the mobile navigation SHALL use a stable 64px icon-and-label row and each destination button SHALL retain a target height of at least 44px. Existing mobile icon size and spacing SHALL remain unchanged.

#### Scenario: Enlarged navigation row
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation row and destination buttons use a 64px height while the icons remain 18px square

#### Scenario: Enlarged geometry remains stable
- **WHEN** the browser visual viewport changes during mobile scrolling
- **THEN** the navigation row and destination button height remain 64px and do not resize based on content

#### Scenario: Mobile content clearance follows the enlarged row
- **WHEN** the mobile navigation is fixed
- **THEN** page content has bottom clearance for the 64px row, its boundary, and any safe-area inset

### Requirement: Slightly larger mobile navigation labels
At viewport widths up to 760px, navigation labels SHALL use a 0.8rem font size in both active and inactive states. Existing active/inactive colors and font-weight distinctions SHALL remain unchanged.

#### Scenario: Mobile labels are slightly larger
- **WHEN** the viewport width is 760px or less
- **THEN** Portfolio, Compare, and Explore labels use a 0.8rem font size and remain on one line at supported mobile widths

#### Scenario: Active and inactive emphasis remains distinct
- **WHEN** a destination is active or inactive at a mobile viewport
- **THEN** the active label remains bold and accent blue while the inactive label remains regular and muted

#### Scenario: Desktop navigation remains unchanged
- **WHEN** the viewport width is greater than 760px
- **THEN** the mobile row and label-size changes do not alter desktop navigation geometry or typography

### Requirement: Navigation is independent from the content frame
The application SHALL render the primary navigation outside the constrained destination-content column. The desktop app bar SHALL be able to span the viewport independently, while destination content SHALL retain a readable maximum width.

#### Scenario: Desktop app bar is not enclosed by the content column
- **WHEN** the application renders at a desktop viewport width
- **THEN** the navigation is visually separate from the centered destination-content column and is not enclosed by the column's outer card frame

#### Scenario: Smartphone content uses the available width
- **WHEN** the application renders at a viewport width of 760px or less
- **THEN** the active destination content uses the viewport width without an additional outer page gutter or rounded outer frame

#### Scenario: Destination internals retain readable spacing
- **WHEN** an active destination renders on a smartphone-sized viewport
- **THEN** its content retains internal padding and its nested tables, charts, and grouped sections remain visually distinguishable

