## MODIFIED Requirements

### Requirement: Extensible and fault-tolerant metadata

The provenance manifest SHALL include a versioned or extensible structure for future metadata fields, and failure to load or parse it SHALL not block the core portfolio UI. The About this build surface SHALL render optional metadata without leaving a duplicate horizontal separator when that metadata is absent, and SHALL retain one separator before its bottom current-selection warnings section.

#### Scenario: Optional details are absent
- **WHEN** the About this build surface has no optional details to display
- **THEN** the hidden optional-details section SHALL not occupy layout space or display a separator

#### Scenario: Warnings remain at the bottom
- **WHEN** the About this build surface is rendered
- **THEN** current-selection warnings SHALL appear after the developer settings and SHALL have one separator immediately above the warnings section

#### Scenario: Future metadata is added
- **WHEN** additional provenance or diagnostic fields are added to the manifest
- **THEN** the build-details surface can render them without changing the primary navigation contract

#### Scenario: Manifest is absent locally
- **WHEN** the app runs without a generated provenance manifest
- **THEN** the core portfolio, comparison, and aggregation workflows remain usable and the About surface reports local development or unavailable metadata

#### Scenario: Manifest is malformed
- **WHEN** the provenance manifest cannot be parsed
- **THEN** the app continues loading its portfolio data and reports unavailable build metadata in the About surface
