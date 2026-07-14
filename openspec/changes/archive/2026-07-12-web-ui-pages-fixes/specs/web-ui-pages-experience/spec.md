## ADDED Requirements

### Requirement: Lightweight white interface
The system MUST present the web UI in a lightweight white visual style and MUST keep the main workflow readable without the heavy dark card treatment used previously.

#### Scenario: Render the app in a light theme
- **WHEN** the user opens the application
- **THEN** the UI SHALL use a light background and light-weight surfaces
- **AND THEN** the interface SHALL remain readable on desktop and mobile screen sizes

### Requirement: Vertical metric sections
The system MUST render the sector, region, and currency sections vertically, one below the other, instead of placing them side by side.

#### Scenario: Show sections in a single column
- **WHEN** the user opens the comparison or aggregated exposure area
- **THEN** the sector, region, and currency sections SHALL be stacked vertically
- **AND THEN** the layout SHALL not require a three-column arrangement for these sections

### Requirement: Reliable doughnut chart rendering
The system MUST render the Chart.js doughnut charts inside stable layout containers so the charts are visible and sized correctly.

#### Scenario: Display comparison charts
- **WHEN** the comparison view is opened
- **THEN** the sector, region, and currency doughnut charts SHALL render inside bounded containers
- **AND THEN** the charts SHALL remain visible rather than expanding to unusable dimensions or disappearing

#### Scenario: Preserve chart readability on mobile
- **WHEN** the comparison view is opened on a narrow viewport
- **THEN** the doughnut charts SHALL remain readable
- **AND THEN** the chart area SHALL not introduce horizontal scrolling for the main content area

### Requirement: Browser-accessible local development server
The system MUST provide a local development server that can be accessed from a browser and MUST support binding beyond localhost when required for device testing.

#### Scenario: Start the dev server locally
- **WHEN** a developer starts the local server
- **THEN** the application SHALL be reachable in a desktop browser

#### Scenario: Access the server from another device
- **WHEN** the developer binds the server to a non-localhost interface
- **THEN** the application SHALL be reachable from a browser on the same network

### Requirement: GitHub Pages publish structure documentation
The system MUST document which frontend and data files need to be uploaded to GitHub Pages and MUST describe the directory structure expected by the static site.

#### Scenario: Review deployment docs
- **WHEN** a developer prepares a GitHub Pages release
- **THEN** the documentation SHALL list the required HTML, CSS, JavaScript, and data files
- **AND THEN** the documentation SHALL describe the folder structure expected on GitHub Pages
