## MODIFIED Requirements

### Requirement: Reduced outer page spacing

The web application SHALL use approximately one-third less spacing at the outer page shell on desktop and tablet-sized viewports, including the gap between top-level sections and the horizontal page gutter around constrained content. The application SHALL retain its centered maximum content width and SHALL NOT reduce internal component spacing as part of this capability.

#### Scenario: Desktop shell exposes more active area

- **WHEN** the application is displayed on a desktop-sized viewport
- **THEN** the top-level section gap and content-column outer gutter SHALL be approximately one third smaller than the previous shell spacing while the content remains centered within the existing maximum width

#### Scenario: Tablet shell remains usable

- **WHEN** the application is displayed on a tablet-sized viewport
- **THEN** the reduced outer spacing SHALL expose more active content area without causing cards, tables, charts, or controls to overlap or clip

#### Scenario: Internal component rhythm is preserved

- **WHEN** the reduced shell spacing is applied
- **THEN** card padding, table cell spacing, chart spacing, typography, and control hit areas SHALL remain unchanged

### Requirement: Responsive spacing boundaries

The reduced desktop/tablet shell spacing SHALL NOT change the established mobile layout boundaries. Mobile content SHALL remain full width where currently defined, and the fixed bottom navigation SHALL retain its existing row height, safe-area clearance, and usable destination controls.

#### Scenario: Mobile content remains full width

- **WHEN** the application is displayed on a mobile-sized viewport
- **THEN** the destination content SHALL retain its existing full-width behavior without an added outer gutter from the desktop density change

#### Scenario: Mobile navigation clearance remains stable

- **WHEN** the application is displayed on a mobile-sized viewport with the fixed bottom navigation visible
- **THEN** page content SHALL retain clearance for the navigation and the navigation row height, safe-area spacing, and destination hit areas SHALL remain unchanged

### Requirement: Compact portfolio valuation basis control

The portfolio-level and import-dialog valuation basis controls SHALL use a maximum width of 224px, which is 30% narrower than the existing 320px shared control width, while retaining responsive shrink-to-fit behavior.

#### Scenario: Portfolio control is compact on wide layouts

- **WHEN** the selected-positions header is displayed with at least 224px of available inline space
- **THEN** the portfolio-level valuation basis control SHALL be no wider than 224px

#### Scenario: Portfolio control remains usable on narrow layouts

- **WHEN** the selected-positions header has less than 224px of available inline space
- **THEN** the portfolio-level valuation basis control SHALL shrink to fit its container without horizontal overflow

#### Scenario: Import valuation control is compact

- **WHEN** the import review dialog renders its valuation control
- **THEN** that control SHALL use the same maximum width of 224px without changing its labels, options, or behavior
