## ADDED Requirements

### Requirement: Three color-mode preferences

The web application SHALL provide exactly three color-mode preferences: `Bright`, `Automatic`, and `Dark`.

#### Scenario: User opens the color-mode control

- **WHEN** the user opens the color-mode control
- **THEN** the application presents Bright, Automatic, and Dark as distinct selectable choices

#### Scenario: User selects an explicit mode

- **WHEN** the user selects Bright or Dark
- **THEN** the application applies the corresponding appearance immediately and marks that choice as selected

### Requirement: Automatic mode follows the system preference

The application SHALL make Automatic the default preference and SHALL resolve it from `prefers-color-scheme`.

#### Scenario: No stored preference exists

- **WHEN** the application loads without a valid stored color-mode preference
- **THEN** the selected preference is Automatic and the effective appearance follows the browser or operating system color preference

#### Scenario: System preference changes in Automatic mode

- **WHEN** the browser or operating system preference changes while Automatic is selected
- **THEN** the effective appearance and theme-sensitive charts update without requiring a page reload

#### Scenario: Explicit mode ignores system changes

- **WHEN** the browser or operating system preference changes while Bright or Dark is selected
- **THEN** the application keeps the explicitly selected appearance

### Requirement: Persistent local preference

The application SHALL persist the selected color-mode preference in browser `localStorage` using a dedicated versioned key and SHALL restore it on later loads.

#### Scenario: Preference survives reload

- **WHEN** a user selects a color mode and reloads the page
- **THEN** the application restores the selected mode and its corresponding appearance

#### Scenario: Stored value is missing or invalid

- **WHEN** the stored color-mode value is missing, malformed, or unsupported
- **THEN** the application ignores it and uses Automatic

#### Scenario: Browser storage is unavailable

- **WHEN** browser storage cannot be read or written
- **THEN** the application remains usable, applies the current in-memory selection, and does not fail to start

### Requirement: Complete theme coverage

The application SHALL apply the effective color mode consistently to all user-facing visual elements, including page backgrounds, navigation, panels, cards, dialogs, text, borders, shadows, forms, tables, badges, warnings, empty states, hover states, focus states, and responsive mobile navigation.

#### Scenario: Dark mode renders all primary surfaces

- **WHEN** Dark is active
- **THEN** the page, navigation, panels, cards, dialog, inputs, tables, and mobile navigation use dark-theme colors with readable text and borders

#### Scenario: Bright mode preserves the existing appearance

- **WHEN** Bright is active
- **THEN** the application uses the existing bright visual scheme without dark-theme overrides

### Requirement: Theme-aware charts

Comparison charts and their legends SHALL remain legible in both effective appearances, and SHALL refresh theme-sensitive presentation colors when the effective appearance changes.

#### Scenario: Chart renders in dark mode

- **WHEN** a comparison chart is rendered while Dark is active
- **THEN** chart borders, labels, tooltips, and legends have sufficient contrast against dark surfaces

#### Scenario: Chart updates after mode change

- **WHEN** the effective appearance changes while comparison data exists
- **THEN** visible and subsequently displayed comparison charts use colors for the new effective appearance

### Requirement: Accessible compact color-mode control

The color-mode control SHALL be keyboard accessible, expose its current state to assistive technology, and provide recognizable sun, monitor, and moon icon states for Bright, Automatic, and Dark.

#### Scenario: Control is navigated by keyboard

- **WHEN** a keyboard user focuses and operates the color-mode control
- **THEN** the user can open it, choose any of the three modes, and observe a visible focus and selected state

#### Scenario: Icon state identifies the preference

- **WHEN** the selected preference changes
- **THEN** the control updates its icon and accessible name to identify Bright, Automatic, or Dark
