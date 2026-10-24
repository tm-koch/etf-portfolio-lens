# Spec Delta

## MODIFIED Requirements

### Requirement: Generate a localized bright-mode PDF
The app SHALL generate and directly download the report as an A4 landscape PDF using the currently selected interface language and the website font in a bright presentation, independently of the active application color mode. Report text, including headings, labels, tables, metrics, and legends, SHALL be native selectable PDF text; chart plots MAY remain graphics.

#### Scenario: Export from a dark application theme
- **WHEN** the user generates a report while the application is in dark or automatic-dark mode
- **THEN** the PDF uses the bright report presentation and the app's color-mode preference remains unchanged

#### Scenario: Export follows the selected language
- **WHEN** the user generates a report after selecting a supported interface language
- **THEN** report headings, labels, taxonomy names, numbers, dates, and currency values use that language and its formatting conventions

#### Scenario: Report text is selectable
- **WHEN** the generated report contains headings, table cells, metrics, or chart legends
- **THEN** those contents are represented as native PDF text that users can select, search, and copy
- **AND** chart plots may be embedded as graphics

#### Scenario: Successful PDF export closes the dialog
- **WHEN** PDF generation succeeds
- **THEN** the app downloads the PDF and closes the Export dialog automatically
- **AND** the dialog remains open with an error status if PDF generation fails

### Requirement: Present exposure analysis
The third report section SHALL be titled exactly `3 · Exposure Analysis` and SHALL present the sector, region, and currency comparison charts and the pairwise ETF overlap heatmap for the current portfolio. It SHALL omit the pairwise holdings drill-down table.

#### Scenario: Exposure charts fit and represent current positions
- **WHEN** the current portfolio has data for one or more exposure charts
- **THEN** the charts use the selected portfolio ETFs and the same exposure calculations as the app
- **AND** each doughnut plot uses a 252px fixed-size frame
- **AND** each chart legend starts at least 48px below its plot to remain visually separate
- **AND** all three plots fit inside the printable page width without cropping
- **AND** doughnut rendering is complete before the PDF is saved

#### Scenario: Donut charts use the website bright palette
- **WHEN** a donut chart is rendered in the PDF
- **THEN** its slice colors use the same palette as the regular website in bright mode

#### Scenario: Pairwise drill-down is excluded
- **WHEN** the report is generated
- **THEN** the pairwise heatmap may be included but the pairwise holdings drill-down detail table is not included

#### Scenario: Pairwise ETF overlap starts on a fresh page
- **WHEN** the pairwise ETF overlap heading and heatmap are rendered
- **THEN** they begin on a new page
