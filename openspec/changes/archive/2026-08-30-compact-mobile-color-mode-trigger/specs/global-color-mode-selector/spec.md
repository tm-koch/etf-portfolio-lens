## MODIFIED Requirements

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