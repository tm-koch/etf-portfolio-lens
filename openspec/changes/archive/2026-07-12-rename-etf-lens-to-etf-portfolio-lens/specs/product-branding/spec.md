## ADDED Requirements

### Requirement: Product name is consistent across user-facing surfaces
The system SHALL present the product name as "ETF Portfolio Lens" across the web application, repository documentation, and local server messaging.

#### Scenario: Web app displays the new brand
- **WHEN** a user opens the web application
- **THEN** the browser title and visible hero branding SHALL show "ETF Portfolio Lens"
- **AND** startup error messaging SHALL use the same product name

#### Scenario: Documentation uses the new brand
- **WHEN** a user reads the repository README files or product idea documentation
- **THEN** the product name SHALL appear as "ETF Portfolio Lens"
- **AND** old branding SHALL not remain in those visible docs

### Requirement: Technical identifiers remain stable during branding updates
The system SHALL keep technical identifiers, snapshot paths, data keys, and product data files unchanged when updating branding text.

#### Scenario: Branding update does not rename data artifacts
- **WHEN** the product name is updated across the repository
- **THEN** snapshot filenames, registry entries, catalog paths, and data keys SHALL remain unchanged
- **AND** the rename SHALL not alter ingestion behavior or published data structure
