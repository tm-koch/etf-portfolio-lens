## ADDED Requirements

### Requirement: Enlarged mobile navigation geometry
At viewport widths up to 760px, the mobile navigation SHALL use a stable 64px icon-and-label row and each destination button SHALL retain a target height of at least 44px. Existing mobile icon size and spacing SHALL remain unchanged.

#### Scenario: Enlarged navigation row
- **WHEN** the viewport width is 760px or less
- **THEN** the navigation row and destination buttons use a 64px height while the icons remain 18px square

#### Scenario: Enlarged geometry remains stable
- **WHEN** the browser visual viewport changes during mobile scrolling
- **THEN** the navigation row and destination button height remain 64px and do not resize based on content

#### Scenario: Mobile content clearance follows the enlarged row
- **WHEN** the mobile navigation is fixed
- **THEN** page content has bottom clearance for the 64px row, its boundary, and any safe-area inset

### Requirement: Slightly larger mobile navigation labels
At viewport widths up to 760px, navigation labels SHALL use a 0.8rem font size in both active and inactive states. Existing active/inactive colors and font-weight distinctions SHALL remain unchanged.

#### Scenario: Mobile labels are slightly larger
- **WHEN** the viewport width is 760px or less
- **THEN** Portfolio, Compare, and Explore labels use a 0.8rem font size and remain on one line at supported mobile widths

#### Scenario: Active and inactive emphasis remains distinct
- **WHEN** a destination is active or inactive at a mobile viewport
- **THEN** the active label remains bold and accent blue while the inactive label remains regular and muted

#### Scenario: Desktop navigation remains unchanged
- **WHEN** the viewport width is greater than 760px
- **THEN** the mobile row and label-size changes do not alter desktop navigation geometry or typography
