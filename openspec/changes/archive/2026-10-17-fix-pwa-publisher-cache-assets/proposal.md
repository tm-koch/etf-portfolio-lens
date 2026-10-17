# Proposal

## Why

GitHub Pages publication fails while calculating the PWA cache generation because the staging worktree omits `redundancy.js`, even though the cache generator requires and hashes it. The publisher's module-copy contract also misses imports with version-query suffixes, allowing this class of omission to escape detection.

## What Changes

- Ensure the Pages staging list includes `redundancy.js` and stays consistent with the cache-sensitive PWA assets.
- Strengthen the publisher contract check to recognize local JavaScript imports with optional query strings so required modules cannot be silently omitted.
- Preserve the existing published paths and cache-generation behavior.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
None. Existing `pwa-publishing` and `pwa-cache-coherence` requirements already cover publishing required JavaScript assets and validating a complete cache-sensitive shell. This is an implementation and regression-test correction, so the change opts out of delta specs.

## Impact

- `scripts/publish-gh-pages.ps1`
- `scripts/pwa-cache-generation.ps1` as the source of cache-sensitive asset requirements
- `tests/test_web_contract.py`
