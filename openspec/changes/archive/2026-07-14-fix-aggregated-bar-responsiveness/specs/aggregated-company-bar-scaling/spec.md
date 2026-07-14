## ADDED Requirements

### Requirement: Responsive company bar scaling
The aggregated top-company bar visualization SHALL scale each company row's full bar length to fit the available width of its container whenever the view is resized or the available layout width changes. The rendered bar SHALL remain fully contained within the visible frame and preserve the existing internal stacked-segment proportions.

#### Scenario: Window resize updates bar length
- **WHEN** the user resizes the window or the aggregated container width changes
- **THEN** each company bar SHALL be re-laid out to fit the new width without overflowing the frame
- **AND** the internal stacked segments SHALL remain proportional to the company total
