## Why

The scheduled live-data workflow currently commits the generated `data/live_prices.json` artifact to `main` before publishing the site. This adds generated runtime data to the source branch and makes `main` carry deployment output that is only needed by the GitHub Pages site. The workflow should publish validated live data directly to the Pages branch while preserving the existing validation and deployment behavior.

## What Changes

- Remove the workflow step that commits and pushes generated `data/live_prices.json` to `main`.
- Keep generating and validating the live-data artifact in the Actions workspace.
- Publish the validated artifact through the existing GitHub Pages publisher to `origin/gh-pages`.
- Preserve failure behavior so invalid or incomplete live data does not replace the existing Pages publication.
- Update workflow and publishing contract tests and documentation/specification scenarios to describe branch-only publication.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `scheduled-market-data-publication`: Generated live-data refreshes are published without creating a generated-data commit on `main`, while scheduled, manual, validation, secret-handling, and failure semantics remain intact.
- `pwa-publishing`: The Pages publication consumes the validated workspace artifact and publishes it to the configured `gh-pages` branch as part of the deployment tree.

## Impact

- Affected workflow: `.github/workflows/live-market-data.yml`.
- Affected publication contract and tests for `scripts/publish-gh-pages.ps1` and the scheduled workflow.
- `main` will retain any existing historical `data/live_prices.json` file but future scheduled refreshes will no longer update or commit it.
- GitHub Pages continues to expose the current artifact at `data/live_prices.json` and remains the deployment source for the live web application.
