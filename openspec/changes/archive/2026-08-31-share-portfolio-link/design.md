## Context

The web app is a static JavaScript application published to GitHub Pages. The editable portfolio is held in `state.portfolio` as an array of ETF ISIN and share-count objects, persisted in browser `localStorage`, while catalog metadata and ETF snapshots are loaded from the deployed static files. There is no server-side persistence or share API.

The feature needs to transfer a portfolio between browsers without exposing a new service dependency. The link must reproduce the selection and share counts, while accepting that the recipient uses the latest catalog and snapshot data published with the application.

## Goals / Non-Goals

**Goals:**

- Create a portable link from the Portfolio tab containing the current portfolio.
- Load a valid linked portfolio during bootstrap before local portfolio fallback.
- Preserve the existing `{ isin, shares }` state shape and rendering pipeline.
- Validate untrusted URL data and provide clear feedback for malformed or stale links.
- Keep the feature compatible with local development and static GitHub Pages hosting.

**Non-Goals:**

- Server-side share records, short URLs, accounts, or access control.
- Pinning a link to historical catalog or ETF snapshot data.
- Sharing private user information; the payload contains only portfolio identifiers and share counts.
- Synchronizing later edits between the sender and recipient.

## Decisions

### Encode state in the URL fragment

The share action will serialize a versioned object such as `{ version: 1, portfolio: [{ isin, shares }] }` into a URL-safe encoded value under a fragment key such as `portfolio`. The fragment works on static hosting and is not sent in HTTP requests. A small JSON payload is sufficient for the expected number of positions, so no compression dependency is needed initially.

Alternatives considered:

- Query parameters are also stateless, but require more escaping and expose portfolio data in request URLs and server logs.
- A server-backed identifier would produce shorter links and permit revocation or historical data, but would add storage, an API, and operational complexity incompatible with the current static-only deployment.

### Give linked state precedence over local state

Bootstrap will attempt to decode and validate the share payload before reading `localStorage`. A valid linked portfolio replaces the locally stored portfolio and is persisted locally after the catalog has loaded. A missing or invalid payload falls back to the existing local behavior and does not prevent the app from loading.

The initial view for a shared link will be the Portfolio tab so the recipient can immediately see the imported positions. The existing locally stored active tab remains unchanged when no share payload is present.

### Validate at the application boundary

The decoder will require the supported version, an array portfolio, non-empty string ISINs, finite non-negative share counts, and duplicate-free positions. Values will be normalized to the existing state shape rather than accepting arbitrary URL object properties. Unknown ISINs will remain visible through the existing unknown-position handling and warning surface; malformed payloads will be rejected as a whole.

### Use the latest deployed data

The payload will not include holdings, catalog metadata, or snapshot contents. After importing the portfolio, the existing catalog and snapshot loaders will resolve the latest published data. A later data refresh can therefore change exposure details while preserving the shared ETF selections and share counts.

### Provide explicit share and load feedback

The Portfolio tab will expose an accessible share control. Successful link creation will copy the URL when clipboard access is available and report the result in the UI. The app will report whether a shared portfolio was loaded or whether a link was invalid, without blocking normal portfolio editing.

## Risks / Trade-offs

- [Link contents are readable by anyone who receives the link] → Include only ISINs and share counts, and document that links are not private credentials.
- [A large portfolio can produce a long URL] → Use compact field names and base64url encoding; introduce compression or a server-backed short link only if practical portfolio sizes exceed browser and messaging limits.
- [Latest snapshots may differ from the sender's view] → Make the latest-data behavior explicit in the share feedback/documentation and retain the payload version for future evolution.
- [URL data is user-controlled] → Strictly validate decoded values, bound numeric inputs to the same accepted semantics as the UI, and treat decode failures as non-fatal.
- [Clipboard APIs may be unavailable] → Keep the generated URL available for a manual-copy fallback and report the copy outcome.

## Migration Plan

No data migration is required. Existing `localStorage` portfolios remain valid because the shared-link loader falls back to the current storage format. Deploy the static frontend changes together; older deployments simply ignore the new fragment and newer deployments can continue to open links generated by the same payload version.

Rollback consists of publishing the previous static frontend. Existing local portfolios remain unaffected, and shared links become inert on the rolled-back version rather than changing stored data.

## Open Questions

- Whether a successful import should replace local state immediately or first offer an explicit confirmation when the recipient already has positions. The initial implementation can use replacement because the link is an intentional initialization request, but the UI should make the imported state visible.