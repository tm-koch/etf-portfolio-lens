# Spec Delta

## ADDED Requirements

### Requirement: Enter whole share quantities

In shares mode, the Portfolio tab SHALL accept only finite, non-negative integer values when a user commits a manual share-count edit. Fractional edits SHALL be rejected and the previous committed value restored; the application SHALL NOT round fractional input. This validation SHALL NOT alter existing saved or imported values unless the user edits that position.

#### Scenario: Commit a whole share count
- **WHEN** a user enters a finite non-negative integer share count in shares mode
- **THEN** the application persists the value and updates the selected-position analysis

#### Scenario: Reject a fractional share edit
- **WHEN** a user attempts to commit a fractional share count in shares mode
- **THEN** the application rejects the edit, restores the previous committed value, and does not round or persist the fractional value

#### Scenario: Preserve existing fractional stored values
- **WHEN** a saved or imported shares-based portfolio contains a fractional share count and the user has not edited that position
- **THEN** loading or rendering the portfolio does not coerce or replace that stored value

### Requirement: Widen position entry fields

The numeric position-entry field SHALL be approximately 15% wider than its current 84px width, targeting about 97px in both shares and relative allocation modes, while remaining within the available layout on desktop and mobile.

#### Scenario: Position entry width across modes and viewports
- **WHEN** the Portfolio tab displays a Shares or Allocation input on desktop or mobile
- **THEN** the input is approximately 97px wide and does not cause horizontal overflow of the selected positions layout
