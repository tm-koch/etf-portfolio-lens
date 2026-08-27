## ADDED Requirements

### Requirement: Explore warning surface

When compact Explore preview mode is enabled, the application SHALL render the compact holdings presentation without a warnings panel in the Explore `/aggregated` tab. When compact preview mode is disabled, the standard aggregated Explore presentation SHALL also omit the warnings panel. Current-selection warnings SHALL remain available in the About this build dialog.

#### Scenario: Compact preview has no Explore warnings panel
- **WHEN** compact Explore preview mode is enabled and the user opens the `/aggregated` tab
- **THEN** the tab SHALL render the compact holdings presentation and SHALL NOT render an Explore warnings panel at the bottom

#### Scenario: Standard Explore has no warnings panel
- **WHEN** compact Explore preview mode is disabled and the user opens the `/aggregated` tab
- **THEN** the tab SHALL render the standard aggregated presentation and SHALL NOT render an Explore warnings panel at the bottom

#### Scenario: Build dialog retains warnings
- **WHEN** the user opens About this build
- **THEN** the dialog SHALL continue to render current-selection warnings in its existing warnings section
