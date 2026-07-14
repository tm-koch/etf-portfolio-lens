## Why

The current site can be published as static files, but the data paths in the frontend assume a root-hosted deployment. This change defines a root-hosted GitHub Pages workflow so the website and its published snapshot data can be pushed to the `gh-pages` branch without rewriting asset URLs.

## What Changes

- Define a root-hosted GitHub Pages publishing flow for the static website.
- Keep the published snapshot URLs root-absolute so the current data loading paths continue to work.
- Publish the frontend and the relevant `data/raw/<date>/snapshots` assets together on the `gh-pages` branch.
- Document or automate the publish tree so the deployed layout is consistent and repeatable.

## Capabilities

### New Capabilities
- `github-pages-root-host-deployment`: the repository can publish the website and relevant data to a root-hosted GitHub Pages target using the `gh-pages` branch.

### Modified Capabilities
- None.

## Impact

- Affects the publish layout for `web/`, `data/`, and the `gh-pages` branch content.
- May require a deployment script or documented publish procedure.
- Does not change portfolio analytics or ingestion behavior.
