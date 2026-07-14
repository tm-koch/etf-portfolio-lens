## Context

The current web app already serves ETF portfolio data and renders a comparison/aggregated experience, but the visual system is dark and heavy, the doughnut charts are not reliably sized, and the local development server binds only to localhost by default. In parallel, the project needs an explicit GitHub Pages publishing guide so the static app and its JSON data can be deployed consistently.

This change affects the frontend layout, chart container strategy, local server defaults, and documentation. It does not change the ETF ingestion backend or the portfolio math.

## Goals / Non-Goals

**Goals:**
- Move the UI to a lighter, white-first visual system.
- Stack sector, region, and currency sections vertically.
- Make Chart.js doughnut charts render reliably inside bounded containers.
- Allow browser access to the local dev server from the same machine and, when desired, from the local network.
- Document the GitHub Pages file tree clearly.

**Non-Goals:**
- Redesigning the data model or changing exposure calculations.
- Adding new authentication or backend services.
- Introducing a build pipeline or frontend framework migration.
- Implementing GitHub Pages deployment automation.

## Decisions

### 1. Use a light, content-forward visual system
The web UI should switch to a mostly white palette with restrained borders, shadows, and background accents. The goal is to reduce visual weight and make the charts and data feel like the primary content.

Alternatives considered:
- Keep the dark glassmorphism look: visually strong, but too heavy for the requested direction.
- A fully minimal monochrome layout: clean, but risks feeling too flat for a data product.

### 2. Make sector, region, and currency vertical sections
The sections should be stacked in a single column so the comparison and aggregation views read like a report rather than a dashboard grid. This reduces horizontal density and improves mobile behavior.

Alternatives considered:
- Keep a three-column layout: compact on desktop, but too cramped and inconsistent with the requested UX.
- Use tabs per metric: less useful because the user wants the categories visible one below the other.

### 3. Constrain Chart.js with fixed-height wrappers
The doughnut charts need a stable container height to prevent runaway canvas growth. The chart canvas should live inside a dedicated wrapper with explicit sizing so Chart.js can calculate radii correctly when `maintainAspectRatio` is disabled.

Alternatives considered:
- Re-enable `maintainAspectRatio`: safer, but less flexible for responsive cards.
- Let the canvas auto-size itself: this caused the current layout failure.

### 4. Make the dev server bind configurable
The server should still work on localhost by default, but the binding should be configurable so device testing can happen on the same network when needed. That keeps the desktop workflow simple while removing the browser access restriction.

Alternatives considered:
- Hardcode `0.0.0.0`: convenient for network testing, but more permissive than necessary.
- Keep localhost only: too restrictive for smartphone or remote browser testing.

### 5. Document a static GitHub Pages file tree
The docs should spell out the files that need to be published and the directory structure expected by GitHub Pages. That reduces ambiguity around what is static content versus source code and helps keep the deployed tree reproducible.

Alternatives considered:
- Mention deployment vaguely in prose: not enough for repeatable publishing.
- Add automation only: useful later, but the immediate need is clarity.

## Risks / Trade-offs

- [Light theme may feel sparse] → Use subtle borders, spacing, and shadows so the UI still feels intentional.
- [Single-column metric sections may use more vertical space] → Accept the trade-off to improve readability and mobile use.
- [Fixed-height chart wrappers may waste space on some screens] → Tune the heights responsively so the charts remain stable without feeling oversized.
- [Network-exposed dev server increases reachability] → Keep localhost as the default and document the wider bind option explicitly.
- [GitHub Pages path mismatches can break asset loading] → Document the publish structure with relative paths and keep the static tree consistent.

## Migration Plan

1. Update the frontend styling to the lighter white theme.
2. Rework the comparison and aggregated layouts into vertical metric sections.
3. Add fixed-height chart wrappers and validate doughnut rendering.
4. Adjust the dev server defaults and document network binding.
5. Update the documentation with the GitHub Pages publish tree and required files.
6. Verify the published file structure against the app’s runtime asset paths before release.

Rollback is straightforward because the change is presentation and documentation focused. If chart sizing or layout changes regress, the UI can fall back to the previous structure without affecting the backend data.

## Open Questions

- Should the server default remain localhost, with an explicit `--host 0.0.0.0` option for LAN testing, or should network binding become the default?
- Should the GitHub Pages documentation describe a root-site deployment only, or also include project-site subpath handling?
- Should the static publish tree include the raw snapshot files directly, or should it publish a compact generated data bundle instead?
