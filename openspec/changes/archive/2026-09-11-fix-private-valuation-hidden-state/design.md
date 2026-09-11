## Context

Private shared portfolios set `state.portfolioMode` to `percentage`. The renderer then assigns the HTML `hidden` property to the valuation basis control and portfolio-level valuation status box. The existing stylesheet declares `display: grid` for `.portfolio-valuation-control` and `display: inline-flex` for `.portfolio-valuation-status`, so those author rules override the browser's default hidden presentation and leave both elements visible.

The fix is limited to the presentation layer. The existing mode boundary, valuation calculations, share payloads, and full-portfolio behavior are already correct.

## Goals / Non-Goals

**Goals:**

- Make both valuation elements reliably absent when their `hidden` attribute is present.
- Preserve their existing layout and visible behavior for full portfolios.
- Add a focused stylesheet contract test so a future CSS change cannot reintroduce the defect unnoticed.

**Non-Goals:**

- Changing portfolio-mode transitions or share-link decoding.
- Changing valuation calculations, status labels, or animations.
- Hiding valuation UI for full portfolios or changing the PDF import mode.

## Decisions

- Add targeted `[hidden]` selectors for `.portfolio-valuation-control` and `.portfolio-valuation-status` with `display: none`. This directly repairs the two components whose layout declarations override `hidden`.
- Keep the JavaScript `.hidden` assignments as the source of state. CSS will only define the visual contract for that state; it will not infer privacy from URL fragments or other selectors.
- Test both selectors in the existing web contract suite. A source-level assertion is appropriate here because the failure is a static CSS cascade contract and the existing test suite already validates web source contracts without requiring a browser.
- Do not replace the rule with a global `[hidden]` override. A scoped rule minimizes impact on other components that may intentionally define their own hidden behavior.

## Risks / Trade-offs

- [Risk] A future component-specific rule with greater specificity could override the new selectors. -> Mitigation: keep the selectors adjacent to the component display rules and assert their presence in the contract test.
- [Risk] CSS-only coverage does not prove a browser's computed style. -> Mitigation: retain the existing runtime assertions for JavaScript state and verify the focused web test suite after implementation.

## Migration Plan

No data migration is required. Deploy the stylesheet and contract-test change together. Rollback consists of reverting the stylesheet selectors and their test if necessary.

## Open Questions

None.
