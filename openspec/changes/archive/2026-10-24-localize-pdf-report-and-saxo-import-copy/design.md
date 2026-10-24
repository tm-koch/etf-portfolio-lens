# Design

## Context

See `proposal.md` for motivation and the two spec deltas for observable behavior. The PDF renderer already requests numbered section headings through translation keys, while report analytics currently pass each contributor's portfolio-weighted value directly to the PDF. The Saxo file-drop instruction already uses a translation key shared by the three locale resources.

## Goals / Non-Goals

**Goals:**
- Reuse the existing localization and PDF rendering paths for translated section headings.
- Make the Top Companies ETF cells represent each contributor's share of its company's total portfolio exposure, consistent with the website and compact preview.
- Update only the localized Saxo file-drop instruction.

**Non-Goals:**
- Translate the ETF Portfolio Lens product name or change other PDF content.
- Change company ranking, total portfolio contribution, portfolio weighting, or Explore/preview calculations.
- Change Saxo PDF markers, recognition, parsing, extraction, review, or import behavior.

## Decisions

- Keep the existing `export.sectionPortfolio`, `export.sectionAnalytics`, and `export.sectionExposure` keys and provide language-appropriate values in each locale. The renderer, continuation headings, and footer-related section hierarchy already consume these keys; adding a parallel PDF localization mechanism would duplicate existing behavior. Keep the product name unchanged.
- Build the footer generation label from the existing `export.generatedAt` translation, the same key used for the cover's generation-time label. This keeps footer and cover terminology aligned in every locale while preserving the brand, timestamp format, page number, and link bounds.
- Convert each present ETF contributor's weighted contribution to a percentage of the company's total contribution when building report analytics: `contributor.weight / company.weight * 100`. Retain the current total contribution separately, and preserve `null` for ETFs that do not contribute so the renderer continues to show an em dash. This matches the website's `shareOfCompany` meaning without changing portfolio calculations. If the company total is zero, report a zero share rather than dividing by zero.
- Replace the value of the existing `ui.dropPdf` translation key in English, German, and Polish. Keep the HTML binding and parser marker logic unchanged; the instruction describes the expected report, it does not add new document-format support.
- Update the locale contract expectations and add a focused report-data/runtime check for normalized ETF shares, including multiple contributors and a non-contributing ETF. Keep existing Saxo parser tests intact and verify only the locale resources and file-drop copy for the import-text change.
- Extend footer runtime coverage to verify English, German, and Polish generation labels match the cover label and that page numbering and website link annotations remain unchanged.

## Risks / Trade-offs

- [A company row's ETF shares may not sum to exactly 100% after display rounding] → Calculate using the unrounded source weights and describe the invariant as 100% before display rounding.
- [A missing contributor could be mistaken for a zero share] → Preserve missing contributors as `null` and retain the renderer's existing em-dash output.
- [A report title could remain English in a secondary page header] → Reuse the same section translation keys for the primary headings and category-page parent headings, and cover all supported locales in contract/runtime tests.
- [Users could infer that English Saxo PDFs are newly supported] → Change only the instruction text and explicitly leave parsing markers and recognition behavior unchanged.

## Migration Plan

No data or preference migration is required. Update locale values and report analytics/rendering behavior with their focused tests. Rollback consists of reverting these presentation and report-output changes; saved portfolios and supported Saxo input files remain unaffected.