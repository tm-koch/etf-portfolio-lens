## ADDED Requirements

### Requirement: Publish all required frontend modules
The GitHub Pages publishing workflow SHALL copy every frontend JavaScript module required by `web/app.js`, including `portfolio-import.js`, into the published site root alongside the entry module.

#### Scenario: PDF importer module is published
- **WHEN** the publishing workflow prepares the GitHub Pages worktree
- **THEN** the published site contains `portfolio-import.js` at the path imported by `app.js`

#### Scenario: Published application bootstraps
- **WHEN** a user opens the published GitHub Pages application
- **THEN** the application loads without a required-module 404 and renders its navigation and color-mode controls

#### Scenario: Import controls remain available after deployment
- **WHEN** the published application has bootstrapped
- **THEN** the Portfolio tab exposes the existing PDF import workflow without changing its parsing behavior
