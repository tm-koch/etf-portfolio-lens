# Tasks

## 1. Registry and Published Data

- [x] 1.1 Add validated TER, TER provenance, distribution policy, and explicit investment-universe metadata to registry models and all supplied ETF entries; verify registry loading and invalid/missing metadata tests.
- [x] 1.2 Add verified normalized country identifiers to new holding snapshots while preserving source country labels and unknown diagnostics; verify normalization and snapshot-serialization tests.
- [x] 1.3 Publish TER, distribution, and investment-universe metadata in generated catalog entries; verify catalog-generation tests preserve existing identity, snapshot, and pairwise fields.
- [x] 1.4 Document metadata units, sleeve classifications, and country-bucket reference/version in the repository data documentation; verify the documented fixture ingestion and catalog-refresh command.

## 2. Country Exposure and Optimizer

- [x] 2.1 Implement versioned country-to-exclusive-bucket aggregation, unclassified coverage, and proportional-overlap scoring; verify boundary, unknown-country, Switzerland-separation, and 95% coverage tests.
- [x] 2.2 Implement deterministic search across one-to-five ETF candidates with non-negative weights summing to 100%, weighted TER, company-level effective holdings, exposure tolerance, and fewer-fund tie-breaking; verify deterministic results against constructed portfolios.
- [x] 2.3 Implement custom sleeve matching with explicit developed-World versus all-country-World classification, sleeve totals, and separate resulting look-through exposures; verify overlapping-sleeve and invalid-total tests.
- [x] 2.4 Apply accumulating/distributing filters and independently enabled TER/effective-company limits, including closest-alternative results when constraints conflict; verify each filter, limit, and no-qualifying-mix scenario.

## 3. Lab Interface

- [x] 3.1 Add the Lab destination and MixLab panel using the existing navigation and responsive layout conventions; verify destination activation, persistence, keyboard access, and empty-portfolio behavior.
- [x] 3.2 Add both modes, the TER/diversification slider, enabled limit controls, distribution filter defaulting to Both, and editable CHF 10,000 value default for percentage portfolios; verify validation and that Lab does not mutate saved portfolio positions.
- [x] 3.3 Render ranked mixes, country/sleeve comparisons, estimated costs, exposure coverage, constraint failures, and methodology disclosures; verify successful, partial-data, and no-qualifying-result states. Keep snapshot dates out of result cards.
- [x] 3.4 Add and validate MixLab localization strings for supported locales; verify locale switching retains the active Lab destination and localizes labels and disclosures.
- [x] 3.5 Place Mix type inside the shared controls card, remove the Distribution policy divider, and add Home summary weighted TER and annual CHF cost with unavailable states; verify localized UI and responsive behavior.
- [x] 3.6 Increase spacing above the Distribution policy selector and show annual TER change as candidate cost minus baseline, so cost improvements are negative; verify responsive spacing and signed currency display.
- [x] 3.7 Ensure hidden consolidation state cards do not occupy layout space and match Explore's 18px vertical card gap between visible Lab boxes; verify both portfolio states at desktop and mobile widths.
- [x] 3.8 Show 0% TER and CHF 0.00 annual cost on Home for an empty portfolio while preserving unavailable states for non-empty portfolios with incomplete data; verify both states.
- [x] 3.9 Default Lab maximum weighted TER and minimum effective companies to available current-portfolio metrics, preserve user edits, and leave the constraints disabled; verify populated, unavailable, and edited states.
- [x] 3.10 Place the fund-sleeve allocation title inside its card and retain accessible group labeling; verify the rendered layout.
- [x] 3.11 Label maximum weighted TER with (%) and limit TER and effective-company inputs to three and one decimal places respectively; verify defaults, typed values, and translations.
- [x] 3.12 Keep fractional constraint values editable while typing and enforce precision when committed; verify fractional TER and effective-company values.

## 4. Integration Verification

- [x] 4.1 Verify the full current-portfolio and custom-sleeve flows at desktop and mobile widths, including chart/readability checks and no horizontal overflow.
- [x] 4.2 Verify MixLab inputs and results do not appear in generated PDF reports, then run the focused web, ingestion, catalog, and OpenSpec validation suites.
- [x] 4.3 Include verified weighted portfolio TER in PDF summary metrics, preserving Home's empty and unavailable states and keeping MixLab state excluded; verify portfolio export behavior.
- [x] 4.4 Add estimated annual CHF TER cost as detail in the PDF TER card, preserving empty and unavailable states; verify portfolio, percentage-only, and incomplete-data cases.
- [x] 4.5 Reduce PDF summary metric card height and adjust text baselines so analytics content does not overlap the footer; verify card layout and footer clearance.
- [x] 4.6 Slightly reduce spacing in the PDF summary metric cards while preserving readable TER detail and footer clearance; verify the renderer layout contract.
