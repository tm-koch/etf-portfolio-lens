## 1. Share Payload Utilities

- [x] 1.1 Define the versioned portfolio share payload and URL-fragment key in the frontend state module.
- [x] 1.2 Implement URL-safe serialization and deserialization for `{ isin, shares }` positions.
- [x] 1.3 Validate payload version, portfolio shape, identifiers, finite non-negative share counts, and duplicate positions without applying partial state.

## 2. Startup Initialization

- [x] 2.1 Load and validate a shared portfolio during bootstrap before local-storage fallback.
- [x] 2.2 Persist a valid imported portfolio locally, select the Portfolio tab, and preserve existing local behavior when no payload is present.
- [x] 2.3 Preserve valid unknown ISIN positions and surface malformed-link feedback without blocking catalog and snapshot loading.

## 3. Portfolio Sharing UX

- [x] 3.1 Add an accessible Share portfolio control to the Portfolio tab with a stable feedback or fallback URL surface.
- [x] 3.2 Generate a link from the current positions, copy it when supported, and report success or clipboard failure.
- [x] 3.3 Handle empty portfolios and successful or failed imports with concise user-visible status messaging.
- [x] 3.4 Add responsive styling consistent with the existing Portfolio tab controls and mobile layout.

## 4. Verification and Documentation

- [x] 4.1 Extend web contract tests for payload encoding and validation, shared-state precedence, latest-data resolution, and accessibility hooks.
- [x] 4.2 Run the focused web contract test suite and address regressions in existing local-storage initialization behavior.
- [x] 4.3 Document the share-link behavior, readable payload limitation, and latest-data semantics in the web README.