# Spec Delta

## MODIFIED Requirements

### Requirement: Translate user-facing interface content
All application-authored user-facing text SHALL be available in English, German, and Polish, including static content, dynamic messages, form labels, accessibility names, chart legends and tooltips, import and share feedback, document metadata, and the Home headline.

#### Scenario: Dynamic content follows the selected language
- **WHEN** the user switches language while viewing generated portfolio, comparison, or Explore content
- **THEN** the visible labels, messages, chart descriptions, tooltips, and accessibility names are rendered in the selected language

#### Scenario: Financial data is not translated as interface copy
- **WHEN** the application renders ETF, company, provider, ticker, or ISIN names
- **THEN** it preserves the canonical source data while translating surrounding interface text

#### Scenario: Home headline follows the selected language
- **WHEN** the Home tab is displayed in English, German, or Polish
- **THEN** its headline communicates privacy-first ETF portfolio exposure and clarity across screen sizes using the selected locale's wording:
  - English: "Privacy-first ETF portfolio exposure, clear on any screen."
  - German: "Datenschutz zuerst. Klare ETF-Portfolio-Exponierung auf jedem Bildschirm."
  - Polish: "Prywatność przede wszystkim. Ekspozycja portfela ETF czytelna na każdym ekranie."