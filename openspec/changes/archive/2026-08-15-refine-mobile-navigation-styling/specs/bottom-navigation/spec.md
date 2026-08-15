## MODIFIED Requirements

### Requirement: Responsive navigation placement
The navigation SHALL remain in normal document flow on desktop widths and SHALL be fixed to the viewport bottom at widths up to 760px. At mobile widths, the navigation SHALL span the full viewport width and SHALL have no rounded corners.

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

#### Scenario: Mobile content clearance
- **WHEN** the mobile navigation is fixed
- **THEN** page content has enough bottom clearance for the navigation and its safe-area inset so the navigation does not obscure reachable content

### Requirement: Safe-area and visual treatment
The mobile navigation SHALL use a solid background, SHALL account for devices with a bottom safe-area inset, and SHALL use a restrained visual boundary without a heavy shadow.

#### Scenario: Device has a bottom safe area
- **WHEN** the browser reports a non-zero `env(safe-area-inset-bottom)` value
- **THEN** the navigation includes that inset in its bottom spacing without moving or clipping the destination labels

#### Scenario: Navigation remains visually distinct
- **WHEN** destination content is scrolled behind the fixed mobile navigation
- **THEN** the solid navigation background and a subtle top border keep labels and icons legible and visually separate the navigation from content

#### Scenario: Mobile shadow is restrained
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation does not use the existing heavy drop shadow

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
