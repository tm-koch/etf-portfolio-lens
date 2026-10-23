# Design

## Context

See `proposal.md` for motivation and `specs/portfolio-pdf-export/spec.md` for the report contract. The app is a static client-side site with shared portfolio, catalog, ETF snapshot, live-price, localization, and build-provenance data. Some app views are hidden when inactive, and the Explore company list renders incrementally, so visible DOM is not a complete or stable report source. Installed-PWA exports must not depend on a CDN.

## Goals / Non-Goals

**Goals:**
- Produce a consistent report from one captured view of portfolio and market data.
- Reuse existing calculations and localization while keeping report layout independent of app tabs and theme.
- Keep generation resources available to the offline PWA.
- Preserve readable rows, columns, charts, metadata, and links across variable page counts.

**Non-Goals:**
- Add server-side report generation or transmit portfolio data.
- Change portfolio valuation, allocation, analytics, or color-mode behavior.
- Add pairwise holdings drill-down content or create analytics for ETFs outside the current portfolio.

## Decisions

### Build a dedicated report model and DOM
At generation start, capture the selected scope, portfolio positions, valuation mode, current language, catalog, available ETF snapshots and live prices, and build metadata. Derive report sections from this snapshot using the app's existing calculation and formatting paths. Build a report-only DOM with explicit bright-mode styles rather than capturing application panels. This avoids hidden-tab, theme, and lazy-rendering errors and prevents asynchronous generation from mixing different app states. The full-catalog scope changes only the ETF listing; analytics, comparison charts, company ranking, and pairwise overlap remain based on current portfolio positions.

Alternative considered: print or capture the active application views. This would couple export to navigation state and incomplete or responsive DOM, so it is not used as the report source.

### Use locally bundled html2pdf.js and stamp PDF footers
Bundle a pinned html2pdf.js distribution and its required dependencies under `web/vendor`; do not load export libraries from a CDN. Render the report-only DOM to an A4 landscape PDF with explicit section and row break rules. Split a wide company matrix horizontally into continuation panels when needed, repeating rank, company name, and total-contribution columns in each panel so every current-portfolio ETF contribution remains represented. Render charts from the same report data, not by copying canvases from the live comparison view.

After rendering, use the PDF API to add the page-number/total footer, provenance labels, visible product URL, and clickable link annotation to every page. Keeping these as a post-render pass makes page numbering correct for dynamically added pages and preserves link behavior when HTML rasterization is used.

Alternative considered: browser print CSS or direct vector PDF layout. Print output varies by browser and installed-PWA environment; direct vector layout would require recreating the report's typography, tables, and charts. DOM rendering follows the product note's html2pdf recommendation, with PDF post-processing reserved for pagination metadata and links.

### Keep report styling and font deterministic
Use a report-specific bright stylesheet with the website's Space Grotesk font. Package and serve the font locally, including its license, so it remains available after the PWA shell has been cached. Use the currently selected locale's existing translation and number/date/currency formatting facilities. If individual data or provenance values are unavailable, render a localized unavailable state and continue generating other sections.

Alternative considered: rely on the current remote font stylesheet. That cannot guarantee the requested typeface in an offline PWA and can introduce export timing races.

### Extend the PWA shell and cache checks
Add the local PDF library, font assets, and report code to the service-worker shell resource list and the matching cache-generation validation inputs. Use the existing cache-version generation process so updated resources receive a new cache identity. The export flow reads already cached catalog/snapshot data and does not introduce a network-only generation step.

Alternative considered: lazy-load the PDF dependency from a public CDN. This breaks offline export and adds a third-party request to a private, client-side workflow.

## Risks / Trade-offs

- [DOM-to-canvas rendering rasterizes report text and can soften small text] -> Set an explicit capture scale and minimum report type size; validate representative PDFs at actual A4 landscape size, including long tables and charts.
- [A matrix can exceed page width as portfolio ETF count grows] -> Split ETF contribution columns across continuation panels and repeat identifying columns; never shrink the entire matrix to fit one page.
- [A cached PWA can have incomplete or stale data] -> Capture currently available data and its timestamps together; identify missing fields as unavailable and test the cached offline path.
- [Bundled library or font resources can be omitted from shell caching] -> Keep cache lists and cache-generation validation synchronized, and add a PWA contract test for required export resources.
- [The font or PDF dependency license may impose distribution obligations] -> Retain the dependency's license and the font's license with the bundled assets and review them before implementation is applied.

## Migration Plan

No portfolio or catalog data migration is required. Add the export UI, report module, local library/font assets, and localized strings; update service-worker shell assets and cache-generation checks so a new deployment invalidates the old shell cache. Rollback consists of removing the export entry point and report assets from the shell list and regenerating the cache version; existing portfolio data remains unchanged.
