## ADDED Requirements

### Requirement: Security master is downloaded for every ingestion run
The system MUST download the latest security-master CSV from the configured upstream source before loading it for an ingestion run.

#### Scenario: Ingestion run begins
- **WHEN** the backend starts a snapshot ingestion run
- **THEN** the system SHALL retrieve the latest security-master CSV from the configured upstream URL
- **AND** the downloaded file SHALL be used to build the security master for that run

### Requirement: Downloaded security master is stored with raw inputs
The system MUST persist the downloaded security-master CSV in the run's raw output tree so the exact enrichment source used for the run is retained with the generated snapshots.

#### Scenario: Raw copy is written
- **WHEN** the security-master CSV has been downloaded successfully
- **THEN** the system SHALL write the file into the run's raw output directory
- **AND** snapshot provenance SHALL reference the stored file path or equivalent source metadata

### Requirement: Bundled fallback security master is not used
The system MUST NOT depend on a repository-tracked security-master file when generating snapshots.

#### Scenario: Repository copy is absent
- **WHEN** the repository does not contain a tracked `tickers.csv` file
- **THEN** the ingestion run SHALL still work as long as the upstream security-master CSV can be downloaded
- **AND** the system SHALL NOT read a fallback security-master file from the repository

### Requirement: Security-master download failure stops ingestion
The system MUST fail the ingestion run if the security-master CSV cannot be downloaded.

#### Scenario: Upstream download fails
- **WHEN** the security-master CSV cannot be fetched from the upstream URL
- **THEN** the ingestion run SHALL stop with an error
- **AND** the system SHALL NOT continue by using a bundled fallback copy