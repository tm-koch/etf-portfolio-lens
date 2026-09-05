## Requirements

### Requirement: Mobile navigation suppresses the native tap overlay

The primary navigation buttons MUST suppress the browser's native tap-highlight overlay so a touch does not briefly replace the application's navigation feedback with a platform-default flash.

#### Scenario: Bright mode navigation tap

- **WHEN** a user touches a bottom-navigation button in Bright mode
- **THEN** the button does not display Chrome's default tap-highlight overlay
- **AND** the navigation background remains visually stable during the gesture

#### Scenario: Dark mode navigation tap

- **WHEN** a user touches a bottom-navigation button in Dark mode
- **THEN** the button does not display a browser-default tap overlay
- **AND** the application's pressed-state treatment remains visible against the dark navigation background

### Requirement: Mobile navigation provides intentional pressed feedback

The primary navigation buttons MUST provide a deliberate pressed-state treatment while a pointer or touch is actively pressing a button, without changing which tab is selected.

#### Scenario: Button is actively pressed

- **WHEN** a user presses a bottom-navigation button
- **THEN** the button exposes the application's defined pressed-state styling
- **AND** the existing selected tab remains the only button with persistent active styling

#### Scenario: Press is canceled

- **WHEN** a user presses a bottom-navigation button and releases or cancels outside the button
- **THEN** the temporary pressed styling is removed
- **AND** no tab change occurs unless the existing click behavior is triggered

### Requirement: Navigation remains keyboard-accessible

The primary navigation buttons MUST retain a visible `:focus-visible` indicator that is distinguishable from both the pressed state and the persistent active state.

#### Scenario: Keyboard focus enters navigation

- **WHEN** a keyboard user tabs to a bottom-navigation button
- **THEN** the focused button displays the navigation focus indicator
- **AND** the focus indicator remains visible regardless of whether the button is active

#### Scenario: Touch activation does not leave a focus ring

- **WHEN** a user activates a bottom-navigation button by touch
- **THEN** the navigation does not show a persistent keyboard-only focus indicator solely because of that touch activation

### Requirement: Existing tab activation semantics remain unchanged

The tap-highlight fix MUST preserve the existing navigation behavior: activating a navigation button synchronously applies the active state, updates `aria-current`, and displays the corresponding panel.

#### Scenario: User selects another tab

- **WHEN** a user activates a navigation button for a different tab
- **THEN** that button becomes the active navigation button during the same interaction
- **AND** its `aria-current` value is set to `page`
- **AND** the corresponding panel is shown
- **AND** the previously active button and panel are cleared
