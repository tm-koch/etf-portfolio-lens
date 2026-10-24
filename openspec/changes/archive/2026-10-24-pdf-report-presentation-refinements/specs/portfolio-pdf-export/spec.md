# Spec Delta

## ADDED Requirements

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

## MODIFIED Requirements

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
The cover SHALL identify generation time, website build identifier, ETF snapshot-data timestamp, and live-price-data timestamp in a grouped layout without individual boxes. Every page footer SHALL display `ETF Portfolio Lens | Generated: <timestamp>` on the left and the localized current page of total right-aligned on the same footer line. A website hyperlink SHALL cover only the `ETF Portfolio Lens` label. The footer SHALL NOT include a build identifier, ETF snapshot timestamp, or live-price timestamp.

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
