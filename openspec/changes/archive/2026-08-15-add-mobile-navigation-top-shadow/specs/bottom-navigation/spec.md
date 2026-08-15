## MODIFIED Requirements

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
