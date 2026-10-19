# Spec Delta

## ADDED Requirements

### Requirement: Identify score bar sections on touch
Each colored section of the redundancy and diversification score bars SHALL show its existing localized rating label in a tooltip when tapped on a touch device. The tooltip SHALL appear directly below the user's finger and identify the tapped band, not the score marker's current rating.

#### Scenario: User taps a redundancy band
- **WHEN** a user taps a colored section of the redundancy score bar
- **THEN** the localized label for that section SHALL appear directly below the finger

#### Scenario: User taps a diversification band
- **WHEN** a user taps a colored section of the diversification score bar
- **THEN** the localized label for that section SHALL appear directly below the finger

#### Scenario: Tapped band differs from the current score rating
- **WHEN** the user taps a bar section other than the section containing the score marker
- **THEN** the tooltip SHALL identify the tapped section rather than the marker's current rating
