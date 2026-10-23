# web-localization Specification

## Purpose
Provides users with a consistent English or German interface in the website and installed PWA, including localized financial presentation and offline access.

## Requirements

### Requirement: Select and persist the interface language

The website and installed PWA SHALL let users switch between English (`en-CH`), German (`de-CH`), and Polish (`pl-PL`) at runtime, apply the selected language without a reload, and persist the choice for subsequent visits.

#### Scenario: User switches language
- **WHEN** a user chooses English, German, or Polish in the language control
- **THEN** the visible interface, document language, and page metadata update to the corresponding locale without a reload

#### Scenario: Saved language is restored
- **WHEN** the user opens the website or PWA after saving a supported language choice
- **THEN** the saved language is applied before the user interacts with the interface

### Requirement: Resolve an initial language preference

When no saved language exists, the application SHALL map a supported browser language preference to English (`en-CH`), German (`de-CH`), or Polish (`pl-PL`) and SHALL default to English (`en-CH`) when no supported preference is available.

#### Scenario: Browser prefers German
- **WHEN** no saved choice exists and the browser's preferred language is German
- **THEN** the application starts in German using the `de-CH` locale

#### Scenario: Browser prefers Polish
- **WHEN** no saved choice exists and the browser's preferred language is Polish
- **THEN** the application starts in Polish using the `pl-PL` locale

#### Scenario: Browser language is unsupported
- **WHEN** no saved choice exists and the browser's preferred language is not English, German, or Polish
- **THEN** the application starts in English using the `en-CH` locale

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

### Requirement: Localize taxonomy labels for display

Sector, region, and other supported classification labels SHALL be presented in the selected English, German, or Polish language without changing the underlying classification values used for calculations or data exchange.

#### Scenario: Known taxonomy label is displayed
- **WHEN** a supported taxonomy value is shown in German or Polish
- **THEN** its translated display label is used while the original value remains unchanged in application data

#### Scenario: Unknown taxonomy label is displayed
- **WHEN** a taxonomy value has no translation
- **THEN** the application displays the original value rather than hiding or replacing it with an empty label

### Requirement: Format values using the selected locale

Numbers, percentages, dates, and currency amounts SHALL use the selected locale's formatting conventions without changing the underlying numeric value or currency.

#### Scenario: Financial values use German formatting
- **WHEN** the selected language is German (`de-CH`)
- **THEN** displayed numbers, percentages, dates, and currency amounts use Swiss German locale formatting

#### Scenario: Financial values use English formatting
- **WHEN** the selected language is English (`en-CH`)
- **THEN** displayed numbers, percentages, dates, and currency amounts use Swiss English locale formatting

#### Scenario: Financial values use Polish formatting
- **WHEN** the selected language is Polish (`pl-PL`)
- **THEN** displayed numbers, percentages, dates, and currency amounts use Polish locale formatting

### Requirement: Locales remain available offline

English, German, and Polish interfaces and their translation resources SHALL remain available offline after the application shell has been cached by the website or installed PWA.

#### Scenario: User switches language offline
- **WHEN** the application shell has been cached and the device is offline
- **THEN** the user can switch among English, German, and Polish and the interface updates without requesting translation resources from the network

### Requirement: Polish count messages use Polish plural forms

Polish count-bearing messages SHALL use the Polish grammatical plural form appropriate to the numeric count while displaying the count using Polish locale formatting.

#### Scenario: Count uses the Polish singular form
- **WHEN** a Polish count-bearing message is rendered with a count of 1
- **THEN** the message uses the Polish singular form

#### Scenario: Count uses the Polish few form
- **WHEN** a Polish count-bearing message is rendered with a count in the few category, such as 2, 3, or 4
- **THEN** the message uses the Polish few form

#### Scenario: Count uses the Polish many form
- **WHEN** a Polish count-bearing message is rendered with a count in the many category, such as 5 or 12
- **THEN** the message uses the Polish many form

#### Scenario: Fractional count uses the Polish other form
- **WHEN** a Polish count-bearing message is rendered with a fractional count
- **THEN** the message uses the Polish other form

### Requirement: Language selector labels adapt to viewport
The language selector SHALL show full localized language names for all choices while expanded at every viewport width. When collapsed, it SHALL show the selected language's full localized name on wide viewports and its `EN`, `DE`, or `PL` abbreviation on smartphone-width viewports. It SHALL NOT show a visible arrow or caret. At smartphone-width viewports, the collapsed language trigger SHALL have the same width and height as the adjacent color-mode trigger and SHALL align with its top and bottom edges.

#### Scenario: Expanded selector shows full names at every width
- **WHEN** the language selector is expanded on a wide or smartphone-width viewport
- **THEN** each choice shows its full localized language name

#### Scenario: Collapsed selector shows the selected name on a wide viewport
- **WHEN** the language selector is collapsed on a viewport wider than 760px
- **THEN** it shows the selected language's full localized name

#### Scenario: Collapsed selector shows an abbreviation on a smartphone viewport
- **WHEN** the language selector is collapsed on a viewport 760px wide or narrower
- **THEN** it shows `EN`, `DE`, or `PL` for the selected language

#### Scenario: Selector has no visible arrow
- **WHEN** the language selector is rendered in either collapsed or expanded state
- **THEN** no visible arrow or caret is shown

#### Scenario: Compact language and color controls have matching dimensions
- **WHEN** the language selector and color-mode selector are collapsed on a viewport 760px wide or narrower
- **THEN** their trigger boxes have equal width and height and share the same top and bottom edges, while the language abbreviation remains visible
