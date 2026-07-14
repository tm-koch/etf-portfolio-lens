## Context

The repository uses "ETF Lens" as the product name in the browser UI, docs, server text, and error messages. The rename request is repo-wide, but the underlying data model, snapshot identifiers, and file paths should stay stable because they are not part of the brand.

This is a cross-cutting textual branding change across the static web app and documentation surface.

## Goals / Non-Goals

**Goals:**
- Replace visible product name text with "ETF Portfolio Lens" consistently across the repository.
- Preserve all technical identifiers, data keys, ISINs, snapshot paths, and URLs.
- Keep the rename mechanically simple and low risk.
- Maintain the existing product behavior and layout.

**Non-Goals:**
- Renaming code package identifiers, directory names, or snapshot filenames.
- Changing portfolio, chart, or ingestion behavior.
- Reworking the visual design beyond updating the displayed brand text.

## Decisions

- Update only user-visible copy and lightweight metadata.
  - Rationale: the request is a branding rename, not a restructuring of project identity or runtime behavior.
  - Alternatives considered:
    - Rename package names and internal module identifiers. Rejected because it adds churn without user value.
    - Leave some docs unchanged. Rejected because repo-wide consistency matters for branding.

- Keep technical names stable.
  - Rationale: identifiers such as `web/package.json` package name, catalog snapshot paths, and local file locations are operational details, not brand text.
  - Alternatives considered:
    - Rename everything, including package and folder names. Rejected because it risks breaking tooling and creates unnecessary migration cost.

- Treat the rename as a textual consistency pass across multiple files.
  - Rationale: the change is best implemented by updating all occurrences in one sweep and verifying the visible surfaces afterward.

## Risks / Trade-offs

- Some references may still use the old name in generated outputs or cached screenshots. → Mitigation: update documentation and verify the web app in the browser after the rename.
- Changing only visible text may leave internal package names mismatched with the product brand. → Mitigation: document that internal identifiers are intentionally unchanged unless a later cleanup is requested.
- Missed copy fragments can make the rename feel incomplete. → Mitigation: search the repo for old branding and verify the main user-facing surfaces.
