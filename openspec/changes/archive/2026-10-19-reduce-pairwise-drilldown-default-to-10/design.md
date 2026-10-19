# Design

## Context

The pairwise holdings maximum is a persisted developer preference. When storage has no valid value, the application uses a shared default; invalid stored values also fall back to that default. See `proposal.md` and the `pairwise-product-overlap` delta for scope and behavior.

## Goals / Non-Goals

**Goals:**
- Make 10 the default maximum for new or invalid pairwise holdings preferences.
- Preserve valid saved user-selected maxima.

**Non-Goals:**
- Change the allowed values, preference storage key, or the drill-down ranking and display behavior.
- Reset existing users' saved maxima.

## Decisions

- Change the existing default constant from 20 to 10. The loader already uses this constant for missing and invalid preferences, so the behavior remains centralized.
- Keep the current storage key and preference-loading flow. A valid saved value, including 20, remains the user's explicit choice. Changing the key or rewriting saved values would silently discard that choice and is unnecessary for a default-only change.
- Update the focused preference regression assertions for absent and malformed storage values to expect 10; retain the persistence assertion for a valid saved value.

## Risks / Trade-offs

- Users who previously saved a maximum of 20 will continue to see 20. This is intentional because the new value is a default, not a forced cap; users can clear or change their preference through the existing setting.

## Migration Plan

No migration is required. Fresh installations and installations without a valid saved maximum use 10; valid saved maxima are retained.