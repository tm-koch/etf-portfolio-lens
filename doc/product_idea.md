Source: MS Co-pilot GPT-5.5 Think

## Quick verdict

This is a strong product idea, especially if positioned as a **personal ETF portfolio exposure explorer** rather than a trading or recommendation tool. A static GitHub Pages frontend is a good fit because the site can be HTML/CSS/JavaScript only, and GitHub Pages is explicitly designed to publish static HTML, CSS, and JavaScript from a repository. [[docs.github.com]](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

The key product challenge is not the UI — it is the **data model**: ETF holdings, sector/region/asset-class classifications, currency conversion, changing ETF universes, stale data, missing holdings, and identifiers.

> **Not financial advice:** the product should present portfolio composition and exposure analytics, not investment recommendations.

---

# 1. Refined product concept

## Product name idea

**ETF Portfolio Lens** — a browser-based ETF portfolio exposure analyzer.

## Core promise

> “Create a simple ETF portfolio, save it locally in your browser, and instantly see what you really own across companies, sectors, regions, asset classes, and currencies.”

The user does not need an account. They can:

- Select ETFs from a predefined catalog.
- Enter quantity, value, or percentage allocation.
- Add custom/manual ETFs if needed.
- See aggregated exposure across all ETFs.
- Understand concentration risks, e.g. “How much Apple do I indirectly own?”
- View exposures by:
    - individual holdings,
    - sector,
    - region/country,
    - asset class,
    - currency,
    - ETF provider,
    - maybe TER/cost later.

---

# 2. Recommended architecture

## High-level architecture

Backend data process

|

| Python script

| - fetch ETF data via APIs

| - scrape allowed sources if necessary

| - normalize holdings

| - add FX rates

| - classify regions/sectors/assets

v

public/data/etf-data.json

|

| committed/published to GitHub Pages

v

Static website

|

| React/Vue/Svelte/plain JS

| loads JSON

| stores user portfolio in localStorage

v

User sees portfolio analytics

This works well with GitHub Pages because the frontend is static, and the frequently generated JSON can simply be part of the deployed static files. GitHub Pages can publish static files from a repository and optionally use a build process. [[docs.github.com]](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

---

# 3. Important product decisions

## A. Use `localStorage`, not cookies, for remembering the portfolio

Use **localStorage** for saving the portfolio in the browser.

Reasons:

- `localStorage` persists across browser sessions. [[developer....ozilla.org]](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
- Web Storage is designed for browser-side key/value storage and is generally more appropriate than cookies for client-side app data. [[developer....ozilla.org]](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API)
- Cookies are sent with every request and are limited in size; MDN recommends modern storage APIs such as Web Storage or IndexedDB for general client-side storage. [[developer....ozilla.org]](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies)

Recommended saved object:

{

"schemaVersion": 1,

"baseCurrency": "CHF",

"positions": [

{

"etfId": "IE00B4L5Y983",

"ticker": "IWDA",

"quantity": 25,

"purchasePrice": null,

"manualValue": null

},

{

"etfId": "IE00B3RBWM25",

"ticker": "VWRL",

"quantity": 10

}

],

"customEtfs": [],

"lastUpdated": "2026-07-05T00:00:00Z"

}

For a first version, this is enough. Later, add import/export so users can back up their portfolio.

---

## B. Clarify what “add any new ETF” means

This is the biggest scope risk.

There are three possible meanings:

### Option 1 — Add any ETF already present in the JSON

This is easiest and should be the MVP.

The user can search the predefined ETF catalog and add any ETF that the backend already knows.

### Option 2 — Add a manual/custom ETF

The user can create a custom ETF manually by entering:

- name,
- currency,
- value,
- holdings,
- sector split,
- region split,
- asset-class split.

This is useful for ETFs not yet supported.

### Option 3 — Add any live ETF by ticker/ISIN

This is much harder. A static GitHub Pages site cannot reliably fetch and normalize arbitrary ETF composition data from every provider in real time. If you want this, the backend process must support ticker/ISIN discovery and regenerate the JSON.

My recommendation:

> **MVP:** predefined ETF catalog + local custom/manual ETF.
> **V2:** user can request/add a ticker, and the backend pipeline tries to enrich it in the next data refresh.

---

# 4. Data model design

You should make the JSON file the “single source of truth” for the frontend.

## Suggested JSON structure

{

"schemaVersion": 1,

"generatedAt": "2026-07-05T12:00:00Z",

"baseCurrency": "CHF",

"fxRates": {

"CHF": 1.0,

"EUR": 0.96,

"USD": 1.12

},

"etfs": [

{

"id": "IE00B4L5Y983",

"isin": "IE00B4L5Y983",

"ticker": "IWDA",

"name": "iShares Core MSCI World UCITS ETF",

"currency": "USD",

"price": 105.42,

"provider": "iShares",

"assetClass": "Equity",

"ter": 0.20,

"holdings": [

{

"securityId": "US0378331005",

"name": "Apple Inc.",

"ticker": "AAPL",

"weight": 4.8,

"sector": "Information Technology",

"country": "United States",

"region": "North America",

"currency": "USD",

"assetClass": "Equity"

}

],

"sectorExposure": [

{

"name": "Information Technology",

"weight": 23.5

}

],

"regionExposure": [

{

"name": "North America",

"weight": 68.2

}

],

"dataQuality": {

"holdingsCoveragePercent": 99.2,

"source": "provider/API",

"asOfDate": "2026-07-04"

}

}

]

}

## Why this structure is good

It supports:

- ETF search,
- portfolio valuation,
- company-level aggregation,
- region aggregation,
- sector aggregation,
- asset-class aggregation,
- currency conversion,
- stale-data warnings,
- graceful handling when ETFs disappear.

---

# 5. Portfolio calculation logic

For each ETF in the user portfolio:

ETF position value =

quantity × ETF price × FX conversion to user's base currency

Then for every holding inside the ETF:

Company exposure =

ETF position value × holding weight

Example:

User owns CHF 10,000 of ETF A

ETF A owns Apple at 5%

User’s indirect Apple exposure = CHF 500

Then aggregate across all ETFs:

Total Apple exposure =

Apple exposure from ETF A

+ Apple exposure from ETF B

+ Apple exposure from ETF C

`

This gives the most valuable product feature: **look-through exposure**.

---

# 6. UX proposal

## Main screens

### 1. Portfolio builder

User can:

- search ETFs by name, ticker, ISIN,
- add ETF,
- enter quantity/value/percentage,
- choose base currency,
- remove ETF,
- duplicate ETF,
- reset portfolio,
- export/import portfolio JSON.

### 2. Portfolio overview

Show:

- total portfolio value,
- number of ETFs,
- number of underlying holdings,
- top 10 company exposures,
- top 10 sectors,
- top regions,
- asset classes,
- currency exposure.

### 3. ETF detail page

For a selected ETF:

- name, ticker, ISIN,
- currency,
- price,
- TER,
- data date,
- top holdings,
- sector split,
- region split,
- asset-class split.

### 4. Data quality screen

Very important for trust.

Show:

- JSON generation date,
- ETF holdings date,
- missing holdings,
- stale ETFs,
- removed ETFs,
- FX rate date,
- coverage percentage.

---

# 7. Visualizations

Your “cake diagrams” are usually called **pie charts** or **donut charts**.

Use them selectively.

## Good uses for donut charts

- sector split,
- region split,
- asset-class split,
- currency split.

## Better as sorted lists or bar charts

- individual company holdings,
- top 20 exposures,
- ETF weights,
- country exposure if there are many countries.

For company holdings, a sorted list is better than a pie chart because there may be hundreds or thousands of companies.

Example UI:

Top company exposures



1. Apple Inc. 4.8% CHF 1,920

2. Microsoft Corp. 4.3% CHF 1,720

3. NVIDIA Corp. 3.7% CHF 1,480

4. Amazon.com Inc. 2.1% CHF 840

5. Alphabet Inc. 1.9% CHF 760

---

# 8. Handling changing ETF data

You correctly identified a key issue: ETFs may change, vanish, or appear.

You need a robust matching strategy.

## Use stable identifiers

Prefer this order:

1. ISIN
2. fund provider ID
3. ticker + exchange
4. name fallback

Do **not** rely only on ticker symbols. Tickers can vary by exchange and currency listing.

## When an ETF disappears

Do not delete the user’s portfolio position silently.

Instead show:

This ETF is no longer available in the latest data file.

Your saved position is still shown, but analytics may be incomplete.

Possible states:

{

"status": "active"

}

``

{

"status": "missing_from_latest_data"

}

{

"status": "replaced",

"replacementEtfId": "NEW_ISIN"

}

## When holdings change

That is expected. The frontend should always recompute analytics from the newest JSON.

But the saved user portfolio should only save:

- ETF ID,
- quantity/value/percentage,
- optional notes.

It should **not** save old holdings unless you want historical snapshots.

---

# 9. Currency handling

You have two currency problems:

## A. ETF trading currency

Example:

- ETF price in USD,
- user wants base currency CHF.

## B. Underlying holding currency

Example:

- ETF holds US stocks in USD,
- European stocks in EUR,
- Swiss stocks in CHF.

For MVP, I recommend:

Use ETF price currency for portfolio valuation.

Use holding weights for exposure.

Use one FX table to convert ETF position value into the user’s base currency.

Do not overcomplicate with each underlying security’s trading currency in version 1.

Later, you can add currency exposure based on underlying holdings.

---

# 10. Backend Python script

The Python script should have a clear pipeline:

1. Load configured ETF universe

2. Fetch ETF metadata

3. Fetch holdings

4. Fetch sector/region/asset-class data

5. Fetch FX rates

6. Normalize identifiers

7. Validate weights

8. Write etf-data.json

9. Write data-quality report

Recommended output files:

public/data/etf-data.json

public/data/data-quality.json

public/data/generated-at.json

## Important backend design choice

Avoid making the frontend dependent on live APIs.

Instead:

Frontend = reads static JSON

Backend = responsible for messy API/scraping logic

That keeps the GitHub Pages site simple, fast, and reliable.

---

# 11. Legal/data risk

Be careful with web scraping ETF provider sites.

Your backend should only use:

- official APIs where possible,
- downloadable CSV files if permitted,
- data sources whose terms allow your use case,
- clear attribution where required.

For a private personal tool this may be simpler, but for a public product you need to treat data licensing as a major requirement.

---

# 12. Suggested MVP scope

## MVP should include

- Static responsive website.
- ETF catalog loaded from JSON.
- Add/remove ETF positions.
- Save portfolio in `localStorage`.
- Base currency selection.
- Aggregated portfolio value.
- Top holdings list.
- Sector donut chart.
- Region donut chart.
- Asset-class donut chart.
- ETF allocation chart.
- Data freshness display.
- Import/export portfolio JSON.

## MVP should not include yet

- User accounts.
- Live trading data.
- Automatic broker sync.
- Historical performance.
- Tax optimization.
- Recommendations.
- Arbitrary ETF discovery from frontend.
- Rebalancing engine.

---

# 13. V2 ideas

Once the MVP works, add:

- portfolio drift vs target allocation,
- rebalancing suggestions,
- “overlap analysis” between ETFs,
- concentration warnings,
- dividend/yield view,
- TER/cost summary,
- historical snapshot comparison,
- custom ETF/manual asset support,
- broker CSV import,
- watchlist,
- PWA offline support,
- shareable portfolio links with encoded data,
- dark mode.

---

# 14. Product positioning

I would frame it like this:

> **A privacy-friendly ETF portfolio exposure analyzer that runs entirely in the browser. No login, no broker connection, no uploaded portfolio data. Just select your ETFs and understand what you really own.**

That privacy angle is strong because the portfolio can stay in the user’s browser. `localStorage` is origin-specific browser storage and persists across browser sessions, which fits this use case well. [[developer....ozilla.org]](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)

---

# 15. Main risks and mitigations

|Risk|Mitigation|
|---|---|
|ETF data unavailable or inconsistent|Add data-quality flags and coverage percentages|
|ETF disappears from JSON|Keep saved position, show warning|
|Ticker ambiguity|Use ISIN as primary ID|
|Currency confusion|Let user choose base currency and show conversion date|
|Pie charts become unreadable|Use top-N lists plus “Other” bucket|
|Browser storage cleared|Add export/import|
|Data licensing|Prefer official APIs/downloads and check terms|
|Static site limitations|Push all dynamic work into backend JSON generation|

---

# 16. Recommended final product definition

Build this as:

A static, privacy-friendly ETF portfolio analyzer hosted on GitHub Pages.

The frontend loads a generated ETF data JSON file, lets users build a local portfolio,

stores it in localStorage, and visualizes look-through exposure by company, sector,

region, asset class, ETF, and currency.

The most important product feature should be:

> **“What do I really own across all ETFs?”**

That is much more compelling than just showing ETF allocation.

---

## Suggested next step

Define the first `etf-data.json` schema and build the MVP around 5–10 ETFs before investing time in a complex scraping/API backend.

Great. Let’s define `etf-data.json` as a **versioned, frontend-friendly, static data contract**. The frontend should be able to load this file, validate it loosely, and compute portfolio analytics without needing live APIs.

Below is a proposed **MVP+ schema**: simple enough for version 1, but already structured for future ETF changes, currencies, data quality, and custom calculations.

---

# `etf-data.json` design goals

The JSON should support:

1. **ETF search**

    - by name, ticker, ISIN, provider, asset class.
2. **Portfolio valuation**

    - using ETF price and FX rates.
3. **Look-through exposure**

    - aggregate underlying holdings across multiple ETFs.
4. **Sector, region, country, asset-class, and currency analysis**

5. **Data freshness and quality warnings**

6. **ETF lifecycle changes**

    - active, delisted, merged, replaced, missing holdings, stale data.
7. **Backward-compatible frontend updates**

    - via `schemaVersion`.

---

# Recommended top-level structure

{

"schemaVersion": 1,

"generatedAt": "2026-07-05T12:00:00Z",

"dataAsOf": "2026-07-04",

"baseCurrency": "CHF",

"supportedCurrencies": ["CHF", "EUR", "USD"],

"fxRates": {},

"classifications": {},

"etfs": [],

"securities": {},

"sources": [],

"warnings": []

}

``

## Top-level fields

### `schemaVersion`

Version of the JSON contract.

"schemaVersion": 1

Use this so the frontend can detect incompatible future changes.

---

### `generatedAt`

Timestamp when the backend generated the file.

"generatedAt": "2026-07-05T12:00:00Z"

This is technical freshness: “When was this JSON created?”

---

### `dataAsOf`

The effective date of the financial data.

"dataAsOf": "2026-07-04"

This is business freshness: “What date does the ETF/price/FX data represent?”

---

### `baseCurrency`

Default currency used for normalized calculations.

"baseCurrency": "CHF"

The frontend can allow the user to select another display currency later.

---

### `supportedCurrencies`

Currencies known by the dataset.

"supportedCurrencies": ["CHF", "EUR", "USD"]

---

# FX rate schema

Use one base currency and define conversion rates relative to that base.

"fxRates": {

"baseCurrency": "CHF",

"asOf": "2026-07-04",

"rates": {

"CHF": 1.0,

"EUR": 0.96,

"USD": 1.12

}

}

## Interpretation

If `baseCurrency` is `CHF`, then:

valueInCHF = valueInCurrency / fxRates.rates[currency]

Example:

USD 112 / 1.12 = CHF 100

EUR 96 / 0.96 = CHF 100

Alternatively, you can define rates as:

1 unit of currency = X CHF

That is often easier.

I recommend using this clearer model instead:

"fxRates": {

"baseCurrency": "CHF",

"asOf": "2026-07-04",

"ratesToBase": {

"CHF": 1.0,

"EUR": 1.04,

"USD": 0.89

}

}

Then:

valueInBase = valueInOriginalCurrency × ratesToBase[originalCurrency]

``

This is less ambiguous, so I would use `ratesToBase`.

---

# ETF object schema

Each ETF should be an object in the `etfs` array.

{

"id": "IE00B4L5Y983",

"isin": "IE00B4L5Y983",

"tickers": [

{

"ticker": "IWDA",

"exchange": "LSE",

"currency": "USD",

"primary": true

}

],

"name": "iShares Core MSCI World UCITS ETF",

"shortName": "iShares MSCI World",

"provider": "iShares",

"domicile": "Ireland",

"fundCurrency": "USD",

"tradingCurrency": "USD",

"assetClass": "Equity",

"replicationMethod": "Physical",

"distributionPolicy": "Accumulating",

"ter": 0.20,

"status": "active",

"price": {

"amount": 105.42,

"currency": "USD",

"asOf": "2026-07-04"

},

"nav": {

"amount": 105.31,

"currency": "USD",

"asOf": "2026-07-04"

},

"holdings": [],

"exposures": {},

"dataQuality": {},

"sourceRefs": []

}

---

## Required ETF fields for MVP

For version 1, I would require only these:

{

"id": "IE00B4L5Y983",

"isin": "IE00B4L5Y983",

"name": "iShares Core MSCI World UCITS ETF",

"provider": "iShares",

"fundCurrency": "USD",

"assetClass": "Equity",

"status": "active",

"price": {

"amount": 105.42,

"currency": "USD",

"asOf": "2026-07-04"

},

"holdings": [],

"dataQuality": {}

}

Everything else can be optional.

---

# ETF lifecycle status

Use an enum-like string.

"status": "active"

Recommended values:

active

inactive

delisted

merged

replaced

temporarily_unavailable

data_unavailable

For replaced ETFs:

{

"status": "replaced",

"replacementEtfId": "IE00BK5BQT80"

}

For merged ETFs:

{

"status": "merged",

"mergedIntoEtfId": "IE00BK5BQT80"

}

This lets the frontend show meaningful warnings instead of breaking old saved portfolios.

---

# Holdings schema

Each ETF has a `holdings` array.

"holdings": [

{

"securityId": "US0378331005",

"isin": "US0378331005",

"name": "Apple Inc.",

"ticker": "AAPL",

"weight": 4.82,

"quantity": null,

"marketValue": null,

"currency": "USD",

"country": "US",

"region": "North America",

"sector": "Information Technology",

"industry": "Technology Hardware",

"assetClass": "Equity"

}

]

## Important: define `weight`

Use percent, not decimal.

"weight": 4.82

Meaning:

Apple is 4.82% of this ETF.

``

This is easier to inspect manually.

The frontend calculation is:

holdingValue = etfPositionValue × holding.weight / 100

---

# Security master: optional but recommended

Instead of repeating all security metadata in every ETF holding, you can also define a `securities` dictionary.

"securities": {

"US0378331005": {

"id": "US0378331005",

"isin": "US0378331005",

"name": "Apple Inc.",

"ticker": "AAPL",

"currency": "USD",

"country": "US",

"region": "North America",

"sector": "Information Technology",

"industry": "Technology Hardware",

"assetClass": "Equity"

}

}

Then ETF holdings can be shorter:

"holdings": [

{

"securityId": "US0378331005",

"weight": 4.82

}

]

## My recommendation

For MVP, use the **hybrid approach**:

- Keep `securityId` and `weight` in holdings.
- Also duplicate the most important display fields in each holding.

This makes the frontend simpler and makes the JSON easier to debug.

Later, if the file becomes huge, you can normalize into `securities`.

---

# Exposure summaries

Pre-computing exposures is useful.

Even though the frontend can calculate exposures from holdings, the backend should include ETF-level summaries where available.

"exposures": {

"sectors": [

{

"id": "information_technology",

"name": "Information Technology",

"weight": 23.5

},

{

"id": "financials",

"name": "Financials",

"weight": 15.2

}

],

"regions": [

{

"id": "north_america",

"name": "North America",

"weight": 68.2

},

{

"id": "europe",

"name": "Europe",

"weight": 18.7

}

],

"countries": [

{

"id": "US",

"name": "United States",

"weight": 65.1

},

{

"id": "CH",

"name": "Switzerland",

"weight": 3.4

}

],

"assetClasses": [

{

"id": "equity",

"name": "Equity",

"weight": 100.0

}

],

"currencies": [

{

"id": "USD",

"name": "US Dollar",

"weight": 72.4

},

{

"id": "EUR",

"name": "Euro",

"weight": 12.8

}

]

}

## Why include this?

Because some ETF providers may publish sector/region summaries even when full holdings are incomplete.

Your frontend can choose:

1. Use full holdings if available.
2. Fall back to precomputed ETF exposure summaries.
3. Show warning if neither is available.

---

# Classification dictionary

Use a central dictionary to keep names consistent.

"classifications": {

"assetClasses": {

"equity": {

"name": "Equity"

},

"bond": {

"name": "Bond"

},

"cash": {

"name": "Cash"

},

"commodity": {

"name": "Commodity"

},

"real_estate": {

"name": "Real Estate"

},

"other": {

"name": "Other"

}

},

"regions": {

"north_america": {

"name": "North America"

},

"europe": {

"name": "Europe"

},

"asia_pacific": {

"name": "Asia Pacific"

},

"emerging_markets": {

"name": "Emerging Markets"

},

"other": {

"name": "Other"

}

},

"sectors": {

"information_technology": {

"name": "Information Technology"

},

"financials": {

"name": "Financials"

},

"health_care": {

"name": "Health Care"

},

"consumer_discretionary": {

"name": "Consumer Discretionary"

},

"industrials": {

"name": "Industrials"

},

"other": {

"name": "Other"

}

}

}

This avoids inconsistent labels like:

IT

Information Technology

Technology

Info Tech

---

# Data quality schema

Each ETF should include `dataQuality`.

"dataQuality": {

"holdingsAsOf": "2026-07-04",

"priceAsOf": "2026-07-04",

"holdingsCoveragePercent": 99.2,

"numberOfHoldings": 1472,

"weightSum": 99.87,

"isStale": false,

"missingFields": [],

"warnings": []

}

Example with warnings:

"dataQuality": {

"holdingsAsOf": "2026-06-30",

"priceAsOf": "2026-07-04",

"holdingsCoveragePercent": 92.4,

"numberOfHoldings": 531,

"weightSum": 96.8,

"isStale": false,

"missingFields": ["currency"],

"warnings": [

{

"code": "LOW_HOLDINGS_COVERAGE",

"message": "Holdings coverage is below 95%."

},

{

"code": "WEIGHT_SUM_NOT_100",

"message": "Holding weights sum to 96.8%."

}

]

}

This is important because portfolio-level calculations should not pretend to be exact when source data is incomplete.

---

# Source references

Top-level sources:

"sources": [

{

"id": "ishares",

"name": "iShares",

"type": "provider",

"url": "[https://www.ishares.com](https://www.ishares.com/)",

"retrievedAt": "2026-07-05T11:30:00Z"

},

{

"id": "fx",

"name": "FX data provider",

"type": "fx",

"url": "[https://example.com](https://example.com/)",

"retrievedAt": "2026-07-05T11:35:00Z"

}

]

ETF references:

"sourceRefs": ["ishares", "fx"]

This makes source tracing easier without repeating source details on every ETF.

---

# Complete example `etf-data.json`

Here is a compact but realistic example.

{

"schemaVersion": 1,

"generatedAt": "2026-07-05T12:00:00Z",

"dataAsOf": "2026-07-04",

"baseCurrency": "CHF",

"supportedCurrencies": ["CHF", "EUR", "USD"],

"fxRates": {

"baseCurrency": "CHF",

"asOf": "2026-07-04",

"ratesToBase": {

"CHF": 1.0,

"EUR": 1.04,

"USD": 0.89

}

},

"classifications": {

"assetClasses": {

"equity": {

"name": "Equity"

},

"bond": {

"name": "Bond"

},

"cash": {

"name": "Cash"

},

"commodity": {

"name": "Commodity"

},

"real_estate": {

"name": "Real Estate"

},

"other": {

"name": "Other"

}

},

"regions": {

"north_america": {

"name": "North America"

},

"europe": {

"name": "Europe"

},

"asia_pacific": {

"name": "Asia Pacific"

},

"emerging_markets": {

"name": "Emerging Markets"

},

"other": {

"name": "Other"

}

},

"sectors": {

"information_technology": {

"name": "Information Technology"

},

"financials": {

"name": "Financials"

},

"health_care": {

"name": "Health Care"

},

"industrials": {

"name": "Industrials"

},

"consumer_discretionary": {

"name": "Consumer Discretionary"

},

"other": {

"name": "Other"

}

}

},

"etfs": [

{

"id": "IE00B4L5Y983",

"isin": "IE00B4L5Y983",

"tickers": [

{

"ticker": "IWDA",

"exchange": "LSE",

"currency": "USD",

"primary": true

}

],

"name": "iShares Core MSCI World UCITS ETF",

"shortName": "iShares MSCI World",

"provider": "iShares",

"domicile": "Ireland",

"fundCurrency": "USD",

"tradingCurrency": "USD",

"assetClass": "Equity",

"replicationMethod": "Physical",

"distributionPolicy": "Accumulating",

"ter": 0.2,

"status": "active",

"price": {

"amount": 105.42,

"currency": "USD",

"asOf": "2026-07-04"

},

"nav": {

"amount": 105.31,

"currency": "USD",

"asOf": "2026-07-04"

},

"holdings": [

{

"securityId": "US0378331005",

"isin": "US0378331005",

"name": "Apple Inc.",

"ticker": "AAPL",

"weight": 4.82,

"currency": "USD",

"country": "US",

"region": "north_america",

"sector": "information_technology",

"industry": "Technology Hardware",

"assetClass": "equity"

},

{

"securityId": "US5949181045",

"isin": "US5949181045",

"name": "Microsoft Corp.",

"ticker": "MSFT",

"weight": 4.31,

"currency": "USD",

"country": "US",

"region": "north_america",

"sector": "information_technology",

"industry": "Software",

"assetClass": "equity"

}

],

"exposures": {

"sectors": [

{

"id": "information_technology",

"name": "Information Technology",

"weight": 23.5

},

{

"id": "financials",

"name": "Financials",

"weight": 15.2

}

],

"regions": [

{

"id": "north_america",

"name": "North America",

"weight": 68.2

},

{

"id": "europe",

"name": "Europe",

"weight": 18.7

}

],

"countries": [

{

"id": "US",

"name": "United States",

"weight": 65.1

},

{

"id": "CH",

"name": "Switzerland",

"weight": 3.4

}

],

"assetClasses": [

{

"id": "equity",

"name": "Equity",

"weight": 100.0

}

],

"currencies": [

{

"id": "USD",

"name": "US Dollar",

"weight": 72.4

},

{

"id": "EUR",

"name": "Euro",

"weight": 12.8

}

]

},

"dataQuality": {

"holdingsAsOf": "2026-07-04",

"priceAsOf": "2026-07-04",

"holdingsCoveragePercent": 99.2,

"numberOfHoldings": 1472,

"weightSum": 99.87,

"isStale": false,

"missingFields": [],

"warnings": []

},

"sourceRefs": ["ishares", "fx"]

}

],

"securities": {

"US0378331005": {

"id": "US0378331005",

"isin": "US0378331005",

"name": "Apple Inc.",

"ticker": "AAPL",

"currency": "USD",

"country": "US",

"region": "north_america",

"sector": "information_technology",

"industry": "Technology Hardware",

"assetClass": "equity"

},

"US5949181045": {

"id": "US5949181045",

"isin": "US5949181045",

"name": "Microsoft Corp.",

"ticker": "MSFT",

"currency": "USD",

"country": "US",

"region": "north_america",

"sector": "information_technology",

"industry": "Software",

"assetClass": "equity"

}

},

"sources": [

{

"id": "ishares",

"name": "iShares",

"type": "provider",

"url": "[https://www.ishares.com](https://www.ishares.com/)",

"retrievedAt": "2026-07-05T11:30:00Z"

},

{

"id": "fx",

"name": "FX data provider",

"type": "fx",

"url": "[https://example.com](https://example.com/)",

"retrievedAt": "2026-07-05T11:35:00Z"

}

],

"warnings": []

}

---

# Recommended minimal schema for MVP

If you want to start lean, use this first:

{

"schemaVersion": 1,

"generatedAt": "2026-07-05T12:00:00Z",

"dataAsOf": "2026-07-04",

"baseCurrency": "CHF",

"fxRates": {

"baseCurrency": "CHF",

"asOf": "2026-07-04",

"ratesToBase": {

"CHF": 1.0,

"EUR": 1.04,

"USD": 0.89

}

},

"etfs": [

{

"id": "IE00B4L5Y983",

"isin": "IE00B4L5Y983",

"ticker": "IWDA",

"name": "iShares Core MSCI World UCITS ETF",

"provider": "iShares",

"currency": "USD",

"assetClass": "equity",

"status": "active",

"price": {

"amount": 105.42,

"currency": "USD",

"asOf": "2026-07-04"

},

"holdings": [

{

"securityId": "US0378331005",

"isin": "US0378331005",

"name": "Apple Inc.",

"ticker": "AAPL",

"weight": 4.82,

"currency": "USD",

"country": "US",

"region": "north_america",

"sector": "information_technology",

"assetClass": "equity"

}

],

"dataQuality": {

"holdingsAsOf": "2026-07-04",

"holdingsCoveragePercent": 99.2,

"weightSum": 99.87,

"warnings": []

}

}

]

}

This is enough to build:

- ETF selector,
- saved portfolio,
- total value,
- top holdings,
- region chart,
- sector chart,
- asset-class chart,
- currency conversion.

---

# Frontend calculation contract

The frontend should assume:

## ETF position value

positionValueInEtfCurrency = quantity × etf.price.amount

positionValueInBaseCurrency =

positionValueInEtfCurrency × fxRates.ratesToBase[etf.price.currency]

## Holding exposure

holdingExposureInBaseCurrency =

positionValueInBaseCurrency × holding.weight / 100

## Aggregated portfolio holding weight

holdingPortfolioWeight =

holdingExposureInBaseCurrency / totalPortfolioValueInBaseCurrency × 100

---

# Validation rules for the backend

Before writing `etf-data.json`, your Python script should check:

1. Every ETF has:

    - `id`
    - `isin`
    - `name`
    - `price.amount`
    - `price.currency`
    - `holdings`
2. Every holding has:

    - `securityId`
    - `name`
    - `weight`
3. `weightSum` is calculated.

4. If `weightSum` is far from 100, add warning.

5. Every currency used has an FX rate.

6. Every classification ID exists or is mapped to `other`.

7. Duplicate ETFs are removed or merged by `id`.

8. Duplicate securities are merged by `securityId`.


---

# My recommendation

Start with the **minimal schema**, but reserve field names from the full schema. In other words:

- Use `id` as stable ETF key.
- Use ISIN as default `id` where available.
- Use `ratesToBase`, not ambiguous FX rates.
- Use percent weights, e.g. `4.82`, not decimal `0.0482`.
- Include `dataQuality` from the beginning.
- Include `status` from the beginning.
- Add `exposures` later if needed.

That gives you a clean MVP without painting yourself into a corner.
