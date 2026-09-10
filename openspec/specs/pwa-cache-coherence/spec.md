# pwa-cache-coherence Specification

## Purpose
TBD - created by archiving change prevent-stale-pwa-shell-cache. Update Purpose after archive.
## Requirements
### Requirement: Generate a unique cache generation for each shell publication

The publication process SHALL generate a cache generation that changes whenever a precached shell or installability asset changes, and SHALL inject that generation into the published service worker cache identity.

#### Scenario: Shell asset changes between publications

- **WHEN** a manifest, document, application script, stylesheet, or other precached installability asset changes
- **THEN** the next published service worker uses a different cache generation from the prior publication

#### Scenario: Unchanged inputs are republished

- **WHEN** the same cache-sensitive publication inputs are published again
- **THEN** the generated cache generation remains deterministic and the worker does not create an unnecessary new shell cache

### Requirement: Keep the published shell on one generation

The published service worker, manifest, document, and precached shell assets SHALL be validated as one deployment generation before publication is accepted.

#### Scenario: Complete generation is consistent

- **WHEN** validation examines a generated publication tree
- **THEN** it confirms the worker cache identity contains the expected generation and all required shell assets are present and valid

#### Scenario: Generation metadata is missing or inconsistent

- **WHEN** the worker cannot be matched to the expected generation or a required shell asset is absent
- **THEN** validation fails with an actionable error and the inconsistent tree is not accepted as a deployment

### Requirement: Replace obsolete versioned shell caches

When a newly generated service worker activates, it SHALL remove obsolete versioned shell caches while retaining the active generation and SHALL continue serving the current shell offline.

#### Scenario: New worker activates after a shell change

- **WHEN** a worker with a new cache generation activates over an older generation
- **THEN** the old generation is deleted and requests for current precached assets resolve from the new generation

### Requirement: Include live-data publication inputs in validation
The publication process SHALL validate the live-data artifact as part of the same deployment input set used to generate build metadata and runtime cache behavior, while quote refreshes SHALL remain runtime data and SHALL NOT force a shell cache generation change by themselves.

#### Scenario: Frontend shell changes with live-data support
- **WHEN** application code or service-worker handling for live data changes
- **THEN** the published cache generation changes and the deployment is validated as one coherent shell generation

#### Scenario: Only quote values change
- **WHEN** a valid live-price JSON artifact changes but shell assets do not
- **THEN** the artifact is refreshed through runtime caching without requiring an artificial shell generation change

