# build-provenance Specification

## Purpose
Expose source, deployment, and ETF data timestamps through a secondary About/build-details surface and generated publish metadata.
## Requirements
### Requirement: Secondary About build-details access
The web app SHALL provide a secondary `About this build` action in the hero development/status area. The action SHALL remain outside the primary Portfolio, Compare, and Explore navigation and SHALL open an in-page build-details surface without changing browser URL or history.

#### Scenario: About action is discoverable
- **WHEN** the application loads successfully
- **THEN** the hero development/status area contains an accessible secondary action labelled `About this build`

#### Scenario: About action opens build details
- **WHEN** a user activates `About this build`
- **THEN** an in-page build-details surface opens and the primary navigation destinations remain unchanged

#### Scenario: About surface is keyboard accessible
- **WHEN** a keyboard user opens the build-details surface
- **THEN** the surface has a labelled heading, an operable close control, and can be dismissed using the expected keyboard interaction

### Requirement: Build provenance timestamps
The build-details surface SHALL display separately labelled values for the source commit timestamp, the publish timestamp, and the ETF data timestamp.

#### Scenario: Commit timestamp is displayed
- **WHEN** valid build metadata is available
- **THEN** the build-details surface identifies the timestamp for when the displayed source revision was created

#### Scenario: Publish timestamp is displayed
- **WHEN** valid build metadata is available
- **THEN** the build-details surface identifies the timestamp for when that source revision was deployed

#### Scenario: ETF data timestamp is displayed
- **WHEN** valid build metadata is available
- **THEN** the build-details surface identifies the timestamp or date for when the published ETF catalog/snapshot data was generated

#### Scenario: Timestamp meanings are not conflated
- **WHEN** the three timestamps are displayed
- **THEN** each value has an explicit label distinguishing source commit, publication, and ETF data generation

### Requirement: Source revision identification
The build-details surface SHALL display the full source commit identifier when available and SHALL provide a link to the corresponding repository revision when repository metadata is available.

#### Scenario: Source commit links to revision
- **WHEN** a repository URL and full source commit identifier are available
- **THEN** the build-details surface provides a link targeting that exact repository revision

#### Scenario: Source metadata is unavailable
- **WHEN** the source commit or repository URL is unavailable
- **THEN** the surface displays a clear unavailable/local-development state without preventing the rest of the app from operating

### Requirement: Publish provenance manifest
The publishing workflow SHALL generate and publish a machine-readable provenance manifest containing the source revision, commit timestamp, publish timestamp, and aggregate ETF data timestamp.

#### Scenario: Manifest matches published source
- **WHEN** the publish workflow creates a deployment from a source revision
- **THEN** the published manifest records the full commit identifier and commit timestamp for that source revision

#### Scenario: Manifest records deployment time
- **WHEN** the publish workflow creates a deployment
- **THEN** the published manifest records the publish timestamp separately from the commit timestamp

#### Scenario: Manifest records ETF data time
- **WHEN** the publish workflow copies the catalog and ETF snapshots
- **THEN** the published manifest records the aggregate catalog or snapshot generation timestamp used by the published data

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

