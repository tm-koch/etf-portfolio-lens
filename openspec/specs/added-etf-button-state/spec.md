# added-etf-button-state Specification

## Purpose
TBD - created by archiving change style-added-etf-button. Update Purpose after archive.
## Requirements
### Requirement: Distinguish added ETF catalog buttons

The ETF catalog SHALL expose a dedicated added-state marker on the button for every ETF that is already present in the active portfolio. The button SHALL continue to display `Added` and remain disabled, while ETFs absent from the portfolio SHALL continue to display an actionable `Add` button without the added-state marker.

#### Scenario: Newly added ETF displays status styling
- **WHEN** a user adds an ETF from the catalog
- **THEN** the catalog rerenders that ETF's button with the added-state marker, the label `Added`, and the disabled attribute

#### Scenario: Existing portfolio ETF displays status styling on load
- **WHEN** the application loads a portfolio containing an ETF already present in the catalog
- **THEN** that ETF's catalog button displays the added-state marker, the label `Added`, and the disabled attribute

### Requirement: Render the added state as an outlined blue status

An ETF catalog button with the added-state marker SHALL use a blue border, a white background, and blue text. It SHALL not use the filled blue background used by the actionable `Add` state, and its status styling SHALL remain fully visible rather than being reduced by disabled opacity.

#### Scenario: Added button uses status presentation
- **WHEN** an ETF catalog button has the added-state marker
- **THEN** its computed presentation uses the accent blue for the border and text, white for the background, and full opacity

#### Scenario: Actionable button retains action presentation
- **WHEN** an ETF catalog button does not have the added-state marker
- **THEN** it retains the existing filled accent presentation and remains available to add the ETF

### Requirement: Prevent duplicate ETF additions

The added-state presentation SHALL preserve the existing duplicate-add protection. An ETF already in the active portfolio MUST NOT be added a second time through the catalog button.

#### Scenario: Added button cannot add a duplicate
- **WHEN** a user attempts to activate the catalog control for an ETF already in the active portfolio
- **THEN** the portfolio remains unchanged and contains only the existing position for that ETF

