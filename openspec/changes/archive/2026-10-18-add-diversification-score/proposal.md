# Proposal

## Why

The Explore tab shows duplicated ETF exposure and pairwise overlap, but does not summarize how broadly the portfolio is spread across underlying companies. An effective-number score and qualitative rating give users a compact, interpretable view of company concentration, including when holdings coverage is incomplete.

## What Changes

- Add a portfolio diversification score based on the inverse Herfindahl-Hirschman Index (1/HHI) of look-through company weights.
- Show the score, a concentration/diversification verdict, a segmented bullet bar, and disclosed-coverage warning in a new Explore box below product overlap.
- Calculate from available holdings when coverage is partial and identify the covered share; the coverage warning may be hidden on smartphone view.
- Use rating boundaries from the diversification-score reference, with the scale extending beyond 40 when the effective number exceeds 40.

## Capabilities

### New Capabilities
- `portfolio-diversification-score`: Calculate and present an effective-number-of-companies score, classification, scale, and holdings-coverage warning for the selected portfolio.

### Modified Capabilities

## Impact

- Explore portfolio aggregation and score rendering in `web/app.js`.
- Explore markup and responsive styling in `web/index.html` and `web/styles.css`.
- Localized score labels, ratings, accessibility text, and coverage warning in `web/locales/`.
- Frontend tests and OpenSpec capability documentation.