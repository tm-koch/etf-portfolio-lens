# global-color-mode-selector Specification

## Purpose
TBD - created by archiving change global-color-mode-selector. Update Purpose after archive.
## Requirements
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

### Requirement: Color-mode preference behavior
The global color-mode control SHALL preserve the existing preference semantics: the selected mode SHALL persist in local browser storage, Automatic SHALL follow the system color-scheme preference, and theme-dependent charts SHALL update after a mode change.

#### Scenario: Preference survives reload
- **WHEN** the user selects a color mode and reloads the application
- **THEN** the selected preference is restored before the application is displayed

#### Scenario: Automatic follows the system preference
- **WHEN** Automatic is selected and the system color-scheme preference changes
- **THEN** the effective application theme updates without changing the stored Automatic preference

#### Scenario: Charts reflect the effective theme
- **WHEN** the effective color mode changes
- **THEN** rendered comparison charts refresh using the colors for the new effective theme

### Requirement: Accessible responsive control
The color-mode control SHALL be keyboard operable, expose menu and radio-item semantics, and remain usable at mobile widths without entering the fixed bottom-navigation footprint. At viewport widths of 760px or less, the trigger SHALL display only the current mode's icon while retaining a descriptive accessible name and tooltip; the expanded menu SHALL display Bright, Automatic, and Dark choices with both icons and visible text. At viewport widths greater than 760px, the trigger SHALL retain its existing icon-and-text presentation.

#### Scenario: Keyboard user opens the selector
- **WHEN** a keyboard user focuses and activates the color-mode button
- **THEN** the menu opens, exposes the current option as checked, and places focus on the selected option

#### Scenario: Keyboard user chooses an option
- **WHEN** a keyboard user activates a color-mode option
- **THEN** the selected mode is applied and the menu closes without losing the ability to reach the primary navigation

#### Scenario: Compact mobile trigger is icon-only
- **WHEN** the viewport width is 760px or less
- **THEN** the color-mode trigger displays the current mode's icon without visible mode text, while its accessible name and tooltip identify the current mode

#### Scenario: Compact mobile menu retains labeled alternatives
- **WHEN** the user opens the color-mode menu at a viewport width of 760px or less
- **THEN** Bright, Automatic, and Dark options each display an icon and visible text label

#### Scenario: Wider trigger retains its label
- **WHEN** the viewport width is greater than 760px
- **THEN** the color-mode trigger displays both the current mode's icon and visible text label

#### Scenario: Mobile selector remains separate from bottom navigation
- **WHEN** the viewport width is 760px or less
- **THEN** the color-mode control remains in the top-right utility area and does not overlap or change the geometry of the fixed bottom navigation

