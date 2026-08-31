## Context

The GitHub Pages publishing script builds a clean detached worktree and copies a curated list of files from `web/`. The application entry module imports `portfolio-import.js`, but that module is absent from the copy list, so the published browser requests a missing module and stops before bootstrap can render navigation or bind controls.

## Goals / Non-Goals

**Goals:**

- Ensure every JavaScript module imported by the published entry point is copied to GitHub Pages.
- Add a focused regression check for the publish asset list and module import relationship.
- Republish and verify the deployed application bootstraps and its primary controls operate.

**Non-Goals:**

- Do not change PDF parsing or import behavior.
- Do not change application navigation or color-mode implementation.
- Do not alter portfolio data, catalog generation, or provenance metadata.

## Decisions

- Add `portfolio-import.js` directly to the existing `$webFiles` list. This matches the current static publishing approach and avoids introducing a bundler or changing module paths.
- Test the deployment manifest at the script/source level and perform a deployed smoke check. A source-only JavaScript unit test would not catch a missing copied asset, while a full browser check confirms bootstrap succeeds.
- Keep the publish script's clean worktree and force-with-lease behavior unchanged; only the required asset set changes.

## Risks / Trade-offs

- [Future imports may add another omitted module] -> Keep the asset-list regression test alongside the publish script and review new imports against the publish list.
- [GitHub Pages may serve cached assets briefly] -> Republish after the fix and verify the deployed module URL returns successfully before testing controls.

## Migration Plan

1. Add the missing module to the publish file list.
2. Run focused tests and publish the site to `gh-pages`.
3. Verify the deployed page loads without module 404s and that navigation, color mode, and portfolio import controls work.
4. Roll back by restoring the previous `gh-pages` commit if the deployment introduces an unexpected issue.

## Open Questions

None.
