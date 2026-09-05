## Context

The PWA is a static site published to GitHub Pages by PowerShell. `web/sw.js` uses a manually maintained cache version and precaches installability assets, including `manifest.json`. A deployment can therefore update public files without changing the cache name, allowing an existing service-worker controller to return an older manifest and shell. The fix must preserve offline-first behavior, require no server API, and remain compatible with local development and the current publishing flow.

## Goals / Non-Goals

**Goals:**

- Make each cache-sensitive publication carry an explicit freshness generation.
- Ensure the generated service worker and its precached shell assets belong to the same publication.
- Fail publication or validation when the generation is missing, inconsistent, or stale.
- Preserve service-worker scope, offline startup, runtime caching, and existing asset paths.
- Add deterministic automated checks that reproduce the stale-manifest failure mode without depending on a live browser.

**Non-Goals:**

- Adding Firefox support for `beforeinstallprompt` or programmatic installation.
- Changing portfolio data formats, application routing, or the service-worker caching strategy beyond cache identity and validation.
- Introducing a backend, CDN dependency, or runtime network service.

## Decisions

### Generate cache identity during publication

The publishing process SHALL derive one deployment revision from the publication inputs and inject it into the published service worker's cache identity. The revision may be a stable content digest or an explicitly generated build identifier, but it MUST change when any precached shell or manifest asset changes. This removes the fragile requirement for a developer to remember a manual `CACHE_VERSION` edit.

Alternatives considered: keeping manual version bumps is the smallest code change but permits the incident to recur; deleting all caches on every activation avoids old cache accumulation but does not help when the active worker itself still serves a stale cache; query-string cache busting is insufficient because the service worker currently normalizes requests with `ignoreSearch`.

### Keep source service worker usable and publish a generated worker

The repository source worker will retain a clear replacement token or revision input, while the publisher writes a generated copy into the Pages tree. Local serving and tests SHALL either use a deterministic development revision or validate the source token separately. This keeps generated deployment metadata out of source-controlled application files and makes the published revision inspectable.

Alternatives considered: committing a versioned source worker on every deployment creates noisy generated diffs; computing the revision in the browser is too late because the worker must select its cache before serving the shell.

### Validate generation and asset consistency

Deployment validation SHALL inspect the published worker and required shell assets, verify that the worker contains the expected current revision, and verify the manifest remains reachable and valid. Contract tests SHALL prove that changing a cache-sensitive asset causes a different generated cache identity and that an old cache cannot satisfy a new publication's shell request.

Alternatives considered: checking only HTTP status and content type misses mixed-generation deployments; checking only the manifest catches the visible symptom but not stale JavaScript or CSS.

## Risks / Trade-offs

- [Risk] A content-derived revision can change for unrelated generated data and increase service-worker updates. -> Mitigation: hash only the explicitly precached shell and installability assets, not runtime snapshots or volatile metadata.
- [Risk] A failed or interrupted publication may leave a worker and shell from different generations temporarily available. -> Mitigation: generate the worker in the staging tree, validate the complete tree before publishing, and retain the existing atomic/replace behavior of the script.
- [Risk] Existing clients remain controlled by the old worker until the browser checks for an update. -> Mitigation: keep activation cleanup, validate update behavior, and document that one normal service-worker update cycle is expected; cache identity prevents the old worker from confusing the new worker once installed.

## Migration Plan

1. Add revision generation and worker templating to the publisher while retaining compatibility with the current source worker.
2. Add local contract tests and deployment validation for revision consistency and changed-shell invalidation.
3. Publish a release containing the new generated worker; its new cache identity causes the browser to install a fresh shell cache and remove obsolete versioned caches during activation.
4. If rollback is required, republish the previous application with a newly generated revision rather than reusing a cache identity from the failed deployment.

## Open Questions

- Choose whether the revision should be a SHA-256 digest of selected assets or a deployment identifier supplied by the publishing environment; both satisfy the contract, but the implementation should favor the option that works consistently in local PowerShell runs and GitHub Pages publishing.
