# Spec Delta

## ADDED Requirements

### Requirement: Top utility controls share an outer height
The app-level utility area SHALL render the language, color-mode, report-export, and any visible PWA install controls with equal outer border-box heights and aligned top and bottom edges at desktop and mobile viewport widths.

#### Scenario: Desktop utility controls align
- **WHEN** the viewport is wider than 760px and the utility controls are rendered
- **THEN** the language, color-mode, report-export, and any visible install button boxes have equal heights and aligned top and bottom edges

#### Scenario: Mobile utility controls align
- **WHEN** the viewport is 760px wide or narrower and the utility controls are rendered
- **THEN** the language, color-mode, report-export, and any visible install button boxes have equal heights and aligned top and bottom edges
