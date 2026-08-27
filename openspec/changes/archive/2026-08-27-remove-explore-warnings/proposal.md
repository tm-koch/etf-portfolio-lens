## Why

The Explore tab's aggregated view currently ends with a warnings panel that duplicates diagnostic information from the About this build dialog. Removing that panel keeps Explore focused on portfolio exposure and avoids showing an empty or distracting warning area at the bottom of the view.

## What Changes

- Remove the warnings section from the Explore `/aggregated` tab.
- Stop rendering Explore-specific warnings while preserving current-selection warnings in the About this build dialog.
- Remove the duplicate horizontal separator in the About this build dialog so only one separator appears above the warnings section.
- Update the web contract coverage to assert that the Explore warning surface is absent and the build-dialog warning surface remains available.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `compact-explore-preview`: The compact and standard Explore presentations no longer include a warnings panel at the bottom of the aggregated view.
- `build-provenance`: The About this build dialog uses a single separator before its bottom warnings section and does not render a separator for hidden optional details.

## Impact

- `web/index.html`: remove the Explore warning markup.
- `web/app.js`: remove the Explore warning element lookup and rendering call while retaining build-dialog warning rendering.
- `web/styles.css`: prevent hidden optional build details from contributing a visible separator or layout space.
- `tests/test_web_contract.py`: update the UI contract assertions, including the separator behavior.
- No backend, catalog, ingestion, or external dependency changes.
