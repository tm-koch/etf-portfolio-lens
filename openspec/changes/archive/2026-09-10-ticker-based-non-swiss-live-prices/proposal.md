## Why

Three ETFs in the registry are listed on non-Swiss exchanges and are absent from the live-price configuration because their providers require exchange-qualified tickers rather than ISIN lookups. This leaves the published portfolio valuation incomplete, and source/configuration changes currently require waiting for the scheduled workflow or manually dispatching it.

## What Changes

- Add a ticker-based Yahoo chart quote adapter with strict response validation for EUR market prices and Unix timestamps.
- Extend quote configuration and normalized quote provenance to carry the provider lookup ticker while retaining ISIN as the stable portfolio identity and artifact key.
- Configure live prices for `IE00BF20LF40` (`EUMD.L`), `LU0908500753` (`LYP6.DE`), and `IE00BCLWRD08` (`IS3H.DE`).
- Add the `YAHOO_QUOTE_URL_TEMPLATE` secret/template convention using `{ticker}` substitution without publishing the resolved URL or secret.
- Trigger the live market-data workflow on relevant pushes to `main`, while excluding the generated live-price artifact from the trigger paths to prevent self-triggering publication loops.
- Preserve atomic validation and publication behavior when ticker-based retrieval or any existing quote/FX source fails.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `live-market-data`: Support ticker-based provider lookup, Yahoo chart normalization, non-Swiss ETF configuration, and ticker provenance while preserving ISIN-keyed normalized artifacts.
- `scheduled-market-data-publication`: Add the relevant `main` push trigger, map the new secret, and prevent workflow recursion from generated artifact commits.

## Impact

- Backend quote models, adapter dispatch, URL-template formatting, and Yahoo response parsing.
- `data/live_price_config.json` and the local environment/CI secret convention.
- GitHub Actions workflow triggers, permissions, and publication flow.
- Live-price and adapter tests, including malformed Yahoo responses and configuration coverage.
- The public artifact gains a non-secret ticker field for configured Yahoo quotes; its ISIN-keyed identity and valuation contract remain stable.
