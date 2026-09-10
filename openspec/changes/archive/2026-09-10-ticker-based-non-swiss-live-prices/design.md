## Context

The live market-data pipeline currently formats every provider URL with an ETF ISIN and publishes an ISIN-keyed normalized artifact. The registry also contains ETFs listed outside Switzerland whose provider market symbols are exchange-qualified tickers. The workflow runs manually or on a daily schedule, and its generated artifact is committed before the Pages site is published.

This change crosses configuration, quote models, adapter dispatch/parsing, tests, and GitHub Actions. It must preserve the public artifact contract, existing Swiss retrieval, secret isolation, and atomic publication behavior.

## Goals / Non-Goals

**Goals:**

- Add a provider adapter that formats a secret-backed URL with `{ticker}` and parses Yahoo chart JSON into the existing normalized quote model.
- Store provider lookup tickers in quote configuration and quote provenance while retaining ISIN as the stable identity and artifact map key.
- Cover the three currently missing non-Swiss registry ETFs with explicit EUR configuration.
- Run the same validation/publication pipeline when relevant source, configuration, workflow, or backend changes are pushed to `main`.

**Non-Goals:**

- Replace or redesign the existing Swiss CSV adapter.
- Publish provider URLs, raw responses, credentials, or a second ticker-keyed public data model.
- Add intraday scheduling, historical time series, or a new market-data vendor abstraction beyond the adapter interface already in use.
- Change frontend valuation rules or the existing FX provider.

## Decisions

### Keep ISIN canonical and make ticker provider-specific

The quote configuration will require a ticker for ticker-based adapters and may omit it for ISIN-based adapters. Normalized quotes remain keyed by ISIN and continue to carry ISIN identity; ticker is supplementary provenance needed to explain and reproduce the provider lookup. This avoids breaking portfolio joins and existing Swiss configuration.

Alternative considered: key artifacts by ticker. Rejected because tickers are exchange-specific, can be reused, and are not the portfolio's stable security identity.

### Add a dedicated Yahoo chart adapter

The adapter will validate the expected chart response structure, reject provider errors, require EUR metadata for the configured non-Swiss quotes, accept only finite non-negative prices, and convert the Unix market timestamp to the existing UTC timestamp representation. URL formatting will be adapter-aware: `swiss_csv_v1` receives `{isin}`, while `yahoo_chart_v1` receives `{ticker}`.

Alternative considered: make every provider URL accept both identifiers. Rejected because it hides identifier requirements and weakens configuration validation.

### Use one per-entry secret name with a tracked variable convention

Each Yahoo quote entry will refer to `YAHOO_QUOTE_URL_TEMPLATE`, and local/CI setup will provide that name without committing its value. The template contains `{ticker}` and remains secret-backed at runtime. The concrete provider URL is intentionally excluded from public specs and artifacts.

Alternative considered: hard-code the endpoint in repository configuration. Rejected because the existing design treats provider URL templates as deployment secrets and because it would expose source details publicly.

### Add a path-filtered push trigger on main

The workflow will trigger on pushes to `main` only when relevant source, configuration, workflow, or publication inputs change. `data/live_prices.json` is excluded from those paths, so the workflow's own artifact commit does not trigger another run. Manual dispatch and the daily schedule remain available.

Alternative considered: trigger on every `main` push. Rejected because artifact commits and unrelated changes would create unnecessary runs and possible publication loops.

## Risks / Trade-offs

- [Yahoo response shape or metadata changes] -> Keep parsing defensive, test malformed/error responses, and fail atomically rather than publishing partial quotes.
- [Ticker mapping becomes stale] -> Keep the ticker explicit in versioned per-ETF configuration and add registry/config coverage tests for all configured entries.
- [A non-Swiss quote is unavailable outside market hours] -> Preserve the provider's latest valid timestamp and existing no-age-rejection behavior.
- [Push trigger causes duplicate daily/manual runs] -> Keep all triggers, accept explicit duplicate invocations, and ensure path filtering prevents only self-triggered artifact loops.
- [A shared Yahoo template is changed incompatibly] -> Validate placeholder requirements before fetching and keep the secret value out of logs and artifacts.

## Migration Plan

1. Add adapter/model/parser support and focused tests while the existing Swiss configuration remains unchanged.
2. Add the three Yahoo quote entries and provision `YAHOO_QUOTE_URL_TEMPLATE` locally and in GitHub Actions.
3. Run the fetch/validation pipeline and publish the expanded artifact only after all quotes and FX data succeed.
4. Enable the path-filtered `main` push trigger alongside the existing schedule and manual dispatch.
5. Roll back by removing the Yahoo entries or reverting the change; atomic failure preserves the last valid artifact during a failed rollout.

## Open Questions

None for implementation. The provider URL remains an environment-specific secret value and is intentionally not decided in the OpenSpec artifacts.
