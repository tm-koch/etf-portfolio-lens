## Context

The repository has a registry-driven Python ingestion pipeline, a reusable Amundi full-composition fetcher, a normalized live-price artifact keyed by ISIN, and a vanilla JavaScript portfolio import/valuation flow. The existing valuation model already distinguishes a live quote currency from an imported position currency and converts supported non-CHF sources through published FX rates.

Amundi Prime All Country World UCITS ETF Dist (`IE0009HF1MK9`) has a USD share-class currency but multiple exchange listings. The intended SIX listing for Saxo is `WEBGCHF SW`, whose traded price is in CHF; the same fund also has a USD SIX listing (`WEBG SW`). The supplied workbook is an Amundi full-holdings export containing valid holdings followed by provider metadata/footer content. The change must preserve this distinction without rewriting historical snapshots or introducing a second FX system.

## Goals / Non-Goals

**Goals:**

- Register and ingest `IE0009HF1MK9` through the existing Amundi product-page fetch strategy.
- Filter and validate the supplied workbook so only complete holdings records enter normalization.
- Represent the fund/share-class currency and intended listing metadata separately from source quote currency.
- Configure a CHF SIX live source and preserve its CHF quote in the live artifact.
- Recognize USD in Saxo section and row parsing, while retaining the imported broker currency as authoritative.
- Keep USD/CHF conversion available for USD live or imported sources and avoid conversion for CHF sources.
- Add deterministic tests and regenerate derived catalog/live artifacts during implementation.

**Non-Goals:**

- Adding a new FX provider or changing the CHF portfolio base currency.
- Supporting every exchange listing for the fund in this change.
- Rewriting historical snapshots under `data/raw/`.
- Inferring a holding's currency from the ETF fund currency or constituent currency breakdown.
- Replacing the existing Amundi importer or introducing a new spreadsheet library.

## Decisions

### Use the existing Amundi fetcher and parser contract

The registry entry will use `fetcher_id: amundi_product_page_v1` and `parser_id: amundi_landing_xlsx_v1`, matching the existing Amundi product. The fixture will exercise the same parser path used for live downloads. This keeps provider-specific retrieval separate from table normalization and avoids a product-specific importer.

Alternative considered: add a one-off importer for this workbook. Rejected because the workbook has the same Amundi column contract and a one-off path would duplicate provider logic.

### Filter provider footer rows at the parser boundary

The Amundi parser or its validation layer will retain rows that have the required holding identity and numeric weight fields, and exclude disclaimer/footer rows before normalization. Completeness checks will assert a meaningful holding count and a weight total within an accepted tolerance rather than treating every physical spreadsheet row as a security.

Alternative considered: manually trim the fixture. Rejected because live Amundi downloads can contain the same footer structure and would reintroduce the problem.

### Model fund currency and listing metadata separately

The registry metadata will identify the USD share-class/fund currency, intended exchange, listing ticker, and listing currency. These fields describe the instrument and configured source, but valuation will continue to use the currency on the imported broker row or normalized live quote. The source record is authoritative at runtime.

Alternative considered: use one `currency` field for all purposes. Rejected because it would incorrectly force a CHF SIX quote through USD/CHF or display a CHF Saxo value as USD.

### Configure the intended live source as a CHF Swiss quote

The live configuration will use the existing Swiss adapter and secret-backed URL-template mechanism, with the new ISIN and the CHF listing identifier required by the provider. The normalized quote will carry `currency: CHF`. USD/CHF remains available for the alternate USD source and USD Saxo imports.

Alternative considered: configure the USD listing and always convert it. Rejected because the requested Saxo instrument is traded in CHF and a CHF source is more direct and avoids unnecessary FX risk.

### Extend Saxo currency recognition without changing conversion semantics

The section-level and row-level Saxo regular expressions will recognize `USD` in addition to `CHF` and `EUR`. Parsed rows will continue to carry their source currency into `calculateImportedPosition`; conversion will use USD/CHF only when the imported source is USD.

Alternative considered: infer currency only from the generic document currency detector. Rejected because detailed section and row parsing currently controls the currency attached to each holding.

### Keep generated artifacts derived

The implementation will run focused fixture ingestion, update the catalog from successful results, and refresh live fixture data only through the existing live-data workflow. Historical snapshots and unrelated generated data will remain untouched.

## Risks / Trade-offs

- [Amundi changes workbook footer or column conventions] -> Keep structural validation and fixture tests strict; fail ingestion rather than publish partial holdings.
- [Swiss provider requires a ticker or endpoint identifier different from the public listing label] -> Verify the actual quote URL/template before implementation and keep the configured identifier secret-backed.
- [A broker report uses a USD section with CHF row values or vice versa] -> Preserve row-level currency when present and add fixtures covering section and row currency precedence.
- [The workbook's rounded weights do not total exactly 100%] -> Use a documented tolerance and validate that the excluded footer rows, not missing holdings, explain the difference.
- [Adding registry metadata expands public schema] -> Make new fields optional for legacy entries and validate only when present; do not break existing catalog consumers.

## Migration Plan

1. Implement parser filtering, registry metadata, live configuration, Saxo USD parsing, and focused tests.
2. Run offline fixture ingestion for the new ISIN and existing regression suites.
3. Generate the new snapshot and update `web/data/catalog.json` from the successful run.
4. Run the live-data workflow with the configured Swiss quote template and verify the normalized CHF quote plus USD/CHF FX artifact.
5. Publish the web data and deployment artifacts using the existing scripts.
6. Roll back by removing the new registry/config entries and generated new catalog/snapshot entries; existing ETF entries and historical snapshots remain valid.

## Open Questions

- Which exact Swiss quote URL-template secret and provider endpoint should be used for `WEBGCHF SW`?
- Should the registry call the fund-level field `fund_currency` or `share_class_currency`, and should listing metadata be nested or flat to preserve current JSON style?
- Should the live configuration support both SIX listings now, or only the requested CHF listing until a USD quote use case appears?
