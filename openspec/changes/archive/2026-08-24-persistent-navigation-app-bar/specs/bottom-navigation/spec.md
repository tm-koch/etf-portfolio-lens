## MODIFIED Requirements

### Requirement: Responsive navigation placement
The navigation SHALL be presented before destination content in the document order. At viewport widths greater than 760px, it SHALL occupy a persistent app-bar position above the active destination content, remaining available at the top while the user scrolls. At viewport widths up to 760px, it SHALL be fixed to the viewport bottom. At mobile widths, the navigation SHALL span the full viewport width, SHALL have no rounded corners, and SHALL maintain stable total geometry while the browser visual viewport changes during scrolling. Firefox Android SHALL render the navigation as a simple opaque fixed element without special compositor or containment hints.

#### Scenario: Desktop navigation appears before content
- **WHEN** the application loads at a viewport width greater than 760px
- **THEN** the primary navigation appears before the active destination panel in document and visual order

#### Scenario: Desktop navigation remains available while scrolling
- **WHEN** a user scrolls the active destination at a viewport width greater than 760px
- **THEN** the primary navigation remains available at the top as a persistent app bar

#### Scenario: Mobile navigation placement
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation remains visible at the bottom of the viewport while the user scrolls

#### Scenario: Mobile navigation spans the viewport
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation reaches the viewport's left and right edges without a horizontal inset

#### Scenario: Mobile navigation has rectangular geometry
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation has no rounded corners

#### Scenario: Mobile navigation geometry remains stable
- **WHEN** the browser visual viewport height changes during mobile scrolling
- **THEN** the navigation's internal icon-and-label row height and total navigation height do not change because of content-driven sizing

#### Scenario: Mobile content clearance
- **WHEN** the mobile navigation is fixed
- **THEN** page content has enough bottom clearance for the stable navigation footprint and its safe-area inset so the navigation does not obscure reachable content

## ADDED Requirements

### Requirement: Navigation is independent from the content frame
The application SHALL render the primary navigation outside the constrained destination-content column. The desktop app bar SHALL be able to span the viewport independently, while destination content SHALL retain a readable maximum width.

#### Scenario: Desktop app bar is not enclosed by the content column
- **WHEN** the application renders at a desktop viewport width
- **THEN** the navigation is visually separate from the centered destination-content column and is not enclosed by the column's outer card frame

#### Scenario: Smartphone content uses the available width
- **WHEN** the application renders at a viewport width of 760px or less
- **THEN** the active destination content uses the viewport width without an additional outer page gutter or rounded outer frame

#### Scenario: Destination internals retain readable spacing
- **WHEN** an active destination renders on a smartphone-sized viewport
- **THEN** its content retains internal padding and its nested tables, charts, and grouped sections remain visually distinguishable
