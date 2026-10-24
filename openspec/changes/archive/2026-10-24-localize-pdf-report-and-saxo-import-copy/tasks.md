# Tasks

## 1. Localize Report and Import Copy

- [x] 1.1 Update the numbered PDF section-heading translations and the Saxo file-drop instruction in all three locale resources; verify the exact English, German, and Polish copy with focused localization contract tests.
- [x] 1.2 Update localization contract expectations for the translated section headings and Saxo instruction; verify `python -m unittest tests.test_web_contract` passes.

## 2. Normalize PDF Company Contributions

- [x] 2.1 Build each present ETF contribution cell as its percentage share of the company's total contribution while preserving total contribution and null missing cells; verify report analytics tests cover multiple contributors, a non-contributor, and a zero total.
- [x] 2.2 Verify the PDF Top Companies table renders normalized ETF shares, retains the portfolio total, and shows an em dash for missing contributors; verify focused PDF renderer runtime tests pass.

## 3. Integration Verification

- [x] 3.1 Run the focused localization, report-data, PDF-renderer, and Saxo import tests together; verify Saxo parser behavior is unchanged.
- [x] 3.2 Validate this OpenSpec change and confirm all required artifacts are complete with `openspec validate localize-pdf-report-and-saxo-import-copy --type change` and `openspec status --change localize-pdf-report-and-saxo-import-copy`.

## 4. Localize Footer Generation Label

- [x] 4.1 Use the cover's generation-time translation for the footer label; verify the footer matches the cover wording in English, German, and Polish while preserving page numbers and link bounds.
- [x] 4.2 Run the focused footer and combined localization, PDF, and Saxo import tests; validate the updated OpenSpec change.