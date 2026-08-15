## MODIFIED Requirements

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
The mobile navigation SHALL use a solid background, SHALL use a restrained visual boundary without a heavy shadow, and SHALL reserve a stable safe-area region without changing the icon-and-label row geometry. Firefox Android SHALL not include a dynamically changing `env(safe-area-inset-bottom)` value in the navigation footprint.

#### Scenario: WebKit mobile device has a bottom safe area
- **WHEN** a WebKit mobile browser reports a non-zero `env(safe-area-inset-bottom)` value
- **THEN** the navigation includes that stable inset in its bottom spacing without moving or clipping the destination labels

#### Scenario: Navigation remains visually distinct
- **WHEN** destination content is scrolled behind the fixed mobile navigation
- **THEN** the solid navigation background and a subtle top border keep labels and icons legible and visually separate the navigation from content

#### Scenario: Mobile shadow is restrained
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation does not use the existing heavy drop shadow

#### Scenario: Firefox Android toolbar changes state
- **WHEN** Firefox Android changes the browser toolbar state during mobile scrolling
- **THEN** the navigation remains an opaque fixed element without special-layer jitter and with unchanged footprint and icon-to-bottom spacing
