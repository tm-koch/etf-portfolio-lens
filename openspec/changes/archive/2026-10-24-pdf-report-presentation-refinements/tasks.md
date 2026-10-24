# Tasks

## 1. Portfolio Score Presentation

- [x] 1.1 Add the PDF-specific localized `Portfolio scores` heading for every supported language and verify localization contract tests pass without changing the Explore heading with `pytest tests/test_web_contract.py -q`.
- [x] 1.2 Render redundancy and diversification verdict badges from existing analytics, remove the Holdings coverage card and caveat, and verify PDF runtime tests cover both scores and the absence of coverage output with `pytest tests/test_web_runtime.py -q`.

## 2. Bright-Mode Badge Colors

- [x] 2.1 Map redundancy and all diversification verdicts to the website's bright-mode palette independently of app color mode, and verify focused runtime tests cover bright and dark app themes with `pytest tests/test_web_runtime.py -q`.
- [x] 2.2 Run the focused web contract and PWA cache-generation tests to verify localized report resources remain compatible with browser and installed-PWA export using `pytest tests/test_web_contract.py tests/test_pwa_cache_generation.py -q`.

## 3. Portfolio Table Missing Values

- [x] 3.1 Render unavailable share/allocation, unit-price, market-value, and portfolio-weight cells as `—` without coercing missing values to zero; add runtime coverage for missing values, catalog-only rows, and genuine zeroes with `pytest tests/test_web_runtime.py -q`.
- [x] 3.2 Verify the em-dash behavior is limited to the Portfolio table and other PDF sections retain localized unavailable labels with `pytest tests/test_web_contract.py -q`.

## 4. Footer and Cover Layout

- [x] 4.1 Add the current page number to the right edge of every footer while retaining the left generation text and brand-only link; verify runtime tests cover page numbering and link bounds with `pytest tests/test_web_runtime.py -q`.
- [x] 4.4 Replace the bare footer page number with the localized current-page-of-total label; verify the current and total values on each page with `pytest tests/test_web_runtime.py -q`.
- [x] 4.2 Center the cover separator vertically and shift the icon, title, and provenance layout down while preserving spacing; add runtime assertions for title/separator order and provenance clearance from the footer with `pytest tests/test_web_runtime.py -q`.
- [x] 4.3 Verify PDF contract assertions retain exact section titles and cover/footer requirements with `pytest tests/test_web_contract.py -q`.
