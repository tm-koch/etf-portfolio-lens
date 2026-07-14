## ADDED Requirements

### Requirement: Preserve a source name for unresolved holdings
The system MUST populate `security.name` with the source-provided security label when a holding cannot be fully enriched and no canonical security name is available.

#### Scenario: Unresolved holding keeps source label
- **WHEN** a holding remains unmatched after all security-master match strategies have been attempted
- **AND** the source row contains a non-empty security label
- **THEN** the system MUST set `security.name` to that source label in the normalized output

#### Scenario: Missing source label stays null
- **WHEN** a holding remains unmatched after all security-master match strategies have been attempted
- **AND** the source row does not provide any usable security label
- **THEN** the system MUST leave `security.name` as `null`

### Requirement: Do not override canonical names for matched holdings
The system MUST continue to use the canonical security-master name whenever a holding is matched successfully.

#### Scenario: Matched holding uses canonical name
- **WHEN** a holding is matched by ISIN, ticker-plus-exchange, ticker-only fallback, or alias matching
- **THEN** the system MUST set `security.name` from the matched security-master record
- **AND** the source-provided label MUST NOT replace the canonical name

### Requirement: Preserve unresolved status and diagnostics with fallback names
The system MUST preserve unresolved match status and diagnostics even when a source name fallback is used.

#### Scenario: Fallback name does not imply successful enrichment
- **WHEN** a holding uses a source-provided fallback name because enrichment failed
- **THEN** the system MUST keep the holding marked unresolved
- **AND** the system MUST retain missing-element diagnostics and warning output
