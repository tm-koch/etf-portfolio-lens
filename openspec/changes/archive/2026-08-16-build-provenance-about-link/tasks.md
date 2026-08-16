## 1. Publish Provenance

- [x] 1.1 Define the versioned `build-info.json` schema for full source commit, commit timestamp, publish timestamp, aggregate ETF data timestamp, repository URL, and future fields.
- [x] 1.2 Update `scripts/publish-gh-pages.ps1` to generate `build-info.json` from the source `HEAD`, commit metadata, publish time, and published catalog/data timestamp.
- [x] 1.3 Ensure the generated manifest is included in the GitHub Pages publish tree and remains absent-safe for local development.

## 2. About Build Details Surface

- [x] 2.1 Add the secondary `About this build` action to the hero development/status area without adding a primary navigation destination.
- [x] 2.2 Add an accessible build-details dialog or equivalent in-page surface with explicit labels for commit, publish, and ETF data timestamps.
- [x] 2.3 Load and normalize the provenance manifest with non-blocking local/malformed-metadata fallbacks.
- [x] 2.4 Render the full source commit and repository revision link when metadata is available, with an unavailable state otherwise.
- [x] 2.5 Add extensible rendering space for future provenance or diagnostic metadata without changing the primary navigation contract.
- [x] 2.6 Style the secondary action and build-details surface consistently across desktop and mobile layouts, including focus and close states.

## 3. Verification

- [x] 3.1 Verify the publish workflow generates a manifest whose commit and commit timestamp match the source `HEAD`, and whose publish and data timestamps are distinct fields.
- [x] 3.2 Verify the About action opens and closes accessibly without changing URL/history or the Portfolio, Compare, and Explore navigation.
- [x] 3.3 Verify all three timestamps, full commit identifier, and source revision link render correctly with valid metadata.
- [x] 3.4 Verify local missing and malformed manifests do not block the core UI and show a clear unavailable/local-development state.
- [x] 3.5 Verify the surface remains readable and usable at mobile and desktop widths and that future metadata fields can be added without structural changes.
