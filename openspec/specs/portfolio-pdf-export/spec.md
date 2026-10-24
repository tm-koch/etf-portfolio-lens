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
- **AND** unavailable price data outside Portfolio table cells is identified as unavailable rather than represented as zero

### Requirement: Show em dashes for unavailable portfolio table values
Unavailable share or allocation, unit-price, market-value, and portfolio-weight cells in the PDF `1 · Portfolio` table SHALL display an em dash (`—`) instead of a localized unavailable label. This rule SHALL NOT change genuine zero values or unavailable labels elsewhere in the report.

#### Scenario: A current portfolio value is unavailable
- **WHEN** a current portfolio position lacks a share or allocation, unit-price, market-value, or portfolio-weight value
- **THEN** the corresponding Portfolio table cell displays `—`
- **AND** other available values in that row remain formatted normally

#### Scenario: A catalog-only ETF has no portfolio values
- **WHEN** the full-catalog report includes an ETF that is not in the portfolio
- **THEN** its unavailable allocation, unit-price, market-value, and portfolio-weight cells display `—`

#### Scenario: A portfolio value is zero
- **WHEN** a portfolio table value is available and equals zero
- **THEN** the cell displays the formatted zero value rather than `—`

#### Scenario: Portfolio table has a visible right boundary
- **WHEN** the portfolio table is rendered in the PDF
- **THEN** it remains narrower than the printable content area, with all columns visible and fund names wrapped as needed

### Requirement: Include a link to the current portfolio
The Portfolio section SHALL include a clickable localized text link to a URL that represents the current portfolio using the existing full-share or relative-allocation semantics.

#### Scenario: Shares-based portfolio link
- **WHEN** a report is generated for a shares-based portfolio
- **THEN** the link opens a shared portfolio with the current ETF positions and share counts

#### Scenario: Relative-allocation portfolio link
- **WHEN** a report is generated for a percentage-only portfolio
- **THEN** the link opens a shared portfolio with the current ETF positions and relative allocation units

#### Scenario: Empty portfolio has no share link
- **WHEN** a report is generated with no selected portfolio positions
- **THEN** the Portfolio section does not contain a malformed or empty portfolio link

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

### Requirement: Present portfolio score verdicts
The Portfolio Analytics score section SHALL use the localized heading `Portfolio scores` and present the redundancy and diversification scores with localized verdict badges.

#### Scenario: Both portfolio scores are available
- **WHEN** the PDF report includes portfolio analytics with both scores available
- **THEN** the score section shows each score and its localized verdict badge under the `Portfolio scores` heading
- **AND** the Explore view's redundancy heading remains unchanged

### Requirement: Use bright-mode colors for score verdict badges
Score verdict badges in the PDF SHALL use the website's bright-mode verdict colors regardless of the active application color mode.

#### Scenario: Export while the app uses a dark theme
- **WHEN** a report is generated while the app uses dark or automatic-dark mode
- **THEN** both score verdict badges use the same colors as the website's bright-mode verdicts
- **AND** the app's color-mode preference remains unchanged

### Requirement: Omit holdings coverage from the score section
The PDF score section SHALL NOT display a Holdings coverage card, metric, or caveat.

#### Scenario: Holdings coverage is incomplete
- **WHEN** the report's underlying holdings have incomplete coverage
- **THEN** the score section omits holdings-coverage values and caveats
- **AND** the redundancy and diversification scores remain available when their own inputs permit calculation

### Requirement: Calculate exposure roll-ups from report weights
The report SHALL calculate exposure roll-ups from each position's captured portfolio weight when that weight is available.

#### Scenario: Report positions include captured weights
- **WHEN** a report contains positions with captured weights and usable exposure aggregates
- **THEN** sector, region, and currency roll-ups reflect those weights instead of being reported as unavailable because raw share totals are absent

### Requirement: Bound exposure rollup detail
Each sector, region, and currency rollup SHALL display no more than its 20 highest-weight named entries. If additional entries remain, the report SHALL combine their weights into one localized remainder entry and omit the individual remaining labels.

#### Scenario: Rollup contains more than 20 categories
- **WHEN** a sector, region, or currency rollup contains more than 20 entries
- **THEN** the report displays the 20 highest-weight entries followed by one remainder entry whose value is the sum of all other entries

#### Scenario: Rollup contains at most 20 categories
- **WHEN** a rollup contains 20 or fewer entries
- **THEN** the report displays all entries without a remainder entry

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

### Requirement: Identify the parent section on category pages
Top Companies and Pairwise ETF Overlap pages SHALL show their numbered parent section title in the page header and render the category title at a subordinate heading size.

#### Scenario: Top Companies page hierarchy
- **WHEN** a Top Companies page or continuation page is rendered
- **THEN** its header identifies `2 · Portfolio Analytics` and its Top Companies title is subordinate

#### Scenario: Pairwise ETF Overlap page hierarchy
- **WHEN** a Pairwise ETF Overlap page or continuation page is rendered
- **THEN** its header identifies `3 · Exposure Analysis` and its Pairwise ETF Overlap title is subordinate

### Requirement: Decorate exposure chart titles with aligned separators
Sector, region, and currency chart titles SHALL each have a thin gray horizontal separator below them; each separator SHALL align with its title, span its chart column, and leave a 10 mm gutter between adjacent columns without encoding data values. The currency legend SHALL use four columns.

#### Scenario: Exposure title bars are rendered
- **WHEN** the three exposure charts are rendered
- **THEN** each chart title and its thin gray separator share a left edge, each separator spans its chart column, and adjacent columns are separated by 10 mm

#### Scenario: Currency legend uses four columns
- **WHEN** the currency chart has legend entries
- **THEN** its legend arranges entries in four columns within the currency chart area

### Requirement: Paginate without clipping report content
The report SHALL add continuation pages when variable portfolio, catalog, matrix, or chart content cannot fit legibly, without clipping or omitting required rows; section titles SHALL remain separate from pagination.

#### Scenario: Numbered sections start on new pages
- **WHEN** the report is generated
- **THEN** the cover is page 1, `1 · Portfolio` starts on a following page, and `2 · Portfolio Analytics` and `3 · Exposure Analysis` each start on a new page

#### Scenario: Content continues beyond a base page
- **WHEN** report content exceeds the available printable area or width
- **THEN** the report adds continuation pages and preserves all required content in a readable layout

#### Scenario: Report canvas fits printable page width
- **WHEN** the report is captured for landscape A4 output
- **THEN** its fixed-width canvas remains within the printable width after page margins

#### Scenario: Footer contains generation identity and page position
- **WHEN** the report has one or more pages
- **THEN** every page footer retains `ETF Portfolio Lens | Generated: <timestamp>` on the left and shows the localized current page of total right-aligned on the same footer line, with the cover numbered 1
- **AND** section headings retain the exact titles `1 · Portfolio`, `2 · Portfolio Analytics`, and `3 · Exposure Analysis`

#### Scenario: Analytics fit within the report page
- **WHEN** portfolio analytics are rendered
- **THEN** the analytics content remains inside the printable page width without touching or overlapping its right edge

#### Scenario: Analytics boxes keep a visible right gutter
- **WHEN** metric and exposure rollup boxes are rendered
- **THEN** the rightmost boxes remain fully visible with clear space between their right borders and the analytics section edge

#### Scenario: Company names have more table width
- **WHEN** the Top Holdings company matrix is rendered
- **THEN** its company-name column is twice the previous 108px width and company names continue to wrap within the column

### Requirement: Present a branded report cover
The PDF SHALL begin with a standalone cover page containing the PWA launcher icon, the ETF Portfolio Lens title, and the report's generation provenance grouped without individual metadata boxes. The cover separator SHALL be centered at the page's vertical midpoint, with the icon and title above it and provenance below it.

#### Scenario: Report cover is generated
- **WHEN** a PDF report is generated
- **THEN** its first page presents the PWA icon and ETF Portfolio Lens title together with generation time, build identifier, ETF snapshot timestamp, and live-price timestamp in a visually grouped layout without individual boxes
- **AND** a horizontal separator is centered at the page's vertical midpoint, with the icon and title above it and provenance below it

### Requirement: Include grouped report provenance and a compact footer
The cover SHALL identify generation time, website build identifier, ETF snapshot-data timestamp, and live-price-data timestamp in a grouped layout without individual boxes. Every page footer SHALL display `ETF Portfolio Lens | Generated: <timestamp>` on the left and the localized current page of total right-aligned on the same footer line, with a website hyperlink over only the `ETF Portfolio Lens` label. The footer SHALL NOT include a build identifier, ETF snapshot timestamp, or live-price timestamp.

#### Scenario: Cover provenance is available
- **WHEN** the report is generated with build, snapshot, and live-price metadata available
- **THEN** the cover displays separately labelled generation, build, snapshot-data, and live-price values together without individual metadata boxes

#### Scenario: Footer remains minimal
- **WHEN** any report page is rendered
- **THEN** its left-side footer text is `ETF Portfolio Lens | Generated: <timestamp>`
- **AND** its localized current page of total is right-aligned on the same footer line
- **AND** its only footer link annotation covers the `ETF Portfolio Lens` label

#### Scenario: Footer brand opens the website
- **WHEN** a user activates `ETF Portfolio Lens` in a report footer
- **THEN** the PDF opens the ETF Portfolio Lens website without making the generated timestamp part of the link

#### Scenario: Some cover provenance is unavailable
- **WHEN** one or more provenance values are unavailable
- **THEN** the cover labels those values as unavailable and still generates the remaining report content

### Requirement: Keep PDF generation local and PWA-capable
PDF generation SHALL run in the browser without uploading portfolio contents, and SHALL be available in the installed PWA using locally served or cached generation resources.

#### Scenario: Installed PWA exports offline
- **WHEN** the installed PWA is offline and the application shell, ETF catalog, and required portfolio snapshot data have been cached
- **THEN** the user can generate a PDF from cached local data without a third-party CDN request

#### Scenario: Portfolio data remains local
- **WHEN** the user generates a report in the website or installed PWA
- **THEN** portfolio positions and report contents are not uploaded to a server for PDF generation
