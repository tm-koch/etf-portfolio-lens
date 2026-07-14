## ADDED Requirements

### Requirement: Root-hosted GitHub Pages publish target
The repository SHALL support publishing the static website to a root-hosted GitHub Pages target using the `gh-pages` branch.

#### Scenario: Publish to root-hosted Pages
- **WHEN** the publish workflow is run for GitHub Pages
- **THEN** the website content SHALL be placed at the root of the published site
- **AND** the `gh-pages` branch SHALL be used as the publish source

### Requirement: Published data paths remain valid at site root
The published site SHALL preserve the root-absolute snapshot paths used by the frontend data catalog so the application can load its published ETF snapshot JSON files without URL rewriting.

#### Scenario: Load published catalog data
- **WHEN** the site is opened from the GitHub Pages root
- **THEN** the frontend SHALL load `web/data/catalog.json`
- **AND** each catalog entry SHALL resolve its snapshot JSON from the published `data/raw/<date>/snapshots` tree

### Requirement: Static site tree includes frontend and data assets
The publish output SHALL include the frontend files and the relevant published ETF data files in a stable directory structure.

#### Scenario: Inspect publish tree
- **WHEN** the published `gh-pages` content is inspected
- **THEN** it SHALL include the `web/` frontend files
- **AND** it SHALL include the `data/raw/` snapshot files referenced by the catalog
