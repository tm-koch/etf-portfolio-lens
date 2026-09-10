## ADDED Requirements

### Requirement: Publish live-data provenance safely
The provenance manifest SHALL include the live-data generation timestamp and aggregate status such as complete, unavailable, or fallback-capable, without including provider identities, source URLs, credentials, or raw responses.

#### Scenario: Complete live data is published
- **WHEN** a validated live-data artifact is included in a Pages deployment
- **THEN** build details identify its generation timestamp and complete status

#### Scenario: Live data is unavailable
- **WHEN** the deployment uses an earlier valid artifact because the update workflow failed
- **THEN** build details retain the earlier artifact timestamp and do not claim that a new live update succeeded
