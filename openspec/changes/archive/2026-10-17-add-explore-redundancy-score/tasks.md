# Tasks

## 1. Redundancy Calculation

- [x] 1.1 Derive aggregate duplicated exposure and the `1 - 1/n` scale from existing per-security ETF contributions and current normalized portfolio weights; return unavailable when any positive-weight position lacks usable holdings. Verify with focused runtime cases for one, two, three, and four equal-weight identical ETFs, unequal allocations, unique securities, missing holdings, and zero-weight positions.
- [x] 1.2 Add or extend focused runtime tests for score classification at threshold boundaries and locale-formatted percentage output; run `python -m unittest tests.test_web_runtime`.

## 2. Developer Settings and Explore Presentation

- [x] 2.1 Add developer controls for low/moderate and moderate/high thresholds, defaulting to 10% and 25%, persist valid values locally, and reject invalid pairs. Verify default, persistence, and validation behavior in `tests/test_web_runtime.py`.
- [x] 2.2 Add the independent responsive Explore score box and bullet bar after Rollups and before Top companies, with left-aligned threshold-band labels, no extra eyebrow title, and a clear 0% single-ETF state; verify structure, existing-font use, separation from Top companies, and no pair-warning content in `tests/test_web_contract.py`.
- [x] 2.3 Add localized score, band, explanatory, and developer-setting strings in English, German, and Polish; verify all translation keys with `python -m unittest tests.test_web_contract.WebContractTests.test_static_translation_keys_exist_in_all_locales tests.test_web_contract.WebContractTests.test_app_translation_keys_exist_in_all_locales`.

## 3. Integration Verification

- [x] 3.1 Verify score updates after portfolio edits, allocation changes, and developer-threshold changes, and verify unavailable-data and narrow-viewport behavior; run `python -m unittest discover -s tests` and `openspec validate add-explore-redundancy-score`.
