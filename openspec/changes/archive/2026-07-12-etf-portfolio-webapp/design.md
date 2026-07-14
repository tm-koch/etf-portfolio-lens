## Context

The repository already has a Python ingestion backend that writes one normalized JSON snapshot per ETF under `data/raw/<date>/snapshots`. Those snapshots already contain the holdings and aggregate breakdowns needed for the portfolio UX, but there is no frontend yet. The new work needs to be responsive, work on smartphones, and be easy to test locally on a desktop browser.

The biggest constraint is discovery and valuation: the UI needs a stable ETF catalog, and the portfolio tab needs enough valuation data to turn share counts into portfolio weights.

## Goals / Non-Goals

**Goals:**
- Provide a static, responsive ETF portfolio frontend.
- Support local browser persistence for the user portfolio.
- Show comparison charts for sector, region, and currency exposure.
- Show aggregated look-through company exposure ranked by size.
- Support a local development server for desktop testing.
- Keep the frontend independent from live ETF provider APIs at runtime.

**Non-Goals:**
- CSV portfolio import in the initial release.
- Real-time ETF data fetching from external providers in the browser.
- Accounts, authentication, or server-side portfolio storage.
- Historical performance tracking or tax reporting.

## Decisions

### 1. Use a single-page frontend with a small client-side state layer
The frontend should be a React-based SPA served by a local dev server. A small client-side state layer is enough because the application is single-user, mostly read-only, and derives its analytics from local data plus browser-persisted portfolio state.

Alternatives considered:
- Plain JavaScript: simpler dependencies, but the tabbed UI and chart state would become harder to maintain.
- Next.js or a server-rendered app: unnecessary complexity for a static analytics tool.
- Heavy global state management: overkill for this scope.

### 2. Treat backend snapshots as static content and publish a frontend-friendly catalog
The frontend should not crawl `data/raw/<date>/snapshots` directly at runtime. Instead, the build/data pipeline should publish a small catalog manifest plus the ETF snapshot JSON needed by the UI into a browser-served location.

That catalog should include the stable ETF identity and the metadata required by the portfolio UI, including the snapshot path and whatever valuation field is available for share-based calculations.

Alternatives considered:
- Load individual snapshot files by hard-coded path: brittle and poor UX for discovery.
- Parse the snapshot directory in the browser: not practical for static hosting.
- Fetch live provider data on demand: conflicts with the static frontend goal and creates dependency risk.

### 3. Use Chart.js for all comparative donut visualizations
Chart.js is the right fit for the comparison tab because it supports doughnut charts natively, including multiple datasets that can render as concentric rings. That gives a compact way to compare multiple ETFs on sector, region, and currency composition.

Alternatives considered:
- Custom SVG rendering: too much work for little benefit.
- Other chart libraries: possible, but Chart.js already matches the requested chart style and has the needed doughnut behavior.

### 4. Keep company exposure as a ranked list rather than another donut
Aggregated company exposure can grow to many entries, so a sorted list or ranked bars is more readable than a pie-style visualization. The portfolio view should emphasize the largest overlaps first and show whether a company appears in multiple ETFs.

Alternatives considered:
- Another donut chart: visually appealing but low value once the company count grows.
- Treemap: interesting, but less directly comparable to the requested ranking-first behavior.

### 5. Compute portfolio rollups client-side from ETF position weights
Sector, region, currency, and company exposure should be derived in the browser from the selected ETF positions and the latest snapshot data. That keeps the app fast, offline-friendly, and simple to operate without a backend session.

Alternatives considered:
- Server-side aggregation: unnecessary because the portfolio is user-local.
- Storing precomputed portfolio results: harder to keep in sync when the user edits positions.

## Risks / Trade-offs

- [Valuation data may be incomplete] → The share-count workflow depends on ETF valuation fields being available in the published catalog. If they are missing, the frontend will need a fallback or the backend export must be extended.
- [Large holdings datasets may be heavy in the browser] → Load only the selected ETF snapshots and derive portfolio views lazily.
- [Concentric donut charts can become crowded] → Limit the comparison tab to the selected ETF set and keep legends compact.
- [Snapshot freshness can drift] → Surface generated dates and treat the latest published snapshot set as the source of truth.
- [Mobile layout can collapse under dense chart content] → Use stacked cards, collapsible sections, and a single-column mobile layout.

## Migration Plan

1. Add the frontend shell and local dev server.
2. Add a data adapter for the published ETF catalog and snapshot JSON.
3. Implement portfolio entry and browser persistence.
4. Implement the comparison tab with Chart.js donut charts.
5. Implement the aggregated portfolio ranking and rollups.
6. Wire in responsiveness checks for mobile layouts.
7. Add CSV import later as a separate V2 change.

Rollback is straightforward because the frontend is static and the backend ingestion pipeline remains independent. If a published catalog format changes, the adapter can be reverted without touching the ingestion code.

## Open Questions

- Should the published catalog include ETF price, NAV, or another valuation field, and which source is authoritative?
- Should unsupported ETFs be allowed as manual entries in V1, or should the app only accept ETFs present in the published catalog?
- Should the data publication step copy the latest snapshots into a frontend public directory, or should it generate a separate manifest that points at the snapshot files?
- Should the comparison tab allow selecting the number of ETFs freely, or should it cap the chart at a small number for readability?
