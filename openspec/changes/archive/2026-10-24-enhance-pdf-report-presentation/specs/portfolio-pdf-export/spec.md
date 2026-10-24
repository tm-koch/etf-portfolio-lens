# Spec Delta

## ADDED Requirements

### Requirement: Present a branded report cover
The PDF SHALL begin with a standalone cover page containing the PWA launcher icon, the ETF Portfolio Lens title, and the report's generation provenance grouped without individual metadata boxes.

#### Scenario: Report cover is generated
- **WHEN** a PDF report is generated
- **THEN** its first page presents the PWA icon and ETF Portfolio Lens title together with generation time, build identifier, ETF snapshot timestamp, and live-price timestamp in a visually grouped layout without individual boxes

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

#### Scenario: Footer contains only generation identity
- **WHEN** the report has one or more pages
- **THEN** every page footer contains only `ETF Portfolio Lens | Generated: <timestamp>`, while section headings retain the exact titles `1 · Portfolio`, `2 · Portfolio Analytics`, and `3 · Exposure Analysis`

#### Scenario: Analytics fit within the report page
- **WHEN** portfolio analytics are rendered
- **THEN** the analytics content remains inside the printable page width without touching or overlapping its right edge

#### Scenario: Analytics boxes keep a visible right gutter
- **WHEN** metric and exposure rollup boxes are rendered
- **THEN** the rightmost boxes remain fully visible with clear space between their right borders and the analytics section edge

#### Scenario: Company names have more table width
- **WHEN** the Top Holdings company matrix is rendered
- **THEN** its company-name column is twice the previous 108px width and company names continue to wrap within the column

### Requirement: Include grouped report provenance and a compact footer
The cover SHALL identify generation time, website build identifier, ETF snapshot-data timestamp, and live-price-data timestamp in a grouped layout without individual boxes. Every page footer SHALL contain only the visible text `ETF Portfolio Lens | Generated: <timestamp>`, with a website hyperlink over only the `ETF Portfolio Lens` label. The footer SHALL not include a page number, build identifier, ETF snapshot timestamp, or live-price timestamp.

#### Scenario: Cover provenance is available
- **WHEN** the report is generated with build, snapshot, and live-price metadata available
- **THEN** the cover displays separately labelled generation, build, snapshot-data, and live-price values together without individual metadata boxes

#### Scenario: Footer remains minimal
- **WHEN** any report page is rendered
- **THEN** its only footer text is `ETF Portfolio Lens | Generated: <timestamp>` and its only footer link annotation covers the `ETF Portfolio Lens` label

#### Scenario: Footer brand opens the website
- **WHEN** a user activates `ETF Portfolio Lens` in a report footer
- **THEN** the PDF opens the ETF Portfolio Lens website without making the generated timestamp part of the link

#### Scenario: Some cover provenance is unavailable
- **WHEN** one or more provenance values are unavailable
- **THEN** the cover labels those values as unavailable and still generates the remaining report content