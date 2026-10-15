# Spec Delta

## ADDED Requirements

### Requirement: Keep valuation controls compact on smartphones

On smartphone-width viewports in shares-based mode, the valuation selector and provenance status SHALL appear directly beneath Entry mode on the same horizontal row. The status SHALL be vertically centered with the selector, and the row SHALL fit the available viewport without a fixed empty vertical spacer or horizontal overflow.

#### Scenario: Valuation selector and status share a row on a phone
- **WHEN** the Portfolio tab displays a shares-based portfolio on a smartphone-width viewport
- **THEN** the valuation selector and provenance status appear directly beneath Entry mode on the same row, with their control surfaces vertically centered and no oversized blank region

#### Scenario: Selector and status fit on a narrow phone
- **WHEN** the selected-positions panel is displayed at a 320px viewport width
- **THEN** the selector uses the available row width beside the provenance status, both remain visible and operable, and the page has no horizontal overflow
