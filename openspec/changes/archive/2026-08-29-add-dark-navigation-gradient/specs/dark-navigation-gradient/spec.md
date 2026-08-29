## ADDED Requirements

### Requirement: Dark navigation is visually separated from the frame

The primary navigation SHALL expose a subtle dark-mode gradient edge that begins at the sticky navigation separator and visibly separates the navigation surface from the surrounding dark page frame while preserving readable navigation content.

#### Scenario: Dark mode displays navigation separation

- **WHEN** the application is rendered with Dark as the effective color mode
- **THEN** a top-to-bottom gradient with distinguishable dark surface values begins at the navigation separator while the navigation surface remains flat

#### Scenario: Bright mode remains unchanged

- **WHEN** the application is rendered with Bright as the effective color mode
- **THEN** the primary navigation retains its existing bright visual treatment and active-tab styling, with no change to the navigation surface

#### Scenario: Responsive navigation preserves the gradient

- **WHEN** the application is rendered at a mobile-sized viewport in Dark mode
- **THEN** the primary navigation remains usable and retains the dark gradient edge above its separator without obscuring tab labels or icons
