# Design

## Context

See [proposal.md](proposal.md) for motivation and [specs/live-market-data/spec.md](specs/live-market-data/spec.md) for the behavior contract. Quote configuration is loaded and processed sequentially; parser and fetch failures currently lack quote-entry context. The workflow already provides the Swiss URL-template secret, and publishing is atomic after all quotes and FX rates validate.

## Goals / Non-Goals

**Goals:**

- Add the CHF WRDUSW quote as a live-data concern without changing holdings-ingestion fixture behavior.
- Identify quote failures by ISIN and adapter, with optional progress per configured quote.
- Keep diagnostics useful without exposing secrets, resolved URLs, or provider response content.

**Non-Goals:**

- Change the live artifact schema or partial-publication behavior.
- Change provider URL templates, credentials, or Swiss CSV parsing rules unless confirming the WRDUSW response exposes a concrete format incompatibility.
- Enable automated UBS holdings ingestion for the fixture-only registry entry.

## Decisions

- **Use the existing Swiss quote path for WRDUSW.** Add a CHF `swiss_csv_v1` quote config entry using the existing Swiss secret name and ISIN substitution. This is consistent with the SIX listing metadata and avoids coupling quote eligibility to the registry's holdings fixture status. If the live source does not return the established dated CSV format, treat that as a separate adapter/source issue rather than relaxing date validation.
- **Add quote identity at the per-entry boundary.** When fetching or parsing a configured quote fails, wrap the failure with its ISIN and adapter before it leaves the quote loop. Do not include the resolved URL or the arbitrary exception text in the public failure message; provide a safe stage/reason summary where available. Preserve the underlying exception for local debugging without printing its traceback in the workflow.
- **Make progress logging explicitly opt-in and enable it in Actions.** A CLI debug flag should log quote start and success/failure with ISIN and adapter, then identify the stage of failure. Do not log HTTP request objects, exception representations, URLs, credentials, or response bodies. The GitHub workflow opts in so a failed run identifies the specific ETF.
- **Retain atomic publication.** A quote failure remains fatal and prevents replacing `data/live_prices.json`; adding diagnostics must not make a partial artifact publishable.

## Risks / Trade-offs

- [Risk] The Swiss source may not return the current dated `Time;Price;Volume` format for WRDUSW. -> Validate the configured source response locally without printing its URL or payload, and keep the existing all-or-nothing failure behavior until it is supported.
- [Risk] Debug output could leak provider details if arbitrary exceptions are logged. -> Emit only allowlisted identifiers, stages, and safe reason summaries; do not log exception strings or tracebacks from the fetch path.
- [Trade-off] The CHF quote is independent of `fixture_only`, so registry metadata continues to describe holdings-ingestion availability rather than quote availability. -> Document and test that separation in the live-data contract.

## Migration Plan

No artifact migration is needed. Deploy the config and CLI/workflow changes together; the existing live-price artifact remains untouched if any configured quote fails. To roll back the new quote independently, remove the WRDUSW quote entry while retaining diagnostics; no prior artifact rewrite is required.
