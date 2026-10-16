# Design

## Context

See [proposal.md](proposal.md) for motivation and [specs/portfolio-valuation-mode/spec.md](specs/portfolio-valuation-mode/spec.md) for the behavior contract. Imported values live on individual portfolio positions; full-portfolio mode is stored separately. Imported CHF values can be either stored directly or resolved from an imported source-currency value using available FX data.

## Goals / Non-Goals

**Goals:**
- Use one consistent definition of usable imported valuation for option visibility and portfolio valuation.
- Keep the stored portfolio mode consistent with the options actually available for the current positions.
- Preserve broker position fields when falling back to latest mode.

**Non-Goals:**
- Change the import-review selector, broker parsing, or how imported prices and values are calculated.
- Automatically switch back to imported mode when complete coverage returns; make the option available and leave the active mode at Latest.
- Change percentage-portfolio behavior or private-share payload contents.

## Decisions

1. **Derive eligibility from the current positions and existing imported valuation rules.** Imported valuation is available only for a non-empty shares portfolio when each position resolves to a finite, non-negative CHF value in imported mode. This handles direct stored CHF values and source-currency values that can be converted with available FX, without duplicating valuation policy in the UI. Alternatives considered: showing the option when any position has a value, which permits mixed unavailable results; adding a separate availability flag, which can become stale when positions or FX data change.

2. **Reconcile mode before rendering and persistence.** Re-evaluate eligibility after portfolio load and whenever positions are added or removed. If imported mode is active and coverage is incomplete, switch to Latest before rendering and persist that mode. Once coverage becomes complete again, restore the option but do not silently switch the portfolio back to Imported.

3. **Treat explicit null as missing, not as numeric zero.** Imported parsing can produce `valueChf: null`, while numeric coercion with `Number(null)` yields zero. Imported-value resolution and portfolio/share normalization must preserve that distinction so missing data cannot satisfy the eligibility check. Genuine finite zero values remain valid.

## Risks / Trade-offs

- [Previously normalized null values may already have been saved as zero] → The current data shape cannot reliably distinguish those historical zeros from genuine zero valuations. Correct null handling for newly read and saved data; do not infer a broad migration without evidence that legacy data needs one.
- [FX availability can change imported-mode eligibility for source-currency positions] → Use the same FX-aware resolution as imported valuation and recalculate eligibility when the published live/FX artifact is loaded.

## Migration Plan

No schema migration is required. Existing imported fields remain in storage. On load, an ineligible portfolio in Imported mode falls back to Latest and persists the corrected mode; users can select Imported again if the complete-coverage option is available.
