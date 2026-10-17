# Design

## Context

See [proposal.md](proposal.md) for motivation and [specs/pairwise-product-overlap/spec.md](specs/pairwise-product-overlap/spec.md) for the behavior contract. Catalog generation already receives successful ETF snapshots, and the browser loads the static catalog and per-ETF snapshots for offline use.

## Goals / Non-Goals

**Goals:**
- Keep overlap values, coverage, and the published ETF set in one generated catalog version.
- Preserve the existing offline-first frontend and calculate only the selected matrix presentation in the browser.
- Keep overlap classification consistent between heatmap cells and the score-box warning.

**Non-Goals:**
- Change the aggregate redundancy-score formula or use portfolio allocation weights in pairwise overlap.
- Normalize holdings with incomplete disclosure or fetch pairwise data at runtime.
- Add a general-purpose matrix visualization framework.

## Decisions

### Store pair results in the catalog manifest

Extend `catalog.json` with a top-level pairwise-overlap section containing a metric/version identifier and one record per unordered ETF pair. Identify each ETF by ISIN; record overlap percentage, both ETFs' disclosed coverage percentages, and whether the comparison is available. Generate records in catalog registry order. The existing atomic catalog replacement then publishes the ETF entries and their pair results together.

An alternative is a separate matrix JSON file. That would keep the manifest smaller, but requires coordinated replacement and cache versioning for two related files. A single manifest avoids a mixed-generation state and retains the existing static-fetch model.

### Calculate from snapshot holdings in the backend

For each snapshot, sum disclosed `weight_pct` to derive coverage. Match exact ISIN weights first, then aggregate remaining weight by normalized company identity, preferring `company_id` and falling back to `canonical_name`. This allows share-class identifiers for one company to overlap while ensuring each company's contribution is capped at the smaller total disclosed company weight. Do not renormalize. If either snapshot has no usable holdings or identity data, emit an unavailable pair instead of a measured zero.

Browser-side calculation was considered, but precomputing the values keeps the metric consistent across clients and avoids loading every holdings snapshot solely to construct the matrix.

### Keep the catalog selection semantics

Generate pair records only for the successful snapshots represented by the current catalog run. A full run naturally creates a full matrix; a selected-subset run creates pair records for that subset only. Do not merge pair data from older catalog generations, since that could compare entries whose snapshots and catalog metadata come from different runs.

### Render a selected lower triangle in Explore

Use selected ETF order for row and column labels, and look up each pair without regard to its stored order. Render each unique pair once below the diagonal. Keep the matrix in a fixed-height, bounded-width viewport with its header row and first ETF column sticky. Empty, unavailable, and diagonal cells remain distinct from numeric zero. Threshold classification is a frontend preference applied to the published overlap values, so changing the threshold does not require rebuilding the catalog.

Give all body headers and cells a shared explicit height so empty and sparse rows align with populated rows; keep the column header sizing separate. Use the same theme-aware light-neutral background for the column header row and ETF row labels, with diagonal dash cells and unused cells subtly lighter.

Use the same validated, persisted developer threshold for heatmap marks and the score-box warning. Localize the title, coverage/unavailable labels, threshold setting, and warning text in the supported locales. If an older catalog does not contain pair results, show an unavailable state rather than inferring zero overlap.

At mobile widths, use a compact blue overlap scale with ticker-only visible labels, smaller cells and type, and no per-cell coverage text; keep full names and coverage available through accessible labels. Hide scrollbar tracks without disabling native touch, pointer, or keyboard scrolling. Show a localized legend for the overlap scale, near-identical outline and active threshold, and disclosed coverage range.

At mobile widths, align the Rollups, pairwise heatmap, and Top companies card headings with the Redundancy score heading by sharing its card inset, top spacing, and title size.

## Risks / Trade-offs

- **Catalog size grows quadratically with ETF count** → Store compact unordered-pair records; the registry is bounded and the frontend only renders selected pairs.
- **Fallback company identity may merge distinct securities when ISINs are absent** → Prefer stable company IDs and use canonical names only when no ID exists; keep ISINs authoritative whenever both holdings have them.
- **Older deployed catalogs lack pair data** → Treat missing data as unavailable and regenerate the catalog as part of deployment; do not break loading existing catalog fields.
- **Sticky table headers and first column can overlap on narrow screens** → Use bounded scrolling and explicit sticky-layer backgrounds and stacking order, then verify mobile and desktop layouts.

## Migration Plan

Regenerate the catalog with the backend update command when publishing the frontend change. The frontend remains compatible with existing catalogs by rendering the pairwise section as unavailable until a refreshed catalog is deployed. Rollback uses the prior frontend and catalog together; no user portfolio migration is required. The developer threshold preference is additive and ignored if invalid.
