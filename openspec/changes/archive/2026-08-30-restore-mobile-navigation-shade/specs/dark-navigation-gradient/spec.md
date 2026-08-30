## ADDED Requirements

### Requirement: Dark navigation is visually separated from the frame
The mobile navigation SHALL expose a subtle 9px Dark-mode gradient edge above its separator, transitioning from a lighter dark-slate tone at the navigation border to transparency over the dark frame while preserving readable navigation content. Bright mode SHALL retain its flat mobile navigation treatment.

#### Scenario: Dark mode displays a mobile navigation edge
- **WHEN** the application is rendered with Dark as the effective color mode at a viewport width of 760px or less
- **THEN** a static 9px gradient begins with a lighter dark-slate tone at the navigation border and resolves to transparency above the separator

#### Scenario: Bright mode remains flat
- **WHEN** the application is rendered with Bright as the effective color mode at a viewport width of 760px or less
- **THEN** the mobile navigation does not add the Dark-mode gradient edge

#### Scenario: Edge does not obscure navigation content
- **WHEN** the Dark-mode mobile edge is rendered
- **THEN** it remains outside the navigation row and does not cover tab labels or icons
