[[ETF Portfolio Lens]]

Claude:

I have a Website called etf Portfolio Lens. The Portfolio consists of predefined etfs incl. Name and isin number.

I want to be able to Import an Excel or pdf sheet that cobtains the etf overview with numer of shares isin and current value.

I want to add a Javascript based Importer that ready in the document, Extrakte the Relevant data and auto fills the portfolio. What is a suitable Format and Javascript Library to use.

Can this idea be implemented?

===

Yes, this is very doable — it's a common pattern (broker/bank statement import). Here's how I'd approach it.

**Recommended libraries**

- **Excel/CSV → [SheetJS (xlsx)](https://sheetjs.com/)** — the standard for parsing .xlsx/.xls/.csv entirely client-side, no server needed. Reads the file into a JSON array of rows, easy to map to columns.
- **PDF → [PDF.js](https://mozilla.github.io/pdf.js/)** (Mozilla's library) — extracts raw text/positions from a PDF in the browser. It does *not* understand tables, so you get text fragments with x/y coordinates that you then have to reconstruct into rows/columns yourself.

**Suitable format**

- For Excel/CSV, define your own fixed template with columns like `ISIN | Name | Shares | Value | Currency` — you control the layout, so parsing is trivial and reliable. This should be your primary/recommended path.
- For PDF, don't try to parse arbitrary broker statements generically — layouts vary too much and it gets fragile fast. Instead:
  - Extract all text with PDF.js
  - Use a regex to find ISINs (fixed format: 2 letters + 9 alphanumeric + 1 check digit — you can even validate the checksum) as anchor points
  - Grab the nearby numeric values on the same line/row for shares and current value
  - Always show a **preview/edit step** before committing the import, since PDF-extracted data should be treated as "best guess"

**Practical architecture**

1. User uploads file → detect type (.xlsx/.csv vs .pdf)
2. Excel path: SheetJS → map columns → validate ISINs against your predefined ETF list
3. PDF path: PDF.js → text extraction → regex/ISIN-anchored parsing → structured rows
4. Both paths feed into the same normalized object: `{isin, name, shares, value}[]`
5. Match against your known ETF list by ISIN (most reliable key — names vary in formatting)
6. Show a review table, let the user confirm/correct, then commit to the portfolio

If you want, I can sketch out actual code for either the SheetJS Excel importer or the PDF.js + regex extractor — which would be more useful to start with?

## Current implementation scope

The first implementation supports Saxo Bank text PDFs only. The Portfolio tab accepts a dropped or selected PDF, parses it locally in the browser with PDF.js, and examines the German `Bestände` holdings sections for the CHF and EUR accounts.

Imported rows are matched by ISIN against the published ETF catalog. Unsupported documents, incomplete rows, and ISINs not present in the catalog remain visible as review warnings and cannot be applied. Before replacing the current portfolio, the review dialog allows the user to change inclusion, shares, price, and currency.

Confirmed positions persist their ISIN, share count, price, source currency, market value, and CHF-normalized value. The initial conversion assumption is fixed at `1 EUR = 1 CHF`. Portfolio, comparison, and Explore weights use the normalized monetary value when available and retain share-count weighting for manually entered positions without imported valuation data. The PDF is not uploaded or stored.

Additional broker adapters and live exchange rates are intentionally deferred.
