## Context

The vanilla JavaScript frontend currently formats some CHF summary values with apostrophe-separated thousands, while selected Portfolio values and PDF import review amounts use a less readable fixed-decimal presentation. The requested behavior is presentation-only: users should see consistent CHF and EUR amounts such as `CHF 12'345.67` and `EUR 1'234.56`, while calculations, inputs, persistence, and import semantics remain unchanged.

## Goals / Non-Goals

**Goals:**

- Provide one currency-aware display formatter for supported CHF and EUR monetary values.
- Apply it consistently to Portfolio summary totals, selected position prices and CHF values, and PDF import review values and totals.
- Preserve two decimal places and the existing zero/unavailable behavior.
- Add focused contract coverage for grouping and the affected display paths.

**Non-Goals:**

- Changing numeric input formatting or editable values.
- Changing persisted portfolio data, parsing, currency conversion, or share-count calculations.
- Adding currencies beyond the currently supported CHF and EUR display paths.
- Changing private portfolios' unavailable presentation when absolute values are absent.

## Decisions

Use a generalized currency-aware formatter based on the existing CHF summary formatting behavior. It will format finite monetary values with an English-style decimal point, exactly two fractional digits, and apostrophe replacement for thousands separators, while retaining the currency code as the caller-supplied prefix.

This is preferred over adding display-specific string manipulation at each render site because it gives the Portfolio table, summary, and import review one consistent presentation rule. It is also preferred over changing locale globally because locale behavior would risk altering unrelated labels and numeric inputs.

Keep the formatter at the display boundary. Existing numeric values will continue to flow through the current calculation and persistence paths as numbers; input controls will continue to use raw numeric strings suitable for editing. Private-mode missing absolute values will continue through their existing unavailable branch rather than being passed to the formatter.

Update the existing web contract tests to assert representative CHF and EUR grouping and coverage of the relevant rendered source paths. No new dependency is needed.

## Risks / Trade-offs

- [Risk] A display path may continue to bypass the shared formatter. -> Mitigation: cover summary, selected positions, import review rows, and recalculated import totals in focused contract tests.
- [Risk] Formatting a non-finite or unavailable value could produce misleading text. -> Mitigation: retain existing finite-value guards and unavailable branches before formatting.
- [Risk] Apostrophe grouping may be mistaken for an editable numeric value. -> Mitigation: restrict the formatter to rendered text and preserve raw numeric input values.

## Migration Plan

Implement the formatter and update display call sites, then run the focused web contract tests and the full Python test suite. Rollback consists of reverting the display-only code and test changes; no data migration or persisted-state migration is required.

## Open Questions

None. The requested scope includes both the Portfolio tab and the PDF import review tab.
