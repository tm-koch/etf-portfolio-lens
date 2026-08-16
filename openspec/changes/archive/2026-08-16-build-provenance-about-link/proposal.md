## Why

The published static web UI currently provides no reliable way to identify the exact source revision, deployment event, or ETF data generation behind what a user is viewing. A secondary About link will expose this provenance without turning build metadata into a fourth primary portfolio destination.

## What Changes

- Add a secondary `About this build` link in the existing hero development/status area.
- Add an About/build-details surface that displays the source commit, commit timestamp, publish timestamp, and ETF data timestamp.
- Generate a publish-time provenance manifest from Git and the published catalog/snapshot metadata so the static site can display trustworthy values.
- Link the displayed source commit to the corresponding repository revision when a repository URL is available.
- Provide a clear local-development or unavailable-metadata fallback when the generated manifest is absent.
- Structure the build-details data so additional provenance or diagnostic fields can be added later without changing the navigation model.
- Keep Portfolio, Compare, and Explore as the only primary navigation destinations.

## Capabilities

### New Capabilities

- `build-provenance`: Expose source, deployment, and ETF data timestamps through a secondary About/build-details surface and generated publish metadata.

### Modified Capabilities

## Impact

- `web/index.html`, `web/app.js`, and `web/styles.css`: Add and present the secondary About link and build-details surface.
- `scripts/publish-gh-pages.ps1`: Generate and publish the provenance manifest from the source commit, publish time, and catalog/snapshot data metadata.
- `web/data.js` or a nearby frontend data-loading module: Load and normalize provenance metadata with a local fallback.
- No change to the primary navigation destinations, portfolio state, browser URL/history behavior, or external runtime dependencies.
