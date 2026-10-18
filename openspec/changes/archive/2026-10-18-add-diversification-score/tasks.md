# Tasks

## 1. Diversification calculation

- [x] 1.1 Add a pure diversification-score module that calculates normalized company HHI, inverse HHI, rating, scale maximum, and allocation-weighted disclosed coverage; verify boundary, partial-coverage, zero-coverage, and score-50 cases with focused Node-backed unit tests.

## 2. Explore presentation

- [x] 2.1 Add the responsive diversification score box below pairwise product overlap, following the redundancy score presentation and rendering score, verdict, dynamic bullet bar, and incomplete-coverage warning; verify placement and accessible labels with web contract tests.
- [x] 2.2 Add localized score, rating, coverage-warning, and accessibility strings to all supported locales and add mobile styling that visually hides the warning while preserving it for assistive technology; verify locale key parity and responsive style contracts.
- [x] 2.3 Register any new frontend module and required assets in the service-worker and PWA cache-generation paths; verify the focused PWA cache tests include the new asset.
- [x] 2.4 Remove rating-band captions from the bullet bar and color the verdict badge like redundancy; verify the five badge colors and absence of bar labels with web contract and browser checks.
- [x] 2.5 Add localized rating tooltips to the redundancy and diversification markers and inset both maximum endpoint labels; verify both marker ratings and endpoint spacing with web contract and browser checks.
- [x] 2.6 Add localized hover tooltips to every redundancy and diversification bar section and increase maximum-label clearance to 20px; verify locale switching, all section labels, and max-score spacing with web contract and browser checks.
- [x] 2.7 Remove written redundancy labels beneath its bar and increase the shared track-to-endpoint gap so markers do not overlap endpoint values; verify label absence, endpoint alignment, and marker clearance for both bars.
- [x] 2.8 Right-align both maximum endpoint values with their bar edges while retaining marker clearance; verify right-edge alignment and vertical separation in the browser and web contract.

## 3. Integration verification

- [x] 3.1 Run the complete Python test suite and resolve regressions; verify with `python -m unittest discover -s tests`.