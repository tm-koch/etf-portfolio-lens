## ADDED Requirements

### Requirement: Include live-data publication inputs in validation
The publication process SHALL validate the live-data artifact as part of the same deployment input set used to generate build metadata and runtime cache behavior, while quote refreshes SHALL remain runtime data and SHALL NOT force a shell cache generation change by themselves.

#### Scenario: Frontend shell changes with live-data support
- **WHEN** application code or service-worker handling for live data changes
- **THEN** the published cache generation changes and the deployment is validated as one coherent shell generation

#### Scenario: Only quote values change
- **WHEN** a valid live-price JSON artifact changes but shell assets do not
- **THEN** the artifact is refreshed through runtime caching without requiring an artificial shell generation change
