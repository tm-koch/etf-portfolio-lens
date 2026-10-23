# Design

## Context

The Home H1 uses the existing `ui.heroTitle` translation key in the English, German, and Polish locale files. The selected wording and its localized equivalents are defined in the spec delta. See `proposal.md` for motivation.

## Goals / Non-Goals

**Goals:**
- Keep the English headline concise while retaining the privacy-first and cross-screen messages.
- Use concise, natural German and Polish equivalents with the same intent.
- Preserve runtime locale switching through the existing localization mechanism.

**Non-Goals:**
- Change the hero description, metadata, layout, or other translation strings.
- Change portfolio storage, PDF handling, network requests, or privacy behavior.

## Decisions

- Update only the existing `ui.heroTitle` values, preserving the translation key and current runtime switching behavior. This is smaller and less error-prone than adding a new string or changing localization wiring.
- Use the exact English copy supplied by the user: `Privacy-first ETF portfolio exposure, clear on any screen.` Use concise, natural equivalents rather than literal translations:
  - German: `Datenschutz zuerst. Klare ETF-Portfolio-Exponierung auf jedem Bildschirm.`
  - Polish: `Prywatność przede wszystkim. Ekspozycja portfela ETF czytelna na każdym ekranie.`
- Verify the values for all supported locales and keep the existing translation tests passing; do not add a new dependency or UI behavior.

## Risks / Trade-offs

- [The shortened headline may wrap differently across locales] → Check the Home H1 at narrow and wide viewports; do not lengthen the English source to make every locale identical in length.
- [Privacy-first could be interpreted as a new data-handling guarantee] → Keep implementation limited to copy and leave the supporting privacy details and existing data handling unchanged.