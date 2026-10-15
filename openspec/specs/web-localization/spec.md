# web-localization Specification

## Purpose
Provides users with a consistent English or German interface in the website and installed PWA, including localized financial presentation and offline access.

## Requirements

### Requirement: Select and persist the interface language

The website and installed PWA SHALL let users switch between English (`en-CH`) and German (`de-CH`) at runtime, apply the selected language without a reload, and persist the choice for subsequent visits.

#### Scenario: User switches language
- **WHEN** a user chooses English or German in the language control
- **THEN** the visible interface, document language, and page metadata update to the corresponding locale without a reload

#### Scenario: Saved language is restored
- **WHEN** the user opens the website or PWA after saving a language choice
- **THEN** the saved supported language is applied before the user interacts with the interface

### Requirement: Resolve an initial language preference

When no saved language exists, the application SHALL map a supported browser language preference to English (`en-CH`) or German (`de-CH`) and SHALL default to English (`en-CH`) when no supported preference is available.

#### Scenario: Browser prefers German
- **WHEN** no saved choice exists and the browser's preferred language is German
- **THEN** the application starts in German using the `de-CH` locale

#### Scenario: Browser language is unsupported
- **WHEN** no saved choice exists and the browser's preferred language is not English or German
- **THEN** the application starts in English using the `en-CH` locale

### Requirement: Translate user-facing interface content

All application-authored user-facing text SHALL be available in English and German, including static content, dynamic messages, form labels, accessibility names, chart legends and tooltips, import and share feedback, and document metadata.

#### Scenario: Dynamic content follows the selected language
- **WHEN** the user switches language while viewing generated portfolio, comparison, or Explore content
- **THEN** the visible labels, messages, chart descriptions, tooltips, and accessibility names are rendered in the selected language

#### Scenario: Financial data is not translated as interface copy
- **WHEN** the application renders ETF, company, provider, ticker, or ISIN names
- **THEN** it preserves the canonical source data while translating surrounding interface text

### Requirement: Localize taxonomy labels for display

Sector, region, and other supported classification labels SHALL be presented in the selected language without changing the underlying classification values used for calculations or data exchange.

#### Scenario: Known taxonomy label is displayed
- **WHEN** a supported English taxonomy value is shown in German
- **THEN** its German display label is used while the original value remains unchanged in application data

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

### Requirement: Locales remain available offline

Both supported languages and their translation resources SHALL remain available offline after the application shell has been cached by the website or installed PWA.

#### Scenario: User switches language offline
- **WHEN** the application shell has been cached and the device is offline
- **THEN** the user can switch between English and German and the interface updates without requesting translation resources from the network
