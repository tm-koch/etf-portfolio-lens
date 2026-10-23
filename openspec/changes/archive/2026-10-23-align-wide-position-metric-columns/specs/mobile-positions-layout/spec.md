# Spec Delta

## ADDED Requirements

### Requirement: Wide position metric columns align across funds
In the wide Selected positions layout, the Price, Value CHF, and Weight metrics SHALL use common left-aligned column positions across all selected position boxes.

#### Scenario: Share-based metric columns align across position boxes
- **WHEN** multiple share-based positions are displayed above the mobile reflow breakpoint
- **THEN** the left edges of the Price, Value CHF, and Weight labels and values SHALL align across all position boxes

#### Scenario: Percentage-only positions retain their metric behavior
- **WHEN** a percentage-only portfolio is displayed in the wide layout
- **THEN** Price and Value CHF SHALL remain omitted and Weight SHALL retain its existing display behavior

#### Scenario: Mobile position reflow is unchanged
- **WHEN** selected positions are displayed at or below the mobile reflow breakpoint
- **THEN** the existing mobile card layout SHALL remain in effect without adopting the wide metric columns
