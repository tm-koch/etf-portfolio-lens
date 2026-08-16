## Context

ETF Portfolio Lens is a dependency-light static web app published by copying the `web/` bundle and generated data into a GitHub Pages worktree. The browser currently knows about catalog and snapshot data but has no source-commit or deployment metadata. The existing primary navigation is intentionally limited to Portfolio, Compare, and Explore, and the build provenance should not compete with those workflows.

## Goals / Non-Goals

**Goals:**

- Add a discoverable secondary `About this build` action in the hero development/status panel.
- Show the source commit, commit timestamp, publish timestamp, and ETF data timestamp in an accessible build-details surface.
- Generate provenance at publish time from the exact source `HEAD`, the publish event, and the published catalog/data metadata.
- Link the source commit to the repository revision when a repository URL is configured.
- Keep the metadata schema extensible for future fields such as deployment branch, catalog version, or snapshot warnings.
- Provide a useful local-development fallback when no generated manifest exists.

**Non-Goals:**

- Add About to the primary Portfolio/Compare/Explore navigation.
- Change portfolio state, URL/history behavior, chart behavior, or ETF ingestion semantics.
- Add a runtime dependency or require Git access from the browser.
- Treat the publish timestamp as the commit timestamp; these are separate events.
- Replace per-ETF snapshot provenance already available in the data files.

## Decisions

### Generate a static provenance manifest during publishing

The publish script will create a root-level `build-info.json` in the GitHub Pages worktree. It will derive the source commit SHA and commit timestamp from the source `HEAD`, record the publish timestamp at generation time, and use the published catalog's generated data date as the aggregate ETF data timestamp. The published site can then fetch a deterministic manifest without browser access to Git.

A runtime Git lookup was rejected because GitHub Pages serves static files only. Embedding the values directly into `app.js` was rejected because a standalone JSON manifest is easier to inspect, extend, cache, and consume from other tools.

The manifest should contain a stable shape similar to:

```json
{
  "schemaVersion": 1,
  "repositoryUrl": "https://github.com/tm-koch/etf-portfolio-lens",
  "source": {
    "commit": "full-sha",
    "commitTimestamp": "ISO-8601 UTC"
  },
  "publishedAt": "ISO-8601 UTC",
  "data": {
    "timestamp": "catalog-generated-date"
  }
}
```

### Use the catalog date as the aggregate data timestamp

The initial About surface will display the published catalog's `generatedAt` value as the ETF data timestamp. Individual snapshots can retain their own `snapshot.generated_at` and `snapshot.as_of` values for later detailed diagnostics. This avoids making the publish script parse every snapshot merely to display one aggregate date.

A single undifferentiated "last updated" value was rejected because it cannot distinguish code, deployment, and data changes.

### Use a secondary action and native dialog

Add an `About this build` button styled as a secondary text link inside the existing hero status panel. It opens an accessible native `<dialog>` containing the provenance fields and a reserved extensible details area. The action is a button because it opens an in-page surface rather than navigating to a URL; the visible treatment remains link-like and secondary.

Adding a fourth primary tab was rejected because the existing bottom bar represents the portfolio workflow, while provenance is supporting information. A footer-only link was rejected because it is less discoverable, especially on mobile.

### Load metadata with a non-blocking fallback

The frontend will request `./build-info.json` during bootstrap or when the dialog opens. A missing or malformed manifest will not prevent the portfolio UI from loading; the dialog will show a local-development/unavailable state instead. The source commit link will be omitted or disabled when the repository URL or commit is unavailable.

## Risks / Trade-offs

- [The published manifest can become stale if assets are deployed manually] -> Generate it in the same publish script that copies the bundle and data, and use the source `HEAD` used to create the publish worktree.
- [Commit and publish timestamps can be confused] -> Label each value explicitly and use ISO-8601 UTC in the manifest.
- [The catalog date may not represent every ETF snapshot equally] -> Label it as aggregate ETF data/catalog timestamp and preserve detailed per-snapshot provenance for future expansion.
- [A dialog may be inaccessible if focus handling is incomplete] -> Use native `<dialog>`, a labelled title, explicit close control, keyboard Escape behavior, and focus restoration where supported.
- [The additional metadata request could delay app startup] -> Load it independently and never block catalog, snapshot, or portfolio rendering.

## Migration Plan

1. Add the manifest schema and publish-script generation to the web publish flow.
2. Add the secondary About action and dialog markup, loading, and rendering.
3. Verify published and local-development states, timestamp labels, source link behavior, and keyboard accessibility.
4. Roll back by removing the About action and manifest generation; the primary portfolio workflow remains independent.

## Open Questions

- Should the repository URL be configurable as a publish-script parameter or a checked-in project constant?
- Should future data details list every ETF snapshot timestamp, or only the aggregate catalog timestamp plus a count of source snapshots?
