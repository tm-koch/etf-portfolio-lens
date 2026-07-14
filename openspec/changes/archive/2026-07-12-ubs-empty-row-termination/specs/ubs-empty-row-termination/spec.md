## ADDED Requirements

### Requirement: Stop parsing the UBS holdings table at the first empty row
The system MUST stop reading the UBS holdings table once the first completely empty row in the table is encountered.

#### Scenario: Empty row terminates the holdings table
- **WHEN** the UBS parser reads the CH0130595124 holdings table and encounters a row where all cells are empty
- **THEN** the parser MUST stop collecting holdings rows at that point
- **AND** MUST ignore all following rows in the worksheet

#### Scenario: Disclaimer rows after the empty row are ignored
- **WHEN** rows after the first empty row contain disclaimer or footer text
- **THEN** the parser MUST not include those rows in the parsed holdings output

### Requirement: Preserve holdings before the termination row
The system MUST keep all valid holdings rows that appear before the first empty row.

#### Scenario: Valid holdings remain in output
- **WHEN** the parser encounters valid holdings rows before the first empty row
- **THEN** those rows MUST continue to be parsed into holdings normally
- **AND** the termination rule MUST not remove them
