## ADDED Requirements

### Requirement: Global utility remains distinct from destination navigation
The application SHALL keep the global color-mode control visually and structurally separate from the four primary destination buttons while placing it in the app-level top-right utility area without creating a separate utility frame.

#### Scenario: Desktop utility placement
- **WHEN** the viewport width is greater than 760px
- **THEN** the color-mode control appears at the top right on the active panel title level without changing the order or active-state behavior of Home, Portfolio, Compare, and Explore

#### Scenario: Mobile utility placement
- **WHEN** the viewport width is 760px or less
- **THEN** the color-mode control remains in the top-right utility area while the primary navigation remains fixed at the bottom of the viewport

#### Scenario: Navigation geometry is preserved
- **WHEN** the global color-mode control is rendered at any supported viewport width
- **THEN** the primary navigation's destination buttons, safe-area region, and mobile row height retain their existing geometry
