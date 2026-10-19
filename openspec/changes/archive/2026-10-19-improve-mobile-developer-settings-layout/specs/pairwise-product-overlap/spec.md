# Spec Delta

## MODIFIED Requirements

### Requirement: Configure near-identical pair threshold
Developer settings SHALL provide a persisted near-identical overlap threshold, defaulting to 90%, and accept only finite values from 0% through 100%. A pair SHALL be marked near-identical when its overlap is at or above the configured threshold. The threshold input SHALL match the width of one redundancy threshold input at every viewport width, and the separator before the near-identical threshold section SHALL span the full settings content width.

#### Scenario: Default threshold marks a high-overlap pair
- **WHEN** no valid threshold preference has been saved and a pair overlap is at least 90%
- **THEN** the pair SHALL be marked near-identical

#### Scenario: Threshold changes update selected pairs
- **WHEN** the developer changes the valid threshold or the selected portfolio ETFs change
- **THEN** near-identical heatmap marks SHALL update to reflect the current value and selection

#### Scenario: Invalid threshold is entered
- **WHEN** the configured threshold is non-finite or outside 0% to 100%
- **THEN** the invalid value SHALL NOT be applied and the last valid value or default SHALL remain active

#### Scenario: Near-identical control matches redundancy field width
- **WHEN** the developer settings are viewed at any viewport width
- **THEN** the near-identical threshold input SHALL have the same width as one redundancy threshold input

#### Scenario: Near-identical section divider spans the settings width
- **WHEN** the developer settings are displayed
- **THEN** the separator before the near-identical threshold section SHALL span the full available settings content width
