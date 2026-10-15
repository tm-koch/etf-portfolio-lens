# Spec Delta

## ADDED Requirements

### Requirement: Language selector labels adapt to viewport
The language selector SHALL show full localized language names for all choices while expanded at every viewport width. When collapsed, it SHALL show the selected language's full localized name on wide viewports and its `EN`, `DE`, or `PL` abbreviation on smartphone-width viewports. It SHALL NOT show a visible arrow or caret.

#### Scenario: Expanded selector shows full names at every width
- **WHEN** the language selector is expanded on a wide or smartphone-width viewport
- **THEN** each choice shows its full localized language name

#### Scenario: Collapsed selector shows the selected name on a wide viewport
- **WHEN** the language selector is collapsed on a viewport wider than 760px
- **THEN** it shows the selected language's full localized name

#### Scenario: Collapsed selector shows an abbreviation on a smartphone viewport
- **WHEN** the language selector is collapsed on a viewport 760px wide or narrower
- **THEN** it shows `EN`, `DE`, or `PL` for the selected language

#### Scenario: Selector has no visible arrow
- **WHEN** the language selector is rendered in either collapsed or expanded state
- **THEN** no visible arrow or caret is shown