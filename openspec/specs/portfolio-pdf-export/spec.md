# portfolio-pdf-export Specification

## Purpose
Defines how users configure, generate, and receive a localized portfolio and ETF-catalog PDF report from the website or installed PWA.

## Requirements

### Requirement: Configure report scope and allocation-only output
The app SHALL provide an accessible Export view with scope choices for the current portfolio and the full ETF catalog, defaulting to the current portfolio, and an allocation-only output switch.

#### Scenario: Export view is opened
- **WHEN** the user activates the export icon in the application utility bar
- **THEN** the app opens its Export view without changing the current portfolio, valuation mode, or color-mode preference

#### Scenario: Default report scope
- **WHEN** the Export view opens without a report-scope preference for the current export session
- **THEN** the current portfolio scope is selected

#### Scenario: Full catalog report
- **WHEN** the user selects the full ETF catalog scope
- **THEN** the report lists every ETF in the published catalog while calculated portfolio analytics remain limited to ETFs in the current portfolio

#### Scenario: Allocation-only output
- **WHEN** the user enables allocation-only output
- **THEN** the report omits share quantities, unit prices, and monetary values while retaining portfolio allocation percentages and their dependent analytics
- **AND** the option does not change or persist the portfolio's entry mode or valuation mode

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

### Requirement: Present the portfolio page
The first report section SHALL be titled exactly `1 · Portfolio` and SHALL present the selected portfolio ETFs with available fund identity, share or allocation, valuation, and portfolio-weight details appropriate to the active valuation and export modes.

#### Scenario: Current portfolio report
- **WHEN** the user generates a report using the default current portfolio scope
- **THEN** the `1 · Portfolio` section lists each ETF position in the current portfolio
- **AND** shares-based output includes available current price, currency, value, and portfolio weight
- **AND** percentage-only or allocation-only output does not invent absolute prices, shares, or values

#### Scenario: Catalog report identifies portfolio membership
- **WHEN** the user generates a report using the full ETF catalog scope
- **THEN** the `1 · Portfolio` section lists each catalog ETF and distinguishes current portfolio positions from catalog-only ETFs
- **AND** portfolio allocations and valuation details are shown only for current portfolio positions
- **AND** unavailable price data is identified as unavailable rather than represented as zero

#### Scenario: Portfolio table has a visible right boundary
- **WHEN** the portfolio table is rendered in the PDF
- **THEN** it remains narrower than the printable content area, with all columns visible and fund names wrapped as needed

### Requirement: Present portfolio analytics and top holdings
The second report section SHALL be titled exactly `2 · Portfolio Analytics` and SHALL present current-portfolio summary metrics, exposure rollups and scores, and up to the 20 highest-ranked underlying companies.

#### Scenario: Analytics use the current portfolio
- **WHEN** a report is generated in either scope
- **THEN** all summary metrics, rollups, scores, and company rankings are calculated only from the current portfolio ETFs

#### Scenario: Analytics groups are visibly framed
- **WHEN** portfolio analytics are rendered in the report
- **THEN** summary metrics, scores, and exposure rollup groups appear in bordered boxes

#### Scenario: Top holdings matrix is complete and ranked
- **WHEN** at least one underlying company is available for the current portfolio
- **THEN** the section includes up to the 20 highest-ranked companies in descending portfolio exposure order
- **AND** each row includes the company rank, name, total portfolio contribution, and one contribution column for every ETF in the current portfolio
- **AND** absent ETF contributions are shown as unavailable or not applicable rather than as a positive value
- **AND** report generation does not depend on which Explore rows have already been rendered or loaded on screen

#### Scenario: Top Companies starts on a fresh page
- **WHEN** the company contribution matrix is rendered
- **THEN** its heading and first table panel begin on a new page
- **AND** company table rows use slightly reduced vertical padding to fit more rows per page

#### Scenario: Top Companies percentage columns and missing entries are clear
- **WHEN** the company contribution matrix is rendered
- **THEN** the total and ETF contribution percentage columns are right-aligned
- **AND** missing ETF contributions are shown as an em dash rather than an unavailable label

#### Scenario: Analytics are unavailable
- **WHEN** the current portfolio has insufficient data for a metric or company ranking
- **THEN** the report identifies that metric or ranking as unavailable without blocking the rest of the report

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

### Requirement: Paginate without clipping report content
The report SHALL add continuation pages when variable portfolio, catalog, matrix, or chart content cannot fit legibly, without clipping or omitting required rows, and SHALL number pages separately from the three section titles.

#### Scenario: Numbered sections start on new pages
- **WHEN** the report is generated
- **THEN** `1 · Portfolio` starts on the first page, and `2 · Portfolio Analytics` and `3 · Exposure Analysis` each start on a new page

#### Scenario: Content continues beyond a base page
- **WHEN** report content exceeds the available printable area or width
- **THEN** the report adds continuation pages and preserves all required content in a readable layout

#### Scenario: Report canvas fits printable page width
- **WHEN** the report is captured for landscape A4 output
- **THEN** its fixed-width canvas remains within the printable width after page margins

#### Scenario: Page numbers remain separate from section titles
- **WHEN** the report has one or more pages
- **THEN** each page shows its page number and total page count in the footer, while section headings retain the exact titles `1 · Portfolio`, `2 · Portfolio Analytics`, and `3 · Exposure Analysis`

#### Scenario: Analytics fit within the report page
- **WHEN** portfolio analytics are rendered
- **THEN** the analytics content remains inside the printable page width without touching or overlapping its right edge

#### Scenario: Analytics boxes keep a visible right gutter
- **WHEN** metric and exposure rollup boxes are rendered
- **THEN** the rightmost boxes remain fully visible with clear space between their right borders and the analytics section edge

#### Scenario: Company names have more table width
- **WHEN** the Top Holdings company matrix is rendered
- **THEN** its company-name column is twice the previous 108px width and company names continue to wrap within the column

### Requirement: Include report provenance and website link
Each report page SHALL identify the generation date and time, website build identifier, ETF snapshot-data timestamp, live-price-data timestamp, and a clickable ETF Portfolio Lens website link. Unavailable provenance values SHALL be identified as unavailable.

#### Scenario: Valid provenance is available
- **WHEN** the report is generated with build, snapshot, and live-price metadata available
- **THEN** each page footer or metadata block displays separately labelled generation, build, snapshot-data, and live-price timestamps plus a clickable website link

#### Scenario: Some provenance is unavailable
- **WHEN** one or more provenance values are unavailable
- **THEN** the report labels those values as unavailable and still generates the remaining report content

### Requirement: Keep PDF generation local and PWA-capable
PDF generation SHALL run in the browser without uploading portfolio contents, and SHALL be available in the installed PWA using locally served or cached generation resources.

#### Scenario: Installed PWA exports offline
- **WHEN** the installed PWA is offline and the application shell, ETF catalog, and required portfolio snapshot data have been cached
- **THEN** the user can generate a PDF from cached local data without a third-party CDN request

#### Scenario: Portfolio data remains local
- **WHEN** the user generates a report in the website or installed PWA
- **THEN** portfolio positions and report contents are not uploaded to a server for PDF generation
