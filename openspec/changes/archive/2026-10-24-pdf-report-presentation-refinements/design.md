# Design

## Context

See `proposal.md` for motivation and `specs/portfolio-pdf-export/spec.md` for behavior. PDF analytics and table rows are assembled in the report renderer; footer stamping runs after page layout. The cover currently uses fixed vertical coordinates for its icon, title, separator, and provenance.

## Goals / Non-Goals

**Goals:**
- Keep score values and classifications sourced from existing analytics while refining their PDF presentation.
- Scope em-dash placeholders to missing values in the first Portfolio table.
- Add localized page-of-total numbering without changing the generation text or brand-link bounds.
- Rebalance the cover while retaining clear separation between its title and provenance.

**Non-Goals:**
- Change score calculations, thresholds, diversification bands, portfolio data, or app-wide score UI.
- Change unavailable labels outside the Portfolio table, PDF pagination behavior, report content, or dependencies.
- Change generation footer wording or the link target.

## Decisions

- Add a PDF-specific localized `Portfolio scores` heading and reuse the existing localized score verdicts. Render badges from the existing redundancy level and diversification rating; do not classify scores again in the renderer.
- Resolve badge colors from the website's bright-mode palette independently of the active app theme. Keep the established mapping for all five diversification ratings. Remove coverage output only from the score section; leave coverage calculations untouched elsewhere.
- Use a Portfolio-table-local em-dash placeholder. Check source availability before formatting so missing values do not become zero, while genuine zeroes keep their formatted numeric representation. Do not change the shared unavailable translation.
- Render the localized `export.page` template with current page and total page count as a separate right-aligned value at the printable right margin, with the cover numbered 1. Keep the generation text left-aligned and the hyperlink annotation limited to its brand label.
- Place the cover separator at half the page height and shift the icon, title, and provenance layout by the same vertical offset. Moving the metadata with the title group preserves its spacing below the separator and prevents overlap.

## Risks / Trade-offs

- [A verdict may receive the wrong color or localized label] -> Reuse the established bright-mode mapping and localized verdict labels, with checks for every rating and supported language.
- [Missing values may be displayed as zero] -> Test unavailable and actual-zero cases for each Portfolio table value type.
- [The page number may overlap the timestamp or enter the brand link] -> Keep the number right-aligned and independent, and verify footer text and link bounds at runtime.
- [Shifted cover metadata may approach the footer] -> Preserve existing provenance spacing and verify the final row remains clear of the footer.

## Migration Plan

No stored data or preference migration is required. Update report rendering, localized heading resources, and focused contract/runtime tests together. Existing reports remain compatible; rollback is limited to presentation changes.
