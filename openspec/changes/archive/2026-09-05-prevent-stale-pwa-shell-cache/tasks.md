## 1. Cache Generation Implementation

- [x] 1.1 Define the cache-sensitive PWA asset set and implement deterministic generation of a deployment revision from those inputs.
- [x] 1.2 Update the publishing flow to inject the generated revision into a published service-worker copy without modifying the source worker in place.
- [x] 1.3 Preserve service-worker precaching, runtime caching, activation cleanup, root scope, and local development behavior while using the generated cache identity.

## 2. Deployment Validation

- [x] 2.1 Extend the publishing script to validate that generated worker metadata matches the calculated publication revision before the Pages tree is accepted.
- [x] 2.2 Extend public deployment validation to inspect the manifest, service worker, shell assets, and cache-generation marker as one coherent publication.
- [x] 2.3 Ensure generation failures and mixed-generation assets fail clearly before publication and document the rollback/update-cycle behavior.

## 3. Regression Coverage

- [x] 3.1 Add web contract tests for the revision marker, generated worker expectations, and unchanged-input determinism.
- [x] 3.2 Add a regression test proving that changing the manifest or another precached shell asset produces a new cache identity and cannot reuse the prior shell cache.
- [x] 3.3 Add publishing/deployment validation tests for missing, malformed, or inconsistent generation metadata while retaining existing PWA asset checks.

## 4. Verification

- [x] 4.1 Run focused web and publishing tests, then run the complete test suite.
- [x] 4.2 Exercise a generated publication locally and verify the service worker serves the current manifest offline after activation.
- [x] 4.3 Review deployment documentation and confirm the change does not add Firefox `beforeinstallprompt` behavior or alter portfolio workflows.
