# Proposal

## Why

On a smartphone, the valuation controls are separated from Entry mode by a large blank region. Browser inspection at 390px showed the valuation-details container occupying 360px of height, making the selector and Live status difficult to associate with the mode control.

## What Changes

- Remove the fixed 360px flex basis from the valuation-details container at phone widths so its height follows its contents.
- Keep the valuation selector and provenance status directly below Entry mode on the same phone-width row, vertically aligning the status with the selector while preserving the desktop layout.
- Add phone-width layout coverage and verify the result in the browser.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-valuation-mode`: Require valuation controls to remain visually grouped with Entry mode on smartphone layouts, without an oversized vertical gap.

## Impact

- `web/styles.css` for phone-breakpoint flex sizing and spacing.
- `tests/test_web_contract.py` for responsive layout contracts.
- Browser verification of the valuation controls at smartphone viewport widths.
