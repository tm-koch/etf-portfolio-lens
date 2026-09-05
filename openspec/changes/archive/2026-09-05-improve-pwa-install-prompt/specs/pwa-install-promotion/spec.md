## ADDED Requirements

### Requirement: Offer installation when the browser makes it available

The application SHALL capture the browser's `beforeinstallprompt` event and expose a user-facing install action only after that event is received. The action SHALL invoke the deferred browser prompt at most once for each event and SHALL remain non-blocking when the event is unavailable.

#### Scenario: Browser reports an installable application

- **WHEN** the browser dispatches `beforeinstallprompt` for the application
- **THEN** the application stores the event, prevents an unsolicited duplicate prompt, and reveals an install action

#### Scenario: User accepts or dismisses installation

- **WHEN** the user activates the install action and the browser prompt resolves
- **THEN** the application records no required server state, clears the consumed event, and hides or resets the action until a new install event is received

#### Scenario: Browser does not support the event

- **WHEN** the application loads without a supported `beforeinstallprompt` event
- **THEN** the existing application remains usable and the install action remains hidden

### Requirement: Reflect installed display state

The application SHALL hide its install action when it is running in an installed standalone display mode or after the browser dispatches `appinstalled`.

#### Scenario: Application is already installed

- **WHEN** the application starts in standalone display mode or receives `appinstalled`
- **THEN** no in-app install action is presented
