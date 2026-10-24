# Design

## Context

See [proposal.md](proposal.md) for motivation and [the spec delta](specs/portfolio-pdf-export/spec.md) for required behavior. The report already has a localized snapshot/analytics boundary and a PDF-native renderer. Report snapshots capture `weightPct`; the shared roll-up aggregator currently rejects those positions when their raw share-unit total is zero. The PWA launcher icon is already part of the offline shell cache.

## Goals / Non-Goals

**Goals:**
- Extend the current PDF renderer and report data boundary without changing full/private share payload semantics.
- Keep the report local, selectable, localized, and usable offline.
- Preserve existing section content while clarifying the cover, footer, and subsection hierarchy.

**Non-Goals:**
- Introduce a new sharing service, URL format, PDF dependency, or external asset.
- Change portfolio valuation, allocation, or analytics calculations beyond restoring report roll-ups from captured weights.
- Add quantitative meaning to the exposure title bars; they are decorative only.

## Decisions

- **Render a dedicated cover before report sections.** Use the cached 512px PWA launcher icon beside the product title. Group the four provenance fields in a compact two-column metadata block without individual boxes. The cover participates in the same report pagination; section numbering remains independent.
- **Reuse existing portfolio sharing.** Generate the link from the current selected positions using the existing full-share or private-allocation path according to portfolio mode. Pass the URL into the report renderer and add it as a PDF link annotation over localized link text. Do not duplicate or alter payload encoding; omit the link for an empty portfolio.
- **Allow captured weights through roll-up aggregation.** When every report position has a finite captured weight, aggregate from those weights without requiring raw share-unit totals. Continue requiring a nonzero share total when weights were not captured, and continue skipping positions without snapshots.
- **Separate parent-section context from category headings.** Top Companies pages use `2 · Portfolio Analytics` as the running page header and a smaller Top Companies category title. Pairwise pages use `3 · Exposure Analysis` with a smaller Pairwise ETF Overlap title. Repeat the hierarchy on continuation pages.
- **Bound rollup detail.** Sort each exposure rollup by descending weight, display its top 20 labels, and combine any remaining weights into a single localized remainder value.
- **Use aligned gray chart separators.** Set the exposure-column gutter to 10 mm, left-align each title and its thin gray separator, and draw the separator across that chart column. Use four columns for the currency legend while retaining the existing fixed-size donut plots.
- **Keep the footer to one generated line.** On every page show only `ETF Portfolio Lens | Generated: <timestamp>`; omit provenance repeats, page numbers, and separator rules. Place the website link annotation over only the visible `ETF Portfolio Lens` label.

## Risks / Trade-offs

- [The cover adds a page and changes page totals] → Count it in the existing footer sequence and test section starts and totals with short and multi-page reports.
- [10 mm gutters reduce legend width] → Preserve donut dimensions and test long localized legend labels for wrapping and clipping.
- [The embedded portfolio URL may not represent the active mode] → Reuse the same mode selection and encoder path as the existing share actions; test full and private payloads.
- [Some portfolio positions may lack snapshots or valid weights] → Keep the existing unavailable behavior for missing holdings data and only use captured weights when finite.