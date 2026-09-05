## Context

ETF Portfolio Lens is a static JavaScript application published at the root of a GitHub Pages site. It already serves a same-origin manifest, standalone display mode, launcher icons, and a root service worker. The deployed assets currently respond successfully, but Chrome's automatic install popup is browser-controlled and is not guaranteed after every page load. The application has no way to offer installation when Chrome reports that the page is installable.

The change must remain serverless, preserve the existing portfolio workflow, avoid a new dependency, and work with the relative paths used for both local `/web/` development and the root-hosted Pages publication.

## Goals / Non-Goals

**Goals:**

- Give the manifest a correct, stable application identity.
- Provide a conditional install action driven by Chrome's `beforeinstallprompt` event.
- Hide or disable the action when installation is unavailable or the app is already running standalone.
- Handle prompt acceptance, dismissal, and event reuse without blocking startup.
- Validate the deployed manifest, icons, service worker, and install lifecycle.

**Non-Goals:**

- Forcing Chrome to display its automatic popup or bypassing engagement heuristics.
- Building a native Android wrapper, WebAPK, or Play Store package.
- Adding a server endpoint, analytics system, or persistent install-prompt database.
- Changing portfolio storage, sharing, charting, import, or offline data behavior.

## Decisions

### Use the browser-owned install event

Capture `beforeinstallprompt`, call `preventDefault()` only when the application needs to defer the browser prompt, and retain the event until the user invokes the install action. This is the supported integration point and keeps eligibility decisions in Chrome. A custom imitation dialog is rejected because it cannot install the app and would diverge from browser security and UX.

### Render a conditional install control in the existing utility surface

Add one install action to the existing application utility area. It is hidden by default, becomes visible only after a valid install event, and is hidden after `appinstalled` or when standalone display mode is detected. This keeps the control discoverable without adding a marketing panel or changing navigation.

### Use a stable manifest identity and corrected display name

Set the manifest `id` to the published application URL path and correct the misspelled `Portfolio` display name in the manifest, document title, and related PWA documentation. Relative URLs remain necessary because the same files are served from `/web/` locally and from the published root.

### Validate behavior at two levels

Keep fast static contract tests for metadata and event wiring. Add browser validation for manifest resolution, service-worker registration/control, display-mode detection, and a synthetic install-event lifecycle where the browser test environment permits it. A deployment check must also verify the public HTTPS asset URLs and content types.

## Risks / Trade-offs

- [Chrome does not fire `beforeinstallprompt` for every eligible visit] -> Keep the control conditional and document that the browser menu/install badge remains the fallback.
- [Calling `preventDefault()` can suppress the browser's own prompt if the app mishandles the event] -> Defer only after storing the event, invoke it once, and clear it after `userChoice` settles.
- [Relative manifest identity can differ between local and published paths] -> Use a stable relative `id` aligned with the published root and verify resolved manifest values in both contexts.
- [Standalone detection differs across browsers] -> Treat display-mode detection as an enhancement; absence of the event must leave the application fully usable.
- [GitHub Pages deployment can lag source changes] -> Validate the live URL separately from repository file contracts and document the required post-deployment check.

## Migration Plan

1. Update identity metadata and add the conditional install control and event handling.
2. Extend static tests and browser/deployment checks.
3. Publish to GitHub Pages and verify manifest, service worker control, and install availability in Chrome.
4. If the install control causes issues, remove the event listener/control while retaining the valid manifest and service worker; no stored data migration is required.

## Open Questions

- Whether the install control should use only an icon or an icon plus the text `Install app` in the compact utility bar.
- Which browser automation environment can expose a real `beforeinstallprompt` event rather than only testing the handler with a synthetic event.
