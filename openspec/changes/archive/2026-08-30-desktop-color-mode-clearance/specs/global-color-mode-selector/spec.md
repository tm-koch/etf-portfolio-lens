## MODIFIED Requirements

### Requirement: Global color-mode selection
The application SHALL expose one globally reachable color-mode control in the app-level top-right utility area, independent of the active destination, with Bright, Automatic, and Dark choices. The control SHALL not introduce a separate card or utility frame.

#### Scenario: Selector is available on every destination
- **WHEN** the user views Home, Portfolio, Compare, or Explore
- **THEN** the same color-mode control is available in the app-level top-right utility area

#### Scenario: Current mode is visible
- **WHEN** the color-mode control is rendered
- **THEN** it identifies the current preference with an appropriate icon and accessible name

#### Scenario: Control aligns with the active panel title
- **WHEN** a destination panel is active
- **THEN** the control appears at the top right on the visual level of that panel's primary title row without adding a separate utility frame

#### Scenario: User selects a mode
- **WHEN** the user chooses Bright, Automatic, or Dark
- **THEN** the application applies that preference immediately and updates the control's current-state indication

## ADDED Requirements

### Requirement: Desktop secondary content clears the color-mode control
At viewport widths greater than 760px, secondary content positioned in the upper-right area of the Home, Portfolio, Compare, and Explore panels SHALL begin below the global color-mode control, with enough vertical spacing that the regions do not overlap. This spacing SHALL preserve the existing title alignment and SHALL NOT apply to the compact mobile layout.

#### Scenario: Home metadata clears the selector
- **WHEN** Home is active at a viewport width greater than 760px
- **THEN** the hero metadata and status content begins below the color-mode control with visible clearance and remains readable without overlap

#### Scenario: Portfolio persistence note clears the selector
- **WHEN** Portfolio is active at a viewport width greater than 760px
- **THEN** the heading-side persistence note begins below the color-mode control with visible clearance and remains readable without overlap

#### Scenario: Compare explanatory text clears the selector
- **WHEN** Compare is active at a viewport width greater than 760px
- **THEN** the heading-side explanatory text begins below the color-mode control with visible clearance and remains readable without overlap

#### Scenario: Explore explanatory text clears the selector
- **WHEN** Explore is active at a viewport width greater than 760px
- **THEN** the heading-side explanatory text begins below the color-mode control with visible clearance and remains readable without overlap

#### Scenario: Desktop title alignment is preserved
- **WHEN** Home, Portfolio, Compare, or Explore is active at a viewport width greater than 760px
- **THEN** the primary title remains aligned to the existing title position while only the affected secondary content is spaced downward

#### Scenario: Mobile layout is unchanged
- **WHEN** Home, Portfolio, Compare, or Explore is active at a viewport width of 760px or less
- **THEN** the compact color-mode trigger, panel content flow, and fixed bottom navigation retain their existing geometry without the desktop clearance rule

