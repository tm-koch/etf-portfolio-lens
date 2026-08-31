## Context

The previous share-link visibility change added a `hidden` attribute to the share-link label and toggles that label from `renderShareFeedback()`. However, `.share-portfolio-url-label` declares `display: grid`, and that author rule overrides the browser's user-agent rule for hidden elements. As a result, the label text remains visible while the nested URL input remains hidden.

## Goals / Non-Goals

**Goals:**

- Make the share-link label fully absent from layout when it has the `hidden` attribute.
- Keep the existing JavaScript state transition that reveals the label and input when a generated URL exists.
- Verify both initial hidden and post-share visible presentation states.

**Non-Goals:**

- Changing share URL generation, clipboard handling, or status text.
- Changing the label/input markup or application state model.
- Introducing a global reset for every hidden element in the application.

## Decisions

Add a component-scoped `.share-portfolio-url-label[hidden] { display: none; }` rule next to the label's existing layout styles. This is preferable to a global `[hidden]` override because it fixes the known cascade conflict without changing the behavior of unrelated controls that may intentionally manage their own display rules.

Retain the existing JavaScript visibility control and readonly input behavior. CSS owns the rendered layout consequence of the `hidden` state, while JavaScript continues to decide when that state changes.

Extend the existing web contract test to assert the scoped hidden selector is present, while retaining the markup and JavaScript assertions from the prior change.

## Risks / Trade-offs

- [Risk] Future share-label display rules could reintroduce the cascade conflict. -> Mitigation: keep the `[hidden]` selector adjacent to the base component rule and cover it in the contract test.
- [Risk] A component-scoped rule does not protect other hidden elements. -> Mitigation: this change intentionally limits scope; other components should define their own hidden overrides only when their styles need them.

## Migration Plan

Update `web/styles.css` and the existing contract test, run focused and full tests, then publish the static site. Rollback consists of reverting the scoped CSS rule and its test assertion.

## Open Questions

None.
