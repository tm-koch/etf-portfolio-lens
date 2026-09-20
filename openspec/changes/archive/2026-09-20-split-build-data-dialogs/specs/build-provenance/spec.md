## MODIFIED Requirements

### Requirement: Secondary About build-details access

The web app SHALL provide two secondary actions in the Home hero development/status area: `Build & preview` and `Data details`. Both actions SHALL remain outside the primary Portfolio, Compare, and Explore navigation and SHALL open their own in-page details surface without changing browser URL or history.

#### Scenario: Build and data actions are discoverable
- **WHEN** the application loads successfully
- **THEN** the hero development/status area contains accessible secondary actions labelled `Build & preview` and `Data details`

#### Scenario: Build action opens build details
- **WHEN** a user activates `Build & preview`
- **THEN** the Build & preview in-page surface opens and the primary navigation destinations remain unchanged

#### Scenario: Data action opens data details
- **WHEN** a user activates `Data details`
- **THEN** the Data details in-page surface opens and the primary navigation destinations remain unchanged

#### Scenario: Both surfaces are keyboard accessible
- **WHEN** a keyboard user opens either details surface
- **THEN** the surface has a unique labelled heading, an operable close control, and can be dismissed using the expected keyboard interaction

### Requirement: Build provenance timestamps

The Build & preview surface SHALL display separately labelled values for the source commit timestamp and the publish timestamp. The Data details surface SHALL display the separately labelled ETF data timestamp.

#### Scenario: Commit timestamp is displayed
- **WHEN** valid build metadata is available
- **THEN** the Build & preview surface identifies the timestamp for when the displayed source revision was created

#### Scenario: Publish timestamp is displayed
- **WHEN** valid build metadata is available
- **THEN** the Build & preview surface identifies the timestamp for when that source revision was deployed

#### Scenario: ETF data timestamp is displayed
- **WHEN** valid build metadata is available
- **THEN** the Data details surface identifies the timestamp or date for when the published ETF catalog/snapshot data was generated

#### Scenario: Timestamp meanings are not conflated
- **WHEN** the three timestamps are displayed
- **THEN** each value has an explicit label distinguishing source commit, publication, and ETF data generation

### Requirement: Source revision identification

The Build & preview surface SHALL display the full source commit identifier when available and SHALL provide a link to the corresponding repository revision when repository metadata is available.

#### Scenario: Source commit links to revision
- **WHEN** a repository URL and full source commit identifier are available
- **THEN** the Build & preview surface provides a link targeting that exact repository revision

#### Scenario: Source metadata is unavailable
- **WHEN** the source commit or repository URL is unavailable
- **THEN** the Build & preview surface displays a clear unavailable/local-development state without preventing the rest of the app from operating

### Requirement: Extensible and fault-tolerant metadata

The provenance manifest SHALL include a versioned or extensible structure for future metadata fields, and failure to load or parse it SHALL not block the core portfolio UI. The Build & preview surface SHALL render optional build metadata without leaving a duplicate horizontal separator when that metadata is absent. The Data details surface SHALL retain one separator before its bottom current-selection warnings section.

#### Scenario: Optional details are absent
- **WHEN** the Build & preview surface has no optional build details to display
- **THEN** the hidden optional-details section SHALL not occupy layout space or display a separator

#### Scenario: Warnings remain at the bottom of data details
- **WHEN** the Data details surface is rendered
- **THEN** current-selection warnings SHALL appear at the bottom with one separator immediately above the warnings section

#### Scenario: Future metadata is added
- **WHEN** additional provenance or diagnostic fields are added to the manifest
- **THEN** the appropriate details surface can render them without changing the primary navigation contract

#### Scenario: Manifest is absent locally
- **WHEN** the app runs without a generated provenance manifest
- **THEN** the core portfolio, comparison, and aggregation workflows remain usable and the relevant details surface reports local development or unavailable metadata

#### Scenario: Manifest is malformed
- **WHEN** the provenance manifest cannot be parsed
- **THEN** the app continues loading its portfolio data and reports unavailable build metadata in the Build & preview surface

### Requirement: Publish live-data provenance safely

The provenance manifest SHALL include the live-data generation timestamp and aggregate status such as complete, unavailable, or fallback-capable, without including provider identities, source URLs, credentials, or raw responses. The Data details surface SHALL display the live-data generation timestamp and aggregate status when available.

#### Scenario: Complete live data is published
- **WHEN** a validated live-data artifact is included in a Pages deployment
- **THEN** Data details identify its generation timestamp and complete status

#### Scenario: Live data is unavailable
- **WHEN** the deployment uses an earlier valid artifact because the update workflow failed
- **THEN** Data details retain the earlier artifact timestamp and do not claim that a new live update succeeded